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

import json
import subprocess
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
from lia_workflow_mcp.workflow_format import WorkflowDocument, workflow_files, workflow_text


# The paths advertised by category in the README.
CATALOG = {
    "development": ("dev", "spec", "test"),
    "quality": ("architecture", "constitution", "optimize", "review", "security"),
    "problem-solving": ("investigate", "troubleshoot", "wtf"),
    "research": ("learn", "paper", "recon", "research"),
    "knowledge": ("docs",),
    "strategy": ("innovate", "integrate", "nexus"),
}


STANDARD_NOTEPAD = {
    "KEY INSIGHTS & DISCOVERIES", "TECHNICAL NOTES & IMPLEMENTATION DETAILS",
    "IDEAS & FUTURE ENHANCEMENTS", "CROSS-SYSTEM CONNECTIONS", "USER NOTES", "LLM OBSERVATIONS",
}

CONNECTION_SUBJECT = {
    "dev": "COMPONENT", "spec": "SPECIFICATION", "test": "TESTING", "docs": "DOCUMENTATION",
    "review": "CODE", "learn": "LEARNING", "research": "TECHNOLOGY", "innovate": "COMPONENT",
}

CUSTOM_NOTEPADS = {
    "constitution": {"CURRENT PHASE", "PROJECT OVERVIEW", "EXISTING STANDARDS",
                     "DECISIONS MADE", "STANDARDS DEFINED", "QUESTIONS FOR USER"},
    "recon": {"MISSION", "SEARCH DIMENSIONS DEFINED", "RAW DISCOVERY LOG", "TIER CLASSIFICATION",
              "PATTERN OBSERVATIONS", "CRITICAL DISCOVERIES", "QUESTIONS EMERGING"},
    "paper": {"KEY INSIGHTS & INTELLECTUAL DISCOVERIES", "METHODOLOGICAL NOTES & TECHNICAL DETAILS",
              "RESEARCH QUESTIONS & FUTURE DIRECTIONS", "CROSS-PAPER CONNECTIONS & LITERATURE LINKS",
              "RESEARCHER NOTES", "LLM OBSERVATIONS"},
    "nexus": {"STRATEGIC INSIGHTS & KEY DISCOVERIES", "TEAM COORDINATION NOTES",
              "CLIENT RELATIONSHIP MANAGEMENT", "METHODOLOGY & PROCESS NOTES",
              "INNOVATION OPPORTUNITIES & IDEAS", "CROSS-PROJECT CONNECTIONS",
              "CLIENT FEEDBACK & ITERATIONS", "NEXUS OBSERVATIONS"},
}


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
        self.mermaid_diagrams: list[str] = []
    
    def validate_file(self, filepath: Path) -> Tuple[bool, Dict]:
        """
        Validate a single spec file.
        
        Returns:
            (is_valid, stats): Tuple of validation result and statistics
        """
        self.inspect_file(filepath)
        check_mermaid_diagrams([self])
        return self.result(filepath)

    def result(self, filepath: Path) -> Tuple[bool, Dict]:
        stats = {
            'file': str(filepath),
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'info': len(self.info)
        }
        return not self.errors, stats

    def inspect_file(self, filepath: Path):
        self.errors.clear()
        self.warnings.clear()
        self.info.clear()
        self.mermaid_diagrams.clear()

        # Check file exists
        if not filepath.exists():
            self.errors.append(f"File does not exist: {filepath}")
            return
        
        # Validate TOML syntax
        try:
            with open(filepath, 'rb') as f:
                data = tomli.load(f)
            self.info.append("✓ Valid TOML syntax")
        except Exception as e:
            self.errors.append(f"TOML syntax error: {str(e)}")
            return
        
        try:
            description, prompt = workflow_text(data)
        except ValueError as exc:
            self.errors.append(str(exc))
        else:
            self._validate_description(description)
            self._validate_prompt_content(prompt, filepath.stem)
    
    def _validate_description(self, description: str):
        """Validate description field"""
        if len(description) < 20:
            self.errors.append("Description must contain at least 20 characters")
        else:
            self.info.append(f"✓ Description length: {len(description)} chars")
    
    def _validate_prompt_content(self, prompt: str, name: str):
        """Validate prompt content for required sections"""
        # Check required sections
        document = WorkflowDocument(prompt)
        for section, present in document.required_sections().items():
            if not present:
                self.errors.append(f"Missing required section: '{section}'")
            else:
                self.info.append(f"✓ Found required section: '{section}'")
        
        # Check recommended sections
        for section in self.RECOMMENDED_SECTIONS:
            if not any(h.title.casefold() == section.casefold() for h in document.headings):
                self.warnings.append(f"Missing recommended section: '{section}'")
            else:
                self.info.append(f"✓ Found recommended section: '{section}'")
        
        # Validate workflow diagram
        self._validate_workflow_diagram(document)
        
        # Validate constraints formatting
        self._validate_constraints(prompt)
        
        # Validate notepad template
        self._validate_notepad_template(document, name)
    
    def _validate_workflow_diagram(self, document: WorkflowDocument):
        diagrams = [b for b in document.section_fences("workflow diagram")
                    if b.language in {"mermaid", "text", ""}]
        if not diagrams:
            self.errors.append("Workflow Diagram needs a fenced Mermaid or plain-text diagram")
        for block in diagrams:
            if not block.content.strip():
                self.errors.append("Workflow Diagram contains an empty diagram")
            elif block.language == "mermaid":
                self.mermaid_diagrams.append(block.content)
            else:
                self.info.append("✓ Found plain-text workflow diagram")
    
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
    
    def _validate_notepad_template(self, document: WorkflowDocument, name: str):
        blocks = document.section_fences("0-notepad template", "notepad template")
        template = next((b.content for b in blocks if b.language in {"md", "markdown"}), "")
        titles = {h.title.removeprefix("🔬 ").upper() for h in WorkflowDocument(template).headings
                  if h.level == 2}
        subject = CONNECTION_SUBJECT.get(name)
        if subject and f"CROSS-{subject} CONNECTIONS" in titles:
            titles.add("CROSS-SYSTEM CONNECTIONS")
        missing = CUSTOM_NOTEPADS.get(name, STANDARD_NOTEPAD) - titles
        if missing:
            self.errors.append("Notepad template incomplete. Missing: " + ", ".join(sorted(missing)))
        else:
            self.info.append("✓ Found required notepad sections")
    
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


def check_mermaid_diagrams(validators: list[SpecValidator]):
    """Parse all Mermaid blocks in one Node process and attribute errors to their files."""
    entries = [(v, diagram) for v in validators for diagram in v.mermaid_diagrams]
    if not entries:
        return
    try:
        result = subprocess.run(
            ["node", str(ROOT / "tools" / "parse-mermaid.mjs")],
            input=json.dumps([diagram for _, diagram in entries]),
            capture_output=True, encoding="utf-8", check=True, timeout=60,
        )
        errors = json.loads(result.stdout)
        if len(errors) != len(entries):
            raise ValueError("Incomplete result from Mermaid")
    except (OSError, subprocess.SubprocessError, ValueError) as exc:
        message = f"Cannot check Mermaid diagram ({exc}). Install Node.js and run npm ci --prefix tools."
        for validator, _ in entries:
            validator.errors.append(message)
        return
    for (validator, _), error in zip(entries, errors):
        if error is None:
            validator.info.append("✓ Parsed Mermaid workflow diagram")
        else:
            validator.errors.append(f"Invalid Mermaid workflow diagram: {error}")


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
    reports = []
    for spec_file in spec_files:
        validator = SpecValidator(verbose=args.verbose)
        validator.inspect_file(spec_file)
        reports.append(validator)
    check_mermaid_diagrams(reports)
    results = []
    
    for spec_file, validator in zip(spec_files, reports):
        is_valid, stats = validator.result(spec_file)
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

