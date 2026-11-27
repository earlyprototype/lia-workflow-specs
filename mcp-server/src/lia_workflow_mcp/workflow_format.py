"""Workflow discovery and format rules shared by MCP and the standalone validator."""

import re
from pathlib import Path


def workflow_files(directory: Path) -> list[Path]:
    return sorted(
        path for path in directory.rglob("*.toml")
        if "_common" not in path.relative_to(directory).parts
    )


def workflow_text(data: dict) -> tuple[str, str]:
    """Read both the command format and the metadata/prompt table format."""
    description = data.get("description")
    if "description" not in data and isinstance(data.get("metadata"), dict):
        description = data["metadata"].get("description")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("description must be a nonempty string")
    prompt = data.get("prompt")
    if isinstance(prompt, dict):
        prompt = prompt.get("content")
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("prompt or prompt.content must be a nonempty string")
    return description, prompt


def required_sections(prompt: str) -> dict[str, bool]:
    headings = {h.strip().casefold() for h in re.findall(r"^#{1,6} (.+)$", prompt, re.MULTILINE)}
    if "your role" in headings:
        checks = {"Phase 1": any(h.startswith("phase 1:") for h in headings)}
    else:
        checks = {
            "Workflow Modes": bool(headings & {"workflow modes", "workflow mode system"}),
            "Goal": "goal" in headings,
            "workflow-definition": "<workflow-definition>" in prompt,
        }
    return {
        **checks,
        "Workflow Diagram": "workflow diagram" in headings,
        "IMPORTANT EXECUTION INSTRUCTIONS": "important execution instructions" in headings,
        "Notepad Template": bool(headings & {"0-notepad template", "notepad template"}),
    }
