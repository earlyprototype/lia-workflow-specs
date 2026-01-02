"""
Tests for the models module.
"""

import pytest
from pathlib import Path
import tempfile
import os

from lia_workflow_mcp.models import (
    WorkflowSpec,
    SpecCollection,
    SpecCategory,
    WorkflowPhase,
)


class TestWorkflowPhase:
    """Tests for WorkflowPhase dataclass."""
    
    def test_create_phase(self):
        phase = WorkflowPhase(
            number=1,
            name="Task Analysis",
            description="Analyse the task requirements",
        )
        assert phase.number == 1
        assert phase.name == "Task Analysis"
        assert phase.description == "Analyse the task requirements"
        assert phase.constraints == []


class TestWorkflowSpec:
    """Tests for WorkflowSpec dataclass."""
    
    def test_create_spec(self):
        spec = WorkflowSpec(
            name="test",
            filename="test.toml",
            filepath=Path("/tmp/test.toml"),
            category=SpecCategory.DEVELOPMENT,
            description="A test workflow",
            prompt="Test prompt content",
        )
        assert spec.name == "test"
        assert spec.category == SpecCategory.DEVELOPMENT
    
    def test_extract_phases(self):
        prompt = """
        ### 1. Task Analysis and Planning
        Some content here.
        
        ### 2. Implementation
        More content.
        
        ### 3. Testing
        Final content.
        """
        phases = WorkflowSpec._extract_phases(prompt)
        assert len(phases) == 3
        assert phases[0].number == 1
        assert phases[0].name == "Task Analysis and Planning"
        assert phases[1].number == 2
        assert phases[1].name == "Implementation"
    
    def test_extract_tags(self):
        tags = WorkflowSpec._extract_tags(
            "A development workflow for testing and review",
            SpecCategory.DEVELOPMENT
        )
        assert "development" in tags
        assert "testing" in tags
        assert "review" in tags
    
    def test_to_dict(self):
        spec = WorkflowSpec(
            name="test",
            filename="test.toml",
            filepath=Path("/tmp/test.toml"),
            category=SpecCategory.DEVELOPMENT,
            description="A test workflow",
            prompt="Test prompt",
            phases=[
                WorkflowPhase(number=1, name="Phase 1", description=""),
            ],
            tags=["development", "testing"],
        )
        
        data = spec.to_dict()
        assert data["name"] == "test"
        assert data["category"] == "development"
        assert data["phase_count"] == 1
        assert len(data["phases"]) == 1
    
    def test_get_summary(self):
        spec = WorkflowSpec(
            name="test",
            filename="test.toml",
            filepath=Path("/tmp/test.toml"),
            category=SpecCategory.DEVELOPMENT,
            description="A test workflow for development",
            prompt="Test prompt",
            phases=[
                WorkflowPhase(number=1, name="Planning", description=""),
                WorkflowPhase(number=2, name="Implementation", description=""),
            ],
            tags=["development", "testing"],
        )
        
        summary = spec.get_summary()
        assert "# test" in summary
        assert "development" in summary
        assert "Planning" in summary
        assert "Implementation" in summary
    
    def test_from_toml_file(self):
        # Create a temporary TOML file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".toml", delete=False, dir="/tmp"
        ) as f:
            f.write('''
description = "A test workflow specification"
prompt = """
# Test Workflow

## Goal
Test goal.

### 1. First Phase
Content.

### 2. Second Phase
More content.
"""
''')
            temp_path = Path(f.name)
        
        try:
            spec = WorkflowSpec.from_toml_file(temp_path)
            assert spec.name == temp_path.stem
            assert "test workflow" in spec.description.lower()
            assert len(spec.phases) == 2
        finally:
            os.unlink(temp_path)


class TestSpecCollection:
    """Tests for SpecCollection."""
    
    def test_empty_collection(self):
        collection = SpecCollection()
        assert len(collection.specs) == 0
    
    def test_get_by_name_not_found(self):
        collection = SpecCollection()
        result = collection.get_by_name("nonexistent")
        assert result is None
    
    def test_get_by_name(self):
        spec = WorkflowSpec(
            name="test",
            filename="test.toml",
            filepath=Path("/tmp/test.toml"),
            category=SpecCategory.DEVELOPMENT,
            description="Test",
            prompt="Prompt",
        )
        collection = SpecCollection(specs=[spec])
        
        result = collection.get_by_name("test")
        assert result is not None
        assert result.name == "test"
    
    def test_get_by_category(self):
        specs = [
            WorkflowSpec(
                name="dev",
                filename="dev.toml",
                filepath=Path("/tmp/dev.toml"),
                category=SpecCategory.DEVELOPMENT,
                description="Dev",
                prompt="Prompt",
            ),
            WorkflowSpec(
                name="review",
                filename="review.toml",
                filepath=Path("/tmp/review.toml"),
                category=SpecCategory.QUALITY,
                description="Review",
                prompt="Prompt",
            ),
        ]
        collection = SpecCollection(specs=specs)
        
        dev_specs = collection.get_by_category(SpecCategory.DEVELOPMENT)
        assert len(dev_specs) == 1
        assert dev_specs[0].name == "dev"
    
    def test_search(self):
        specs = [
            WorkflowSpec(
                name="dev",
                filename="dev.toml",
                filepath=Path("/tmp/dev.toml"),
                category=SpecCategory.DEVELOPMENT,
                description="Development workflow",
                prompt="Prompt",
                tags=["development", "coding"],
            ),
            WorkflowSpec(
                name="security",
                filename="security.toml",
                filepath=Path("/tmp/security.toml"),
                category=SpecCategory.QUALITY,
                description="Security assessment workflow",
                prompt="Prompt",
                tags=["security", "audit"],
            ),
        ]
        collection = SpecCollection(specs=specs)
        
        # Search by name
        results = collection.search("dev")
        assert len(results) == 1
        assert results[0].name == "dev"
        
        # Search by description
        results = collection.search("security")
        assert len(results) == 1
        assert results[0].name == "security"
        
        # Search by tag
        results = collection.search("audit")
        assert len(results) == 1
        assert results[0].name == "security"
    
    def test_get_categories(self):
        specs = [
            WorkflowSpec(
                name="dev",
                filename="dev.toml",
                filepath=Path("/tmp/dev.toml"),
                category=SpecCategory.DEVELOPMENT,
                description="Dev",
                prompt="Prompt",
            ),
            WorkflowSpec(
                name="spec",
                filename="spec.toml",
                filepath=Path("/tmp/spec.toml"),
                category=SpecCategory.DEVELOPMENT,
                description="Spec",
                prompt="Prompt",
            ),
            WorkflowSpec(
                name="review",
                filename="review.toml",
                filepath=Path("/tmp/review.toml"),
                category=SpecCategory.QUALITY,
                description="Review",
                prompt="Prompt",
            ),
        ]
        collection = SpecCollection(specs=specs)
        
        categories = collection.get_categories()
        assert "development" in categories
        assert "quality" in categories
        assert len(categories["development"]) == 2
        assert len(categories["quality"]) == 1
    
    def test_recommend_for_task(self):
        specs = [
            WorkflowSpec(
                name="dev",
                filename="dev.toml",
                filepath=Path("/tmp/dev.toml"),
                category=SpecCategory.DEVELOPMENT,
                description="Development implementation workflow",
                prompt="Prompt",
                tags=["development", "implementation"],
            ),
            WorkflowSpec(
                name="security",
                filename="security.toml",
                filepath=Path("/tmp/security.toml"),
                category=SpecCategory.QUALITY,
                description="Security vulnerability assessment",
                prompt="Prompt",
                tags=["security", "vulnerability"],
            ),
            WorkflowSpec(
                name="troubleshoot",
                filename="troubleshoot.toml",
                filepath=Path("/tmp/troubleshoot.toml"),
                category=SpecCategory.PROBLEM_SOLVING,
                description="Problem diagnosis and resolution",
                prompt="Prompt",
                tags=["debug", "problem"],
            ),
        ]
        collection = SpecCollection(specs=specs)
        
        # Test implementation task
        results = collection.recommend_for_task("I need to implement a new feature")
        assert len(results) > 0
        assert results[0].name == "dev"
        
        # Test security task
        results = collection.recommend_for_task("Check for security vulnerabilities")
        assert len(results) > 0
        assert any(r.name == "security" for r in results)
        
        # Test debug task
        results = collection.recommend_for_task("I have a bug to debug")
        assert len(results) > 0


class TestSpecCategory:
    """Tests for SpecCategory enum."""
    
    def test_all_categories(self):
        expected = [
            "development",
            "quality",
            "problem-solving",
            "research",
            "knowledge",
            "strategy",
        ]
        actual = [c.value for c in SpecCategory]
        assert sorted(actual) == sorted(expected)
