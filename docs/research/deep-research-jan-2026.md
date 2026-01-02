# Deep Research: AI-Assisted Coding Workflows
**Research Date**: January 2026  
**Method**: Web research via GitHub API, documentation analysis  
**Scope**: Major frameworks, emerging patterns, best practices

---

## Executive Summary

The AI-assisted coding landscape has matured significantly. **Spec-Driven Development (SDD)** has emerged as the dominant paradigm, with GitHub's Spec Kit (59k+ stars) setting the industry standard. Key insights:

1. **Specifications as source of truth** - Code is generated from specs, not the other way around
2. **Constitution patterns** - Project-wide standards that govern AI behaviour
3. **Progressive disclosure** - Load context on-demand to manage token limits
4. **Self-correction loops** - AI must verify and retry, not just execute
5. **Scope guards** - Explicit mechanisms to prevent over-engineering
6. **Proof artifacts** - Evidence-driven development, not just outputs

---

## Tier 1: Industry Standards

### GitHub Spec Kit ⭐ 59,000+
**The benchmark for spec-driven development**

#### Core Philosophy: "The Power Inversion"
> "For decades, code has been king. Specifications served code—they were the scaffolding we built and then discarded. SDD inverts this power structure. Specifications don't serve code—code serves specifications."

**Key Innovation**: Specifications are **executable**, not documentation. The spec directly generates implementation.

#### The SDD Workflow

```
Constitution → Specify → Plan → Tasks → Implement
     ↓            ↓         ↓        ↓          ↓
  Project     WHAT to    HOW to   Actionable  Execute
  Standards   build      build    breakdown   + verify
```

**Five Commands**:
1. `/speckit.constitution` - Define project principles (mandatory first step)
2. `/speckit.specify` - Describe WHAT to build (product focus, no tech)
3. `/speckit.plan` - Technical implementation plan (HOW)
4. `/speckit.tasks` - Break into actionable items with parallelisation
5. `/speckit.implement` - Execute tasks with verification

#### Constitution Pattern (Critical)

The constitution is **non-negotiable**. It defines:
- **Core Principles** (e.g., Library-First, CLI Interface, Test-First)
- **Quality Gates** (Simplicity Gate, Anti-Abstraction Gate)
- **Governance** (Constitution supersedes all other practices)

Example principles from Spec Kit:
```markdown
### Article VII: Simplicity Gate
- [ ] Using ≤3 projects?
- [ ] No future-proofing?

### Article VIII: Anti-Abstraction Gate  
- [ ] Using framework directly?
- [ ] Single model representation?
```

**Lesson for Lia**: We need a `constitution.toml` spec that runs FIRST.

#### Template-Driven Quality

Spec Kit templates **constrain LLM behaviour**:

1. **Prevent premature implementation** - Focus on WHAT not HOW
2. **Force uncertainty markers** - `[NEEDS CLARIFICATION: specific question]`
3. **Structured checklists** - Self-review for completeness
4. **Constitutional compliance gates** - Must pass before proceeding
5. **Hierarchical detail management** - Complex details in separate files
6. **Test-first thinking** - Tests before implementation
7. **Prevent speculative features** - No "might need" additions

#### User Stories as MVP Slices

Each user story must be:
- **Independently testable**
- **Independently deployable**
- **Independently demoable**

This ensures thin, vertical slices that deliver value.

---

### Vibe Check MCP ⭐ 440+
**Research-backed agent oversight**

#### The Problem: Pattern Inertia & Reasoning Lock-In
> "Large language models can confidently follow flawed plans. Without an external nudge they may spiral into overengineering or misalignment."

#### Research Results
- **+27% success rate** when using Vibe Check
- **-41% harmful actions**
- **Optimal interrupt dosage**: 10-20% of steps

#### Chain-Pattern Interrupt (CPI)

CPI injects "pause points" at risk inflection moments:

```
Agent Phase → Monitor Progress → [high risk?] → CPI Interrupt → Reflect & Adjust
                                 [smooth?]    → Continue
```

**Tools Provided**:
| Tool | Purpose |
|------|---------|
| `vibe_check` | Challenge assumptions, prevent tunnel vision |
| `vibe_learn` | Capture mistakes and fixes for learning |
| `update_constitution` | Set session-specific rules |
| `check_constitution` | Inspect effective rules |

#### Session Constitution

Per-session rules that CPI enforces:
- "No external network calls"
- "Prefer unit tests before refactors"
- "Never write secrets to disk"

**Lesson for Lia**: Add mandatory "scope check" pauses before implementation phases.

---

## Tier 2: Major Frameworks

### Agentic Project Management (APM) ⭐ 1,600+
**Context retention and session handoff**

#### Core Problem Solved
> "Context window limitations. APM uses various context retention techniques so you can maintain productive AI-assisted work for longer periods before facing model hallucinations."

#### Agent Types
- **Project Manager** - Coordination and planning
- **Developers** - Implementation
- **Ad-hoc Specialists** - Domain expertise
- **Setup Expert** - Configuration

#### Supported Tools (10+)
| Tool | Format | Location |
|------|--------|----------|
| Cursor | Markdown | `.cursor/commands` |
| Claude Code | Markdown | `.claude/commands` |
| GitHub Copilot | Markdown | `.github/prompts` |
| Windsurf | Markdown | `.windsurf/workflows` |
| Gemini CLI | TOML | `.gemini/commands` |

**Lesson for Lia**: Consider multi-format export for maximum tool compatibility.

#### Workflow: Setup Phase → Task Loop Phase

APM maintains context through:
1. Knowledge directories
2. Session handoffs
3. Structured memory management

---

### Claude Skills ⭐ (Official Anthropic)
**Progressive disclosure architecture**

#### How Skills Work

```
1. Metadata loading (~100 tokens) - Scan available skills
2. Full instructions (<5k tokens) - Load when relevant
3. Bundled resources - Load only as needed
```

This design allows **multiple skills without overwhelming context**.

#### Key Insight: Skills vs Other Approaches

| Tool | Best For |
|------|----------|
| **Skills** | Reusable procedural knowledge across conversations |
| **Prompts** | One-time instructions |
| **Projects** | Persistent background knowledge |
| **Subagents** | Independent task execution |
| **MCP** | External data/API integration |

**Rule**: "If you find yourself typing the same prompt repeatedly, create a Skill."

**Lesson for Lia**: Our specs are essentially Skills. Consider progressive loading.

---

### Liatrio Spec-Driven Workflow ⭐ 49
**Lightweight markdown-based workflow**

#### Four-Step Workflow

1. **Generate Spec** - Clarifying questions, reviewed spec with demo criteria
2. **Generate Task List** - Parent tasks (demoable units) + subtasks
3. **Manage Tasks** - Implementation with checkpoints and proof artifacts
4. **Validate** - Verify implementation against spec with evidence

#### Context Verification Markers

Each prompt includes markers (SDD1️⃣, SDD2️⃣, etc.) that appear at start of AI responses:
> "These markers help detect **context rot**—a phenomenon where AI performance degrades as input context length increases."

**If marker disappears, context has been lost.**

#### Proof Artifacts Pattern

Evidence created **BEFORE** each commit:
```
docs/specs/[NN]-spec-[feature-name]/
├── [NN]-spec-[feature-name].md
├── [NN]-tasks-[feature-name].md
├── [NN]-proofs/
│   ├── [NN]-task-01-proofs.md
│   └── [NN]-task-02-proofs.md
└── [NN]-validation-[feature-name].md
```

**Lesson for Lia**: Add proof/evidence requirements to implementation phases.

---

### Project CodeGuard ⭐ 358
**Security rules for AI coding agents**

#### Problem Addressed
> "AI coding agents can introduce: skipping input validation, hardcoding secrets, using weak crypto, missing auth checks."

#### Integration Points
- **Before generation** - Design and planning phase
- **During generation** - Prevent issues as code is written
- **After generation** - Code review

#### Security Domains Covered
- Cryptography (including post-quantum)
- Input validation (SQLi, XSS, command injection)
- Authentication (MFA, OAuth, sessions)
- Authorization (RBAC, ABAC, IDOR)
- Supply chain (SBOM, dependencies)
- Cloud security (IaC, containers, K8s)
- Data protection (encryption, storage)

**Lesson for Lia**: Add `security.toml` spec or security phase to dev workflow.

---

### Clavix ⭐ 250
**Agentic-first prompt workflows**

#### CLEAR Framework

Nine commands for structured workflows:

| Command | Purpose |
|---------|---------|
| `/clavix:improve` | Optimize prompts (auto-depth) |
| `/clavix:prd` | Generate PRD through questions |
| `/clavix:plan` | Create task breakdown |
| `/clavix:implement` | Execute tasks |
| `/clavix:start` | Begin conversational session |
| `/clavix:summarize` | Extract requirements from conversation |
| `/clavix:refine` | Iterate on existing PRD |
| `/clavix:verify` | Verify against requirements |
| `/clavix:archive` | Archive completed projects |

#### Three Workflow Paths

**Quick Path** (simple tasks):
```
improve → implement
```

**Full Planning** (complex features):
```
prd → plan → implement → verify → archive
```

**Exploratory** (discovery):
```
start → [conversation] → summarize → plan
```

**Lesson for Lia**: Our specs could support multiple entry paths based on task complexity.

---

## Tier 3: Emerging Patterns

### Claude-Flow ⭐ 11,000+
**Enterprise agent orchestration**

#### Hive-Mind Architecture
- **Queen agent** - Coordination and delegation
- **Worker agents** - Specialised execution
- **Dynamic Agent Architecture (DAA)** - Self-organizing, fault-tolerant

#### 25 Skills (Natural Language Activated)
```bash
"Let's pair program on this feature"        → pair-programming skill
"Review this PR for security issues"        → github-code-review skill
"Create a swarm to build this API"          → swarm-orchestration skill
```

#### AgentDB Integration
- 96x-164x faster vector search
- Semantic understanding
- Reflexion memory
- Skill library auto-consolidation

---

### obra/superpowers ⭐ (Community)
**Core skills library for Claude Code**

Notable features:
- `/brainstorm` - Ideation workflows
- `/write-plan` - Planning phase
- `/execute-plan` - Execution with validation
- 20+ battle-tested skills

---

## Key Patterns Extracted

### 1. Constitutional Governance

**Every project needs a constitution before any work begins.**

```toml
[constitution]
version = "1.0"

[principles]
library_first = "Features start as standalone libraries"
test_first = "TDD mandatory: Tests → Fail → Implement"
simplicity = "Start simple, YAGNI principles"

[gates.simplicity]
max_projects = 3
future_proofing = false

[gates.anti_abstraction]
use_framework_directly = true
single_model_representation = true
```

### 2. Progressive Disclosure

**Load context on-demand, not upfront.**

```
Level 1: Metadata (~100 tokens)
  ↓ [if relevant]
Level 2: Instructions (<5k tokens)
  ↓ [if needed]  
Level 3: Resources (variable)
```

### 3. Proof Artifacts

**Evidence before commits, not after.**

```markdown
## Proof Artifact: Task-01

### Acceptance Criteria Met
- [x] Criterion 1: [Evidence/Screenshot/Test result]
- [x] Criterion 2: [Evidence]

### Tests Passing
[Test output or screenshot]

### No Regressions
[CI status or test suite results]

### Security Review
[Checklist completed]
```

### 4. Context Rot Detection

**Use markers to verify context is still loaded.**

```markdown
## Phase 3 Response

LIA-P3️⃣ Starting implementation phase...

[If marker disappears, context has been lost. Reload the spec.]
```

### 5. Scope Guard Checkpoints

**Mandatory pause before implementation.**

```markdown
### Scope Check (MANDATORY)

Before implementing, verify:
- [ ] This is the simplest solution
- [ ] No unnecessary abstractions
- [ ] No premature optimisation
- [ ] No speculative features
- [ ] Junior developer could understand this

**Assessment**: 🟢 Minimal | 🟡 Reasonable | 🔴 Over-engineered

**If 🔴**: Document what was removed, then proceed with simplified approach.
```

### 6. User Story Independence

**Each story must be independently testable/deployable.**

```markdown
### User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Independent Test**: Can be fully tested by [specific action]
**Standalone Value**: Delivers [specific user value]
**Demo Criteria**: Can demonstrate by [specific demo]

[This story works even if no other stories are implemented]
```

### 7. Self-Correction with Limits

**Verify, retry, but know when to stop.**

```markdown
### Verification Checkpoint

Before proceeding:
- [ ] Output meets requirements
- [ ] No errors introduced
- [ ] Scope check passed

**If verification fails** (max 3 attempts):
1. Document failure reason
2. Analyse root cause
3. Adjust approach and retry
4. After 3 failures → STOP and escalate to user
```

### 8. Security by Default

**Security checks embedded in workflow, not bolted on.**

```markdown
### Security Gate (Before merge/deploy)

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Authentication/authorization checked
- [ ] Dependencies scanned
- [ ] OWASP Top 10 considered
```

---

## Competitive Analysis: Lia vs Market

### What Lia Does Better

| Advantage | Evidence |
|-----------|----------|
| **Tool agnostic** | TOML format works everywhere |
| **Transparent process** | Every phase visible to user |
| **Educational focus** | Learning, not just execution |
| **MCP-native** | Built for emerging standard |
| **Simple start** | No complex CLI or installation |

### Critical Gaps to Address

| Gap | Market Standard | Lia Status | Priority |
|-----|-----------------|------------|----------|
| Constitution/standards | Spec Kit has it | ✅ Added `constitution.toml` | P0 |
| Scope guard | Vibe Check proves value | ✅ Added to base-workflow | P0 |
| Self-correction | Industry standard | ✅ Added to base-workflow | P0 |
| Proof artifacts | Liatrio SDD | ❌ Missing | P1 |
| Context markers | Liatrio SDD | ❌ Missing | P1 |
| Security spec | CodeGuard | ❌ Missing | P1 |
| User story independence | Spec Kit | Partial | P1 |
| Progressive loading | Claude Skills | ❌ Missing | P2 |
| Multi-format export | APM | ❌ Missing | P2 |

---

## Implementation Recommendations

### Immediate (Do Now)

1. **✅ DONE**: Constitution spec created
2. **✅ DONE**: Scope guard added to base-workflow
3. **✅ DONE**: Self-correction loop added
4. **Add proof artifact section** to dev.toml
5. **Add context markers** to all spec prompts

### Short-term (Next Sprint)

6. **Create `security.toml`** spec using CodeGuard patterns
7. **Add user story independence checks** to spec.toml
8. **Implement context rot detection** markers

### Medium-term (Next Month)

9. **Progressive disclosure** - Split large specs into loadable sections
10. **Multi-format export** - Support Cursor, Windsurf, Claude Code formats
11. **Proof artifact validation** - Automated checking

---

## Conclusion

The AI-assisted coding landscape has converged on clear best practices:

1. **Specs drive implementation** - Not the other way around
2. **Constitutions govern behaviour** - Standards before execution
3. **Scope guards prevent bloat** - Explicit simplicity checks
4. **Self-correction is mandatory** - Verify and retry
5. **Evidence trumps outputs** - Proof artifacts for accountability
6. **Context management is critical** - Progressive disclosure, rot detection

Lia Workflow Specs align well with these patterns but need to close key gaps (proof artifacts, security spec, context markers) to reach market parity.

**Our differentiation**: Transparency, education, and tool agnosticism. We show the work; others hide it.

---

## Appendix: Research Sources

| Source | Stars | URL |
|--------|-------|-----|
| GitHub Spec Kit | 59,000+ | https://github.com/github/spec-kit |
| Claude-Flow | 11,000+ | https://github.com/ruvnet/claude-flow |
| APM | 1,600+ | https://github.com/sdi2200262/agentic-project-management |
| Vibe Check MCP | 440+ | https://github.com/PV-Bhat/vibe-check-mcp-server |
| Project CodeGuard | 358 | https://github.com/project-codeguard/rules |
| Spec Kitty | 282 | https://github.com/Priivacy-ai/spec-kitty |
| Clavix | 250 | https://github.com/ClavixDev/Clavix |
| Liatrio SDD | 49 | https://github.com/liatrio-labs/spec-driven-workflow |
| Awesome Claude Skills | 3,965 | https://github.com/travisvn/awesome-claude-skills |
| Official Anthropic Skills | N/A | https://github.com/anthropics/skills |

---

*Research conducted: January 2026*  
*Method: GitHub API queries, documentation analysis*  
*Total repos analysed: 15+*  
*Documentation pages reviewed: 40+*
