# Feature Impact Matrix
**Quick Reference for Prioritisation**  
*Updated with web research - January 2026*

---

## Market Context

| Project | Stars | Category | Key Differentiator |
|---------|-------|----------|-------------------|
| **GitHub Spec Kit** | 59,000+ | Spec-Driven Dev | Industry standard, autonomous execution |
| **Claude-Flow** | 11,000+ | Agent Orchestration | Hive-mind swarms, 100 MCP tools |
| **APM** | 1,600+ | Context Management | Solves context window limits |
| **OpenAgents** | 572 | Plan-First Dev | Approval-based execution |
| **Vibe Check MCP** | 440+ | Agent Oversight | Prevents over-engineering |
| **Lia Specs** | New | Guided Workflows | Transparent, educational, MCP-native |

---

## Impact vs Effort Quadrant

```
                         EFFORT
                 Low ◄─────────────────► High
                 
            ┌────────────────┬────────────────┐
            │                │                │
            │  ★ DO FIRST    │  ⚡ PLAN       │
     High   │                │                │
            │ 1. Constitution│ • Visual editor│
       I    │ 2. Self-correct│ • Multi-agent  │
       M    │ 3. Scope guard │ • State system │
       P    │ 4. Context mgmt│ • Analytics    │
       A    │ 5. Abort conds │ • Dashboard    │
       C    │ 6. Confidence  │                │
       T    │                │                │
            ├────────────────┼────────────────┤
            │                │                │
     Low    │  ✓ BACKLOG     │  ✗ DON'T DO   │
            │                │                │
            │ • More examples│ • Custom DSL   │
            │ • CLI tools    │ • Marketplace  │
            │ • Schema valid │ • Cloud exec   │
            │ • More agents  │ • NL creation  │
            │                │                │
            └────────────────┴────────────────┘
```

---

## Priority Rankings

### 🔴 P0 - Do Now (High Impact, Low Effort)

| # | Feature | Impact | Effort | Market Driver |
|---|---------|--------|--------|---------------|
| 1 | **Constitution spec** | ⬆️⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️ | Spec Kit has it, we don't |
| 2 | **Self-correction loops** | ⬆️⬆️⬆️⬆️⬆️ | ⬇️⬇️ | Industry standard (Claude-Flow) |
| 3 | **Scope guard pattern** | ⬆️⬆️⬆️⬆️⬆️ | ⬇️ | Vibe Check proves +27% success |
| 4 | **Context checkpoints** | ⬆️⬆️⬆️⬆️⬆️ | ⬇️⬇️ | APM's core innovation |
| 5 | **Abort conditions** | ⬆️⬆️⬆️⬆️ | ⬇️ | Safety standard |
| 6 | **Confidence signals** | ⬆️⬆️⬆️⬆️ | ⬇️⬇️ | OpenAgents validation |

**Estimated total effort**: ~13 hours  
**Impact**: Brings specs to market parity + differentiation

---

### 🟡 P1 - Near Term (High Impact, Medium Effort)

| # | Feature | Impact | Effort | Market Driver |
|---|---------|--------|--------|---------------|
| 7 | **Dynamic phase skip** | ⬆️⬆️⬆️⬆️ | ⬇️⬇️ | Flexibility for experts |
| 8 | **Tool capability matching** | ⬆️⬆️⬆️ | ⬇️⬇️⬇️ | Spec Kit influence |
| 9 | **State persistence spec** | ⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️⬇️ | APM session handoff |

**Estimated total effort**: 1-2 weeks

---

### 🟢 P2 - Future (High Impact, High Effort)

| # | Feature | Impact | Effort | Market Driver |
|---|---------|--------|--------|---------------|
| 10 | Visual workflow editor | ⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️⬇️⬇️ | Spec Kitty dashboard |
| 11 | Multi-agent orchestration | ⬆️⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️⬇️⬇️ | Claude-Flow standard |
| 12 | Learning from outcomes | ⬆️⬆️⬆️⬆️ | ⬇️⬇️⬇️⬇️⬇️ | AgentDB integration |

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

## Competitive Gap Analysis (Updated)

| Feature | Spec Kit | Claude-Flow | APM | Lia Has | Gap |
|---------|----------|-------------|-----|---------|-----|
| Constitution/Standards | ✅ | ⚪ | ⚪ | ❌ | **Critical gap** |
| Structured workflows | ✅ | ⚪ | ✅ | ✅ | **Advantage** |
| Self-correction | ⚪ | ✅ | ⚪ | ❌ | **Critical gap** |
| Scope guard | ❌ | ❌ | ❌ | ❌ | **Opportunity** |
| Context management | ⚪ | ✅ | ✅ | ✅ New | Closing |
| Progress checkpoints | ⚪ | ✅ | ✅ | ✅ New | Closing |
| MCP support | ❌ | ✅ | ❌ | ✅ | **Advantage** |
| Transparency | ⚪ | ❌ | ✅ | ✅ | **Advantage** |
| Zero-config | ⚪ | ⚪ | ✅ | ✅ | **Advantage** |
| Tool agnostic | ⚪ | ❌ Claude | ✅ | ✅ | **Advantage** |

---

## Lia Positioning vs Market Leaders

| Spec Kit | Lia Specs |
|----------|-----------|
| Specs execute autonomously | **Guided with checkpoints** |
| Implementation focus | **Understanding focus** |
| Black box execution | **Transparent process** |
| Complex CLI tooling | **Zero-config start** |
| GitHub ecosystem | **Tool agnostic** |

**Tagline**: "Lia teaches you to fish. Spec Kit fishes for you."

---

## Implementation Order (Revised)

```
Week 1:  [P0-1] Constitution spec  →  [P0-2] Self-correction
         ↓
Week 1:  [P0-3] Scope guard       →  [P0-4] Context checkpoints  
         ↓
Week 2:  [P0-5] Abort conditions  →  [P0-6] Confidence signals
         ↓
Week 2:  [P1-7] Dynamic phases    →  [P1-8] Tool capabilities
```

---

## Must-Have Patterns (Copy-Paste Ready)

### 1. Constitution Pattern (NEW - from Spec Kit)
```toml
# constitution.toml - Project-wide standards
[project]
name = "Project Name"
type = "web-app|library|cli|api"

[standards.code]
style = "Follow existing patterns in codebase"
testing = "New code requires tests"
documentation = "Public APIs must be documented"

[standards.process]
review_required = true
security_check = "Before external integrations"

[standards.quality]
complexity = "Functions under 50 lines"
dependencies = "Prefer stdlib, justify external"
```

### 2. Scope Guard Pattern (NEW - from Vibe Check)
```markdown
### Scope Check
**Before implementing, verify:**
- [ ] This is the simplest solution
- [ ] No unnecessary abstractions
- [ ] No premature optimisation  
- [ ] No speculative features
- [ ] A junior dev could understand this

**Assessment**: 🟢 Minimal | 🟡 Reasonable | 🔴 Over-engineered

**If 🔴**: Simplify before proceeding. Document what was removed.
```

### 3. Self-Correction Pattern
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

### 4. Context Summary Pattern
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

### 5. Abort Conditions Pattern
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

### 6. Confidence Signal Pattern
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

**Do these 6 things to close critical gaps:**

| Priority | Feature | Effort | Source |
|----------|---------|--------|--------|
| 1 | Constitution spec | ~3 hours | Spec Kit |
| 2 | Self-correction loops | ~4 hours | Claude-Flow |
| 3 | Scope guard pattern | ~2 hours | Vibe Check |
| 4 | Context checkpoints | ~2 hours | APM |
| 5 | Abort conditions | ~1 hour | Industry |
| 6 | Confidence signals | ~2 hours | OpenAgents |

**Total: ~14 hours to reach market parity + unique advantages**

Everything else is P1+ and should wait until these are done.

---

## Research Sources

- GitHub Spec Kit (59k stars): https://github.com/github/spec-kit
- Claude-Flow (11k stars): https://github.com/ruvnet/claude-flow
- APM (1.6k stars): https://github.com/sdi2200262/agentic-project-management
- Vibe Check MCP (440 stars): https://github.com/PV-Bhat/vibe-check-mcp-server
- OpenAgents (572 stars): https://github.com/darrenhinde/OpenAgents
