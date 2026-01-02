# Strategic Recommendations for Lia Workflow Specs
*Analysis based on AI-assisted coding trends (January 2026)*  
*Updated with web research from GitHub API*

---

## Market Context (NEW)

**Key Competitors Identified:**
| Project | Stars | Key Feature |
|---------|-------|-------------|
| **GitHub Spec Kit** | 59,000+ | Industry-standard spec-driven development |
| **Claude-Flow** | 11,000+ | Hive-mind agent orchestration |
| **APM** | 1,600+ | Context retention and session handoff |
| **Vibe Check MCP** | 440+ | Prevents over-engineering (+27% success) |
| **OpenAgents** | 572 | Plan-first with approval gates |

**Critical Gap Discovered**: GitHub Spec Kit uses a "constitution" pattern to set project-wide standards. We now have `constitution.toml` to address this.

---

## Current State

**17 Workflow Specs:**
- **Development** (3): dev, spec, test
- **Quality** (4): review, architecture, optimize, security
- **Problem-solving** (3): investigate, troubleshoot, wtf
- **Research** (3): research, learn, paper
- **Knowledge** (1): docs
- **Strategy** (3): innovate, integrate, nexus

---

## 1. Recommended New Specs

### High Priority (Common gaps in current coverage)

| Spec | Purpose | Rationale |
|------|---------|-----------|
| **`migrate`** | Database/system migrations | Extremely common task, high risk without structure |
| **`refactor`** | Code restructuring without behaviour change | Different from `optimize` (performance) - focuses on maintainability |
| **`debug`** | Step-by-step debugging sessions | More focused than `troubleshoot`, pairs with AI debugging tools |
| **`deploy`** | Deployment and release workflows | Critical path often done ad-hoc |
| **`mcp`** | Building MCP servers/tools | Meta-spec for extending AI capabilities (see Q4) |

### Medium Priority (Emerging needs)

| Spec | Purpose | Rationale |
|------|---------|-----------|
| **`data`** | Data pipelines and transformations | Growing need with AI/ML workflows |
| **`monitor`** | Observability setup | Often forgotten until production issues |
| **`prototype`** | Rapid prototyping/spike | Different mindset from full `dev` - throwaway code is okay |
| **`onboard`** | Codebase onboarding | Help AI (or humans) understand new codebases systematically |

### Lower Priority (Specialised)

| Spec | Purpose | Rationale |
|------|---------|-----------|
| **`accessibility`** | A11y audit and remediation | Growing regulatory requirements |
| **`localise`** | i18n/l10n workflows | Common but often specialised |
| **`estimate`** | Effort estimation | AI can help analyse complexity |

---

## 2. Low-Hanging Improvements

### A. Structural Consistency Issues

| Issue | Current State | Quick Fix |
|-------|---------------|-----------|
| **Notepad templates vary** | Some have 6 sections, some have emoji headers | Standardise on 6-section format across all specs |
| **Missing workflow diagrams** | `innovate.toml` lacks mermaid diagram | Add diagrams to all specs |
| **Inconsistent phase naming** | Some use numbers, some use names | Standardise: "Phase 1: Name" format |
| **No abort conditions** | Specs don't say when to stop | Add "When to escalate/abort" section |

### B. Missing Common Elements

| Element | Benefit | Implementation |
|---------|---------|----------------|
| **Context gathering phase** | AI works better with explicit context | Add "Phase 0: Context Gathering" to all specs |
| **Checkpoint markers** | Resume interrupted workflows | Add `[CHECKPOINT]` markers at phase boundaries |
| **Success criteria** | Know when you're done | Add explicit "Definition of Done" to each phase |
| **File conventions** | Consistent artifact locations | Document `.lia/{workflow}/{task}/` structure |
| **Token budget hints** | Prevent context overflow | Add guidance on when to summarise/checkpoint |

### C. Quick Documentation Wins

| Item | Current | Improvement |
|------|---------|-------------|
| **Spec selection guide** | Table in overview | Add decision tree/flowchart |
| **Common patterns** | Not documented | Add "Recipes" section (e.g., "Feature from scratch" = spec → dev → test → review) |
| **Anti-patterns** | Not documented | Add "When NOT to use" to each spec |

---

## 3. Three Highest-Impact Improvements

### 🥇 1. Adaptive Phase Execution

**Problem**: Current specs are rigid - all phases must run sequentially.

**Solution**: Add phase skip/branch logic based on context.

```toml
[phases.implementation]
skip_if = ["existing_code_provided", "patch_only_task"]
branch_to = "testing"  # Skip to testing if code exists
```

**Impact**: 
- Reduces unnecessary work for simple tasks
- Allows specs to handle both greenfield and brownfield scenarios
- Better matches how experienced developers actually work

**Implementation effort**: Medium (schema change + spec updates)

---

### 🥈 2. Built-in Self-Correction Loop

**Problem**: AI makes mistakes but specs don't have explicit "verify and iterate" steps.

**Solution**: Add mandatory verification checkpoints with correction triggers.

```markdown
## Phase N: Implementation

### Verification Checkpoint
Before proceeding, verify:
- [ ] Code compiles/runs without errors
- [ ] Tests pass (if applicable)
- [ ] No obvious security issues introduced

### If Verification Fails
1. Analyse the failure
2. Document in notepad: what went wrong, hypothesis
3. Return to relevant step with corrected approach
4. Maximum 3 correction attempts before escalating
```

**Impact**:
- Catches errors before they compound
- Creates audit trail of corrections
- Prevents infinite loops (max attempts)
- Builds pattern library of common mistakes

**Implementation effort**: Low (add sections to existing specs)

---

### 🥉 3. Context Handoff Protocol

**Problem**: Moving between specs or sessions loses context. "What was I doing?"

**Solution**: Standardised context summary format for handoffs.

```markdown
## Context Handoff Summary

### Task State
- **Started**: 2025-12-15T10:30:00
- **Current Phase**: 3 of 5 (Implementation)
- **Completion**: ~60%

### Key Decisions Made
1. Chose PostgreSQL over MongoDB (see notepad section 2)
2. Using repository pattern for data access

### Open Questions
- [ ] Authentication approach not finalised
- [ ] Need user input on error handling strategy

### Files Modified
- `src/auth/login.py` (new)
- `src/models/user.py` (modified)

### Next Actions
1. Complete login endpoint
2. Add input validation
3. Write unit tests

### Handoff To
- [ ] Another session of same spec
- [ ] Different spec: `test`
- [ ] Human review required
```

**Impact**:
- Enables multi-session complex tasks
- Supports spec chaining naturally
- Creates documentation as side effect
- Helps with AI context window management

**Implementation effort**: Medium (new section + tooling support)

---

## 4. Should We Have an MCP Spec?

### **Yes, absolutely.**

MCP (Model Context Protocol) is becoming the standard for AI tool integration. A dedicated `mcp` spec would be highly valuable.

### Rationale

| Factor | Assessment |
|--------|------------|
| **Market direction** | Anthropic's MCP, OpenAI's function calling, Google's extensions - all converging on tool protocols |
| **Meta-benefit** | Using AI to build AI tools creates a virtuous cycle |
| **Community need** | MCP servers are being built ad-hoc; structured approach needed |
| **Dogfooding** | We literally just built an MCP server for this project |

### Proposed `mcp.toml` Spec Structure

```
Phase 1: MCP Server Requirements
- What resources will the server expose?
- What tools will it provide?
- What prompts will it offer?
- Target MCP clients (Claude Desktop, Cursor, etc.)

Phase 2: Data Model Design
- Resource schemas
- Tool input/output schemas
- Error handling patterns

Phase 3: Implementation
- Server scaffolding (Python/TypeScript)
- Resource handlers
- Tool handlers
- Prompt templates

Phase 4: Testing & Validation
- Unit tests for handlers
- Integration tests with MCP client
- Error case coverage

Phase 5: Documentation & Deployment
- README with setup instructions
- Client configuration examples
- PyPI/npm publishing (if applicable)
```

### Key Elements to Include

1. **MCP Protocol compliance** - Ensure spec produces valid MCP servers
2. **Security considerations** - Tool permissions, data access controls
3. **Client compatibility** - Testing across Claude Desktop, Cursor, etc.
4. **Versioning strategy** - How to handle MCP protocol updates
5. **Example patterns** - Common MCP server architectures

---

## Summary Matrix

| Question | Recommendation | Priority |
|----------|----------------|----------|
| **New specs to add** | `migrate`, `refactor`, `debug`, `deploy`, `mcp` | High |
| **Low-hanging improvements** | Standardise notepad, add context phase, checkpoint markers | Quick wins |
| **Highest impact changes** | 1. Adaptive phases, 2. Self-correction loops, 3. Context handoff | Strategic |
| **MCP spec** | Yes - create dedicated `mcp.toml` | High |

---

## Recommended Next Steps

### ✅ Completed (This PR)
- [x] Add context handoff template to base-workflow.toml
- [x] Document the 6-section notepad standard (`docs/notepad-standard.md`)
- [x] Create `constitution.toml` spec (Spec Kit pattern)
- [x] Add scope guard pattern to base-workflow.toml (Vibe Check pattern)
- [x] Add self-correction loop to base-workflow.toml
- [x] Add confidence signals pattern
- [x] Add abort conditions

### Short-term (Next Sprint)
- [ ] Create `mcp.toml` spec
- [ ] Create `migrate.toml` spec  
- [ ] Apply new patterns (scope guard, self-correction) to existing specs
- [ ] Test constitution workflow end-to-end

### Medium-term (Next Month)
- [ ] Implement adaptive phase execution
- [ ] Create `refactor.toml` and `debug.toml`
- [ ] Build spec selection decision tree
- [ ] Consider progress tracking (à la Spec Kitty dashboard)

### Positioning vs Competition
- **Against Spec Kit**: We emphasise transparency and learning; they emphasise autonomous execution
- **Against Claude-Flow**: We're tool-agnostic; they're Claude-specific
- **Against APM**: Similar context management; we have richer workflow structure

---

## Research Sources

- GitHub Spec Kit (59k stars): https://github.com/github/spec-kit
- Claude-Flow (11k stars): https://github.com/ruvnet/claude-flow
- APM (1.6k stars): https://github.com/sdi2200262/agentic-project-management
- Vibe Check MCP (440 stars): https://github.com/PV-Bhat/vibe-check-mcp-server
- OpenAgents (572 stars): https://github.com/darrenhinde/OpenAgents
- Spec Kitty (282 stars): https://github.com/Priivacy-ai/spec-kitty

---

*Analysis performed: January 2026*  
*Updated with live web research via GitHub API*  
*Based on: AI-assisted coding trends, MCP ecosystem growth, and observed workflow patterns*
