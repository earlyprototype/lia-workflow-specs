# Feature Spec Example: User Authentication System

This example demonstrates the complete `spec.toml` workflow from initial idea to implementation tasks.

## Initial Request

```
User: "I want to use the spec workflow to design a user authentication system 
with email/password login and JWT tokens."
```

## Workflow Execution

### Phase 1: Requirements (Approved after 2 iterations)

**Initial Draft:**
The AI generated initial requirements based on the rough idea.

**User Feedback (Iteration 1):**
- "Add OAuth 2.0 support for Google and GitHub"
- "Include password reset functionality"
- "Add rate limiting for brute force protection"

**Final Requirements:** See [1-requirements.md](1-requirements.md)

---

### Phase 2: Design (Approved after 1 iteration)

**Initial Draft:**
Complete architectural design including:
- JWT token structure
- Database schema
- API endpoints
- Security measures

**User Feedback:**
- Approved without changes

**Final Design:** See [2-design.md](2-design.md)

---

### Phase 3: Implementation Tasks (Approved immediately)

**Generated Tasks:**
Complete checklist of 18 implementation tasks, each referencing specific requirements.

**Final Tasks:** See [3-tasks.md](3-tasks.md)

---

## Artifacts Generated

The workflow produced a complete `.lia/specs/user-authentication/` directory:

```
.lia/specs/user-authentication/
├── 0-notepad.md          # Insights and observations
├── 1-requirements.md     # Approved requirements with EARS format
├── 2-design.md           # Complete architectural design
└── 3-tasks.md            # Implementation checklist
```

---

## Key Insights from 0-notepad.md

### 🧠 Key Insights & Discoveries
- OAuth integration complexity higher than initially anticipated
- Rate limiting critical for production readiness
- Password reset token expiry needs careful consideration

### 🔧 Technical Notes
- JWT refresh token rotation prevents token theft
- bcrypt cost factor set to 12 for future-proofing
- Database indexes essential for auth queries

### 💡 Ideas & Future Enhancements
- Consider WebAuthn/FIDO2 for passwordless
- Add 2FA in version 2
- Implement session management dashboard

---

## Timeline

- **Phase 1 (Requirements):** 15 minutes (with 2 iterations)
- **Phase 2 (Design):** 12 minutes
- **Phase 3 (Tasks):** 5 minutes
- **Total Time:** 32 minutes

---

## What Worked Well

✅ **Systematic Approach:** Each phase built on the previous, ensuring alignment
✅ **Requirement Traceability:** Every task referenced specific requirements
✅ **Iteration Friendly:** Easy to refine requirements before committing to design
✅ **Knowledge Capture:** 0-notepad.md preserved valuable insights
✅ **Implementation Ready:** Tasks were immediately actionable

---

## Lessons Learned

1. **Be Specific Early:** Adding OAuth in iteration 1 would have been easier than in design phase
2. **Review Thoroughly:** The approval gate prevented rushing to implementation
3. **Use the Notepad:** Captured ideas for v2 features without disrupting current spec
4. **Requirements First:** Having solid requirements made design much faster

---

## Next Steps

After completing this spec:
1. Execute tasks using `dev.toml` workflow
2. Build test suite using `test.toml` workflow
3. Security review using `security.toml` workflow

---

## View Complete Artifacts

- [0-notepad.md](0-notepad.md) - Insights and observations
- [1-requirements.md](1-requirements.md) - Complete requirements
- [2-design.md](2-design.md) - Architectural design
- [3-tasks.md](3-tasks.md) - Implementation tasks

