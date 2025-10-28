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
# Install dependencies
pip install tomli

# Validate single file
python tools/spec-validator.py specs/development/spec.toml

# Validate all specs
python tools/spec-validator.py specs/

# Verbose output (show all checks)
python tools/spec-validator.py specs/ -v

# Quiet mode (errors only)
python tools/spec-validator.py specs/ -q
```

**Example Output:**

```
Validating: spec.toml
============================================================

❌ ERRORS:
  • Missing required section: 'Workflow Diagram'

⚠️  WARNINGS:
  • Missing recommended section: 'Agent Self-Development'
  • Only found 4/6 notepad sections

SUMMARY:
  ✗ INVALID
  Errors: 1
  Warnings: 2
```

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
- name: Validate TOML files
  run: python tools/spec-validator.py specs/
```

---

## License

MIT License - see [LICENSE](../LICENSE) for details.

