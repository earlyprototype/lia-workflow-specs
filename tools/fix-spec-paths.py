#!/usr/bin/env python3
"""
Fix hardcoded Windows paths in workflow spec files.

Replaces Windows-specific paths with portable alternatives using
environment variables or relative paths.
"""

import re
import sys
from pathlib import Path


def fix_windows_paths(content: str) -> str:
    """Replace hardcoded Windows paths with portable alternatives."""
    
    # Replacement patterns
    replacements = [
        # Main docs folder
        (
            r'C:\\Users\\Fab2\\Desktop\\AI\\POC\\Development\\v0\.7\\docs\\',
            '${WORKSPACE}/docs/ or ./docs/'
        ),
        (
            r'C:/Users/Fab2/Desktop/AI/POC/Development/v0\.7/docs/',
            '${WORKSPACE}/docs/ or ./docs/'
        ),
        # New implementations folder
        (
            r'C:\\Users\\Fab2\\Desktop\\AI\\POC\\Development\\v0\.7\\docs\\development\\Blueprint 1\\Phase 1\\New_Implimentations\\',
            '${WORKSPACE}/docs/development/new-implementations/'
        ),
        (
            r'C:/Users/Fab2/Desktop/AI/POC/Development/v0\.7/docs/development/Blueprint 1/Phase 1/New_Implimentations/',
            '${WORKSPACE}/docs/development/new-implementations/'
        ),
        # Proposals folder  
        (
            r'C:\\Users\\Fab2\\Desktop\\AI\\POC\\Development\\v0\.7\\docs\\development\\Blueprint 1\\Phase 1\\Proposals_For_Review\\',
            '${WORKSPACE}/docs/development/proposals/'
        ),
        (
            r'C:/Users/Fab2/Desktop/AI/POC/Development/v0\.7/docs/development/Blueprint 1/Phase 1/Proposals_For_Review/',
            '${WORKSPACE}/docs/development/proposals/'
        ),
    ]
    
    result = content
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result)
    
    return result


def process_file(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single spec file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        fixed_content = fix_windows_paths(content)
        
        if content != fixed_content:
            if dry_run:
                print(f"Would fix: {filepath}")
            else:
                filepath.write_text(fixed_content, encoding='utf-8')
                print(f"Fixed: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Fix hardcoded Windows paths in spec files'
    )
    parser.add_argument(
        'specs_dir',
        type=str,
        help='Path to specs directory'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without making changes'
    )
    
    args = parser.parse_args()
    specs_dir = Path(args.specs_dir)
    
    if not specs_dir.exists():
        print(f"Error: Directory not found: {specs_dir}")
        sys.exit(1)
    
    fixed_count = 0
    total_count = 0
    
    for toml_file in specs_dir.rglob('*.toml'):
        total_count += 1
        if process_file(toml_file, args.dry_run):
            fixed_count += 1
    
    action = "Would fix" if args.dry_run else "Fixed"
    print(f"\n{action} {fixed_count}/{total_count} files")


if __name__ == '__main__':
    main()
