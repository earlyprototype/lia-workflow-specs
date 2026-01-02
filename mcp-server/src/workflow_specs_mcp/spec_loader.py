"""
Spec Loader Module

Utilities for loading, parsing, and analysing workflow specification files.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import tomli


@dataclass
class SpecMetadata:
    """Metadata extracted from a workflow spec."""

    name: str
    path: str
    category: str
    description: str
    version: str = "1.0.0"
    phases: list[str] = field(default_factory=list)
    constraints: dict[str, int] = field(default_factory=dict)
    has_mermaid_diagram: bool = False
    has_notepad_template: bool = False
    modes: list[str] = field(default_factory=list)
    output_directory: str = ""
    # New trigger fields
    on_complete: list[str] = field(default_factory=list)
    can_chain_from: list[str] = field(default_factory=list)
    provides: list[str] = field(default_factory=list)
    requires: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    authors: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of spec validation."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    info: list[str] = field(default_factory=list)


class SpecLoader:
    """Loads and parses workflow specification files."""

    REQUIRED_SECTIONS = [
        "Workflow Mode System",
        "Goal",
        "workflow-definition",
        "Workflow Diagram",
        "IMPORTANT EXECUTION INSTRUCTIONS",
        "0-Notepad Template",
    ]

    RECOMMENDED_SECTIONS = [
        "Agent Mindset",
        "Agent Self-Development",
    ]

    NOTEPAD_SECTIONS = [
        "## 🧠 Key Insights",
        "## 🔧 Technical Notes",
        "## 💡 Ideas",
        "## 🔗 Cross-",
        "## 📝 User Notes",
        "## 🤖 LLM Observations",
    ]

    def __init__(self, specs_directory: Path):
        """
        Initialise the spec loader.

        Args:
            specs_directory: Path to the specs directory
        """
        self.specs_directory = specs_directory
        self._cache: dict[str, dict] = {}

    def discover_specs(self) -> list[Path]:
        """
        Discover all .toml spec files in the specs directory.

        Returns:
            List of paths to spec files
        """
        if not self.specs_directory.exists():
            return []
        return sorted(self.specs_directory.rglob("*.toml"))

    def load_spec(self, spec_path: Path) -> Optional[dict]:
        """
        Load and parse a spec file.

        Args:
            spec_path: Path to the spec file

        Returns:
            Parsed spec data or None if loading fails
        """
        cache_key = str(spec_path)
        if cache_key in self._cache:
            return self._cache[cache_key]

        try:
            with open(spec_path, "rb") as f:
                data = tomli.load(f)
            self._cache[cache_key] = data
            return data
        except tomli.TOMLDecodeError:
            # Some spec files may have invalid escape sequences (e.g., Windows paths)
            # Fall back to raw string parsing
            try:
                content = spec_path.read_text(encoding="utf-8")
                data = self._parse_spec_fallback(content)
                if data:
                    self._cache[cache_key] = data
                return data
            except Exception:
                return None
        except Exception:
            return None

    def _parse_spec_fallback(self, content: str) -> Optional[dict]:
        """
        Fallback parser for specs with TOML escape sequence issues.
        Extracts description and prompt fields manually.
        """
        result = {}

        # Extract description
        desc_match = re.search(r'^description\s*=\s*"([^"]*)"', content, re.MULTILINE)
        if desc_match:
            result["description"] = desc_match.group(1)

        # Extract prompt (multiline string)
        prompt_start = content.find('prompt = """')
        if prompt_start != -1:
            prompt_start += len('prompt = """')
            prompt_end = content.rfind('"""')
            if prompt_end > prompt_start:
                result["prompt"] = content[prompt_start:prompt_end]

        return result if result else None

    def get_spec_content(self, spec_path: Path) -> Optional[str]:
        """
        Get the raw content of a spec file.

        Args:
            spec_path: Path to the spec file

        Returns:
            Raw file content or None
        """
        try:
            return spec_path.read_text(encoding="utf-8")
        except Exception:
            return None

    def extract_metadata(self, spec_path: Path) -> Optional[SpecMetadata]:
        """
        Extract metadata from a spec file.

        Args:
            spec_path: Path to the spec file

        Returns:
            SpecMetadata object or None
        """
        data = self.load_spec(spec_path)
        if not data:
            return None

        prompt = data.get("prompt", "")
        description = data.get("description", "")

        # Extract category from path
        try:
            category = spec_path.parent.name
        except Exception:
            category = "unknown"

        # Extract phases from workflow definition
        phases = self._extract_phases(prompt)

        # Count constraints
        constraints = {
            "MUST": len(re.findall(r"\bMUST\b", prompt)),
            "SHOULD": len(re.findall(r"\bSHOULD\b", prompt)),
            "MAY": len(re.findall(r"\bMAY\b", prompt)),
        }

        # Check for mermaid diagram
        has_mermaid = "```mermaid" in prompt.lower()

        # Check for notepad template
        notepad_sections_found = sum(1 for s in self.NOTEPAD_SECTIONS if s in prompt)
        has_notepad = notepad_sections_found >= 4

        # Extract modes
        modes = []
        if "Collaboration Mode" in prompt:
            modes.append("collaboration")
        if "Silent Mode" in prompt:
            modes.append("silent")

        # Extract output directory pattern
        output_dir = self._extract_output_directory(prompt)

        # Extract triggers
        triggers = data.get("triggers", {})
        on_complete = triggers.get("on_complete", [])
        can_chain_from = triggers.get("can_chain_from", [])
        provides = triggers.get("provides", [])
        requires = triggers.get("requires", [])

        # Extract metadata fields
        metadata_section = data.get("metadata", {})
        tags = metadata_section.get("tags", [])
        authors = metadata_section.get("authors", [])
        version = metadata_section.get("version", "1.0.0")

        return SpecMetadata(
            name=spec_path.stem,
            path=str(spec_path.relative_to(self.specs_directory.parent)),
            category=category,
            description=description,
            version=version,
            phases=phases,
            constraints=constraints,
            has_mermaid_diagram=has_mermaid,
            has_notepad_template=has_notepad,
            modes=modes,
            output_directory=output_dir,
            on_complete=on_complete,
            can_chain_from=can_chain_from,
            provides=provides,
            requires=requires,
            tags=tags,
            authors=authors,
        )

    def _extract_phases(self, prompt: str) -> list[str]:
        """Extract phase names from a spec prompt."""
        phases = []
        # Look for numbered phases like "### 1. Phase Name"
        pattern = r"###\s*\d+\.\s*([^\n]+)"
        matches = re.findall(pattern, prompt)
        phases.extend(m.strip() for m in matches)
        return phases

    def _extract_output_directory(self, prompt: str) -> str:
        """Extract the output directory pattern from a spec."""
        patterns = [
            r"\.lia/([a-z-]+)/\{[a-z_]+\}",
            r"'\.lia/([a-z-]+)/",
        ]
        for pattern in patterns:
            match = re.search(pattern, prompt)
            if match:
                return f".lia/{match.group(1)}/"
        return ""

    def validate_spec(self, spec_path: Path) -> ValidationResult:
        """
        Validate a spec file.

        Args:
            spec_path: Path to the spec file

        Returns:
            ValidationResult with errors, warnings, and info
        """
        result = ValidationResult(is_valid=True)

        # Check file exists
        if not spec_path.exists():
            result.is_valid = False
            result.errors.append(f"File does not exist: {spec_path}")
            return result

        # Load and parse TOML
        data = self.load_spec(spec_path)
        if data is None:
            result.is_valid = False
            result.errors.append("Invalid TOML syntax")
            return result
        result.info.append("Valid TOML syntax")

        # Check required keys
        for key in ["description", "prompt"]:
            if key not in data:
                result.is_valid = False
                result.errors.append(f"Missing required key: '{key}'")
            else:
                result.info.append(f"Found required key: '{key}'")

        # Validate prompt content
        prompt = data.get("prompt", "")

        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in prompt:
                result.is_valid = False
                result.errors.append(f"Missing required section: '{section}'")
            else:
                result.info.append(f"Found required section: '{section}'")

        # Check recommended sections
        for section in self.RECOMMENDED_SECTIONS:
            if section not in prompt:
                result.warnings.append(f"Missing recommended section: '{section}'")
            else:
                result.info.append(f"Found recommended section: '{section}'")

        # Check mermaid diagram
        if "```mermaid" not in prompt.lower():
            result.warnings.append("No Mermaid workflow diagram found")
        else:
            result.info.append("Found Mermaid workflow diagram")

        # Check constraints
        must_count = len(re.findall(r"\bMUST\b", prompt))
        should_count = len(re.findall(r"\bSHOULD\b", prompt))

        if must_count == 0:
            result.warnings.append("No MUST constraints found")
        else:
            result.info.append(f"Found {must_count} MUST constraints")

        if should_count > 0:
            result.info.append(f"Found {should_count} SHOULD constraints")

        # Check notepad template
        notepad_sections = sum(1 for s in self.NOTEPAD_SECTIONS if s in prompt)
        if notepad_sections < 4:
            result.errors.append(f"Notepad template incomplete ({notepad_sections}/6 sections)")
            result.is_valid = False
        else:
            result.info.append(f"Notepad template: {notepad_sections}/6 sections")

        # Check description
        description = data.get("description", "")
        if not description or len(description) < 20:
            result.warnings.append("Description is missing or very short")

        return result

    def search_specs(
        self, query: str, category: Optional[str] = None
    ) -> list[tuple[Path, SpecMetadata]]:
        """
        Search specs by keyword in name, description, or content.

        Args:
            query: Search query string
            category: Optional category filter

        Returns:
            List of (path, metadata) tuples matching the query
        """
        results = []
        query_lower = query.lower()

        for spec_path in self.discover_specs():
            # Filter by category if specified
            if category and spec_path.parent.name != category:
                continue

            # Load spec data
            data = self.load_spec(spec_path)
            if not data:
                continue

            # Search in name
            if query_lower in spec_path.stem.lower():
                metadata = self.extract_metadata(spec_path)
                if metadata:
                    results.append((spec_path, metadata))
                continue

            # Search in description
            description = data.get("description", "").lower()
            if query_lower in description:
                metadata = self.extract_metadata(spec_path)
                if metadata:
                    results.append((spec_path, metadata))
                continue

            # Search in prompt content
            prompt = data.get("prompt", "").lower()
            if query_lower in prompt:
                metadata = self.extract_metadata(spec_path)
                if metadata:
                    results.append((spec_path, metadata))

        return results

    def get_categories(self) -> list[str]:
        """
        Get all unique categories (subdirectories) in the specs directory.

        Returns:
            List of category names
        """
        categories = set()
        for spec_path in self.discover_specs():
            categories.add(spec_path.parent.name)
        return sorted(categories)

    def get_specs_by_category(self) -> dict[str, list[SpecMetadata]]:
        """
        Get all specs organised by category.

        Returns:
            Dictionary mapping category names to lists of SpecMetadata
        """
        by_category: dict[str, list[SpecMetadata]] = {}

        for spec_path in self.discover_specs():
            metadata = self.extract_metadata(spec_path)
            if metadata:
                category = metadata.category
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append(metadata)

        return by_category

    def clear_cache(self):
        """Clear the spec cache."""
        self._cache.clear()
