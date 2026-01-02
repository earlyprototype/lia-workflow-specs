# MCP Server Configuration Files

This directory contains ready-to-use configuration files for various MCP clients.

## Claude Desktop

Copy `claude-desktop.json` contents to your Claude Desktop config:

**Linux/macOS:**
```bash
# Location: ~/.config/claude/claude_desktop_config.json
cat config/claude-desktop.json
```

**Windows:**
```
Location: %APPDATA%\Claude\claude_desktop_config.json
```

## Cursor

Add the contents of `cursor.json` to your Cursor MCP settings.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LIA_SPECS_DIR` | Path to workflow specs directory | Auto-detected |

### Recommended Paths

- **Global install**: `~/.lia/specs`
- **Project-local**: `./specs` or `${workspaceFolder}/specs`
- **Custom location**: Set `LIA_SPECS_DIR` to your specs directory

## Installation Steps

### 1. Install the MCP Server

```bash
# From the mcp-server directory
pip install -e .

# Or install from package
pip install lia-workflow-specs-mcp
```

### 2. Copy Specs to Your Location

```bash
# Global location
mkdir -p ~/.lia/specs
cp -r /path/to/lia-workflow-specs/specs/* ~/.lia/specs/

# Or use project-local
# specs/ directory in your project root
```

### 3. Configure Your MCP Client

Add the appropriate configuration to your client's config file.

### 4. Restart Your Client

Restart Claude Desktop or Cursor to load the MCP server.

## Verification

After setup, you should see `lia-workflow-specs` in your available MCP servers.

Test with:
- "List all workflow specs" → Should show 17 specs
- "Recommend a workflow for implementing a feature" → Should suggest dev/spec
