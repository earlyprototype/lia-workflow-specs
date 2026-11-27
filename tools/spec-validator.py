#!/usr/bin/env python3
"""
Lia Workflow Spec Validator

Validates workflow specification files for:
- TOML syntax correctness
- Required sections presence
- Workflow diagram existence
- Constraint formatting
- Notepad template inclusion
"""

import sys
from pathlib import Path
from typing import List, Tuple, Dict
import re

try:
    import tomllib as tomli
except ImportError:
    import tomli

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp-server" / "src"))
from lia_workflow_mcp.workflow_format import required_sections, workflow_files, workflow_text


# The paths advertised by category in the README.
CATALOG = {
    "development": ("dev", "spec", "test"),
    "quality": ("architecture", "constitution", "optimize", "review", "security"),
    "problem-solving": ("investigate", "troubleshoot", "wtf"),
    "research": ("learn", "paper", "recon", "research"),
    "knowledge": ("docs",),
    "strategy": ("innovate", "integrate", "nexus"),
}


def count_notepad_sections(prompt: str) -> int:
    """Count headings in the Markdown template inside the notepad section."""
    lines = iter(prompt.splitlines())
    notepad_level = 0
    for line in lines:
        heading = re.fullmatch(r" {0,3}(#{1,6})(?:[ \t]+(.*))?", line)
        if heading:
            level = len(heading[1])
            if notepad_level and level <= notepad_level:
                break
            if (heading[2] or "").strip().casefold() in {"0-notepad template", "notepad template"}:
                notepad_level = level

        fence = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", line)
        if fence:
            marker, language = fence.groups()
            closing = re.compile(rf" {{0,3}}{marker}{marker[0]}*[ \t]*")
            is_template = notepad_level > 0 and language.strip().lower() in {"markdown", "md"}
            sections = set()
            # Headings inside a fenced example cannot open or close a document section.
            for code_line in lines:
                if closing.fullmatch(code_line):
                    if is_template:
                        return len(sections)
                    break
                if is_template and code_line.startswith("## ") and code_line[3:].strip():
                    sections.add(code_line[3:].strip())
    return 0


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class SpecValidator:
    """Validates workflow specification files"""
    
    # Recommended sections
    RECOMMENDED_SECTIONS = [
        'Agent Mindset',
        'Agent Self-Development',
    ]
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
    
    def validate_file(self, filepath: Path) -> Tuple[bool, Dict]:
        """
        Validate a single spec file.
        
        Returns:
            (is_valid, stats): Tuple of validation result and statistics
        """
        self.errors = []
        self.warnings = []
        self.info = []
        
        stats = {
            'file': str(filepath),
            'errors': 0,
            'warnings': 0,
            'info': 0
        }
        
        # Check file exists
        if not filepath.exists():
            self.errors.append(f"File does not exist: {filepath}")
            stats['errors'] = len(self.errors)
            return False, stats
        
        # Validate TOML syntax
        try:
            with open(filepath, 'rb') as f:
                data = tomli.load(f)
            self.info.append("✓ Valid TOML syntax")
        except Exception as e:
            self.errors.append(f"TOML syntax error: {str(e)}")
            stats['errors'] = len(self.errors)
            return False, stats
        
        try:
            description, prompt = workflow_text(data)
        except ValueError as exc:
            self.errors.append(str(exc))
        else:
            self._validate_description(description)
            self._validate_prompt_content(prompt)
        
        # Update stats
        stats['errors'] = len(self.errors)
        stats['warnings'] = len(self.warnings)
        stats['info'] = len(self.info)
        
        return len(self.errors) == 0, stats
    
    def _validate_description(self, description: str):
        """Validate description field"""
        if len(description) < 20:
            self.errors.append("Description must contain at least 20 characters")
        else:
            self.info.append(f"✓ Description length: {len(description)} chars")
    
    def _validate_prompt_content(self, prompt: str):
        """Validate prompt content for required sections"""
        # Check required sections
        for section, present in required_sections(prompt).items():
            if not present:
                self.errors.append(f"Missing required section: '{section}'")
            else:
                self.info.append(f"✓ Found required section: '{section}'")
        
        # Check recommended sections
        for section in self.RECOMMENDED_SECTIONS:
            if section not in prompt:
                self.warnings.append(f"Missing recommended section: '{section}'")
            else:
                self.info.append(f"✓ Found recommended section: '{section}'")
        
        # Validate workflow diagram
        self._validate_workflow_diagram(prompt)
        
        # Validate constraints formatting
        self._validate_constraints(prompt)
        
        # Validate notepad template
        self._validate_notepad_template(prompt)
    
    def _validate_workflow_diagram(self, prompt: str):
        """Validate that workflow diagram exists and uses Mermaid"""
        if '```mermaid' in prompt.lower():
            self.info.append("✓ Found Mermaid workflow diagram")
        else:
            self.warnings.append("Workflow diagram may not use Mermaid format")
    
    def _validate_constraints(self, prompt: str):
        """Validate constraint formatting"""
        # Look for constraint patterns
        must_count = len(re.findall(r'\bMUST\b', prompt))
        should_count = len(re.findall(r'\bSHOULD\b', prompt))
        may_count = len(re.findall(r'\bMAY\b', prompt))
        
        if must_count > 0:
            self.info.append(f"✓ Found {must_count} MUST constraints")
        else:
            self.warnings.append("No MUST constraints found")
        
        if should_count > 0:
            self.info.append(f"✓ Found {should_count} SHOULD constraints")
        
        if may_count > 0:
            self.info.append(f"✓ Found {may_count} MAY constraints")
    
    def _validate_notepad_template(self, prompt: str):
        """Validate notepad template structure"""
        found_sections = count_notepad_sections(prompt)
        
        if found_sections >= 5:
            self.info.append(f"✓ Found {found_sections} notepad sections")
        elif found_sections >= 3:
            self.warnings.append(f"Only found {found_sections} notepad sections")
        else:
            self.errors.append(f"Notepad template incomplete ({found_sections} sections)")
    
    def print_results(self, filepath: Path, is_valid: bool):
        """Print validation results with colors"""
        print(f"\n{Colors.BOLD}Validating: {filepath.name}{Colors.RESET}")
        print("=" * 60)
        
        # Print errors
        if self.errors:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ ERRORS:{Colors.RESET}")
            for error in self.errors:
                print(f"  {Colors.RED}• {error}{Colors.RESET}")
        
        # Print warnings
        if self.warnings:
            print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️  WARNINGS:{Colors.RESET}")
            for warning in self.warnings:
                print(f"  {Colors.YELLOW}• {warning}{Colors.RESET}")
        
        # Print info (only if verbose)
        if self.verbose and self.info:
            print(f"\n{Colors.BLUE}{Colors.BOLD}ℹ️  INFO:{Colors.RESET}")
            for info in self.info:
                print(f"  {Colors.BLUE}• {info}{Colors.RESET}")
        
        # Print summary
        print(f"\n{Colors.BOLD}SUMMARY:{Colors.RESET}")
        if is_valid:
            print(f"  {Colors.GREEN}✓ VALID{Colors.RESET}")
        else:
            print(f"  {Colors.RED}✗ INVALID{Colors.RESET}")
        
        print(f"  Errors: {len(self.errors)}")
        print(f"  Warnings: {len(self.warnings)}")
        print()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Validate Lia workflow specification files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate single file
  python spec-validator.py specs/development/spec.toml
  
  # Validate all specs in directory
  python spec-validator.py specs/
  
  # Verbose output
  python spec-validator.py specs/ -v
  
  # Quiet mode (errors only)
  python spec-validator.py specs/ -q
        """
    )
    
    parser.add_argument(
        'path',
        type=str,
        help='Path to spec file or directory'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output (show all info)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Quiet mode (errors only)'
    )
    
    parser.add_argument('--catalog', action='store_true',
                        help='Check the complete shipped inventory in a copy of the specs directory')
    args = parser.parse_args()
    
    # Get path
    path = Path(args.path)
    
    if not path.exists():
        print(f"{Colors.RED}Error: Path does not exist: {path}{Colors.RESET}")
        sys.exit(1)
    
    # Find spec files
    if path.is_file():
        spec_files = [path]
    else:
        spec_files = workflow_files(path)

    inventory_errors = []
    if args.catalog or path.resolve() == ROOT / 'specs':
        expected = {Path(category) / f'{name}.toml' for category, names in CATALOG.items() for name in names}
        actual = {file.relative_to(path) for file in spec_files}
        inventory_errors.extend(f"Missing workflow: {p}" for p in sorted(expected - actual))
        inventory_errors.extend(f"Unexpected workflow: {p}" for p in sorted(actual - expected))
    if not spec_files:
        inventory_errors.append(f"No workflow .toml files found in {path}")
    for error in inventory_errors:
        print(error)
    
    # Validate each file
    validator = SpecValidator(verbose=args.verbose)
    results = []
    
    for spec_file in spec_files:
        is_valid, stats = validator.validate_file(spec_file)
        results.append((spec_file, is_valid, stats))
        
        if not args.quiet:
            validator.print_results(spec_file, is_valid)
        else:
            for error in validator.errors:
                print(f"{spec_file}: {error}")
    
    # Print overall summary
    print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}OVERALL SUMMARY{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")
    
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    total_errors = len(inventory_errors) + sum(stats['errors'] for _, _, stats in results)
    total_warnings = sum(stats['warnings'] for _, _, stats in results)
    
    print(f"Total files: {len(results)}")
    print(f"{Colors.GREEN}Valid: {valid_count}{Colors.RESET}")
    print(f"{Colors.RED}Invalid: {invalid_count}{Colors.RESET}")
    print(f"{Colors.RED}Total errors: {total_errors}{Colors.RESET}")
    print(f"{Colors.YELLOW}Total warnings: {total_warnings}{Colors.RESET}")
    
    # Exit code
    if total_errors:
        print(f"\n{Colors.RED}❌ Validation failed{Colors.RESET}")
        sys.exit(1)
    elif total_warnings > 0:
        print(f"\n{Colors.YELLOW}⚠️  Validation passed with warnings{Colors.RESET}")
        sys.exit(0)
    else:
        print(f"\n{Colors.GREEN}✅ All specs valid{Colors.RESET}")
        sys.exit(0)


if __name__ == '__main__':
    sys.stdout.reconfigure(errors="backslashreplace")
    main()

