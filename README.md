# Lia: The AI Slow-Code Framework

> **Understand what you're building.**

While "vibe coding" ships fast and breaks things, **slow-code** is deliberate AI development that prioritises understanding over speed. Every phase visible. Every decision documented. You finish knowing *why* it works, not just *that* it works.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Specs](https://img.shields.io/badge/specs-18-green.svg)](#workflow-specifications)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## 🎯 What Is Slow-Code?

**Slow-code** is a counter-movement to "vibe coding" — the practice of rapidly generating AI code without understanding it.

| Vibe Coding | Slow-Code |
|-------------|-----------|
| "AI does the work for you" | "AI teaches you while you work" |
| Ship fast, fix later | Understand first, ship confidently |
| Black box execution | Glass box transparency |
| Hope it works | Know why it works |
| Debugging is pain | Debugging is structured |

### Why Slow-Code?

1. **Vibe coding creates debt** — Fast AI output without understanding compounds into maintenance nightmares
2. **The Troubleshooting Cliff** — AI tools achieve ~100% success creating code, then fail catastrophically debugging it
3. **Understanding is speed** — Developers who understand their code ship faster long-term

### What Makes Lia Different

- **🐢 Slow-Code Philosophy** — Deliberate, phase-by-phase development
- **🔍 Transparency** — Every phase visible, every decision documented
- **🔧 Troubleshooting First** — Structured debugging when others leave you stranded
- **📚 Educational DNA** — Learning specs (`learn.toml`, `research.toml`, `paper.toml`)
- **🛠️ Tool Agnostic** — TOML works in Cursor, Claude, Windsurf, anywhere
- **📦 Simplicity** — Single files, no complex multi-file sync

---

## 🔧 Headline Feature: Troubleshooting Ecosystem

Most AI tools help you **create** code. Few help you **debug** it. Lia has a complete troubleshooting ecosystem:

| Spec | When to Use | What It Does |
|------|-------------|--------------|
| `troubleshoot.toml` | Something's broken | Systematic diagnosis and resolution |
| `wtf.toml` | Code is mysterious | Feature archaeology — understand why code exists |
| `investigate.toml` | Need root cause | Forensic analysis for crashes, data loss, security |

**Why This Matters**: Research shows AI tools achieve near-perfect success during creation, then fail catastrophically during debugging (the "Troubleshooting Cliff"). Lia solves what others can't.

```bash
# When your code breaks and you don't know why
lia troubleshoot "API returning 500 errors intermittently"

# When you inherit mysterious legacy code
lia wtf "What does this auth middleware actually do?"

# When you need forensic root cause analysis
lia investigate "Production database corruption incident"
```

---

## 🚀 Quick Start

### 1. Choose Your Workflow

```bash
# 🛠️ Development & Implementation
dev.toml        # Feature implementation with proof artifacts
spec.toml       # Requirements → Design → Tasks (brownfield-aware)
test.toml       # Testing strategy and automation

# ✅ Code Quality & Architecture
review.toml        # Code review and quality assessment
architecture.toml  # System architecture design
security.toml      # Security assessment and hardening
optimize.toml      # Performance optimisation
constitution.toml  # Project standards definition (run first!)

# 🔧 Problem Solving & Diagnosis ← OUR STRENGTH
troubleshoot.toml  # Systematic problem diagnosis
investigate.toml   # Forensic root cause analysis
wtf.toml           # Feature archaeology (mysterious code)

# 📚 Research & Learning ← EDUCATIONAL DNA
research.toml   # Technology research and evaluation
learn.toml      # Project-based skill development
paper.toml      # Academic paper analysis
recon.toml      # Strategic landscape reconnaissance

# 📝 Knowledge & Documentation
docs.toml       # Documentation and knowledge management

# 🚀 Strategy & Innovation
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

## 🔌 MCP Server - Remote Agent Access

Connect any MCP-compatible AI agent to your workflow specs with the built-in MCP server.

### Quick Setup

```bash
# Install the MCP server
cd mcp-server
pip install -e .

# Or use the installer
./install.sh --global
```

### Configure Your Client

**Claude Desktop** (`~/.config/claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "lia-workflow-specs": {
      "command": "python3",
      "args": ["-m", "lia_workflow_mcp.server"],
      "env": {"LIA_SPECS_DIR": "~/.lia/specs"}
    }
  }
}
```

### Available Features

| Feature | Description |
|---------|-------------|
| **37 Resources** | Access specs, metadata, and quick reference guides |
| **11 Tools** | Search, recommend, validate, compare workflows |
| **20+ Prompts** | Ready-to-use workflow starter templates |

### Example Usage

```
User: "I need to implement a secure authentication feature"

Agent uses MCP tools:
→ recommend_workflow("implement secure authentication")
→ Returns: spec → dev → security → test

Agent uses MCP prompt:
→ start-spec(task="user authentication with OAuth2")
→ Begins systematic requirements gathering
```

📖 See [mcp-server/README.md](mcp-server/README.md) for full documentation.

---

## 💡 Why Lia?

### The Problem with "Fast AI"

Most AI coding tools optimise for **speed**. But speed without understanding creates technical debt:

```
You: "Build me a login system"
AI: *generates 500 lines of code in 30 seconds*
You: "It's broken. Fix it."
AI: *tries 5 different fixes, none work*
You: "WHY is it broken?!"
AI: *no structured approach, circular debugging*
```

This is the **Troubleshooting Cliff** — AI achieves near-perfect success during creation, then fails catastrophically during maintenance.

### The Lia Approach: Understand First

```
You: "Let's build a login system" (using spec.toml)

AI: LIA-SPEC-1️⃣ [Phase 1] Let me understand the requirements...
    • User story: As a user, I want to log in securely...
    • Acceptance: WHEN user submits credentials THEN system SHALL...
    • Scope Check: 🟢 Minimal complexity
    Review? [You understand and approve]

AI: LIA-SPEC-2️⃣ [Phase 2] Here's the design with rationale...
    • JWT-based authentication — because {reason}
    • Integration with existing user service — here's how it fits
    • Security: bcrypt + rate limiting — addressing these threats
    Review? [You understand and approve]

AI: LIA-SPEC-3️⃣ [Phase 3] Implementation tasks with traceability...
    ☐ 1. Set up JWT middleware [Req: AUTH-001]
    ☐ 2. Implement password hashing [Req: SEC-002]
    ...
```

**Result:** You understand every decision. When something breaks, you know why.

### When It Breaks (And It Will)

```
You: "The login is failing intermittently"

AI: [Using troubleshoot.toml]
    Phase 1: Symptom documentation...
    Phase 2: Hypothesis generation...
    Phase 3: Systematic testing...
    Phase 4: Root cause identified — race condition in token refresh
    Phase 5: Verified fix with proof artifact
```

**Other tools**: Leave you stranded at the Troubleshooting Cliff.  
**Lia**: Has a structured path down.

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

### Lia vs Speed-Focused Tools

| Dimension | Spec Kit / OpenSpec | Lia |
|-----------|---------------------|-----|
| **Philosophy** | "AI does the work" | "AI teaches you to work" |
| **Speed** | Fast, autonomous | Deliberate, transparent |
| **Troubleshooting** | Limited / ad-hoc | Structured ecosystem |
| **Complexity** | Multi-file, CLI-heavy | Single TOML, simple |
| **Learning curve** | Steep | Gentle |
| **Best for** | Experienced devs, speed | All devs, understanding |

### Feature Comparison

| Feature | Lia | Speed Tools | Basic AI |
|---------|-----|-------------|----------|
| **Transparency** | ✅ Every step visible | ⚠️ Partial | ❌ Black box |
| **Troubleshooting** | ✅ 3 dedicated specs | ❌ Ad-hoc | ❌ None |
| **Phase Approval** | ✅ Enforced | ⚠️ Optional | ❌ None |
| **Context Markers** | ✅ Detect context rot | ❌ None | ❌ None |
| **Proof Artifacts** | ✅ Before commit | ⚠️ Implicit | ❌ None |
| **Tool Agnostic** | ✅ Works anywhere | ⚠️ Vendor-specific | ✅ Yes |
| **Educational Focus** | ✅ Core value | ❌ Not a goal | ❌ None |
| **Simplicity** | ✅ Single files | ❌ Complex setup | ✅ Simple |

---

## 🗺️ Roadmap

### v1.0 (Current)
- ✅ 18 core workflow specs
- ✅ Troubleshooting ecosystem (troubleshoot, wtf, investigate)
- ✅ Educational specs (learn, research, paper, recon)
- ✅ Constitution and scope guards
- ✅ Context markers and proof artifacts
- ✅ Collaboration and Silent modes
- ✅ MCP server for remote agent access

### v1.1 (In Progress)
- [ ] Alternative reasoning backup patterns
- [ ] Error propagation strategies
- [ ] Enhanced security spec
- [ ] Spec validation tooling
- [ ] Troubleshooting quick-start guide

### v2.0 (Future)
- [ ] Lightweight progress viewer (simple, not dashboard)
- [ ] VSCode extension (spec browser)
- [ ] University/bootcamp partnerships
- [ ] Community spec library
- [ ] Case studies and learning outcomes

### Explicitly Not Planned
- ❌ Autonomous execution mode (contradicts our positioning)
- ❌ Multi-agent orchestration (not our differentiation)
- ❌ Full dashboard (keep it simple)

See [DEVELOPMENT_ROADMAP.md](DEVELOPMENT_ROADMAP.md) for detailed planning.
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

