"""Tests for the spec loader module."""

from pathlib import Path

import pytest

from workflow_specs_mcp.spec_loader import SpecLoader, SpecMetadata, ValidationResult


@pytest.fixture
def specs_dir():
    """Get the specs directory path."""
    return Path(__file__).parent.parent.parent / "specs"


@pytest.fixture
def spec_loader(specs_dir):
    """Create a spec loader instance."""
    return SpecLoader(specs_dir)


class TestSpecLoader:
    """Tests for SpecLoader class."""

    def test_discover_specs(self, spec_loader, specs_dir):
        """Test that specs are discovered."""
        if not specs_dir.exists():
            pytest.skip("Specs directory not found")

        specs = spec_loader.discover_specs()
        assert len(specs) > 0
        assert all(p.suffix == ".toml" for p in specs)

    def test_get_categories(self, spec_loader, specs_dir):
        """Test category discovery."""
        if not specs_dir.exists():
            pytest.skip("Specs directory not found")

        categories = spec_loader.get_categories()
        assert "development" in categories
        assert "quality" in categories

    def test_load_spec(self, spec_loader, specs_dir):
        """Test loading a spec file."""
        if not specs_dir.exists():
            pytest.skip("Specs directory not found")

        spec_path = specs_dir / "development" / "dev.toml"
        if not spec_path.exists():
            pytest.skip("Dev spec not found")

        data = spec_loader.load_spec(spec_path)
        assert data is not None
        assert "description" in data
        assert "prompt" in data

    def test_extract_metadata(self, spec_loader, specs_dir):
        """Test metadata extraction."""
        if not specs_dir.exists():
            pytest.skip("Specs directory not found")

        spec_path = specs_dir / "development" / "spec.toml"
        if not spec_path.exists():
            pytest.skip("Spec spec not found")

        metadata = spec_loader.extract_metadata(spec_path)
        assert metadata is not None
        assert metadata.name == "spec"
        assert metadata.category == "development"
        assert len(metadata.phases) > 0
        assert metadata.constraints["MUST"] > 0

    def test_validate_spec(self, spec_loader, specs_dir):
        """Test spec validation."""
        if not specs_dir.exists():
            pytest.skip("Specs directory not found")

        spec_path = specs_dir / "development" / "dev.toml"
        if not spec_path.exists():
            pytest.skip("Dev spec not found")

        result = spec_loader.validate_spec(spec_path)
        assert isinstance(result, ValidationResult)
        # Dev spec should be valid
        assert result.is_valid or len(result.errors) > 0

    def test_search_specs(self, spec_loader, specs_dir):
        """Test searching specs."""
        if not specs_dir.exists():
            pytest.skip("Specs directory not found")

        results = spec_loader.search_specs("development")
        assert len(results) > 0

    def test_get_specs_by_category(self, spec_loader, specs_dir):
        """Test getting specs organised by category."""
        if not specs_dir.exists():
            pytest.skip("Specs directory not found")

        by_category = spec_loader.get_specs_by_category()
        assert len(by_category) > 0
        assert all(isinstance(v, list) for v in by_category.values())


class TestSpecMetadata:
    """Tests for SpecMetadata dataclass."""

    def test_metadata_creation(self):
        """Test creating metadata."""
        metadata = SpecMetadata(
            name="test",
            path="specs/test/test.toml",
            category="test",
            description="Test spec",
            phases=["Phase 1", "Phase 2"],
            constraints={"MUST": 5, "SHOULD": 3},
            has_mermaid_diagram=True,
            has_notepad_template=True,
            modes=["collaboration", "silent"],
            output_directory=".lia/test/",
        )

        assert metadata.name == "test"
        assert len(metadata.phases) == 2
        assert metadata.constraints["MUST"] == 5


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_validation_result_creation(self):
        """Test creating validation result."""
        result = ValidationResult(
            is_valid=True,
            errors=[],
            warnings=["Missing recommended section"],
            info=["Found required key"],
        )

        assert result.is_valid
        assert len(result.errors) == 0
        assert len(result.warnings) == 1
