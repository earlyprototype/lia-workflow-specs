# Best Practices: Mastering Systematic AI Workflows

## Table of Contents

1. [Workflow Selection](#workflow-selection)
2. [Phase Management](#phase-management)
3. [Artifact Organization](#artifact-organization)
4. [Team Collaboration](#team-collaboration)
5. [Common Patterns](#common-patterns)
6. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
7. [Performance Tips](#performance-tips)
8. [Scaling Workflows](#scaling-workflows)

---

## Workflow Selection

### Match Workflow to Context

| Situation | Recommended Workflow | Why |
|-----------|---------------------|-----|
| New feature from scratch | `spec.toml` | Complete requirements → design → tasks |
| Bug in production | `troubleshoot.toml` | Systematic diagnosis and resolution |
| System crashed | `investigate.toml` | Forensic investigation and recovery |
| Mystery feature | `wtf.toml` | Archaeological reconstruction of intent |
| Learning new tech | `learn.toml` | Project-based skill development |
| Pre-merge review | `review.toml` | Quality assessment and feedback |
| Performance issues | `optimize.toml` | Data-driven optimization |
| Security concerns | `security.toml` | Comprehensive security assessment |
| Evaluating technology | `research.toml` | Systematic evaluation |
| Reading papers | `paper.toml` | Critical analysis and synthesis |
| Feature enhancement | `innovate.toml` | Creative improvement |
| Documentation | `docs.toml` | Knowledge management |

### When to Combine Workflows

**Research → Design → Build:**
```
1. research.toml   # Evaluate authentication approaches
2. spec.toml       # Design auth system
3. dev.toml        # Implement with TDD
```

**Review → Fix → Test:**
```
1. review.toml     # Identify issues
2. dev.toml        # Fix problems
3. test.toml       # Validate fixes
```

**Understand → Enhance → Integrate:**
```
1. wtf.toml        # Understand existing feature
2. innovate.toml   # Design enhancements
3. integrate.toml  # Plan integration
```

---

## Phase Management

### Iteration Strategy

**Iterate Early:**
- Requirements phase: Cheap to change
- Design phase: Moderate cost
- Implementation phase: Expensive to change

**When to Iterate:**
- Missing requirements discovered
- Better approach identified
- Unclear acceptance criteria
- Design doesn't align with constraints

**When to Move Forward:**
- Good enough for now
- Can refine during implementation
- Minor details that won't block progress

### Approval Mindset

**Take Your Time:**
```
BAD:  Rushed approval: "Sure, looks fine" (without reading)
GOOD: Thoughtful review: "Let me check... can you clarify point 3?"
```

**Ask Questions:**
```
BAD:  Accepting confusion: "I don't fully understand but ok"
GOOD: Seeking clarity: "Why JWT instead of sessions here?"
```

**Challenge Assumptions:**
```
BAD:  Passive acceptance: "If you say so"
GOOD: Active engagement: "Have we considered the scalability impact?"
```

### Phase Documentation

**During Phases:**
- Add observations to notepad in real-time
- Capture rationale for decisions
- Document alternatives considered
- Note future enhancement ideas

**Between Phases:**
- Review previous phase artifacts
- Ensure consistency across phases
- Update notepad with connections
- Verify traceability

---

## Artifact Organization

### Directory Structure

**Recommended:**
```
project/
├── .lia/
│   ├── specs/
│   │   ├── user-authentication/
│   │   │   ├── 0-notepad.md
│   │   │   ├── 1-requirements.md
│   │   │   ├── 2-design.md
│   │   │   └── 3-tasks.md
│   │   └── payment-integration/
│   ├── reviews/
│   │   └── pre-merge-2025-10-28/
│   ├── research/
│   │   └── database-evaluation/
│   └── optimizations/
│       └── api-performance/
├── src/
├── tests/
└── docs/
```

### Artifact Maintenance

**Version Control:**
```bash
# Commit artifacts with code
git add .lia/specs/user-authentication/
git commit -m "Complete user authentication specification

- 8 requirements with EARS format
- JWT-based architecture design
- 15 implementation tasks"
```

**Update as Project Evolves:**
- Requirements change → Update 1-requirements.md
- Design evolves → Update 2-design.md
- Tasks completed → Check off in 3-tasks.md
- Insights gained → Add to 0-notepad.md

**Reference in Documentation:**
```markdown
# User Authentication

See specification: [.lia/specs/user-authentication/](../.lia/specs/user-authentication/)

## Requirements
[Link to requirements doc]

## Design Decisions
[Reference design doc]
```

---

## Team Collaboration

### Shared Workflows

**Individual Workflows:**
Each developer runs workflows locally:
```
Developer A: spec.toml → user-auth feature
Developer B: spec.toml → payment integration
Developer C: review.toml → code quality
```

**Shared Artifacts:**
Commit .lia/ artifacts to repository:
- Team sees reasoning
- Context is preserved
- Knowledge is shared

### Code Review Integration

**Pre-Review:**
```
1. review.toml (self-review)
2. Address findings
3. Submit PR with .lia/reviews/ artifacts
```

**PR Description:**
```markdown
## Changes
- Implemented user authentication

## Specification
See: .lia/specs/user-authentication/

## Self-Review
Ran review.toml workflow:
- [x] No critical issues
- [!] 2 minor improvements documented
See: .lia/reviews/user-auth-self-review/
```

### Knowledge Sharing

**Onboarding:**
```
New team member reads:
1. .lia/specs/ for feature context
2. .lia/reviews/ for quality standards
3. .lia/research/ for technology decisions
```

**Architecture Decisions:**
```
.lia/architecture/api-design/
├── 0-notepad.md  # Rationale and tradeoffs
├── 1-analysis.md # Current state
└── 2-design.md   # Proposed architecture
```

---

## Common Patterns

### Pattern: Learning Loop

**Use Case:** Building while learning new technology

```
1. learn.toml (Start learning React)
   → Creates @Learning/react-basics/
   
2. Project: Build TODO app
   → Captures learning in notepad
   
3. @Learning grows with each project
   → Reference in future React projects
```

**Benefits:**
- Cumulative learning
- Contextual knowledge
- Reusable patterns

### Pattern: Innovation Cycle

**Use Case:** Enhancing existing features

```
1. wtf.toml (Understand current implementation)
   → Document how it works
   
2. innovate.toml (Design enhancements)
   → Generate creative improvements
   
3. spec.toml (Detail specification)
   → Plan implementation
   
4. dev.toml (Build with tests)
   → Implement systematically
```

### Pattern: Quality Gate

**Use Case:** Ensuring production readiness

```
Before merge:
1. review.toml    # Code quality
2. security.toml  # Security assessment
3. optimize.toml  # Performance check
4. test.toml      # Test coverage

All artifacts committed with PR
```

### Pattern: Research Pipeline

**Use Case:** Technology evaluation and adoption

```
1. research.toml (Evaluate options)
   → Compare 3-5 solutions
   → @Research/database-evaluation/
   
2. paper.toml (Read key papers)
   → Understand theory
   → @Research/papers/
   
3. spec.toml (Design integration)
   → Plan implementation
   
4. dev.toml (Build POC)
   → Prove concept
```

### Pattern: Incident Response

**Use Case:** Production issues

```
1. troubleshoot.toml (Diagnose)
   → Identify root cause
   
2. investigate.toml (If data loss)
   → Forensic recovery
   
3. spec.toml (Design fix)
   → Proper solution
   
4. dev.toml (Implement)
   → With tests
   
5. docs.toml (Document)
   → Incident report + prevention
```

---

## Anti-Patterns to Avoid

### Anti-Pattern: Skipping Approval Gates

**Problem:**
```
AI: Here's the requirements [shows output]
    Moving to design...  [doesn't wait]
```

**Impact:**
- Misaligned expectations
- Wasted effort on wrong design
- Late discovery of issues

**Solution:**
```
"Please wait for my approval after each phase. 
Don't proceed to the next phase without explicit confirmation."
```

### Anti-Pattern: Ignoring the Notepad

**Problem:**
```
0-notepad.md remains empty or generic
No insights captured during workflow
```

**Impact:**
- Lost knowledge
- No learning accumulation
- Missing context for future

**Solution:**
- Add your own notes actively
- Review and update notepad
- Use it as thinking space

### Anti-Pattern: Wrong Workflow Selection

**Problem:**
```
Using dev.toml for a new feature (no spec)
Using troubleshoot.toml for a mystery feature (need wtf.toml)
```

**Impact:**
- Missing important phases
- Inadequate methodology
- Poor outcomes

**Solution:**
- Consult [Workflow Selection](#workflow-selection)
- Use spec.toml for new features
- Match workflow to context

### Anti-Pattern: Passive Collaboration Mode

**Problem:**
```
User: "Looks good" (without reviewing)
User: "Approved" (didn't read artifacts)
```

**Impact:**
- Quality issues slip through
- Misalignment discovered late
- Defeats purpose of approval gates

**Solution:**
- Actually read the artifacts
- Ask questions
- Iterate until genuinely satisfied

### Anti-Pattern: Silent Mode Overuse

**Problem:**
```
Using silent mode for:
- Learning situations
- Complex ambiguous tasks
- High-stakes decisions
```

**Impact:**
- Missing learning opportunities
- Wrong assumptions made
- Suboptimal outcomes

**Solution:**
- Use collaboration mode for learning
- Reserve silent mode for routine tasks
- Review assumptions in notepad carefully

### Anti-Pattern: Abandoning Artifacts

**Problem:**
```
Workflow completes → Files ignored
Project evolves → Artifacts not updated
Team member asks → "I don't remember why"
```

**Impact:**
- Lost institutional knowledge
- Context erosion
- Repeated mistakes

**Solution:**
- Commit artifacts to version control
- Update as project evolves
- Reference in discussions

---

## Performance Tips

### Speed Up Workflows

**1. Use Silent Mode for Routine Tasks:**
```
Simple, well-understood features → Silent mode
Complex, ambiguous features → Collaboration mode
```

**2. Approve Quickly When Confident:**
```
If requirements look solid → Approve
If design is straightforward → Approve
Don't overthink routine decisions
```

**3. Iterate in Batches:**
```
BAD:  Sequential: "Add OAuth" → wait → "Add 2FA" → wait
GOOD: Batched: "Add OAuth and 2FA support"
```

**4. Prepare Context:**
```
Before starting workflow:
- Gather related documents
- Clarify constraints
- Identify stakeholders
- Define success criteria
```

### Reduce Iteration Cycles

**Be Specific Initially:**
```
BAD:  Vague: "Build user authentication"
GOOD: Specific: "Build JWT-based authentication with OAuth 
             support for Google and GitHub, password reset, 
             and rate limiting"
```

**Anticipate Requirements:**
```
Think ahead:
- What integrations are needed?
- What scale/performance?
- What security requirements?
- What compliance needs?
```

**Reference Examples:**
```
"Build authentication similar to how GitHub does it"
"Follow the OAuth 2.0 spec precisely"
"Use the same patterns as our user service"
```

---

## Scaling Workflows

### Individual to Team

**Start Individual:**
```
You: Run workflows locally
Artifacts: Personal learning
```

**Scale to Team:**
```
Team: Share workflow artifacts
Repository: .lia/ committed
Benefits: Shared context, knowledge preservation
```

### Single Project to Portfolio

**Single Project:**
```
.lia/
└── specs/
    └── feature-a/
```

**Portfolio:**
```
.lia/
├── specs/
│   ├── feature-a/
│   ├── feature-b/
│   └── feature-c/
├── @Learning/      # Cumulative learning
├── @Research/      # Technology knowledge
└── @Architecture/  # Design decisions
```

### Process to Culture

**Adoption Phases:**

**Phase 1: Individual Adoption**
- You use workflows
- Prove value personally
- Build expertise

**Phase 2: Team Introduction**
- Demo to teammates
- Share successful artifacts
- Collaborative workflows

**Phase 3: Team Standard**
- Spec before code (required)
- Review workflow (mandatory)
- Artifacts in all PRs

**Phase 4: Organizational Culture**
- Workflows for all development
- Knowledge repositories valued
- Systematic approach default

---

## Summary

### Do:
- Choose appropriate workflows
- Iterate within phases
- Take time to review
- Capture knowledge in notepad
- Commit artifacts to git
- Reference artifacts in discussions
- Update artifacts as project evolves
- Share workflows with team

### Don't:
- Skip approval gates
- Ignore the notepad
- Use wrong workflow for context
- Rush through reviews
- Overuse silent mode
- Abandon artifacts after workflow
- Keep knowledge siloed

---

## Next Steps

- Read [Workflow Guide](workflow-guide.md) for deep dive
- Try [Getting Started](../GETTING_STARTED.md) tutorial
- Explore [Examples](../examples/) for patterns
- Check [Customization](customization.md) for adaptation

---

**Build better software through systematic AI collaboration.**
