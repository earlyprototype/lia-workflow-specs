# Workflow Composition Guide

## Core Principle: Every Spec is Independent

**Each workflow spec is designed to run completely independently.** There are no hard dependencies between specs. You can start any workflow at any time with any task.

The "composition" features described below are purely **optional suggestions** - they exist to help users discover useful workflow sequences, not to enforce dependencies.

---

## What Composition Actually Means

### What It Does NOT Mean

- Specs do NOT have mandatory prerequisites
- You are NOT required to run specs in any order
- No spec "needs" another spec to function
- There are no blocking dependencies

### What It DOES Mean

- **Suggestions**: "After finishing X, you might find Y useful"
- **Common patterns**: "Users often do X → Y → Z for this type of task"
- **Context hints**: "This workflow works well when you have X available"

---

## Understanding the Terminology

The `workflow-triggers.toml` file uses terms that can be misleading. Here's what they actually mean:

| Term | Misleading Interpretation | Actual Meaning |
|------|---------------------------|----------------|
| `requires` | "Cannot run without this" | "Works best when you have this context" |
| `on_complete` | "Must run next" | "You might want to consider these next" |
| `can_chain_from` | "Can only follow these" | "Often follows naturally from these" |
| `provides` | "Required output" | "Typically produces these artefacts" |

### Example: The `dev` Spec

```toml
[triggers.dev]
on_complete = ["test", "review"]      # Suggestions for what to do after development
can_chain_from = ["spec", "troubleshoot"]  # Often follows spec creation or troubleshooting
provides = ["implementation", "code"]  # What you'll typically have afterwards
requires = ["design", "tasks"]         # Works best with these, but NOT mandatory
```

**Reality**: You can run `/dev` with just a verbal description of what you want to build. No prior `spec` workflow is required. The "requires" is just noting that having design docs helps - it's guidance, not enforcement.

---

## How to Use Specs

### Standalone Usage (Most Common)

Simply invoke any spec with your task:

```
/dev implement user authentication
/review check the auth module for security issues  
/test create tests for the login flow
```

Each command is complete on its own. No setup required.

### Sequential Usage (When It Makes Sense)

Sometimes you naturally want to chain workflows:

```
/spec design a caching system
  ↓ (produces design documents)
/dev implement the caching system from the spec
  ↓ (produces implementation)
/test write tests for the cache implementation
```

This sequence makes sense, but each step is still independent. You could:
- Skip `/spec` and just `/dev` directly
- Run `/test` without having run `/dev` (e.g., testing existing code)
- Jump to `/review` at any point

---

## Predefined Chains (Optional Templates)

The `workflow-triggers.toml` defines some common sequences as templates:

```toml
[chains.development]
description = "Feature development chain: research → spec → dev → test"
sequence = ["research", "spec", "dev", "test"]
```

These are **not pipelines** - they're just documented patterns. Think of them as recipes, not rules.

### When Chains Are Useful

- **New to the workflow system**: Chains suggest a logical order
- **Large features**: Systematic approach helps track progress
- **Team coordination**: Shared understanding of workflow stages

### When to Ignore Chains

- **Quick fixes**: Just `/dev` or `/troubleshoot` directly
- **Exploration**: `/research` or `/wtf` standalone
- **Code review**: `/review` on existing code - no prior workflow needed

---

## The MCP Server Tools

The MCP server provides tools that reference these compositions:

| Tool | What It Does |
|------|--------------|
| `get_workflow_chain` | Shows a suggested sequence (purely informational) |
| `list_workflow_chains` | Lists available chain templates |
| `recommend_workflow` | Suggests starting points based on task description |

**Important**: These tools provide suggestions only. They never enforce or require anything.

---

## Design Philosophy

### Why No Hard Dependencies?

1. **Flexibility**: Real work rarely follows rigid sequences
2. **Accessibility**: Any spec should be immediately usable
3. **Context-agnostic**: Specs work with any input you provide
4. **User autonomy**: You decide the workflow, not the system

### Why Have Composition at All?

1. **Discovery**: Helps users find related workflows
2. **Guidance**: Suggests logical next steps
3. **Documentation**: Captures common patterns
4. **Tooling**: Enables smart recommendations

---

## Summary

| Aspect | Reality |
|--------|---------|
| **Spec independence** | All specs work standalone |
| **Running order** | Any order you choose |
| **Prerequisites** | None required |
| **Chains** | Optional templates |
| **Triggers** | Suggestions only |

**Bottom line**: Pick any spec, run it with your task. That's it. Everything else is optional guidance.
