"""
Tests for the MCP server module.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock

from lia_workflow_mcp.server import (
    validate_spec_content,
    compare_specs,
    generate_quick_reference,
)
from lia_workflow_mcp.models import (
    WorkflowSpec,
    SpecCategory,
    WorkflowPhase,
)


class TestValidateSpecContent:
    """Tests for spec validation."""
    
    def test_valid_spec(self):
        spec = WorkflowSpec(
            name="test",
            filename="test.toml",
            filepath=Path("/tmp/test.toml"),
            category=SpecCategory.DEVELOPMENT,
            description="Test workflow",
            prompt="""
# Test Workflow

## Workflow Mode System
Collaboration and Silent modes.

## Goal
Test goal.

<workflow-definition>
Workflow definition here.
</workflow-definition>

## Workflow Diagram
```mermaid
graph TD
    A --> B
```

## IMPORTANT EXECUTION INSTRUCTIONS
Instructions here.

## 0-Notepad Template
Template here.
            """,
            phases=[
                WorkflowPhase(number=1, name="Phase 1", description=""),
            ],
        )
        
        result = validate_spec_content(spec)
        assert "VALID" in result
        assert "✓ Found required section" in result
    
    def test_missing_sections(self):
        spec = WorkflowSpec(
            name="test",
            filename="test.toml",
            filepath=Path("/tmp/test.toml"),
            category=SpecCategory.DEVELOPMENT,
            description="Test workflow",
            prompt="Minimal prompt without required sections",
        )
        
        result = validate_spec_content(spec)
        assert "Missing required section" in result
        assert "INVALID" in result
    
    def test_no_mermaid_diagram(self):
        spec = WorkflowSpec(
            name="test",
            filename="test.toml",
            filepath=Path("/tmp/test.toml"),
            category=SpecCategory.DEVELOPMENT,
            description="Test workflow",
            prompt="""
## Workflow Mode System
## Goal
<workflow-definition></workflow-definition>
## IMPORTANT EXECUTION INSTRUCTIONS
## 0-Notepad Template
            """,
        )
        
        result = validate_spec_content(spec)
        assert "No Mermaid diagram" in result


class TestCompareSpecs:
    """Tests for spec comparison."""
    
    def test_compare_different_specs(self):
        spec1 = WorkflowSpec(
            name="dev",
            filename="dev.toml",
            filepath=Path("/tmp/dev.toml"),
            category=SpecCategory.DEVELOPMENT,
            description="Development workflow for implementing features",
            prompt="Prompt 1",
            phases=[
                WorkflowPhase(number=1, name="Planning", description=""),
                WorkflowPhase(number=2, name="Implementation", description=""),
            ],
            tags=["development", "implementation"],
        )
        
        spec2 = WorkflowSpec(
            name="review",
            filename="review.toml",
            filepath=Path("/tmp/review.toml"),
            category=SpecCategory.QUALITY,
            description="Code review workflow for quality assessment",
            prompt="Prompt 2",
            phases=[
                WorkflowPhase(number=1, name="Context", description=""),
                WorkflowPhase(number=2, name="Review", description=""),
                WorkflowPhase(number=3, name="Summary", description=""),
            ],
            tags=["quality", "review"],
        )
        
        result = compare_specs(spec1, spec2)
        
        assert "# Comparison: dev vs review" in result
        assert "development" in result
        assert "quality" in result
        assert "2" in result  # phases count
        assert "3" in result  # phases count


class TestGenerateQuickReference:
    """Tests for quick reference generation."""
    
    def test_generate_with_specs(self):
        """Test quick reference generation with controlled test data."""
        from lia_workflow_mcp.server import spec_collection
        from lia_workflow_mcp.models import WorkflowSpec, SpecCategory
        from pathlib import Path
        
        # Store original specs
        original_specs = spec_collection.specs
        
        try:
            # Populate with controlled test data
            spec_collection.specs = [
                WorkflowSpec(
                    name="test-dev",
                    filename="dev.toml",
                    filepath=Path("/tmp/dev.toml"),
                    category=SpecCategory.DEVELOPMENT,
                    description="Test development workflow",
                    prompt="Prompt",
                    tags=["development"],
                ),
            ]
            
            result = generate_quick_reference()
            assert isinstance(result, str)
            assert "# Lia Workflow Specs Quick Reference" in result
            assert "## Overview" in result
            assert "test-dev" in result
        finally:
            # Restore original specs
            spec_collection.specs = original_specs
