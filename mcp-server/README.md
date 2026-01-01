# Workflow Specs MCP Server

MCP (Model Context Protocol) server that provides remote agent access to **Lia Workflow Specifications** for systematic AI-powered development workflows.

## Overview

This MCP server enables AI agents and tools to connect remotely to the Lia Workflow Specs repository, providing:

- **Resources**: Browse and read workflow specifications
- **Tools**: Search, validate, and get metadata about specs
- **Prompts**: Execute workflows with pre-built prompt templates

## Features

### Resources

| Resource URI | Description |
|-------------|-------------|
| `specs://catalogue` | Complete catalogue of all specs organised by category |
| `specs://category/{name}` | All specs in a specific category |
| `specs://spec/{category}/{name}` | Individual spec content |

### Tools

| Tool | Description |
|------|-------------|
| `list_specs` | List all available specs with optional category filter |
| `get_spec` | Get full content of a specific spec |
| `get_spec_prompt` | Get only the prompt instructions from a spec |
| `validate_spec` | Validate a spec for correctness and completeness |
| `search_specs` | Search specs by keyword |
| `get_spec_metadata` | Get structured metadata (phases, constraints, etc.) |
| `get_categories` | List all available categories |
| `compare_specs` | Compare two specs side-by-side |
| `suggest_workflow` | Get workflow suggestions based on task description |

### Prompts

Execute any workflow spec with:
- `execute_dev` - Development workflow
- `execute_spec` - Specification workflow  
- `execute_review` - Code review workflow
- `execute_test` - Testing workflow
- ... and more for all 16 specs

## Installation

### From Source

```bash
cd mcp-server
pip install -e .
```

### Using pip (when published)

```bash
pip install workflow-specs-mcp
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WORKFLOW_SPECS_DIR` | Path to the specs directory | `../specs` |

### Claude Desktop Configuration

Add to your Claude Desktop config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "workflow-specs": {
      "command": "workflow-specs-mcp",
      "env": {
        "WORKFLOW_SPECS_DIR": "/path/to/lia-workflow-specs/specs"
      }
    }
  }
}
```

### Using with uvx

```json
{
  "mcpServers": {
    "workflow-specs": {
      "command": "uvx",
      "args": ["workflow-specs-mcp"],
      "env": {
        "WORKFLOW_SPECS_DIR": "/path/to/specs"
      }
    }
  }
}
```

## Usage Examples

### Listing Available Specs

```python
# Using the list_specs tool
result = await client.call_tool("list_specs", {})
# Returns all specs organised by category

# Filter by category
result = await client.call_tool("list_specs", {"category": "development"})
```

### Getting a Spec

```python
# Get full spec content
result = await client.call_tool("get_spec", {"name": "dev", "category": "development"})

# Get just the prompt
result = await client.call_tool("get_spec_prompt", {"name": "spec"})
```

### Searching Specs

```python
# Search by keyword
result = await client.call_tool("search_specs", {"query": "testing"})

# Search within a category
result = await client.call_tool("search_specs", {
    "query": "security",
    "category": "quality"
})
```

### Validating Specs

```python
result = await client.call_tool("validate_spec", {"name": "dev"})
# Returns: {is_valid, errors, warnings, info}
```

### Getting Workflow Suggestions

```python
result = await client.call_tool("suggest_workflow", {
    "task_description": "I need to review the code quality of my API"
})
# Returns: suggestions for review.toml, security.toml, etc.
```

### Executing a Workflow

```python
# Get a workflow execution prompt
prompt = await client.get_prompt("execute_spec", {
    "task": "Design a user authentication system",
    "mode": "collaboration"
})
```

## Available Categories

| Category | Specs | Purpose |
|----------|-------|---------|
| `development` | dev, spec, test | Implementation and testing |
| `quality` | review, architecture, security, optimize | Code quality and architecture |
| `problem-solving` | troubleshoot, investigate, wtf | Debugging and forensics |
| `research` | research, learn, paper | Learning and research |
| `knowledge` | docs | Documentation |
| `strategy` | innovate, integrate, nexus | Innovation and strategy |

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Formatting

```bash
ruff check .
ruff format .
```

### Building

```bash
pip install build
python -m build
```

## API Reference

### SpecMetadata

```python
@dataclass
class SpecMetadata:
    name: str              # Spec name (e.g., "dev")
    path: str              # Relative path to spec file
    category: str          # Category (e.g., "development")
    description: str       # Spec description
    phases: list[str]      # List of workflow phases
    constraints: dict      # Count of MUST/SHOULD/MAY constraints
    has_mermaid_diagram: bool
    has_notepad_template: bool
    modes: list[str]       # ["collaboration", "silent"]
    output_directory: str  # e.g., ".lia/dev/"
```

### ValidationResult

```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]      # Critical issues
    warnings: list[str]    # Recommended improvements
    info: list[str]        # Informational messages
```

## Architecture

```
mcp-server/
├── pyproject.toml           # Package configuration
├── README.md                # This file
└── src/
    └── workflow_specs_mcp/
        ├── __init__.py      # Package init
        ├── server.py        # MCP server implementation
        └── spec_loader.py   # Spec loading utilities
```

## License

MIT License - see the main repository LICENSE file.

## Related

- [Lia Workflow Specs](../) - Main workflow specs repository
- [MCP Protocol](https://modelcontextprotocol.io/) - Model Context Protocol documentation
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Python SDK for MCP
