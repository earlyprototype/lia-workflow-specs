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
import os
from pathlib import Path
from typing import List, Tuple, Dict
import re

try:
    import tomli
except ImportError:
    print("Error: tomli package required. Install with: pip install tomli")
    sys.exit(1)


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
    
    # Required top-level keys
    REQUIRED_KEYS = ['description', 'prompt']
    
    # Required sections in prompt content
    REQUIRED_SECTIONS = [
        'Workflow Mode System',
        'Goal',
        'workflow-definition',
        'Workflow Diagram',
        'IMPORTANT EXECUTION INSTRUCTIONS',
        '0-Notepad Template'
    ]
    
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
        
        # Validate required keys
        self._validate_required_keys(data)
        
        # Validate prompt content
        if 'prompt' in data:
            self._validate_prompt_content(data['prompt'])
        
        # Validate description
        if 'description' in data:
            self._validate_description(data['description'])
        
        # Update stats
        stats['errors'] = len(self.errors)
        stats['warnings'] = len(self.warnings)
        stats['info'] = len(self.info)
        
        return len(self.errors) == 0, stats
    
    def _validate_required_keys(self, data: dict):
        """Validate that all required top-level keys are present"""
        for key in self.REQUIRED_KEYS:
            if key not in data:
                self.errors.append(f"Missing required key: '{key}'")
            else:
                self.info.append(f"✓ Found required key: '{key}'")
    
    def _validate_description(self, description: str):
        """Validate description field"""
        if not description or not description.strip():
            self.warnings.append("Description is empty")
        elif len(description) < 20:
            self.warnings.append("Description is very short (< 20 chars)")
        else:
            self.info.append(f"✓ Description length: {len(description)} chars")
    
    def _validate_prompt_content(self, prompt: str):
        """Validate prompt content for required sections"""
        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in prompt:
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
        required_notepad_sections = [
            '## 🧠 Key Insights',
            '## 🔧 Technical Notes',
            '## 💡 Ideas',
            '## 🔗 Cross-',
            '## 📝 User Notes',
            '## 🤖 LLM Observations'
        ]
        
        found_sections = sum(1 for section in required_notepad_sections if section in prompt)
        
        if found_sections >= 5:
            self.info.append(f"✓ Found {found_sections}/6 notepad sections")
        elif found_sections >= 3:
            self.warnings.append(f"Only found {found_sections}/6 notepad sections")
        else:
            self.errors.append(f"Notepad template incomplete ({found_sections}/6 sections)")
    
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


def find_spec_files(directory: Path) -> List[Path]:
    """Find all .toml files in directory and subdirectories"""
    return list(directory.rglob('*.toml'))


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
        spec_files = find_spec_files(path)
    
    if not spec_files:
        print(f"{Colors.YELLOW}No .toml files found in {path}{Colors.RESET}")
        sys.exit(0)
    
    # Validate each file
    validator = SpecValidator(verbose=args.verbose)
    results = []
    
    for spec_file in spec_files:
        is_valid, stats = validator.validate_file(spec_file)
        results.append((spec_file, is_valid, stats))
        
        if not args.quiet:
            validator.print_results(spec_file, is_valid)
    
    # Print overall summary
    print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}OVERALL SUMMARY{Colors.RESET}")
    print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")
    
    valid_count = sum(1 for _, is_valid, _ in results if is_valid)
    invalid_count = len(results) - valid_count
    total_errors = sum(stats['errors'] for _, _, stats in results)
    total_warnings = sum(stats['warnings'] for _, _, stats in results)
    
    print(f"Total files: {len(results)}")
    print(f"{Colors.GREEN}Valid: {valid_count}{Colors.RESET}")
    print(f"{Colors.RED}Invalid: {invalid_count}{Colors.RESET}")
    print(f"{Colors.RED}Total errors: {total_errors}{Colors.RESET}")
    print(f"{Colors.YELLOW}Total warnings: {total_warnings}{Colors.RESET}")
    
    # Exit code
    if invalid_count > 0:
        print(f"\n{Colors.RED}❌ Validation failed{Colors.RESET}")
        sys.exit(1)
    elif total_warnings > 0:
        print(f"\n{Colors.YELLOW}⚠️  Validation passed with warnings{Colors.RESET}")
        sys.exit(0)
    else:
        print(f"\n{Colors.GREEN}✅ All specs valid{Colors.RESET}")
        sys.exit(0)


if __name__ == '__main__':
    main()

