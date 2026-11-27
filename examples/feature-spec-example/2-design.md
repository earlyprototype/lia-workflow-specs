# User authentication design

The web client sends registration, login and account management requests over HTTPS to the authentication service. The service owns the account database, signs short-lived access tokens and queues transactional email. Google and GitHub supply identities through OAuth. Application endpoints verify the access token locally.

## Stored records

| Record | Fields and constraints |
| --- | --- |
| Account | User ID, unique canonical email, optional bcrypt password hash, role, verification state, creation time and lock expiry |
| Provider identity | User ID, provider and provider subject ID, with a unique constraint on the provider and subject together |
| Email challenge | Account, purpose (verification or reset), token digest, expiry and consumption time |
| Session | Account, refresh-token digest, expiry, revocation time, device, approximate location and last activity |
| Audit event | Timestamp, user identifier when available, IP, user agent, event type and outcome |

Index the account email, token digests and session owner. Keep password hashes and token values out of logs. A shared counter store tracks failed logins per account and IP and reset requests per account.

## Registration and login

1. `POST /register` validates the email and password. Require at least eight characters, upper and lower case, a digit and a special character. Reject breached passwords. Store a bcrypt hash at cost 12. Return field errors for invalid input and offer password reset on duplicate registration.
2. Send a verification link after account creation. `POST /verify` consumes a valid challenge and marks the email verified. Accounts still unverified after 24 hours remain pending verification.
3. `POST /login` checks the account and IP limits, verifies the password and issues a session. Unknown accounts and incorrect passwords produce the same invalid-credentials response. With valid credentials, a pending account receives a verification reminder and a locked account receives its lockout message.

## OAuth sign-in

`GET /oauth/{provider}` redirects to Google or GitHub. The callback checks the state bound to the initiating browser and exchanges the code for tokens. Look up the verified provider identity by subject. For a new identity, obtain a verified email before creating an account. If the email belongs to an existing account, require the user to authenticate to that account and confirm the link before storing the association. Subsequent sign-ins resolve the saved association.

## Tokens and sessions

The signed access JWT carries user ID, email, role and a 15-minute expiry. Protected endpoints validate its signature and expiry and return HTTP 401 for an invalid token. The client stores the seven-day refresh credential in a Secure, HttpOnly cookie. Cookie-authenticated state changes require CSRF protection.

`POST /refresh` checks the digest and expiry, consumes the active refresh credential and stores its replacement in one transaction. Only one of two simultaneous refreshes can succeed. The response supplies a fresh access token and refresh cookie. `POST /logout` revokes the current refresh credential. Previously issued access tokens expire after their 15-minute lifetime.

`GET /sessions` returns the caller's devices, locations and last activity. Session termination checks ownership and revokes either one session or all except the caller's current session. An authenticated password change also revokes the other sessions.

## Password recovery

`POST /password-reset` issues a one-hour reset challenge for a registered email and invalidates older reset challenges. The public response is the same for an unknown email. The reset link opens the new-password form after token validation. On submission, check the token again, apply the registration password policy, consume the challenge and replace the hash atomically. Revoke all sessions on an unauthenticated reset and send confirmation email. An expired link offers a fresh reset request.

## Limits, errors and audit

Count failures in a rolling 15-minute window. The sixth failure locks the account for 15 minutes. The twenty-first failure from one IP temporarily blocks that address. A successful login clears the account's failure count. Limit reset requests to three per hour. Include the time until retry in rate-limit responses and release expired locks automatically.

Record every login outcome, provider failures and token validation failures, distinguishing signature mismatch from expiry. Alert on suspicious activity and notify the user when an account locks. Return a generic error on an internal failure and record the diagnostic server-side.

The [implementation checklist](3-tasks.md) links each change to its [acceptance criteria](1-requirements.md).
