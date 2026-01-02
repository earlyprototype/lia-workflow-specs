# Lia: The AI Slow-Code Framework

> **Understand what you're building.**

This document provides a comprehensive overview of all 18 workflow specs in Lia — the **slow-code** framework for deliberate AI development.

**What is Slow-Code?** A counter-movement to "vibe coding." While vibe coding ships fast and breaks things, slow-code prioritises understanding over speed. You finish knowing *why* it works, not just *that* it works.

**Core Philosophy**: Transparent, phase-by-phase workflows that leave you more knowledgeable than before.

**Competitive Advantage**: Our troubleshooting ecosystem (`troubleshoot`, `wtf`, `investigate`) solves the "Troubleshooting Cliff" — where AI succeeds at creation but fails at debugging.

---

## Command Reference

### 1. architecture.toml
**Purpose:** System Architecture Design and Architectural Decision Making

Guides systematic architecture workflows for designing robust system architectures, making architectural decisions, establishing design patterns, and implementing architectural governance.

**Key Capabilities:**
- Architectural requirements and context analysis
- Architectural vision and strategy development
- High-level architecture design
- Detailed component architecture design
- Integration and interface architecture design
- Quality attributes and non-functional requirements design
- Architecture validation and review
- Architecture implementation and governance

**When to Use:** When designing system architectures, making architectural decisions, or establishing design patterns for scalable, maintainable systems.

---

### 2. dev.toml
**Purpose:** Development Implementation, Testing, and Coding Tasks

Guides systematic development workflows for implementing features, fixing bugs, building systems, and conducting comprehensive testing through structured, iterative approaches.

**Key Capabilities:**
- Task analysis and planning
- Environment and setup configuration
- Feature implementation
- Testing and quality assurance
- Documentation and handover
- Deployment and validation

**When to Use:** When implementing new features, fixing bugs, building systems, or conducting comprehensive testing for any development task.

---

### 3. docs.toml
**Purpose:** Documentation and Knowledge Management

Guides systematic documentation and knowledge management workflows for creating comprehensive documentation, organizing knowledge effectively, and maintaining documentation quality.

**Key Capabilities:**
- Documentation requirements and audience analysis
- Documentation strategy and information architecture design
- Content planning and outline development
- Documentation content creation and development
- Documentation review and quality assurance
- Documentation publication and distribution
- Documentation maintenance and continuous improvement

**When to Use:** When creating technical documentation, user guides, API documentation, or establishing knowledge management systems.

---

### 4. innovate.toml
**Purpose:** Creative Innovation and Feature Enhancement

Specialises in expanding and enhancing existing implementations through creative exploration, strategic thinking, and systematic innovation. Helps discover untapped potential and high-impact, low-cost features.

**Key Capabilities:**
- Discovery and analysis (SWOT, capability inventory, gap analysis)
- Creative ideation (SCAMPER, brainstorming, analogical thinking)
- Strategic evaluation and prioritisation (Impact/Effort Matrix, RICE Framework)
- Innovation implementation planning (rapid prototyping, MVP development)
- User-led intelligence (learning from user preferences and patterns)

**When to Use:** When looking to enhance existing features, discover synergistic opportunities, or systematically explore innovation possibilities in current implementations.

---

### 5. integrate.toml
**Purpose:** Integration and API Development

Guides systematic integration and API development workflows for designing robust APIs, planning system integrations, implementing interfaces, and validating integration success.

**Key Capabilities:**
- Integration requirements and scope analysis
- API design and interface specification
- Integration architecture and design
- Integration implementation and development
- Integration testing and validation
- Integration deployment and configuration
- Integration monitoring and maintenance

**When to Use:** When developing APIs, integrating systems, implementing interfaces, or establishing connectivity between components.

---

### 6. investigate.toml
**Purpose:** Forensic Investigation and Recovery (Crashes, Data Loss, System State Changes)

Guides systematic forensic investigation workflows after crashes, data loss, or system state changes. Helps analyse current state, identify discrepancies, and recover to stable, functional state.

**Key Capabilities:**
- Incident context and scope analysis
- Current state assessment and evidence collection
- Last known good state reconstruction (including .chats/ and docs/ analysis)
- Discrepancy analysis and root cause investigation
- Recovery planning and risk assessment
- Recovery execution and validation
- Post-recovery analysis and prevention planning

**When to Use:** When investigating crashes, data loss, corruption, or system state changes requiring forensic analysis and recovery.

---

### 7. learn.toml
**Purpose:** Learning Co-pilot and Skill Development

Guides systematic project-based learning workflows for non-native developers using AI coding as hands-on learning opportunity. Builds technical, architectural, and professional literacies.

**Key Capabilities:**
- Learning profile assessment and project context
- Tool ecosystem mapping and educational reconnaissance
- Architecture design with educational scaffolding
- Implementation planning with learning checkpoints
- Guided implementation with proactive learning support
- Code quality and professional practice integration
- Knowledge synthesis and pattern recognition development
- Competency assessment using Three Epochs framework (Recognise → Understand → Communicate)

**When to Use:** When learning new technologies, building projects for educational purposes, or developing systematic software development skills through hands-on practice.

---

### 8. nexus.toml
**Purpose:** Innovation Consulting Coordinator

Manages specialized innovation consulting teams to deliver comprehensive consulting services for design, strategy, and transformation projects. Coordinates domain specialists for enterprise-grade innovation initiatives.

**Key Capabilities:**
- Client discovery and project scoping
- Innovation strategy and approach design
- Current state analysis and assessment
- Innovation opportunity identification
- Solution design and development
- Implementation planning and roadmap development
- Risk assessment and mitigation planning
- Team coordination (Client Owner, Service Designer, UX Specialist, Business Analyst, Technical Evaluator, Change Management, Project Coordinator)

**When to Use:** When conducting complex innovation consulting projects, coordinating multiple specialist perspectives, or delivering comprehensive transformation strategies.

---

### 9. optimize.toml
**Purpose:** Performance Optimization

Guides systematic performance optimization workflows for analysing system performance, identifying bottlenecks, implementing optimizations, and validating improvements through data-driven approaches.

**Key Capabilities:**
- Performance baseline and goal definition
- Performance profiling and bottleneck identification
- Root cause analysis and optimization strategy
- Optimization implementation and testing
- Performance validation and benchmarking
- Monitoring and long-term performance management

**When to Use:** When addressing performance issues, optimizing system performance, reducing resource usage, or improving response times.

---

### 10. research.toml
**Purpose:** Technology Research, Vendor Evaluation, and Proof of Concept

Guides systematic research workflows for conducting thorough technology research, evaluating solutions, assessing vendors, developing proof of concepts, and making informed technology decisions.

**Key Capabilities:**
- Research scope and requirements analysis
- Research methodology and approach design
- Technology landscape and market research
- Solution evaluation and comparison analysis
- Vendor assessment and due diligence
- Proof of concept development and testing
- Research synthesis and recommendation development

**When to Use:** When evaluating technologies, researching solutions, assessing vendors, or developing proof of concepts for technology decisions.

---

### 11. review.toml
**Purpose:** Code Review and Quality Assessment

Guides systematic code review workflows for analysing code quality, identifying issues, suggesting improvements, and ensuring best practices through structured, thorough review processes.

**Key Capabilities:**
- Code context and scope analysis
- Project structure and build documentation analysis (identifying canonical vs defunct documentation)
- Code structure and architecture review
- Code quality and standards assessment
- Security and safety review
- Testing and validation assessment
- Improvement recommendations and action items

**When to Use:** When conducting code reviews, assessing code quality, identifying improvement opportunities, or establishing quality standards.

---

### 12. security.toml
**Purpose:** Security Assessment and Hardening

Guides systematic security assessment workflows for identifying security vulnerabilities, assessing risks, implementing security controls, and validating security measures.

**Key Capabilities:**
- Security scope and context analysis
- Threat modeling and risk assessment
- Security architecture and control review
- Vulnerability assessment and testing
- Security control implementation and remediation
- Security validation and testing
- Security monitoring and continuous assessment

**When to Use:** When conducting security assessments, identifying vulnerabilities, implementing security controls, or establishing security governance.

---

### 13. spec.toml
**Purpose:** Technical Specification Development (Requirements → Design → Tasks)

Guides systematic feature specification development by transforming rough ideas into detailed design documents with implementation plans following spec-driven development methodology.

**Key Capabilities:**
- Requirement gathering (EARS format with user stories)
- Feature design document creation (architecture, components, data models, testing strategy)
- Task list creation (coding tasks with requirement traceability)
- Iterative refinement with user approval at each stage

**When to Use:** When developing complex features requiring systematic planning, creating design documents, or establishing implementation roadmaps from initial ideas.

---

### 14. test.toml
**Purpose:** Testing Strategy and Automation

Guides systematic testing strategy and automation workflows for designing comprehensive testing approaches, selecting appropriate frameworks, implementing test automation, and establishing quality assurance processes.

**Key Capabilities:**
- Testing requirements and quality objectives analysis
- Testing strategy and approach design
- Test automation framework and tool selection
- Test automation implementation and development
- Testing execution and validation
- Test maintenance and continuous improvement

**When to Use:** When designing testing strategies, implementing test automation, establishing quality assurance processes, or improving testing practices.

---

### 15. troubleshoot.toml
**Purpose:** Troubleshooting and Problem Resolution

Guides systematic troubleshooting workflows for diagnosing, analysing, and resolving technical issues through structured, methodical approaches that ensure thorough investigation and effective solutions.

**Key Capabilities:**
- Issue assessment and initial analysis
- Information gathering and investigation
- Root cause analysis
- Solution development and planning
- Solution implementation and testing
- Verification and monitoring
- Documentation and knowledge management

**When to Use:** When diagnosing technical issues, resolving bugs, investigating system problems, or implementing systematic problem-solving approaches.

---

### 16. wtf.toml
**Purpose:** Feature Archaeology (Understanding Mysterious Features)

Guides systematic feature archaeology workflows for analysing mysterious or poorly understood features, reconstructing original intent, and developing coherent integration strategies.

**Key Capabilities:**
- Feature context and scope analysis
- Historical evidence collection and timeline reconstruction (git history, PRs, .chats/, docs/)
- Original intent and business context reconstruction
- Technical decision analysis and architecture assessment
- Evolution history and modification patterns
- Current relevance and impact assessment
- Ecosystem analysis and alternative assessment
- Integration strategy and implementation planning

**When to Use:** When encountering mysterious features, understanding legacy code, reconstructing historical context, or developing integration strategies for undocumented functionality.

---

### 17. recon.toml
**Purpose:** Strategic Landscape Reconnaissance

Guides systematic landscape reconnaissance for discovering, analysing, and synthesising intelligence about technology ecosystems, competitive spaces, and market landscapes before making strategic decisions.

**Key Capabilities:**
- Multi-dimensional search taxonomy creation
- Systematic scanning across 8-12 dimensions
- Tiered discovery classification (Dominant → Major → Growing → Emerging)
- Deep dive analysis on category leaders
- Pattern extraction across projects
- Gap and opportunity analysis
- Competitive positioning assessment
- Strategic recommendations with priority actions

**When to Use:** When entering a new technology space, evaluating competitive landscapes, making build-vs-buy decisions, or needing comprehensive ecosystem understanding before strategic planning.

---

### 18. constitution.toml
**Purpose:** Project Standards and Governance Definition

Guides systematic definition of project-wide standards, principles, and quality gates that govern all development activities. Inspired by the industry-standard "constitution" pattern.

**Key Capabilities:**
- Project context and stakeholder analysis
- Code standards definition (style, quality, patterns)
- Quality gate establishment (testing, documentation, review)
- Process rule definition (branching, commits, dependencies)
- AI collaboration guidelines
- Governance and enforcement mechanisms

**When to Use:** When starting a new project, establishing team standards, onboarding AI assistants, or formalising development governance.

---

## Common Workflow Characteristics

### Operating Modes
All workflows support two distinct modes:

**Collaboration Mode (Default):**
- Stepwise execution with user approval at each stage
- Interactive feedback and iterative refinement
- User control over workflow progression
- Collaborative decision-making throughout

**Silent Mode (User-Triggered):**
- Continuous autonomous execution without interruption
- Complete workflow execution from start to finish
- Assumption-based progression (recorded in 0-notepad.md)
- No user approval requests during execution

### Standard Features

**Core Features:**
- **0-notepad.md:** Every workflow creates a notepad file for capturing insights, ideas, and observations
- **Systematic Approach:** All workflows follow structured, phase-based methodologies
- **User Approval:** Collaboration mode requires explicit user approval before proceeding between phases
- **Professional Standards:** All workflows operate with the highest professional standards and best practices
- **Documentation:** Comprehensive documentation is created throughout each workflow

**Advanced Patterns (from Research):**
- **Context Markers:** `LIA-DEV-1️⃣` markers detect context rot in long sessions
- **Proof Artifacts:** Evidence created BEFORE commits, not just outputs
- **Scope Guards:** Mandatory simplicity checks before implementation
- **Self-Correction Loops:** Verify and retry (max 3 attempts, then escalate)
- **Alternative Reasoning Backups:** Genuine alternatives, not simple retries
- **Error Propagation Strategies:** `halt_on_critical`, `continue_and_log`, `collaborative_review`
- **Troubleshooting Escalation:** After 3 failed attempts, switch to structured debugging
- **Verification Before Status:** Prove it works before claiming "fixed"

---

## Workflow Selection Guide

### 🔧 Problem Solving & Diagnosis ← OUR STRENGTH

| When You Need To... | Use This Spec |
|---------------------|---------------|
| Debug something that's broken | `troubleshoot` |
| Understand mysterious/legacy code | `wtf` |
| Investigate crashes, data loss, security incidents | `investigate` |

*Most AI tools help you create. Lia helps you debug. This is our competitive advantage.*

### 📚 Research & Learning ← EDUCATIONAL DNA

| When You Need To... | Use This Spec |
|---------------------|---------------|
| Learn through hands-on project work | `learn` |
| Research technologies before deciding | `research` |
| Analyse academic papers | `paper` |
| Scout a competitive landscape | `recon` |

### 🛠️ Development & Implementation

| When You Need To... | Use This Spec |
|---------------------|---------------|
| Implement features or fix bugs | `dev` |
| Create specifications from ideas | `spec` |
| Design testing strategies | `test` |
| Build APIs or integrate systems | `integrate` |

### ✅ Code Quality & Architecture

| When You Need To... | Use This Spec |
|---------------------|---------------|
| Define project standards (do first!) | `constitution` |
| Design system architecture | `architecture` |
| Review code quality | `review` |
| Assess security | `security` |
| Improve performance | `optimize` |

### 📝 Knowledge & Strategy

| When You Need To... | Use This Spec |
|---------------------|---------------|
| Create documentation | `docs` |
| Enhance existing features creatively | `innovate` |
| Coordinate complex consulting projects | `nexus` |

---

## Getting Started

Each command follows a similar pattern:

1. **Initial Context:** The workflow begins by understanding the task context
2. **Systematic Phases:** Work proceeds through structured phases with clear objectives
3. **User Collaboration:** Regular checkpoints ensure alignment with user goals
4. **Documentation:** Comprehensive artifacts are created throughout the process
5. **Knowledge Capture:** Insights and observations are recorded in notepad files

To use any command, invoke it through the Lia CLI system with your specific task or question. The workflow agent will guide you through the systematic process appropriate for your needs.

---

*Document generated from command specifications in .lia/commands/*

