# Actionable Insights from Deep Research
**Summary of key learnings and immediate actions**

---

## Top 10 Learnings

### 1. Constitution First, Always
**From**: GitHub Spec Kit (59k stars)

Before any development, define project standards in a constitution. This governs all AI behaviour and prevents inconsistency.

**Action**: ✅ Created `specs/quality/constitution.toml`

---

### 2. Scope Guard Prevents Over-Engineering
**From**: Vibe Check MCP (+27% success rate)

Mandatory pause before implementation to verify simplicity. Research shows this significantly improves outcomes.

**Action**: ✅ Added to `specs/_common/base-workflow.toml`

Pattern:
```markdown
### Scope Check 🔍
- [ ] Simplest solution?
- [ ] No unnecessary abstractions?
- [ ] Junior dev could understand?

Assessment: 🟢 Minimal | 🟡 Reasonable | 🔴 Over-engineered
```

---

### 3. Self-Correction with Limits
**From**: Industry standard (all major frameworks)

AI must verify outputs and retry, but know when to stop (max 3 attempts).

**Action**: ✅ Added to `specs/_common/base-workflow.toml`

---

### 4. Proof Artifacts Before Commits
**From**: Liatrio Spec-Driven Workflow

Create evidence BEFORE committing, not after. Documentation of "why it works" not just "what it does."

**Action**: ✅ Added template to `specs/_common/base-workflow.toml`

**TODO**: Add proof generation to `dev.toml` implementation phase

---

### 5. Context Rot Detection
**From**: Liatrio SDD

Use markers (LIA-P1️⃣, LIA-P2️⃣) at response start to detect when context is lost.

**Action**: ✅ Added template to `specs/_common/base-workflow.toml`

**TODO**: Add markers to individual spec prompts

---

### 6. User Stories as Independent Slices
**From**: GitHub Spec Kit

Each user story must be independently testable, deployable, and demoable. This ensures thin vertical slices.

**Action**: 🔲 TODO - Update `spec.toml` to emphasise this pattern

---

### 7. Progressive Disclosure Architecture
**From**: Claude Skills

Load context on-demand: Metadata (~100 tokens) → Instructions (<5k) → Resources (as needed).

**Action**: 🔲 TODO - Consider for large specs like `nexus.toml`

---

### 8. Security as First-Class Concern
**From**: Project CodeGuard

Security checks embedded in workflow, not bolted on. Before, during, and after generation.

**Action**: 🔲 TODO - Create `security.toml` spec

---

### 9. Multiple Workflow Paths
**From**: Clavix

Support different entry points based on task complexity:
- Quick path: improve → implement
- Full planning: prd → plan → implement → verify
- Exploratory: start → discuss → summarise → plan

**Action**: 🔲 TODO - Consider adding workflow variants

---

### 10. Tool-Agnostic Export
**From**: APM (10+ tools supported)

Same workflow, different formats:
| Tool | Format | Location |
|------|--------|----------|
| Cursor | Markdown | `.cursor/commands` |
| Claude Code | Markdown | `.claude/commands` |
| Windsurf | Markdown | `.windsurf/workflows` |
| Gemini CLI | TOML | `.gemini/commands` |

**Action**: 🔲 TODO - Consider multi-format export for Lia specs

---

## Patterns We've Adopted

| Pattern | Source | Status |
|---------|--------|--------|
| Constitution | Spec Kit | ✅ Implemented |
| Scope Guard | Vibe Check | ✅ Implemented |
| Self-Correction | Industry | ✅ Implemented |
| Context Handoff | APM | ✅ Implemented |
| Checkpoint Markers | APM | ✅ Implemented |
| Confidence Signals | OpenAgents | ✅ Implemented |
| Abort Conditions | Industry | ✅ Implemented |
| Proof Artifacts | Liatrio SDD | ✅ Template added |
| Context Rot Detection | Liatrio SDD | ✅ Template added |

---

## Patterns Still Needed

| Pattern | Source | Priority | Effort |
|---------|--------|----------|--------|
| User Story Independence | Spec Kit | P1 | ~2h |
| Security Spec | CodeGuard | P1 | ~4h |
| Context Markers in Prompts | Liatrio | P1 | ~2h |
| Progressive Loading | Claude Skills | P2 | ~8h |
| Multi-Format Export | APM | P2 | ~12h |
| Workflow Variants | Clavix | P2 | ~8h |

---

## Our Positioning

### We're Better At:
1. **Transparency** - Every phase visible, nothing hidden
2. **Education** - Learning focus, not just execution
3. **Tool Agnostic** - TOML works everywhere
4. **Simple Start** - No complex CLI or installation
5. **MCP Native** - Built for emerging standard

### We Need To Match:
1. ✅ Constitution pattern
2. ✅ Scope guards
3. ✅ Self-correction
4. 🔲 Proof artifacts (template done, needs integration)
5. 🔲 Security workflow

### We Could Add Later:
1. Multi-format export
2. Progressive disclosure
3. Real-time dashboard (Spec Kitty)
4. Multi-agent orchestration (Claude-Flow)

---

## Key Quotes to Remember

> "Specifications don't serve code—code serves specifications." — GitHub Spec Kit

> "LLMs can confidently follow flawed plans. Without an external nudge they may spiral into overengineering." — Vibe Check

> "Context rot doesn't announce itself with errors. It creeps in silently." — Liatrio SDD

> "If you find yourself typing the same prompt repeatedly, create a Skill." — Anthropic Skills

---

## Next Steps (Prioritised)

### This Week
1. Add context markers (LIA-DEV️⃣ etc.) to individual spec prompts
2. Integrate proof artifact generation into `dev.toml`
3. Create `security.toml` spec

### Next Week
4. Update `spec.toml` to enforce user story independence
5. Add proof validation step to `review.toml`
6. Document all new patterns in user-facing docs

### This Month
7. Consider progressive loading for large specs
8. Explore multi-format export (Cursor, Claude Code, Windsurf)
9. Evaluate dashboard/tracking features
