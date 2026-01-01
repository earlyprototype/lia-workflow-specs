# Lia Workflow Specs MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that provides remote agent access to Lia Workflow Specifications. This enables AI agents to discover, read, and utilise systematic development workflows.

## Features

### Resources

The server exposes workflow specs as MCP resources:

| Resource URI | Description |
|--------------|-------------|
| `specs://index` | Complete index of all workflow specs |
| `specs://categories` | List of categories and their specs |
| `specs://summary` | Quick reference guide for all workflows |
| `specs://{category}/{name}` | Full prompt for a specific spec |
| `specs://{category}/{name}/metadata` | Metadata and structure for a spec |

### Tools

The server provides tools for working with specs:

| Tool | Description |
|------|-------------|
| `search_specs` | Search specs by keyword |
| `recommend_workflow` | Get workflow recommendations based on task description |
| `get_spec_details` | Get detailed information about a spec |
| `list_specs_by_category` | List all specs in a category |
| `get_workflow_phases` | Get phases for a workflow |
| `validate_spec` | Validate a spec file |
| `get_spec_prompt` | Get the full prompt text for a spec |
| `compare_specs` | Compare two specs |

## Installation

### Using pip

```bash
pip install lia-workflow-specs-mcp
```

### From source

```bash
cd mcp-server
pip install -e .
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LIA_SPECS_DIR` | Path to specs directory | Auto-detected |

### Claude Desktop Configuration

Add to your Claude Desktop config (`~/.config/claude/claude_desktop_config.json` on Linux, `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "lia-workflow-specs": {
      "command": "lia-mcp-server",
      "env": {
        "LIA_SPECS_DIR": "/path/to/your/specs"
      }
    }
  }
}
```

### Using with Python

```json
{
  "mcpServers": {
    "lia-workflow-specs": {
      "command": "python",
      "args": ["-m", "lia_workflow_mcp.server"],
      "env": {
        "LIA_SPECS_DIR": "/path/to/your/specs"
      }
    }
  }
}
```

### Using with Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "lia-workflow-specs": {
      "command": "lia-mcp-server",
      "env": {
        "LIA_SPECS_DIR": "/path/to/your/specs"
      }
    }
  }
}
```

## Usage Examples

### Discovering Workflows

An agent can ask: "What workflow should I use to implement a new feature?"

The `recommend_workflow` tool will suggest:
1. `spec` - For requirements and design
2. `dev` - For implementation

### Reading a Workflow

An agent can read the full workflow spec:

```
Resource: specs://development/spec
```

This returns the complete prompt that defines the workflow phases, constraints, and execution instructions.

### Searching Specs

```python
# Tool call: search_specs
{"query": "security"}

# Returns specs matching "security":
# - security.toml (Security Assessment & Hardening)
# - review.toml (includes security review phase)
```

### Validating Specs

```python
# Tool call: validate_spec
{"spec_name": "dev"}

# Returns validation results:
# ✓ Found required sections
# ✓ Contains Mermaid diagram
# ✓ Has 6 defined phases
# Status: ✅ VALID
```

## Spec Categories

| Category | Description | Specs |
|----------|-------------|-------|
| **development** | Implementation and testing | dev, spec, test |
| **quality** | Code quality and security | review, security, architecture, optimize |
| **problem-solving** | Debugging and investigation | troubleshoot, investigate, wtf |
| **research** | Learning and analysis | research, learn, paper |
| **knowledge** | Documentation | docs |
| **strategy** | Innovation and integration | innovate, integrate, nexus |

## Prompts

The server provides ready-to-use prompt templates for starting workflows:

### Workflow Starters

Each workflow has a `start-{name}` prompt:

```python
# Example: Start a dev workflow
prompt = get_prompt("start-dev", {
    "task": "Implement user authentication",
    "mode": "collaboration"  # or "silent"
})
```

### Helper Prompts

| Prompt | Description | Arguments |
|--------|-------------|-----------|
| `choose-workflow` | Help choose the right workflow | `task` |
| `workflow-sequence` | Plan a sequence for complex projects | `project` |
| `resume-workflow` | Resume an interrupted workflow | `workflow`, `task_name` |

### Using Prompts with Claude

Once configured, you can use prompts directly:

> "Use the start-spec prompt for: Create a REST API for user management"

The MCP client will automatically fill in the prompt template and start the workflow.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client (AI Agent)                     │
│                  (Claude, Cursor, etc.)                      │
└─────────────────────────┬───────────────────────────────────┘
                          │ MCP Protocol (stdio)
┌─────────────────────────▼───────────────────────────────────┐
│                    MCP Server                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Resource Handlers                       │    │
│  │  • specs://index       → Index all specs            │    │
│  │  • specs://categories  → List categories            │    │
│  │  • specs://{cat}/{name}→ Read spec prompt           │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                Tool Handlers                         │    │
│  │  • search_specs       → Keyword search              │    │
│  │  • recommend_workflow → Task-based recommendation   │    │
│  │  • validate_spec      → Spec validation             │    │
│  │  • compare_specs      → Spec comparison             │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Spec Collection                         │    │
│  │  • Loads .toml files from specs directory           │    │
│  │  • Parses phases and constraints                    │    │
│  │  • Provides search and filtering                    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Specs Directory                            │
│  specs/                                                      │
│  ├── development/  (dev.toml, spec.toml, test.toml)         │
│  ├── quality/      (review.toml, security.toml, ...)        │
│  ├── problem-solving/ (troubleshoot.toml, investigate.toml) │
│  ├── research/     (research.toml, learn.toml, paper.toml)  │
│  ├── knowledge/    (docs.toml)                              │
│  └── strategy/     (innovate.toml, integrate.toml, nexus)   │
└─────────────────────────────────────────────────────────────┘
```

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Running the Server Directly

```bash
# Set specs directory
export LIA_SPECS_DIR=/path/to/specs

# Run server
python -m lia_workflow_mcp.server
```

### Adding New Tools

Extend `server.py` to add new tools:

```python
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools
        Tool(
            name="my_new_tool",
            description="Description of what it does",
            inputSchema={...},
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    if name == "my_new_tool":
        # Implementation
        pass
```

## Troubleshooting

### Server Not Finding Specs

Ensure `LIA_SPECS_DIR` points to the correct directory containing `.toml` spec files.

### Connection Issues

1. Check the server is running: `lia-mcp-server`
2. Verify the MCP client configuration
3. Check stderr for server logs

### Invalid Spec Errors

Use the `validate_spec` tool to check spec formatting:

```python
{"name": "validate_spec", "arguments": {"spec_name": "your-spec"}}
```

## Licence

MIT Licence - see [LICENSE](../LICENSE) for details.

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.
