"""
Data models for workflow specifications.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional
import tomli


class SpecCategory(str, Enum):
    """Categories of workflow specifications."""
    DEVELOPMENT = "development"
    QUALITY = "quality"
    PROBLEM_SOLVING = "problem-solving"
    RESEARCH = "research"
    KNOWLEDGE = "knowledge"
    STRATEGY = "strategy"


@dataclass
class WorkflowPhase:
    """Represents a phase in a workflow."""
    number: int
    name: str
    description: str
    output_file: Optional[str] = None
    constraints: list[str] = field(default_factory=list)


@dataclass
class WorkflowSpec:
    """Represents a workflow specification."""
    name: str
    filename: str
    filepath: Path
    category: SpecCategory
    description: str
    prompt: str
    phases: list[WorkflowPhase] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    
    @classmethod
    def from_toml_file(cls, filepath: Path) -> "WorkflowSpec":
        """Load a workflow spec from a TOML file."""
        # Read the file content and fix common TOML escape issues
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Fix Windows paths that cause TOML parsing issues
        # Backslashes in TOML triple-quoted strings can cause escape sequence errors
        import re
        
        # Simply replace all backslashes with forward slashes
        # This is safe for TOML content as forward slashes work in paths
        # and other uses of backslash (like \n) are typically not used in these specs
        def fix_backslashes(text: str) -> str:
            # Replace backslashes that look like Windows paths
            # Match patterns like C:\Users, \docs\, \Phase 1\, etc.
            # Be careful not to break valid TOML escapes in simple strings
            
            # First, handle complete Windows drive paths on a line
            # This regex matches lines containing Windows-style paths
            lines = text.split('\n')
            fixed_lines = []
            for line in lines:
                # If line contains a Windows drive path pattern, fix all backslashes in it
                if re.search(r'[A-Z]:\\', line):
                    line = line.replace('\\', '/')
                fixed_lines.append(line)
            return '\n'.join(fixed_lines)
        
        content = fix_backslashes(content)
        
        # Parse the fixed content
        import io
        data = tomli.load(io.BytesIO(content.encode("utf-8")))
        
        # Determine category from parent directory
        category_name = filepath.parent.name
        try:
            category = SpecCategory(category_name)
        except ValueError:
            category = SpecCategory.DEVELOPMENT
        
        # Extract name from filename
        name = filepath.stem
        
        # Parse phases from prompt content
        phases = cls._extract_phases(data.get("prompt", ""))
        
        # Extract tags from description
        tags = cls._extract_tags(data.get("description", ""), category)
        
        return cls(
            name=name,
            filename=filepath.name,
            filepath=filepath,
            category=category,
            description=data.get("description", ""),
            prompt=data.get("prompt", ""),
            phases=phases,
            tags=tags,
        )
    
    @staticmethod
    def _extract_phases(prompt: str) -> list[WorkflowPhase]:
        """Extract workflow phases from prompt content."""
        import re
        phases = []
        
        # Pattern to match phase headers like "### 1. Task Analysis and Planning"
        phase_pattern = r"###\s*(\d+)\.\s*([^\n]+)"
        matches = re.findall(phase_pattern, prompt)
        
        for number_str, name in matches:
            number = int(number_str)
            phases.append(WorkflowPhase(
                number=number,
                name=name.strip(),
                description="",  # Would require more sophisticated parsing
            ))
        
        return phases
    
    @staticmethod
    def _extract_tags(description: str, category: SpecCategory) -> list[str]:
        """Extract tags from description and category."""
        tags = [category.value]
        
        # Common keywords to look for
        keywords = [
            "development", "testing", "review", "security", "architecture",
            "troubleshooting", "research", "documentation", "innovation",
            "learning", "integration", "specification", "optimization"
        ]
        
        description_lower = description.lower()
        for keyword in keywords:
            if keyword in description_lower:
                tags.append(keyword)
        
        return list(set(tags))
    
    def to_dict(self) -> dict:
        """Convert spec to dictionary for JSON serialisation."""
        return {
            "name": self.name,
            "filename": self.filename,
            "filepath": str(self.filepath),
            "category": self.category.value,
            "description": self.description,
            "phase_count": len(self.phases),
            "phases": [
                {"number": p.number, "name": p.name}
                for p in self.phases
            ],
            "tags": self.tags,
        }
    
    def get_summary(self) -> str:
        """Get a concise summary of the spec."""
        phase_list = "\n".join(
            f"  {p.number}. {p.name}" for p in self.phases[:5]
        )
        if len(self.phases) > 5:
            phase_list += f"\n  ... and {len(self.phases) - 5} more phases"
        
        return f"""# {self.name}
**Category**: {self.category.value}
**Phases**: {len(self.phases)}

## Description
{self.description}

## Workflow Phases
{phase_list}

## Tags
{', '.join(self.tags)}
"""


@dataclass
class SpecCollection:
    """Collection of workflow specifications."""
    specs: list[WorkflowSpec] = field(default_factory=list)
    specs_dir: Optional[Path] = None
    
    def load_from_directory(self, specs_dir: Path) -> None:
        """Load all specs from a directory."""
        self.specs_dir = specs_dir
        self.specs = []
        
        if not specs_dir.exists():
            return
        
        for toml_file in specs_dir.rglob("*.toml"):
            try:
                spec = WorkflowSpec.from_toml_file(toml_file)
                self.specs.append(spec)
            except Exception as e:
                # Log error but continue loading other specs
                print(f"Warning: Failed to load {toml_file}: {e}")
    
    def get_by_name(self, name: str) -> Optional[WorkflowSpec]:
        """Get a spec by name."""
        for spec in self.specs:
            if spec.name == name or spec.filename == name:
                return spec
        return None
    
    def get_by_category(self, category: SpecCategory) -> list[WorkflowSpec]:
        """Get all specs in a category."""
        return [s for s in self.specs if s.category == category]
    
    def search(self, query: str) -> list[WorkflowSpec]:
        """Search specs by keyword in name, description, or tags."""
        query_lower = query.lower()
        results = []
        
        for spec in self.specs:
            if (query_lower in spec.name.lower() or
                query_lower in spec.description.lower() or
                any(query_lower in tag for tag in spec.tags)):
                results.append(spec)
        
        return results
    
    def get_categories(self) -> dict[str, list[str]]:
        """Get all categories and their spec names."""
        categories: dict[str, list[str]] = {}
        
        for spec in self.specs:
            cat_name = spec.category.value
            if cat_name not in categories:
                categories[cat_name] = []
            categories[cat_name].append(spec.name)
        
        return categories
    
    def recommend_for_task(self, task_description: str) -> list[WorkflowSpec]:
        """Recommend specs based on a task description."""
        task_lower = task_description.lower()
        scored_specs: list[tuple[WorkflowSpec, int]] = []
        
        # Keyword mappings to spec names
        keyword_mappings = {
            "dev.toml": ["implement", "build", "code", "feature", "fix", "bug"],
            "spec.toml": ["requirement", "design", "plan", "specification"],
            "test.toml": ["test", "testing", "quality", "automation", "qa"],
            "review.toml": ["review", "code review", "quality", "assess"],
            "troubleshoot.toml": ["debug", "issue", "problem", "error", "fix"],
            "investigate.toml": ["crash", "failure", "investigate", "forensic"],
            "security.toml": ["security", "vulnerability", "secure", "audit"],
            "optimize.toml": ["performance", "optimize", "speed", "slow"],
            "architecture.toml": ["architecture", "design", "structure", "system"],
            "research.toml": ["research", "evaluate", "compare", "technology"],
            "learn.toml": ["learn", "tutorial", "understand", "education"],
            "paper.toml": ["paper", "academic", "literature", "research paper"],
            "docs.toml": ["documentation", "docs", "document", "write"],
            "innovate.toml": ["innovate", "improve", "enhance", "creative"],
            "integrate.toml": ["integrate", "api", "connect", "interface"],
            "wtf.toml": ["mysterious", "legacy", "understand", "archaeology"],
        }
        
        for spec in self.specs:
            score = 0
            
            # Check keyword mappings
            keywords = keyword_mappings.get(spec.filename, [])
            for keyword in keywords:
                if keyword in task_lower:
                    score += 10
            
            # Check description match
            if any(word in task_lower for word in spec.description.lower().split()):
                score += 2
            
            # Check tag match
            for tag in spec.tags:
                if tag in task_lower:
                    score += 5
            
            if score > 0:
                scored_specs.append((spec, score))
        
        # Sort by score descending
        scored_specs.sort(key=lambda x: x[1], reverse=True)
        
        return [spec for spec, _ in scored_specs[:3]]
