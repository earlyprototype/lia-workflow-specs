# MCP Server Examples

This directory contains example scripts demonstrating how to use the Lia Workflow Specs MCP Server.

## Prerequisites

```bash
# Install the MCP server
cd mcp-server
pip install -e .

# Set specs directory (optional, auto-detected if not set)
export LIA_SPECS_DIR=/path/to/specs
```

## Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates all MCP server features:
- Resource listing and reading
- Tool usage (search, recommend, validate)
- Prompt templates

```bash
python examples/basic_usage.py
```

### 2. Interactive Workflow Starter (`workflow_starter.py`)

Interactive CLI for choosing and starting workflows:
- Task-based recommendations
- Category browsing
- Workflow sequence planning

```bash
python examples/workflow_starter.py
```

## Using with MCP Clients

These examples show programmatic usage. For real-world use, configure the MCP server with your AI client:

### Claude Desktop

```json
{
  "mcpServers": {
    "lia-workflow-specs": {
      "command": "python3",
      "args": ["-m", "lia_workflow_mcp.server"],
      "env": {"LIA_SPECS_DIR": "/path/to/specs"}
    }
  }
}
```

### Example Prompts to Try

Once configured, try these with your AI assistant:

1. **Find a workflow:**
   > "Search for workflows related to security"

2. **Get recommendations:**
   > "What workflow should I use to implement a new API endpoint?"

3. **Start a workflow:**
   > "Start the dev workflow for implementing user profile editing"

4. **Plan a sequence:**
   > "Plan a workflow sequence for building a complete authentication system with security review"

5. **Compare workflows:**
   > "Compare the troubleshoot and investigate workflows"

## Output Examples

### Resource: specs://summary

```markdown
# Lia Workflow Specs Quick Reference

## Overview
Total workflows available: 17

## Development
- **dev**: Development implementation workflow
- **spec**: Requirements → Design → Tasks
- **test**: Testing strategy and automation
...
```

### Tool: recommend_workflow

```
Recommended workflows for: 'implement new feature'

1. **spec** (development)
   Creates requirements, design, and task list
   Phases: 3

2. **dev** (development)
   Implements features with testing
   Phases: 6
```

### Prompt: start-dev

```markdown
# Starting dev Workflow

## Task
Implement user profile editing feature

## Mode
Collaboration Mode

## Instructions
You are now operating as a dev workflow agent...
```
