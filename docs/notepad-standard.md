# Standard Notepad Template

Every workflow creates a `0-notepad.md` file to capture insights during execution. This document defines the standard format.

## Why Notepads?

- **Capture tacit knowledge**: Things you notice that don't fit elsewhere
- **Enable learning**: Patterns recognised across sessions
- **Support handoffs**: Context for future sessions or other workflows
- **Create documentation**: Side-effect of good workflow execution

---

## Standard 6-Section Format

All workflow notepads should use this structure:

```markdown
# {Workflow Name} Notepad
**Workflow**: {Workflow Type}  
**Task**: {task_name}  
**Created**: {date}

---

## KEY INSIGHTS & DISCOVERIES
<!-- Unexpected findings, patterns, or "aha moments" -->

## TECHNICAL NOTES & IMPLEMENTATION DETAILS  
<!-- Technical considerations, constraints, implementation specifics -->

## IDEAS & FUTURE ENHANCEMENTS
<!-- Ideas, improvements, enhancement opportunities for later -->

## CROSS-SYSTEM CONNECTIONS
<!-- Links to other components, related work, architectural insights -->

## USER NOTES
<!-- Space for user to add their own observations -->

## LLM OBSERVATIONS
<!-- AI-generated insights about patterns and strategies -->

---
*This notepad captures valuable insights that emerge during systematic analysis*
```

---

## Section Purposes

| Section | What to Capture | Examples |
|---------|-----------------|----------|
| **KEY INSIGHTS** | Unexpected discoveries, "aha" moments, pattern recognition | "The auth module is tightly coupled to the user model - this explains the circular import" |
| **TECHNICAL NOTES** | Implementation details, constraints, gotchas | "Rate limiting needs Redis; SQLite won't scale" |
| **IDEAS & FUTURE** | Enhancement opportunities, "nice to have" items | "Could add caching here for 10x speedup" |
| **CROSS-SYSTEM** | Connections to other parts of the system | "This relates to the logging module we reviewed last week" |
| **USER NOTES** | Reserved for human annotations | User adds context the AI might miss |
| **LLM OBSERVATIONS** | AI meta-observations about the work | "This codebase follows repository pattern consistently" |

---

## When to Update the Notepad

Update the notepad when you encounter:

1. **Surprises**: Something unexpected or counter-intuitive
2. **Decisions**: Choices made and their rationale
3. **Blockers**: Issues that slowed progress
4. **Connections**: Links to other work or patterns
5. **Ideas**: Things to consider for later
6. **Learnings**: Knowledge worth preserving

---

## Workflow-Specific Customisation

Some workflows may add domain-specific sections **after** the standard 6:

```markdown
## KEY INSIGHTS & DISCOVERIES
## TECHNICAL NOTES & IMPLEMENTATION DETAILS  
## IDEAS & FUTURE ENHANCEMENTS
## CROSS-SYSTEM CONNECTIONS
## USER NOTES
## LLM OBSERVATIONS

# --- Workflow-specific sections below ---

## SECURITY CONSIDERATIONS        # security.toml specific
## PERFORMANCE OBSERVATIONS       # optimize.toml specific
```

The standard 6 sections should be present; additional sections are optional.

### Special Case: nexus.toml

The `nexus.toml` (Innovation Consulting Coordinator) uses 8 sections tailored for consulting engagements:

- STRATEGIC INSIGHTS & KEY DISCOVERIES
- TEAM COORDINATION NOTES
- CLIENT RELATIONSHIP MANAGEMENT
- METHODOLOGY & PROCESS NOTES
- INNOVATION OPPORTUNITIES & IDEAS
- CROSS-PROJECT CONNECTIONS
- CLIENT FEEDBACK & ITERATIONS
- NEXUS OBSERVATIONS

This is acceptable because nexus.toml coordinates multi-agent consulting teams with specific client management needs.

---

## Anti-Patterns

**Don't do this:**

- Empty notepad (defeats the purpose)
- Duplicating main deliverables (notepad is for *incidental* insights)
- Long prose (use bullet points)
- Skipping sections (at minimum write "Nothing notable")
- Mixing concerns between sections

**Do this:**

- Brief, scannable bullet points
- Concrete observations with context
- Update as you work, not just at the end
- Include "negative results" (what didn't work)

---

## Example: Well-Written Notepad

```markdown
# Development Workflow Notepad
**Workflow**: Development  
**Task**: add-user-authentication  
**Created**: 2025-12-15

---

## KEY INSIGHTS & DISCOVERIES
- The existing session middleware already has hooks for auth - can reuse
- Password hashing is inconsistent across the codebase (some bcrypt, some argon2)
- Found undocumented rate limiting in the login route

## TECHNICAL NOTES & IMPLEMENTATION DETAILS  
- JWT tokens set to 24h expiry - matches existing API tokens
- Refresh token rotation implemented to prevent token reuse
- Had to patch passport.js for async/await compatibility

## IDEAS & FUTURE ENHANCEMENTS
- [ ] Add "remember me" functionality (extend token to 30 days)
- [ ] Consider OAuth2 social login for v2
- [ ] Password strength meter on frontend would improve UX

## CROSS-SYSTEM CONNECTIONS
- Auth module connects to: User model, Session middleware, Email service
- Related PR: #142 (added email verification)
- See also: security.toml review from last week

## USER NOTES
- Client prefers email-based 2FA over SMS (cost reasons)

## LLM OBSERVATIONS
- Codebase consistently uses middleware pattern for cross-cutting concerns
- Error handling follows the AppError class pattern throughout
- Test coverage expectation appears to be >80% based on existing tests

---
*This notepad captures valuable insights that emerge during systematic analysis*
```

---

## Integration with Context Handoff

When creating a `handoff.md` for session transitions, reference the notepad:

```markdown
## Notes for Next Session
See `0-notepad.md` for detailed observations, especially:
- Key Insights section: explains the middleware reuse decision
- Technical Notes: JWT configuration rationale
```

The notepad and handoff work together - notepad captures details, handoff summarises state.
