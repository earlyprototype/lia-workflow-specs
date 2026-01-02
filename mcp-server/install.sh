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
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python 3 is required but not found"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
    print_success "Found Python: $PYTHON_VERSION"
}

check_pip() {
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        print_error "pip is required but not found"
        exit 1
    fi
    print_success "Found pip"
}

install_package() {
    print_info "Installing MCP server package..."
    cd "$SCRIPT_DIR"
    $PYTHON_CMD -m pip install -e . --quiet
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
    local config_type=$1
    local output_file=$2
    
    case $config_type in
        "claude-desktop")
            cat > "$output_file" << EOF
{
  "mcpServers": {
    "lia-workflow-specs": {
      "command": "$PYTHON_CMD",
      "args": ["-m", "lia_workflow_mcp.server"],
      "env": {
        "LIA_SPECS_DIR": "$SPECS_DIR"
      }
    }
  }
}
EOF
            ;;
        "cursor")
            cat > "$output_file" << EOF
{
  "mcpServers": {
    "lia-workflow-specs": {
      "command": "$PYTHON_CMD",
      "args": ["-m", "lia_workflow_mcp.server"],
      "env": {
        "LIA_SPECS_DIR": "$SPECS_DIR"
      }
    }
  }
}
EOF
            ;;
    esac
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
check_pip

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
generate_config "claude-desktop" "$SCRIPT_DIR/config/generated-config.json"
print_success "Generated config file"

# Show completion
show_next_steps
