# Troubleshooting Quick-Start Guide

> Most AI tools help you create code. Lia helps you **debug** it.

This guide gets you troubleshooting systematically in under 5 minutes.

---

## When to Use Which Spec

| Symptom | Use This | Why |
|---------|----------|-----|
| **Something's broken** | `troubleshoot.toml` | Systematic diagnosis and fix |
| **Code is mysterious** | `wtf.toml` | Feature archaeology — understand why |
| **Need root cause** | `investigate.toml` | Forensic analysis for crashes/data loss |

---

## Quick Start: troubleshoot.toml

### Step 1: Describe the Problem

```
"I want to use the troubleshoot workflow. 

The API returns 500 errors intermittently. It works most of the time
but fails randomly, especially under load. Started happening after 
last week's deployment."
```

### Step 2: The Workflow Guides You

```
AI: LIA-TROUBLESHOOT-1 [Assessment]
    ├─ Symptom: Intermittent 500 errors
    ├─ Impact: User-facing, high severity
    ├─ Timeline: Post-deployment (last week)
    ├─ Pattern: Load-correlated
    └─ Reproducibility: Intermittent
    
    Approve this assessment?
```

### Step 3: Systematic Investigation

```
AI: LIA-TROUBLESHOOT-2 [Investigation]
    ├─ Logs: Found connection pool exhaustion warnings
    ├─ Metrics: Response time spikes correlate with errors
    ├─ Config: Connection pool size unchanged (10)
    ├─ Recent changes: Added async batch processing
    └─ Hypothesis: Connection leak in new async code
    
    Approve investigation findings?
```

### Step 4: Root Cause Identified

```
AI: LIA-TROUBLESHOOT-3 [Root Cause]
    
    ROOT CAUSE: Connection leak in async batch processor
    
    Evidence:
    - Connection pool exhausts after ~100 batch operations
    - New async code doesn't use context manager
    - Connections not returned to pool on exceptions
    
    Approve root cause analysis?
```

### Step 5: Fix with Verification

```
AI: LIA-TROUBLESHOOT-5 [Implementation]
    
    Fix applied: Added context manager to async connections
    
    VERIFICATION:
    - [x] Ran 1000 batch operations — no pool exhaustion
    - [x] Load test passed (500 concurrent users)
    - [x] No 500 errors in 30-minute test
    
    Evidence: Load test results attached
    
    Approve fix?
```

---

## Quick Start: wtf.toml (Feature Archaeology)

Use when you inherit mysterious code and need to understand **why** it exists.

### Example

```
"I want to use the wtf workflow.

There's a UserAuthMiddleware class that does something with tokens
but it's not documented. Half the methods seem unused. I need to
understand what it actually does before I can modify it."
```

### What You Get

```
AI: LIA-WTF-3 [Intent Reconstruction]

    ORIGINAL PURPOSE: Rate limiting + token refresh
    
    Timeline:
    - 2022-03: Created for v1 auth (PR #142)
    - 2022-09: Token refresh added (PR #287)
    - 2023-01: Rate limiting disabled (PR #401, "temporary")
    - 2024-06: Unused methods from rate limiting still present
    
    Current State:
    - ACTIVE: Token validation, refresh logic
    - DEAD CODE: Rate limiting methods (disabled but not removed)
    - UNKNOWN: Legacy compatibility shim (still needed?)
    
    Recommend: Remove rate limiting code, keep token logic
```

---

## Quick Start: investigate.toml (Forensic Analysis)

Use after crashes, data loss, or security incidents.

### Example

```
"I want to use the investigate workflow.

Production database had corruption last night. Some user records
have NULL values where there should be data. Need to understand
what happened and recover if possible."
```

### What You Get

```
AI: LIA-INVESTIGATE-4 [Discrepancy Analysis]

    INCIDENT: Data corruption in users table
    
    Timeline Reconstruction:
    - 02:14 - Backup job started (normal)
    - 02:17 - Migration script ran (UNEXPECTED)
    - 02:18 - Migration failed mid-execution
    - 02:19 - Records with NULL values appear in logs
    
    Root Cause: Cron job triggered migration in production
    
    Recovery Options:
    1. Restore from 02:00 backup (lose 17 min of data)
    2. Manual reconstruction from audit logs
    3. Hybrid: Backup restore + audit log replay
    
    Recommended: Option 3 (minimal data loss)
```

---

## The Troubleshooting Cliff

**Why this matters:** Research shows AI tools achieve near-perfect success during code **creation**, then fail catastrophically during **debugging**.

```
Traditional AI:
┌──────────────────────────────────────────────────────┐
│ Creation Phase          │ Debugging Phase            │
│ ████████████████████    │                            │
│ ~95% success            │ ~30% success               │
│                         │ (Troubleshooting Cliff) ↓  │
└──────────────────────────────────────────────────────┘

Lia:
┌──────────────────────────────────────────────────────┐
│ Creation Phase          │ Debugging Phase            │
│ ████████████████████    │ ████████████████████       │
│ ~95% success            │ ~85% success               │
│                         │ (Structured approach)      │
└──────────────────────────────────────────────────────┘
```

**Lia solves what others can't** because we have structured troubleshooting workflows, not ad-hoc debugging.

---

## Escalation Pattern

If you're stuck in `dev.toml` and debugging isn't working:

```
3 failed fix attempts?
         │
         ▼
    STOP ad-hoc debugging
         │
         ▼
    Document what you tried
         │
         ▼
    Switch to troubleshoot.toml
         │
         ▼
    Follow structured phases
         │
         ▼
    Return to dev.toml after resolution
```

This is built into the workflow. After 3 failed attempts, you should escalate.

---

## Common Patterns

### Pattern 1: The Flaky Test

```
Symptom: Test passes locally, fails in CI
Use: troubleshoot.toml

Common causes:
- Race conditions
- Environment differences
- Shared state between tests
- Timing assumptions
```

### Pattern 2: The Mystery Regression

```
Symptom: Feature worked yesterday, broken today
Use: investigate.toml (with git bisect)

Approach:
1. Identify last known good state
2. Binary search through commits
3. Find breaking change
4. Understand why it broke
```

### Pattern 3: The Legacy Monster

```
Symptom: Nobody knows what this code does
Use: wtf.toml

Approach:
1. Git history archaeology
2. PR and issue analysis
3. Intent reconstruction
4. Document for future
```

### Pattern 4: The Performance Cliff

```
Symptom: System slow under load
Use: troubleshoot.toml → then optimize.toml

Approach:
1. Identify bottleneck (troubleshoot)
2. Profile systematically (optimize)
3. Fix with evidence
4. Verify improvement
```

---

## Tips for Effective Troubleshooting

### 1. Be Specific About Symptoms

```
BAD:  "It's broken"
GOOD: "Returns 500 error when user submits form with > 100 items"
```

### 2. Include Context

```
GOOD additions:
- When it started
- What changed recently
- Environment (prod/staging/local)
- Error messages (exact text)
- How to reproduce
```

### 3. Document Your Attempts

Before escalating, note:
- What you tried
- Why it didn't work
- What you learned

### 4. Trust the Process

The workflow phases exist for a reason:
1. Assessment → Understand the problem
2. Investigation → Gather evidence
3. Root Cause → Find the why
4. Solution → Plan the fix
5. Implementation → Apply with verification
6. Validation → Prove it works

Don't skip phases.

---

## Artifacts Created

After troubleshooting, you'll have:

```
.lia/troubleshoot/{task_name}/
├── 0-notepad.md          # Insights and observations
├── 1-assessment.md       # Problem definition
├── 2-investigation.md    # Evidence gathered
├── 3-root-cause.md       # Analysis and determination
├── 4-solution-plan.md    # Fix strategy
├── 5-implementation.md   # What was changed
├── 6-verification.md     # Proof it works
└── 7-documentation.md    # Knowledge capture
```

These artifacts are valuable for:
- Future similar issues
- Team knowledge sharing
- Incident post-mortems
- Audit trails

---

## Next Steps

- Read [Workflow Guide](workflow-guide.md) for detailed concepts
- Try `troubleshoot.toml` on a real bug
- Explore `wtf.toml` on legacy code you've been avoiding
- Check [Best Practices](best-practices.md) for patterns

---

**Remember:** Structured debugging beats ad-hoc debugging. Every time.
