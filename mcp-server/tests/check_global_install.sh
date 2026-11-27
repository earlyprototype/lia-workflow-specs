#!/usr/bin/env bash
# Set PIP_FIND_LINKS to a wheelhouse containing the installer dependencies.
set -eu

server_dir=$(cd "$(dirname "$0")/.." && pwd)
fixture=$(mktemp -d)
fixture=$(cd "$fixture" && pwd)
trap 'rm -rf -- "$fixture"' EXIT
mkdir -p "$fixture/bin" "$fixture/李 home" "$fixture/windows profile" "$fixture/mcp-server/tests"
cp -R "$server_dir/../specs" "$fixture/"
cp -R "$server_dir/src" "$server_dir/pyproject.toml" "$server_dir/README.md" \
    "$server_dir/install.sh" "$fixture/mcp-server/"
cp "$server_dir/tests/check_global_install.py" "$fixture/mcp-server/tests/"

venv="$fixture/李 home/lia installer"
python -m venv "$venv"
scripts="$venv/bin"
if [[ -d "$venv/Scripts" ]]; then
    scripts="$venv/Scripts"
fi

# A Windows Store alias resolves on PATH but fails when invoked.
printf '#!/bin/sh\nexit 49\n' > "$fixture/bin/python3"
chmod +x "$fixture/bin/python3"
export PATH="$fixture/bin:$scripts:$PATH"
export HOME="$fixture/李 home"
export USERPROFILE="$fixture/windows profile"
export PIP_NO_INDEX=1
unset PYTHONPATH PYTHONUTF8

PYTHONIOENCODING=cp1252 "$fixture/mcp-server/install.sh" --global
python "$fixture/mcp-server/tests/check_global_install.py" "$HOME/.lia/specs"
