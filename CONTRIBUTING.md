# Contributing to Lia Workflow Specs

Thank you for your interest in contributing! This document provides guidelines and information for contributing to the Lia Workflow Specs project.

---

## 🎯 Ways to Contribute

### 1. **New Workflow Specs**
Design and submit new systematic workflows for different domains or use cases.

### 2. **Improve Existing Specs**
Enhance phases, constraints, templates, or documentation in current specs.

### 3. **Examples & Case Studies**
Share real-world usage examples, before/after scenarios, and outcomes.

### 4. **Documentation**
Improve guides, add tutorials, clarify concepts, or fix typos.

### 5. **Tools & Utilities**
Build validators, visualizers, generators, or integrations.

### 6. **Bug Reports**
Report issues with specs, documentation, or tooling.

### 7. **Community Support**
Help others in discussions, answer questions, share experiences.

---

## 📋 Before You Start

### Read These First
- [README.md](README.md) - Project overview and philosophy
- [Workflow Guide](docs/workflow-guide.md) - How workflows operate
- [Best Practices](docs/best-practices.md) - Design patterns and conventions

### Check Existing Work
- Browse [open issues](../../issues) to avoid duplicates
- Review [pull requests](../../pulls) for ongoing work
- Join [discussions](../../discussions) for proposals

---

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/lia-workflow-specs.git
cd lia-workflow-specs
git remote add upstream https://github.com/ORIGINAL_OWNER/lia-workflow-specs.git
```

### 2. Create a Branch
```bash
# Use descriptive branch names:
git checkout -b feature/new-data-analysis-spec
git checkout -b fix/spec-toml-syntax-error
git checkout -b docs/improve-getting-started-guide
```

### 3. Make Your Changes
Follow the guidelines below for your specific contribution type.

### 4. Test Your Changes
```bash
# Validate TOML syntax
python tools/spec-validator.py specs/your-category/your-spec.toml

# Generate workflow diagram
python tools/workflow-visualizer.py specs/your-category/your-spec.toml

# Run any other relevant tests
```

### 5. Commit and Push
```bash
# Write clear, descriptive commit messages
git add .
git commit -m "Add data analysis workflow spec

- Designed 7-phase workflow for systematic data analysis
- Includes exploratory, statistical, and visualization phases
- Supports both batch and streaming data contexts"

git push origin feature/new-data-analysis-spec
```

### 6. Create Pull Request
- Use the pull request template
- Link to related issues
- Describe your changes clearly
- Wait for review and feedback

---

## ✍️ Spec Design Guidelines

### Spec Structure Requirements

Every spec MUST include:

```toml
description = "Brief description of the workflow"

prompt = """
# System Prompt - [Workflow Name] Agent

## Workflow Mode System
[Standard dual-mode section - Collaboration and Silent]

## Goal
[Clear statement of what this workflow accomplishes]

## [Workflow Name] to Execute

<workflow-definition>
# Systematic [Workflow Name]

## Overview
[Comprehensive workflow description]

### Phase 1: [Phase Name]
**Constraints:**
- The model MUST create '.lia/[workflow_type]/{task_name}/0-notepad.md'
- The model MUST create '.lia/[workflow_type]/{task_name}/1-[phase-name].md'
- The model MUST [specific requirements]
- The model MUST ask user to review and approve before proceeding
- [Additional constraints]

[Repeat for all phases]

## Workflow Diagram
[Mermaid diagram showing phase flow]

# [Workflow Name] Instructions
[Execution guidelines]

# IMPORTANT EXECUTION INSTRUCTIONS
[Critical constraints and approval requirements]

## Agent Self-Development
[Continuous improvement guidance]

## 0-Notepad Template
[Standard notepad markdown template]

</workflow-definition>
"""
```

### Phase Design Principles

**1. Clear Objectives**
Each phase must have a single, clear purpose:
- ✅ "Evidence Analysis and Claims Evaluation"
- ❌ "Do some analysis and stuff"

**2. Explicit Constraints**
Use precise requirement language:
- **MUST** - Mandatory requirement
- **SHOULD** - Recommended best practice
- **MAY** - Optional enhancement

**3. Approval Gates**
Every phase must:
- Create a markdown document
- Ask for user review
- Require explicit approval
- Support iteration on feedback

**4. Persistent Artifacts**
All analysis and decisions must be captured in markdown files:
```
.lia/[workflow_type]/{task_name}/
├── 0-notepad.md          # Always present
├── 1-[phase1-name].md
├── 2-[phase2-name].md
└── ...
```

**5. Agent Mindset**
Define the philosophical approach:
```toml
## Agent Mindset and Capabilities
**[Quality] Excellence:**
- Approach [task] with [perspective]
- Consider [aspects] across [scope]
[etc.]
```

### Common Patterns to Follow

**Notepad Structure:**
```markdown
## 🧠 Key Insights & Discoveries
## 🔧 Technical Notes & Implementation Details
## 💡 Ideas & Future Enhancements
## 🔗 Cross-[Domain] Connections
## 📝 User Notes
## 🤖 LLM Observations
```

**Approval Pattern:**
```toml
- The model MUST ask the user to review and approve [phase output] before proceeding
- The model MUST iterate on [phase output] based on user feedback until explicitly approved
```

**Silent Mode Pattern:**
```toml
- **Silent Mode**: The model MUST proceed with [action] and record any assumptions in the 0-notepad.md file
```

### Anti-Patterns to Avoid

❌ **Don't:**
- Skip approval gates
- Combine multiple phases into one
- Make assumptions without recording them (in Silent Mode)
- Create phases without clear deliverables
- Use vague or ambiguous language
- Forget the workflow diagram
- Omit the 0-notepad template

✅ **Do:**
- Create discrete, focused phases
- Require explicit user approval
- Document all assumptions
- Use precise constraint language
- Include visual workflow representation
- Provide comprehensive notepad template

---

## 📝 Documentation Guidelines

### Markdown Standards
- Use ATX-style headers (`#` not `====`)
- Include code blocks with language tags
- Add alt text to images
- Keep line length reasonable (80-100 chars)
- Use relative links for internal references

### Example Standards
- Include complete, runnable examples
- Show before and after states
- Explain the context and goals
- Demonstrate common variations
- Include expected outputs

### Tutorial Standards
- Start with prerequisites
- Use step-by-step structure
- Include explanations, not just commands
- Show expected results at each step
- End with next steps or further reading

---

## 🔧 Code Guidelines

### Python (for tools)
```python
# Follow PEP 8
# Use type hints
# Include docstrings
# Add unit tests

def validate_spec(spec_path: str) -> bool:
    """
    Validate a workflow spec file.
    
    Args:
        spec_path: Path to the TOML spec file
        
    Returns:
        True if valid, False otherwise
        
    Raises:
        FileNotFoundError: If spec file doesn't exist
        TOMLDecodeError: If spec has invalid TOML syntax
    """
    pass
```

### TOML (for specs)
```toml
# Use clear key names
# Add comments for complex sections
# Maintain consistent formatting
# Validate syntax before committing

[phase]
name = "Evidence Analysis"  # Clear, descriptive name
required_fields = [
    "claims_evaluation",
    "evidence_quality",
    "alternative_interpretations"
]
```

---

## 🧪 Testing

### Spec Validation
All specs must pass validation:
```bash
python tools/spec-validator.py specs/your-category/your-spec.toml
```

Checks:
- ✅ Valid TOML syntax
- ✅ Required sections present
- ✅ Workflow diagram exists
- ✅ Phase constraints properly formatted
- ✅ Notepad template included

### Example Testing
Examples should be:
- ✅ Reproducible
- ✅ Well-documented
- ✅ Representative of real usage
- ✅ Include expected outputs

### Documentation Testing
Documentation should be:
- ✅ Accurate and up-to-date
- ✅ Free of broken links
- ✅ Clear and understandable
- ✅ Properly formatted

---

## 📬 Pull Request Process

### 1. Use the Template
Our PR template will guide you through:
- Description of changes
- Related issues
- Type of change
- Testing performed
- Documentation updates

### 2. PR Title Format
```
[type]: brief description

Examples:
feat: add data analysis workflow spec
fix: correct approval gate in innovate.toml
docs: improve getting started guide
refactor: reorganize spec directory structure
test: add spec validator unit tests
```

Types:
- `feat` - New feature or spec
- `fix` - Bug fix
- `docs` - Documentation only
- `refactor` - Code restructuring
- `test` - Test additions or fixes
- `chore` - Maintenance tasks

### 3. Review Process
- Maintainer will review within 72 hours
- Address feedback and requested changes
- Get approval from at least one maintainer
- Squash or rebase as requested
- Maintainer will merge when ready

### 4. After Merge
- Delete your branch
- Pull latest from upstream
- Update CHANGELOG if significant

---

## 🎨 Style Guide

### Voice and Tone
- **Professional but approachable** - Avoid overly casual or overly formal
- **Clear and direct** - Get to the point quickly
- **Inclusive** - Use "we" and "you", avoid "he/she"
- **Action-oriented** - Focus on what to do, not just what is

### Terminology
Use consistent terms:
- **Workflow** not "process" or "procedure"
- **Phase** not "step" or "stage"  
- **Spec** not "template" or "prompt"
- **Agent** not "AI" or "assistant" (when referring to workflow execution)
- **Constraint** not "rule" or "requirement" (in spec context)
- **Approval gate** not "checkpoint" or "review point"

### Formatting
- **Bold** for emphasis and UI elements
- *Italics* for technical terms on first use
- `Code` for file names, commands, variables
- > Quotes for callouts and important notes

---

## 🐛 Bug Reports

### Before Reporting
1. Check [existing issues](../../issues)
2. Ensure you're using the latest version
3. Verify it's a bug, not expected behavior
4. Try to reproduce consistently

### Report Template
```markdown
## Bug Description
Clear and concise description of the bug.

## To Reproduce
Steps to reproduce the behavior:
1. Load spec '...'
2. Execute phase '...'
3. Observe error '...'

## Expected Behavior
What should have happened.

## Actual Behavior
What actually happened.

## Context
- Spec: [spec name and version]
- AI System: [Claude, GPT-4, etc.]
- OS: [Windows, Mac, Linux]
- Additional context: [any other relevant information]

## Logs/Screenshots
If applicable, add logs or screenshots.
```

---

## 💡 Feature Requests

### Before Requesting
1. Check [existing requests](../../issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)
2. Consider if it aligns with project goals
3. Think about implementation complexity
4. Draft a clear proposal

### Request Template
```markdown
## Feature Description
Clear description of the proposed feature.

## Motivation
Why is this feature valuable? What problem does it solve?

## Proposed Solution
How would this feature work? What would the workflow look like?

## Alternatives Considered
What other approaches did you consider?

## Additional Context
Examples, mockups, related projects, etc.
```

---

## 🤝 Code of Conduct

### Our Pledge
We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, religion, or nationality.

### Our Standards
**Positive behaviors:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behaviors:**
- Trolling, insulting/derogatory comments, personal or political attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement
Violations of the Code of Conduct may result in:
1. Warning
2. Temporary ban
3. Permanent ban

Report violations to [conduct@lia-workflows.org](mailto:conduct@lia-workflows.org).

---

## 📚 Resources

### Learning
- [Workflow Design Patterns](docs/workflow-patterns.md)
- [Best Practices](docs/best-practices.md)
- [Example Gallery](examples/)

### Tools
- [Spec Validator](tools/spec-validator.py)
- [Workflow Visualizer](tools/workflow-visualizer.py)
- [Spec Generator](tools/spec-generator.py)

### Community
- [Discussions](../../discussions)
- [Discord](https://discord.gg/lia-workflows)
- [Blog](https://blog.lia-workflows.org)

---

## 🙏 Recognition

Contributors are recognized in:
- README.md Contributors section
- CHANGELOG.md for significant contributions
- Annual contributor spotlight blog posts

Thank you for making Lia Workflow Specs better! 🎉

---

**Questions?** Open a [discussion](../../discussions) or reach out on [Discord](https://discord.gg/lia-workflows).

