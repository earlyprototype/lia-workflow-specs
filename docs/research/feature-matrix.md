# Feature Impact Matrix
**Quick Reference for Prioritisation**

---

## Impact vs Effort Quadrant

```
                         EFFORT
                 Low ◄─────────────────► High
                 
            ┌────────────────┬────────────────┐
            │                │                │
            │  ★ DO FIRST    │  ⚡ PLAN       │
     High   │                │                │
            │ 1. Self-correct│ • Visual editor│
       I    │ 2. Context mgmt│ • Multi-agent  │
       M    │ 3. Abort conds │ • State system │
       P    │ 4. Confidence  │ • Analytics    │
       A    │ 5. Phase skip  │                │
       C    │                │                │
       T    ├────────────────┼────────────────┤
            │                │                │
     Low    │  ✓ BACKLOG     │  ✗ DON'T DO   │
            │                │                │
            │ • More examples│ • Custom DSL   │
            │ • CLI tools    │ • Marketplace  │
            │ • Schema valid │ • Cloud exec   │
            │                │ • NL creation  │
            │                │                │
            └────────────────┴────────────────┘
```

---

## Priority Rankings

### 🔴 P0 - Do Now (High Impact, Low Effort)

| # | Feature | Impact | Effort | Notes |
|---|---------|--------|--------|-------|
| 1 | **Self-correction loops** | ⬆️⬆️⬆️⬆️⬆️ | ⬇️⬇️ | Add verify/retry to each phase |
| 2 | **Context summarisation** | ⬆️⬆️⬆️⬆️⬆️ | ⬇️⬇️ | Checkpoint every 2-3 phases |
| 3 | **Abort conditions** | ⬆️⬆️⬆️⬆️ | ⬇️ | When to stop and escalate |
| 4 | **Confidence signals** | ⬆️⬆️⬆️⬆️ | ⬇️⬇️ | 🟢🟡🔴 uncertainty rating |
| 5 | **Dynamic phase skip** | ⬆️⬆️⬆️⬆️ | ⬇️⬇️ | Conditional phase execution |

**Estimated total effort**: 2-3 days  
**Impact**: Brings specs to market parity

---

### 🟡 P1 - Near Term (High Impact, Medium Effort)

| # | Feature | Impact | Effort | Notes |
|---|---------|--------|--------|-------|
| 6 | **MCP client guidance** | ⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️ | How to use specs via MCP |
| 7 | **Tool capability matching** | ⬆️⬆️⬆️ | ⬇️⬇️⬇️ | Declare required tools |
| 8 | **State persistence spec** | ⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️⬇️ | Resume interrupted workflows |

**Estimated total effort**: 1-2 weeks

---

### 🟢 P2 - Future (High Impact, High Effort)

| # | Feature | Impact | Effort | Notes |
|---|---------|--------|--------|-------|
| 9 | Visual workflow editor | ⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️⬇️⬇️ | GUI for workflow design |
| 10 | Multi-agent orchestration | ⬆️⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️⬇️⬇️ | Coordinate specialist agents |
| 11 | Learning from outcomes | ⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️⬇️⬇️ | Improve based on results |

**Estimated total effort**: 1-3 months each

---

### ⚪ Defer - Avoid Scope Creep

| Feature | Why Defer |
|---------|-----------|
| Custom DSL | TOML is sufficient, adds complexity |
| Workflow marketplace | Nice-to-have, not core value |
| Cloud execution platform | Infrastructure overhead |
| Natural language creation | Current format is clearer |
| Workflow analytics | Need usage first |

---

## Competitive Gap Analysis

| Feature | Market Has | Lia Has | Gap |
|---------|------------|---------|-----|
| Structured workflows | ⚪ Few | ✅ Strong | **Advantage** |
| Self-correction | ✅ Standard | ❌ Missing | **Critical gap** |
| Context management | ✅ Standard | ⚪ Partial | **Gap** |
| Progress checkpoints | ✅ Standard | ⚪ New | Closing |
| MCP support | ⚪ Growing | ✅ Built | **Advantage** |
| Transparency | ⚪ Rare | ✅ Strong | **Advantage** |
| Zero-config | ⚪ Rare | ✅ Strong | **Advantage** |
| Phase flexibility | ✅ Standard | ❌ Missing | **Gap** |

---

## Implementation Order

```
Week 1:  [P0-1] Self-correction  →  [P0-2] Context checkpoints
         ↓
Week 1:  [P0-3] Abort conditions →  [P0-4] Confidence signals  
         ↓
Week 2:  [P0-5] Dynamic phases   →  [P1-6] MCP client docs
         ↓
Week 3+: [P1-7] Tool capabilities → [P1-8] State persistence
```

---

## Must-Have Patterns (Copy-Paste Ready)

### Self-Correction Pattern
```markdown
### Verification Checkpoint
Before proceeding:
- [ ] Output meets stated requirements
- [ ] No errors or warnings introduced
- [ ] Assumptions documented in notepad

**If verification fails** (max 3 attempts):
1. Document failure reason
2. Analyse and correct approach  
3. Retry from last checkpoint
4. After 3 failures → escalate to user
```

### Context Summary Pattern
```markdown
### Context Checkpoint
**Progress**: Phase {N} of {M} complete ({X}%)

**Completed**:
- {Phase 1 outcome}
- {Phase 2 outcome}

**Current focus**: {Active work}

**Key decisions**: 
- {Decision 1}
- {Decision 2}

**Remaining**: {Phases left}
```

### Abort Conditions Pattern
```markdown
### When to Stop & Escalate
Immediately pause and consult user if:
- 🔴 Circular logic or infinite loop detected
- 🔴 3+ failed correction attempts
- 🔴 Scope grew >50% beyond estimate
- 🔴 Security or data safety concern
- 🔴 Missing critical info after 2 clarification requests
- 🔴 Conflicting requirements discovered
```

### Confidence Signal Pattern
```markdown
### Confidence Assessment
**Phase confidence**: 🟢 High | 🟡 Medium | 🔴 Low

🟢 **High**: Standard pattern, clear requirements, proven approach
🟡 **Medium**: Some assumptions made, edge cases possible
🔴 **Low**: Significant uncertainty, multiple valid approaches

**If 🔴 Low**: List uncertainties and request user review before proceeding.
```

---

## Summary

**Do these 5 things to close critical gaps:**

| Priority | Feature | Effort | 
|----------|---------|--------|
| 1 | Self-correction loops | ~4 hours |
| 2 | Context checkpoints | ~2 hours |
| 3 | Abort conditions | ~1 hour |
| 4 | Confidence signals | ~2 hours |
| 5 | Dynamic phase skipping | ~4 hours |

**Total: ~13 hours to reach market parity**

Everything else is P1+ and should wait until these are done.
