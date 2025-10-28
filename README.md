# Lia Workflow Specs

> **Systematic AI-Powered Development Workflows for Professional Software Engineering**

Transform AI assistants from reactive code generators into expert collaborators with structured, phase-based workflows that ensure thorough planning, rigorous execution, and continuous learning.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Specs](https://img.shields.io/badge/specs-17-green.svg)](#workflow-specifications)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🎯 What Are Workflow Specs?

Workflow specs are **structured prompts** that guide AI agents through systematic, phase-based processes. Instead of ad-hoc code generation, these specs create:

- **Stepwise execution** with user approval at each stage
- **Iterative refinement** through feedback loops
- **Persistent knowledge** captured in structured artifacts
- **Professional standards** embedded in every workflow
- **Learning systems** that improve over time

Think of them as **expert methodologies** that any AI can follow to deliver professional-grade outcomes.

---

## 🚀 Quick Start

### 1. Choose Your Workflow

```bash
# Development & Implementation
dev.toml        # Feature implementation and testing
spec.toml       # Requirements → Design → Tasks
test.toml       # Testing strategy and automation

# Code Quality & Architecture
review.toml     # Code review and quality assessment
architecture.toml  # System architecture design
security.toml   # Security assessment and hardening
optimize.toml   # Performance optimization

# Problem Solving & Diagnosis
troubleshoot.toml  # Problem diagnosis and resolution
investigate.toml   # Forensic investigation (crashes, data loss)
wtf.toml          # Feature archaeology (mysterious code)

# Research & Learning
research.toml   # Technology research and evaluation
learn.toml      # Project-based skill development
paper.toml      # Academic paper analysis

# Knowledge & Documentation
docs.toml       # Documentation and knowledge management

# Strategy & Innovation
innovate.toml   # Creative innovation and enhancement
nexus.toml      # Innovation consulting coordination
integrate.toml  # Integration and API development
```

### 2. Load and Execute

```python
# Example: Using with your AI assistant
from lia import load_workflow

# Load the workflow spec
workflow = load_workflow("specs/development/spec.toml")

# Start with a rough idea
workflow.execute("I want to build a user authentication system")

# The workflow guides you through:
# 1. Requirements gathering (EARS format)
# 2. Design document creation
# 3. Implementation task list
# Each phase requires your approval before proceeding
```

### 3. Review Artifacts

Every workflow creates structured documentation:
```
.lia/
└── specs/
    └── user-authentication/
        ├── 0-notepad.md          # Insights and observations
        ├── 1-requirements.md     # EARS format requirements
        ├── 2-design.md           # Architecture and design
        └── 3-tasks.md            # Implementation checklist
```

---

## 💡 Why Use Workflow Specs?

### Before: Ad-Hoc AI Assistance
```
You: "Build me a login system"
AI: *generates 500 lines of code*
You: "Wait, I needed OAuth..."
AI: *generates different 500 lines*
You: "This doesn't match our architecture..."
```

### After: Systematic Workflow
```
You: "Let's build a login system" (using spec.toml)

AI: [Phase 1] Here are the requirements I've drafted...
    • User story: As a user, I want to log in securely...
    • Acceptance: WHEN user submits credentials THEN system SHALL...
    Review? [You approve or iterate]

AI: [Phase 2] Here's the design considering your architecture...
    • JWT-based authentication
    • Integration with existing user service
    • Security: bcrypt + rate limiting
    Review? [You approve or iterate]

AI: [Phase 3] Implementation tasks (12 items)...
    ☐ 1. Set up JWT middleware
    ☐ 2. Implement password hashing
    ...
    Review? [You approve and execute]
```

**Result:** Aligned expectations, documented decisions, executable plan.

---

## 🌟 Key Features

### 1. **Two Operating Modes**

**Collaboration Mode** (default)
- Stepwise execution with approval gates
- Interactive feedback at each phase
- Perfect for learning and complex decisions

**Silent Mode** (user-triggered)
- Autonomous execution from start to finish
- Assumptions recorded in notepad
- Great for routine or well-understood tasks

### 2. **Persistent Knowledge Capture**

Every workflow creates a **0-notepad.md** file capturing:
- 🧠 Key insights and discoveries
- 🔧 Technical notes and implementation details
- 💡 Ideas and future enhancements
- 🔗 Cross-system connections
- 📝 User and AI observations

### 3. **Learning Systems**

Specs like `innovate.toml` and `learn.toml` include **user-led intelligence**:
- Tracks your decision patterns
- Adapts to your preferences over time
- Suggests approaches based on past successes
- Builds cumulative expertise

### 4. **Professional Standards**

Every spec embeds industry best practices:
- EARS requirements format (`spec.toml`)
- Forensic investigation methodology (`investigate.toml`)
- Academic critical analysis (`paper.toml`)
- Security assessment frameworks (`security.toml`)

### 5. **Explicit Approval Gates**

No phase skipping. No assumptions. The AI **MUST**:
- Complete each phase document
- Ask for explicit approval
- Iterate on feedback until approved
- Only then proceed to next phase

---

## 📚 Workflow Categories

### 🛠️ Development & Implementation
Build features systematically from idea to deployment.

**Use cases:**
- Feature implementation with TDD
- Bug fixing with root cause analysis
- Test automation framework setup

### 🏗️ Code Quality & Architecture
Ensure code excellence and system robustness.

**Use cases:**
- Pre-merge code reviews
- Architecture decision records
- Security vulnerability assessment
- Performance bottleneck identification

### 🔍 Problem Solving & Diagnosis
Systematically diagnose and resolve issues.

**Use cases:**
- Production incident troubleshooting
- Crash forensics and data recovery
- Understanding legacy code (feature archaeology)

### 📖 Research & Learning
Build knowledge systematically.

**Use cases:**
- Technology evaluation and POC
- Learning new frameworks through projects
- Academic literature review

### 📝 Knowledge & Documentation
Create and maintain comprehensive documentation.

**Use cases:**
- API documentation generation
- User guide creation
- Knowledge base establishment

### 🚀 Strategy & Innovation
Drive innovation and integration initiatives.

**Use cases:**
- Feature enhancement ideation
- Innovation consulting projects
- System integration planning

---

## 🎓 Example: Feature Specification Workflow

```toml
# spec.toml - Transform ideas into executable plans

[workflow]
phases = [
  "Requirements Gathering",      # EARS format with user stories
  "Design Document Creation",    # Architecture, components, data models
  "Implementation Task List"      # Coding tasks with traceability
]

[constraints]
• MUST create requirements in EARS format
• MUST ask for approval after each phase
• MUST NOT skip ahead without explicit approval
• MUST reference requirements in each task
• MUST ensure tasks are coding-focused (no deployment, user testing)

[output]
.lia/specs/{feature_name}/
  ├── 0-notepad.md           # Insights captured during process
  ├── 1-requirements.md      # User stories + acceptance criteria
  ├── 2-design.md            # Architecture decisions
  └── 3-tasks.md             # Checkbox task list with requirements traceability
```

**Real-world example:** See [examples/simple-feature-spec/](examples/simple-feature-spec/)

---

## 🔧 Advanced Usage

### Combining Workflows

Some tasks benefit from multiple workflows:

```bash
# Research → Spec → Dev
1. research.toml   # Evaluate authentication libraries
2. spec.toml       # Design your auth system
3. dev.toml        # Implement and test

# Review → Optimize → Test
1. review.toml     # Identify performance issues
2. optimize.toml   # Systematic performance improvement
3. test.toml       # Validate optimizations
```

### Customizing Specs

Fork and modify for your domain:

```toml
# custom-medical-review.toml
# Extends review.toml with medical device compliance checks

[extends]
base = "specs/quality/review.toml"

[additional_phases]
7.5 = "Medical Device Compliance Assessment"
  • ISO 13485 requirements check
  • FDA 21 CFR Part 11 validation
  • Risk management per ISO 14971
```

### Silent Mode for Automation

```python
# Automated nightly code review
workflow = load_workflow("specs/quality/review.toml")
workflow.mode = "silent"  # No user approval needed
workflow.execute(changed_files=git.get_diff())
# Results logged to .lia/review/nightly-{date}/
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:

- **New spec proposals** - Have a systematic workflow to share?
- **Spec improvements** - Better phases, constraints, or templates?
- **Examples** - Real-world usage and results?
- **Documentation** - Clearer explanations and guides?
- **Tools** - Validators, visualizers, generators?

### Spec Design Principles

When creating new specs, follow these principles:

1. **Phase-based structure** - Clear, sequential stages
2. **Explicit constraints** - MUST/SHOULD/MAY requirements
3. **Approval gates** - User review between phases
4. **Persistent artifacts** - Structured documentation output
5. **Learning capture** - 0-notepad.md for insights
6. **Professional standards** - Industry best practices embedded
7. **Dual modes** - Support both collaboration and silent execution

---

## 📊 Comparison with Other Tools

| Feature | Lia Workflows | Traditional PM Tools | Basic AI Assistants |
|---------|---------------|---------------------|---------------------|
| **Systematic Process** | ✅ Built-in | ⚠️ Manual setup | ❌ Ad-hoc |
| **Phase Approval** | ✅ Enforced | ⚠️ Optional | ❌ None |
| **Knowledge Capture** | ✅ Automatic | ⚠️ Manual | ❌ Lost |
| **Learning System** | ✅ Adaptive | ❌ Static | ❌ None |
| **AI-Native** | ✅ Yes | ❌ No | ✅ Yes |
| **Professional Standards** | ✅ Embedded | ⚠️ Template-based | ❌ None |
| **Customizable** | ✅ Open source | ⚠️ Vendor lock-in | ❌ Black box |

---

## 🗺️ Roadmap

### v1.0 (Current)
- ✅ 17 core workflow specs
- ✅ Collaboration and Silent modes
- ✅ Persistent knowledge capture
- ✅ User-led intelligence (innovate, learn)

### v1.1 (Next)
- [ ] Spec validation tooling
- [ ] Workflow visualization
- [ ] VS Code extension
- [ ] Example library expansion

### v2.0 (Future)
- [ ] Spec composition (combine workflows)
- [ ] Analytics and metrics
- [ ] Team collaboration features
- [ ] Spec marketplace
- [ ] AI fine-tuning on workflow patterns

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

## 📖 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [Workflow Guide](docs/workflow-guide.md)
- [Customization Guide](docs/customization.md)
- [Best Practices](docs/best-practices.md)
- [Comparison with Alternatives](docs/comparison.md)
- [API Reference](docs/api-reference.md)

---

## 💬 Community

- **Discussions:** [GitHub Discussions](../../discussions)
- **Discord:** [Join our community](https://discord.gg/lia-workflows)
- **Blog:** [Workflow patterns and case studies](https://blog.lia-workflows.org)
- **Twitter:** [@LiaWorkflows](https://twitter.com/liaworkflows)

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Inspired by:
- **Systematic Software Engineering** - Rigorous development methodologies
- **Academic Research Protocols** - Evidence-based systematic reviews
- **Design Thinking** - Human-centered iterative processes
- **Agile/XP Practices** - Incremental, feedback-driven development
- **AI Agent Research** - LangChain, AutoGPT, BabyAGI patterns

Built with lessons from thousands of hours of AI-assisted development.

---

## 🌟 Star History

If you find these workflow specs valuable, please star the repository! It helps others discover systematic AI collaboration.

[![Star History Chart](https://api.star-history.com/svg?repos=username/lia-workflow-specs&type=Date)](https://star-history.com/#username/lia-workflow-specs&Date)

---

**Ready to transform your AI assistant into an expert collaborator?**

[Get Started →](docs/getting-started.md) | [Browse Specs →](specs/) | [See Examples →](examples/)

---

<div align="center">
Made with ❤️ by developers, for developers
<br>
<sub>Building the future of systematic AI collaboration</sub>
</div>

