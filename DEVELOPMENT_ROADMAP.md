# Lia Development Roadmap
**Version**: 2.0  
**Last Updated**: January 2026  
**Status**: Active

---

## Vision Alignment

This roadmap implements the strategic vision: **"Understand what you're building."**

Every item is evaluated against three questions:
1. Does it help developers understand?
2. Does it maintain simplicity?
3. Does it leverage our competitive advantages?

---

## Current State Assessment

### What We Have (✅)

| Category | Specs | Status |
|----------|-------|--------|
| **Development** | `dev.toml`, `spec.toml`, `test.toml` | ✅ Strong |
| **Quality** | `review.toml`, `architecture.toml`, `optimize.toml`, `security.toml`, `constitution.toml` | ✅ Strong |
| **Problem-Solving** | `troubleshoot.toml`, `investigate.toml`, `wtf.toml` | ✅ **Competitive advantage** |
| **Research** | `research.toml`, `learn.toml`, `paper.toml`, `recon.toml` | ✅ Strong |
| **Knowledge** | `docs.toml` | ✅ Adequate |
| **Strategy** | `innovate.toml`, `integrate.toml`, `nexus.toml` | ✅ Adequate |
| **Infrastructure** | MCP Server, base-workflow patterns | ✅ Functional |

### Recent Additions (from Research)

| Addition | Source | File |
|----------|--------|------|
| Constitutional governance | Spec Kit | `constitution.toml` |
| Scope guards | Vibe Check | `base-workflow.toml` |
| Self-correction loops | Industry | `base-workflow.toml` |
| Confidence signals | OpenAgents | `base-workflow.toml` |
| Abort conditions | Industry | `base-workflow.toml` |
| Context markers | Liatrio SDD | `dev.toml`, `spec.toml` |
| Proof artifacts | Liatrio SDD | `dev.toml` |
| Brownfield support | OpenSpec | `spec.toml` |
| Recon methodology | Internal | `recon.toml` |

### Gaps Identified (from Spec_Engine Analysis)

| Gap | Source | Priority |
|-----|--------|----------|
| Alternative reasoning backups | Spec_Engine Article VII | P1 |
| Error propagation strategies | Spec_Engine Article VIII | P1 |
| Verification before status | Spec_Engine weakness | P1 |
| Criticality guidance | Spec_Engine Article VI | P1 |
| Troubleshooting integration | Spec_Engine weakness | P1 |
| Pre-flight validation | Spec_Engine Article IV | P2 |

---

## Phase 1: Foundation Strengthening (Weeks 1-2)

**Theme**: Adopt Spec_Engine's wisdom without its weight

### 1.1 Alternative Reasoning Backups
**Priority**: P1 | **Effort**: 3h | **Owner**: TBD

Add to `base-workflow.toml`:

```markdown
# BACKUP METHOD PHILOSOPHY
# 
# Valid backups are ALTERNATIVE REASONING PATHS, not retries:
# ✅ "If documentation incomplete, inspect source code directly"
# ✅ "If unit tests insufficient, try integration testing approach"
# ✅ "If automated analysis fails, apply manual heuristics"
# ❌ "Try again" (NOT a valid backup)
# ❌ "Retry with same approach" (NOT a valid backup)
#
# When primary approach fails:
# 1. Document why it failed
# 2. Identify genuinely different approach
# 3. Apply alternative reasoning
# 4. If no alternatives exist, escalate
```

**Acceptance Criteria**:
- [ ] Pattern documented in `base-workflow.toml`
- [ ] Referenced in `dev.toml` and `troubleshoot.toml`
- [ ] Example added to documentation

---

### 1.2 Error Propagation Strategies
**Priority**: P1 | **Effort**: 4h | **Owner**: TBD

Add to `base-workflow.toml`:

```markdown
# ERROR PROPAGATION STRATEGIES
#
# At workflow start, select strategy:
#
# 1. **halt_on_critical** (Default for production)
#    Stop immediately on critical failure
#    Use when: Deployment, security-sensitive work
#
# 2. **continue_and_log** (For exploration)
#    Log failure, continue to next step
#    Use when: Research, prototyping, learning
#
# 3. **collaborative_review** (Recommended default)
#    Pause and request human decision
#    Use when: Complex decisions, uncertain outcomes
#
# Document chosen strategy in notepad at workflow start.
```

**Acceptance Criteria**:
- [ ] Three strategies documented in `base-workflow.toml`
- [ ] Strategy selection prompt in workflow start
- [ ] Integration with abort conditions

---

### 1.3 Verification Before Status
**Priority**: P1 | **Effort**: 2h | **Owner**: TBD

Add to `base-workflow.toml`:

```markdown
# VERIFICATION BEFORE STATUS REPORTING
#
# Before marking ANY item "Fixed", "Complete", or "Done":
#
# ```markdown
# ### Verification Checkpoint
# **Claimed Status**: {Fixed/Complete/Done}
#
# - [ ] Automated tests pass (if applicable)
# - [ ] Manual verification performed
# - [ ] Evidence captured (screenshot, output, or test result)
# - [ ] No new warnings or errors introduced
# - [ ] Regression check completed
#
# **Evidence**: {Link to proof artifact or inline evidence}
# ```
#
# Status based on OUTCOME, not INTENT.
# "I wrote the fix" ≠ "It's fixed"
# "I tested and it works" = "It's fixed"
```

**Acceptance Criteria**:
- [ ] Verification checkpoint template in `base-workflow.toml`
- [ ] Integration with proof artifacts in `dev.toml`
- [ ] Referenced in `troubleshoot.toml`

---

### 1.4 Criticality Guidance
**Priority**: P1 | **Effort**: 1h | **Owner**: TBD

Add to `base-workflow.toml` and `spec.toml`:

```markdown
# CRITICALITY BALANCE GUIDANCE
#
# When marking steps as critical vs non-critical:
#
# **Target**: 40-60% of steps should be critical
#
# - **Under-critical (<20%)**: Failures accumulate silently
# - **Balanced (40-60%)**: Appropriate escalation
# - **Over-critical (>80%)**: Everything escalates, workflow halts
#
# **Exception**: Production deployments may warrant 70%+ critical
#
# Document criticality rationale for each step in notepad.
```

**Acceptance Criteria**:
- [ ] Guidance documented in `base-workflow.toml`
- [ ] Referenced in `spec.toml` task breakdown phase
- [ ] Example criticality assessment added

---

### 1.5 Troubleshooting Integration
**Priority**: P1 | **Effort**: 3h | **Owner**: TBD

Add to `dev.toml` and `base-workflow.toml`:

```markdown
# TROUBLESHOOTING ESCALATION
#
# If implementation fails after 3 attempts:
#
# 1. STOP ad-hoc debugging immediately
# 2. Document all prior attempts in notepad
# 3. Switch to structured troubleshooting:
#    - Use `troubleshoot.toml` for general issues
#    - Use `wtf.toml` for mysterious behaviour
#    - Use `investigate.toml` for root cause analysis
# 4. Follow troubleshooting phases systematically
# 5. Return to dev workflow only after resolution
#
# **Anti-pattern**: Circular debugging without structured approach
# **Evidence**: Spec_Engine's "Troubleshooting Cliff" — 100% creation success,
#              systemic debugging failure. Structured troubleshooting prevents this.
```

**Acceptance Criteria**:
- [ ] Escalation path documented in `base-workflow.toml`
- [ ] Integration point in `dev.toml` Phase 4
- [ ] Cross-reference to troubleshooting specs

---

## Phase 2: Core Spec Enhancements (Weeks 3-4)

**Theme**: Strengthen flagship specs with research insights

### 2.1 Security Spec Enhancement
**Priority**: P1 | **Effort**: 4h | **Owner**: TBD

Create or enhance `security.toml` based on CodeGuard patterns:

**Phases**:
1. Threat modelling
2. Security requirements (OWASP Top 10)
3. Implementation review
4. Security testing
5. Remediation verification

**Domains to cover**:
- Input validation (SQLi, XSS, command injection)
- Authentication/Authorization
- Cryptography
- Data protection
- Dependency security

**Acceptance Criteria**:
- [ ] 5-phase security workflow
- [ ] OWASP Top 10 checklist
- [ ] Integration with `dev.toml` and `review.toml`
- [ ] Proof artifact for security sign-off

---

### 2.2 Troubleshooting Headline Positioning
**Priority**: P1 | **Effort**: 2h | **Owner**: TBD

Enhance troubleshooting specs visibility:

- Update `README.md` to feature troubleshooting prominently
- Create troubleshooting quick-start guide
- Add case studies/examples
- Cross-reference from `dev.toml`

**Acceptance Criteria**:
- [ ] Troubleshooting featured in README (top 3 use cases)
- [ ] Quick-start guide for troubleshooting workflow
- [ ] At least 2 example troubleshooting scenarios

---

### 2.3 Pre-Flight Validation Checklist
**Priority**: P2 | **Effort**: 4h | **Owner**: TBD

Add optional pre-flight validation (lighter than Spec_Engine's 10-step):

```markdown
# PRE-FLIGHT VALIDATION (Optional)
#
# Before starting workflow execution:
#
# - [ ] Objective clearly stated
# - [ ] Required context available (codebase, docs, etc.)
# - [ ] Output location confirmed
# - [ ] Error propagation strategy selected
# - [ ] Time estimate acknowledged
#
# Skip pre-flight with: "proceed without validation"
```

**Acceptance Criteria**:
- [ ] 5-item validation checklist (not 10)
- [ ] Optional, not mandatory
- [ ] Documented in `base-workflow.toml`

---

## Phase 3: Documentation & Positioning (Weeks 5-6)

**Theme**: Communicate our differentiation clearly

### 3.1 README Overhaul
**Priority**: P1 | **Effort**: 3h | **Owner**: TBD

Update README with:
- New positioning: "Understand what you're building"
- Troubleshooting as headline feature
- Educational focus emphasised
- Simplicity value proposition
- Competitive differentiation

**Acceptance Criteria**:
- [ ] New tagline in README header
- [ ] Troubleshooting in top 3 featured workflows
- [ ] "Why Lia?" section updated
- [ ] Comparison table updated

---

### 3.2 Getting Started Guide Update
**Priority**: P2 | **Effort**: 2h | **Owner**: TBD

Align getting started with new positioning:
- Emphasise learning journey
- Include troubleshooting scenario
- Show transparency in action

---

### 3.3 Case Studies
**Priority**: P2 | **Effort**: 4h | **Owner**: TBD

Create 2-3 case studies demonstrating:
- Learning through spec workflow
- Troubleshooting success story
- Understanding complex codebase (wtf.toml)

---

## Phase 4: Infrastructure Enhancement (Weeks 7-8)

**Theme**: Improve developer experience without adding complexity

### 4.1 MCP Server Enhancements
**Priority**: P2 | **Effort**: 8h | **Owner**: TBD

Enhance MCP server with:
- Workflow state as MCP resources
- Troubleshooting-specific tools
- Better spec recommendation based on context

---

### 4.2 Spec Validation Tooling
**Priority**: P2 | **Effort**: 6h | **Owner**: TBD

Create/enhance spec validator:
- Validate TOML structure
- Check for required sections
- Lint for best practices
- Integration with CI

---

## Backlog (Future Phases)

### Quarter 2

| Item | Priority | Effort | Notes |
|------|----------|--------|-------|
| Lightweight progress viewer | P3 | 12h | Simple markdown-based, not full dashboard |
| VSCode extension (basic) | P3 | 20h | Spec browser and launcher |
| Multi-format export | P3 | 12h | Cursor, Claude Code, Windsurf formats |

### Quarter 3+

| Item | Priority | Effort | Notes |
|------|----------|--------|-------|
| Community spec library | P3 | Ongoing | User-contributed specs |
| University partnerships | P3 | Ongoing | Educational institution adoption |
| Certification programme | P4 | TBD | Future consideration |

### Explicitly Deferred

| Item | Reason |
|------|--------|
| Multi-agent orchestration | Not our differentiation |
| Autonomous execution mode | Contradicts positioning |
| Three-file architecture | Complexity without benefit |
| Full dashboard | Beyond scope; keep simple |
| 15+ AI tool native support | Universal format is enough |

---

## Success Criteria

### Phase 1 Complete When:
- [ ] All 5 Spec_Engine patterns integrated
- [ ] `base-workflow.toml` updated
- [ ] `dev.toml` includes troubleshooting escalation
- [ ] Documentation updated

### Phase 2 Complete When:
- [ ] `security.toml` enhanced
- [ ] Troubleshooting prominently positioned
- [ ] Pre-flight validation available

### Phase 3 Complete When:
- [ ] README reflects new positioning
- [ ] Getting started guide aligned
- [ ] At least 2 case studies published

### Phase 4 Complete When:
- [ ] MCP server enhanced
- [ ] Validation tooling functional
- [ ] CI integration working

---

## Review Schedule

| Checkpoint | Date | Focus |
|------------|------|-------|
| Phase 1 Review | Week 2 | Foundation patterns |
| Phase 2 Review | Week 4 | Core specs |
| Phase 3 Review | Week 6 | Documentation |
| Phase 4 Review | Week 8 | Infrastructure |
| Q1 Retrospective | Week 12 | Overall progress |

---

## Appendix: Research Sources

This roadmap is informed by:
- `MASTER_RESEARCH_SYNTHESIS.md` - Comprehensive landscape analysis
- `deep-research-jan-2026.md` - Framework deep dives
- `strategic-synthesis-jan-2026.md` - Market insights
- Spec_Engine analysis - Internal experiment learnings
- `TGACGTCA_weakness_summary_20260102.md` - Troubleshooting cliff insight

---

*Roadmap established: January 2026*  
*Next review: End of Phase 1*
