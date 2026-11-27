# Lia Workflow Specs - Tools

Supporting tools for workflow specification development and validation.

## Tools Available

### spec-validator.py

Validates workflow specification files for compliance with Lia standards.

**Features:**
- ✅ TOML syntax validation
- ✅ Required sections checking
- ✅ Workflow diagram verification
- ✅ Constraint formatting validation
- ✅ Notepad template structure validation
- ✅ Colorized output
- ✅ Verbose and quiet modes

**Usage:**

```bash
# Install the schema validator and TOML reader
python -m pip install -r tools/requirements.txt

# Install the diagram parser once with Node.js 24
npm ci --prefix tools --ignore-scripts

# Validate single file
python tools/spec-validator.py specs/development/spec.toml

# Validate all specs
python tools/spec-validator.py specs/

# Check an installed copy against the same 19 category and filename pairs
python tools/spec-validator.py ~/.lia/specs --catalog

# Verbose output (show all checks)
python tools/spec-validator.py specs/ -v

# Quiet mode (errors only)
python tools/spec-validator.py specs/ -q
```

The repository-wide check also reports missing and unexpected workflow files.
Directory discovery skips `_common`. The validator reads both top-level
`description` and `prompt` strings and the `metadata.description` and
`prompt.content` table fields used by `constitution` and `recon`.
Each workflow must match the [workflow schema](../schemas/workflow-spec.schema.json).
Number phases consecutively from 1. Each phase needs instructions outside
fenced examples and HTML comments. Contributor workflows use third-level
phase headings. The `constitution` and `recon` workflows use second-level
phase headings.
In the feature-spec workflow, the final phase (phase 3) must instruct the model
to write `3-tasks.md`. In every workflow, place execution instructions between
the Important Execution Instructions heading and the next heading.
The validator parses Mermaid blocks in the Workflow Diagram section and checks
for workflow elements. It also accepts nonempty plain-text diagram blocks.
It checks the six standard notepad headings with or without the icons shown in
the base template. It also checks the custom templates used by `constitution`,
`recon`, `paper` and `nexus`.

**Example Output:**

```
Validating: spec.toml
============================================================

❌ ERRORS:
  • Missing required section: 'Workflow Diagram'

⚠️  WARNINGS:
  • Missing recommended section: 'Agent Self-Development'

SUMMARY:
  ✗ INVALID
  Errors: 1
  Warnings: 1
```

---

## MCP Server

### workflow-specs-mcp (NEW!)

Model Context Protocol (MCP) server enabling remote AI agent access to workflow specs.

**Location:** [`../mcp-server/`](../mcp-server/)

**Features:**
- 📚 **Resources**: Browse and read specs via `specs://` URIs
- 🔧 **Tools**: Search, validate, compare, and get metadata
- 💬 **Prompts**: Execute workflows with pre-built templates
- 🔍 **Suggestions**: AI-powered workflow recommendations

**Installation:**

```bash
cd mcp-server
pip install -e .
```

**Claude Desktop Configuration:**

```json
{
  "mcpServers": {
    "workflow-specs": {
      "command": "workflow-specs-mcp",
      "env": {
        "WORKFLOW_SPECS_DIR": "/path/to/specs"
      }
    }
  }
}
```

**Available Tools:**
- `list_specs` - List all specs by category
- `get_spec` - Get full spec content
- `get_spec_prompt` - Get workflow instructions only
- `validate_spec` - Check the structure of a loaded prompt
- `search_specs` - Keyword search
- `get_spec_metadata` - Extract structured metadata
- `compare_specs` - Compare two specs
- `suggest_workflow` - Task-based recommendations

See [`../mcp-server/README.md`](../mcp-server/README.md) for full documentation.

---

## Planned Tools

### workflow-visualizer.py (Coming Soon)

Generate workflow diagrams from specs:
- Extract Mermaid diagrams
- Export to PNG/SVG
- Create overview graphics

**Planned Usage:**
```bash
python tools/workflow-visualizer.py specs/development/spec.toml --output diagram.png
```

### spec-generator.py (Coming Soon)

Interactive wizard for creating new specs:
- Template selection
- Phase definition
- Constraint specification
- Auto-generate TOML structure

**Planned Usage:**
```bash
python tools/spec-generator.py --interactive
```

### spec-analyzer.py (Coming Soon)

Analyze spec usage and patterns:
- Count phases across specs
- List all constraints
- Extract common patterns
- Generate statistics

**Planned Usage:**
```bash
python tools/spec-analyzer.py specs/ --report stats.md
```

---

## Development

### Requirements

```bash
pip install -r tools/requirements.txt
npm ci --prefix tools --ignore-scripts
```

### Testing

```bash
# Test validator on all specs
python tools/spec-validator.py specs/ -v

# Should pass with 0 errors
```

### Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines on:
- Adding new tools
- Testing requirements
- Code style
- Documentation standards

---

## CI/CD Integration

These tools are used in GitHub Actions:

```yaml
# .github/workflows/validate-specs.yml
- name: Install schema validator
  run: python -m pip install -r tools/requirements.txt
- name: Install diagram parser
  run: npm ci --prefix tools --ignore-scripts
- name: Validate the shipped workflow catalog
  run: python tools/spec-validator.py specs/
```

---

## License

MIT License - see [LICENSE](../LICENSE) for details.

