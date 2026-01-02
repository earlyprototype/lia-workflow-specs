# Getting Started with Lia: The AI Slow-Code Framework

> **Understand what you're building.**

Welcome to **slow-code** — deliberate AI development that prioritises understanding over speed. While "vibe coding" ships fast and breaks things, slow-code ensures you finish knowing *why* your code works, not just *that* it works.

This guide will help you start using Lia's workflow specs to transform your AI assistant from a code generator into a teaching partner.

---

## 🎯 What You'll Learn

1. How to choose the right workflow
2. How to load and execute a workflow
3. How to review and approve phases
4. How to work with generated artifacts
5. Common patterns and tips

---

## 📋 Prerequisites

### Required
- Access to an AI assistant (Claude, GPT-4, or compatible LLM)
- Basic understanding of software development
- Willingness to provide feedback and iterate

### Optional but Helpful
- Git for version control
- Text editor with TOML support
- Understanding of systematic methodologies

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Choose Your First Workflow

For your first workflow, we recommend **spec.toml** - it's the most versatile and teaches core workflow concepts.

**What it does:** Transforms a rough feature idea into detailed requirements, design, and implementation tasks.

**Good for:** Any feature, from simple to complex.

### Step 2: Load the Workflow

Share the spec with your AI assistant:

```
"I want to use the spec workflow. Here's the content from spec.toml:
[paste spec.toml content]

Let's design a user authentication feature."
```

### Step 3: Engage with the Workflow

The AI will guide you through three phases:

**Phase 1: Requirements** (10-15 minutes)
```
AI: I've drafted initial requirements based on your idea:

### Requirement 1: User Login
**User Story:** As a user, I want to log in securely...

**Acceptance Criteria:**
1. WHEN user enters valid credentials THEN system SHALL authenticate...
2. WHEN user enters invalid credentials THEN system SHALL reject...

Do the requirements look good?
```

You respond:
- "Yes, looks good" → Proceeds to next phase
- "Add OAuth support" → AI iterates
- "Change security approach" → AI revises

**Phase 2: Design** (15-20 minutes)
```
AI: Here's the architectural design:

## Architecture
- JWT-based authentication
- bcrypt password hashing
- Rate limiting middleware
[detailed design...]

Does the design look good?
```

Review, provide feedback, approve when ready.

**Phase 3: Tasks** (5-10 minutes)
```
AI: Implementation task list:

- [ ] 1. Set up JWT middleware
     - Create auth middleware with token validation
     - _Requirements: 1.1, 1.2_

- [ ] 2. Implement password hashing
     - Use bcrypt with salt rounds=10
     - _Requirements: 1.3_

[complete task list...]

Do the tasks look good?
```

Approve, and you have a complete specification!

### Step 4: Review Artifacts

Check the generated documentation:

```
.lia/
└── specs/
    └── user-authentication/
        ├── 0-notepad.md          # Insights captured during design
        ├── 1-requirements.md     # Your approved requirements
        ├── 2-design.md           # Your approved design
        └── 3-tasks.md            # Your implementation checklist
```

**Congratulations!** You've completed your first workflow. 🎉

---

## 📚 Understanding Workflows

### Core Concepts

**1. Phases**
Each workflow is divided into discrete phases:
- Clear objective
- Specific deliverables
- Approval gate before proceeding

**2. Approval Gates**
You must explicitly approve each phase:
- ✅ "Yes", "approved", "looks good" → Proceed
- 🔄 "Change X", "Add Y" → Iterate
- ❌ "Go back", "restart" → Revise

**3. Artifacts**
Every workflow creates structured markdown files:
- Persistent documentation
- Version control friendly
- Human-readable
- AI-parseable

**4. Notepad**
The 0-notepad.md captures:
- Key insights during the process
- Technical considerations
- Ideas for future enhancement
- Cross-system connections

### Operating Modes

**Collaboration Mode** (Default)
```
User: [Start workflow]
AI: [Phase 1 output]
AI: Do you approve?
User: [Feedback/Approval]
AI: [Iterate or proceed]
```

**Silent Mode** (Advanced)
```
User: [Start workflow] - run in silent mode
AI: [Executes all phases]
AI: [Returns complete artifact set]
Note: Assumptions recorded in notepad
```

---

## 🎓 Workflow Selection Guide

### When to Use Which Workflow

**Starting a New Feature?**
→ **spec.toml** - Get complete specification first

**Need to Understand Existing Code?**
→ **wtf.toml** - Feature archaeology

**Building Something While Learning?**
→ **learn.toml** - Project-based skill development

**Fixing a Bug?**
→ **troubleshoot.toml** - Systematic diagnosis

**System Crashed?**
→ **investigate.toml** - Forensic recovery

**Code Review Time?**
→ **review.toml** - Systematic quality assessment

**Performance Problems?**
→ **optimize.toml** - Data-driven optimization

**Evaluating Technologies?**
→ **research.toml** - Systematic evaluation

**Reading Academic Papers?**
→ **paper.toml** - Critical analysis and synthesis

**Enhancing Existing Features?**
→ **innovate.toml** - Creative enhancement

**Writing Documentation?**
→ **docs.toml** - Systematic documentation

**Security Concerns?**
→ **security.toml** - Security assessment

**Designing Architecture?**
→ **architecture.toml** - Architectural decisions

**Building Integrations?**
→ **integrate.toml** - API and integration design

**Comprehensive Consulting?**
→ **nexus.toml** - Multi-specialist coordination

**Setting Up Testing?**
→ **test.toml** - Testing strategy

---

## 💡 Tips for Success

### 1. Be Specific in Feedback

❌ Bad: "This doesn't look right"
✅ Good: "Change the authentication approach from sessions to JWT tokens"

### 2. Don't Skip Phases

The workflow is designed to build understanding incrementally:
- Requirements clarify what
- Design explains how
- Tasks break down execution

Skipping phases leads to confusion later.

### 3. Use the Notepad

Add your own observations to 0-notepad.md:
```markdown
## 📝 User Notes
- Need to check with security team about password requirements
- Consider adding 2FA in version 2
- OAuth integration might conflict with existing LDAP
```

### 4. Iterate Freely

Don't feel pressured to approve immediately:
- Ask questions
- Request alternatives
- Challenge assumptions
- Add requirements

The workflow is designed for iteration.

### 5. Save Artifacts

Commit the .lia/ directory to version control:
```bash
git add .lia/specs/user-authentication/
git commit -m "Complete user authentication specification"
```

These artifacts are valuable documentation.

### 6. Combine Workflows

Some tasks benefit from multiple workflows:
```
research.toml → spec.toml → dev.toml
(Evaluate)     (Design)     (Build)

review.toml → optimize.toml → test.toml
(Assess)      (Improve)        (Validate)
```

### 7. Customize for Your Domain

Fork and adapt specs to your needs:
- Add domain-specific phases
- Include compliance requirements
- Adjust approval criteria
- Add specialized constraints

---

## 🔧 Common Patterns

### Pattern 1: The Learning Loop

Using learn.toml while building:
```
1. Start learn.toml with project idea
2. Learn about required technologies
3. Build with educational scaffolding
4. Capture learning in @Learning repository
5. Reference learning in future projects
```

### Pattern 2: The Innovation Cycle

Using innovate.toml for enhancement:
```
1. Analyze current implementation
2. Ideate creative improvements
3. Evaluate by impact/effort
4. Plan implementation
5. Execute with dev.toml
```

### Pattern 3: The Research Pipeline

Using research.toml + paper.toml:
```
1. research.toml: Evaluate technology landscape
2. paper.toml: Analyze key academic papers
3. @Research repository: Build knowledge base
4. spec.toml: Design based on research
```

### Pattern 4: The Quality Cycle

Continuous improvement:
```
1. review.toml: Identify issues
2. security.toml: Check vulnerabilities
3. optimize.toml: Improve performance
4. test.toml: Validate improvements
```

---

## 🐛 Troubleshooting

### "The AI isn't following the workflow"

**Solution:** Explicitly state:
```
"Please follow the spec.toml workflow exactly as specified, including 
all phases and approval gates. Do not skip phases or combine steps."
```

### "I want to go back a phase"

**Solution:**
```
"Let's revise the requirements phase. I want to add OAuth support."
```

The workflow supports going back at any time.

### "The workflow feels too rigid"

**Solution:** Remember:
- Iteration is encouraged within phases
- You control the pace
- Silent mode available for routine tasks
- Customize specs for your needs

### "I don't understand a phase output"

**Solution:**
```
"Can you explain the JWT authentication approach in simpler terms?"
```

Ask for clarification before approving.

---

## 📖 Next Steps

### Learn More
- Read [Workflow Guide](workflow-guide.md) for detailed concepts
- Review [Best Practices](best-practices.md) for patterns
- Check [Examples](../examples/) for real-world usage

### Try More Workflows
- Start with **spec.toml** (you've done this!)
- Try **learn.toml** for educational projects
- Experiment with **innovate.toml** for creativity
- Use **troubleshoot.toml** for real bugs

### Customize
- Fork specs for your domain
- Add company-specific requirements
- Create team templates
- Build domain expertise

### Contribute
- Share your examples
- Propose new workflows
- Improve documentation
- Help others in discussions

---

## 🆘 Getting Help

**Questions about workflows?**
- Open a [Discussion](../../discussions)
- Check [FAQ](docs/faq.md)
- Join [Discord](https://discord.gg/lia-workflows)

**Found a bug?**
- Open an [Issue](../../issues)
- Include workflow name and phase
- Share relevant artifacts

**Want to contribute?**
- Read [CONTRIBUTING.md](CONTRIBUTING.md)
- Propose in [Discussions](../../discussions) first
- Submit a Pull Request

---

**Ready to become a systematic AI collaborator?**

Start with [spec.toml](../specs/development/spec.toml) and transform your next feature idea into a complete specification.

Happy systematic development! 🚀

