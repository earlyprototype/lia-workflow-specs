#!/bin/bash
# Lia Workflow Specs MCP Server - Installation Script
#
# Usage:
#   ./install.sh              # Install with default settings
#   ./install.sh --global     # Install specs to ~/.lia/specs
#   ./install.sh --help       # Show help

set -e

# Colours for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

# Default values
INSTALL_GLOBAL=false
SPECS_DIR=""
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║         Lia Workflow Specs MCP Server Installer              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

show_help() {
    echo "Usage: ./install.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --global        Install specs to ~/.lia/specs"
    echo "  --specs-dir DIR Specify custom specs directory"
    echo "  --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./install.sh                    # Local install"
    echo "  ./install.sh --global           # Global install to ~/.lia/specs"
    echo "  ./install.sh --specs-dir /path  # Custom specs location"
}

check_python() {
    local candidate interpreter
    for candidate in python3 python; do
        interpreter=$("$candidate" -c 'import sys; print(sys.executable if sys.version_info >= (3, 10) else "")' 2>/dev/null) || continue
        # Native Windows Python writes CRLF when its output is captured by Bash.
        interpreter=${interpreter%$'\r'}
        if [[ -n "$interpreter" ]] && "$interpreter" -m pip --version &> /dev/null; then
            PYTHON_CMD="$interpreter"
            print_success "Found Python with pip ($candidate)"
            return
        fi
    done
    print_error "Install Python 3.10 or later with pip and make python3 or python available on PATH"
    exit 1
}

install_package() {
    print_info "Installing MCP server package..."
    cd "$SCRIPT_DIR"
    "$PYTHON_CMD" -m pip install -e . --quiet
    print_success "MCP server package installed"
}

install_specs_global() {
    SPECS_DIR="$HOME/.lia/specs"
    mkdir -p "$SPECS_DIR"
    
    if [ -d "$PROJECT_ROOT/specs" ]; then
        print_info "Copying specs to $SPECS_DIR..."
        cp -r "$PROJECT_ROOT/specs/"* "$SPECS_DIR/"
        print_success "Specs installed to $SPECS_DIR"
    else
        print_warning "No specs directory found in project root"
    fi
}

generate_config() {
    local output_file=$1
    local config_specs_dir="$SPECS_DIR"
    if [ "$INSTALL_GLOBAL" = true ]; then
        # Ask the installing interpreter for the native path of the directory Bash populated.
        config_specs_dir=$(cd -- "$SPECS_DIR" && "$PYTHON_CMD" -c 'import os; print(os.getcwd(), end="")')
    fi
    
    "$PYTHON_CMD" - "$config_specs_dir" > "$output_file" <<'PY'
import json
import sys

server = {
    "command": sys.executable,
    "args": ["-m", "lia_workflow_mcp.server"],
    "env": {"LIA_SPECS_DIR": sys.argv[1]},
}
print(json.dumps({"mcpServers": {"lia-workflow-specs": server}}, indent=2))
PY
}

show_next_steps() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    Installation Complete!                     ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Specs directory: $SPECS_DIR"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo ""
    echo "1. Add to Claude Desktop config:"
    echo "   Location: ~/.config/claude/claude_desktop_config.json (Linux)"
    echo "            ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)"
    echo ""
    cat "$SCRIPT_DIR/config/generated-config.json"
    echo ""
    echo ""
    echo "2. Restart your MCP client (Claude Desktop, Cursor, etc.)"
    echo ""
    echo "3. Test with: \"List all workflow specs\""
    echo ""
    echo -e "${BLUE}Documentation:${NC} $SCRIPT_DIR/README.md"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --global)
            INSTALL_GLOBAL=true
            shift
            ;;
        --specs-dir)
            SPECS_DIR="$2"
            shift 2
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Main installation
print_header

# Check requirements
check_python

# Install package
install_package

# Handle specs directory
if [ "$INSTALL_GLOBAL" = true ]; then
    install_specs_global
elif [ -z "$SPECS_DIR" ]; then
    # Default to project specs if available
    if [ -d "$PROJECT_ROOT/specs" ]; then
        SPECS_DIR="$PROJECT_ROOT/specs"
        print_info "Using project specs: $SPECS_DIR"
    else
        SPECS_DIR="$HOME/.lia/specs"
        print_warning "No specs found, using default: $SPECS_DIR"
    fi
fi

# Generate config
mkdir -p "$SCRIPT_DIR/config"
generate_config "$SCRIPT_DIR/config/generated-config.json"
print_success "Generated config file"

# Show completion
show_next_steps
