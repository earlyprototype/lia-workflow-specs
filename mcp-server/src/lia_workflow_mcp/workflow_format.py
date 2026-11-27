"""Workflow discovery and format rules shared by MCP and the standalone validator."""

import re
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent


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


@dataclass(frozen=True)
class Heading:
    line: int
    level: int
    title: str


@dataclass(frozen=True)
class CodeBlock:
    line: int
    language: str
    content: str


class WorkflowDocument:
    """Index Markdown headings and closed fences by their position in the prompt."""

    def __init__(self, prompt: str):
        self.headings: list[Heading] = []
        self.fences: list[CodeBlock] = []
        self.prose = dedent(prompt).splitlines()
        lines = iter(enumerate(self.prose))
        for number, line in lines:
            fence = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", line)
            if fence:
                marker, language = fence.groups()
                closing = re.compile(rf" {{0,3}}{marker}{marker[0]}*[ \t]*")
                content = []
                self.prose[number] = ""
                for index, code in lines:
                    self.prose[index] = ""
                    if closing.fullmatch(code):
                        self.fences.append(CodeBlock(number, language.strip().casefold(), "\n".join(content)))
                        break
                    content.append(code)
            elif heading := re.fullmatch(r" {0,3}(#{1,6})[ \t]+(.+?)\s*", line):
                title = re.sub(r"[ \t]+#+$", "", heading[2]).strip()
                self.headings.append(Heading(number, len(heading[1]), title))

    def section_end(self, heading: Heading) -> int:
        return next((h.line for h in self.headings if h.line > heading.line and h.level <= heading.level),
                    len(self.prose))

    def section_fences(self, *titles: str):
        for heading in self.headings:
            if heading.title.casefold() in titles:
                end = self.section_end(heading)
                yield from (block for block in self.fences if heading.line < block.line < end)

    def phase_headings(self):
        for heading in self.headings:
            if heading.level == 3:
                match = re.fullmatch(r"(\d+)[.:]\s*(\S.*)", heading.title)
            elif heading.level == 2:
                match = re.fullmatch(r"phase\s+(\d+)[.:]\s*(\S.*)", heading.title, re.IGNORECASE)
            else:
                continue
            if match:
                yield heading, int(match[1]), match[2]

    def has_instructions(self, heading: Heading) -> bool:
        body = self.prose[heading.line + 1:self.section_end(heading)]
        return any(line.strip() and line.strip() not in {"---", "</workflow-definition>"}
                   and not line.lstrip().startswith("#") for line in body)

    def required_sections(self) -> dict[str, bool]:
        titles = {h.title.casefold() for h in self.headings}
        phases = self.phase_headings()
        if "your role" in titles:
            checks = {"Phase 1": any(self.has_instructions(h) for h, n, _ in phases if h.level == 2 and n == 1)}
        else:
            checks = {
                "Numbered workflow phase": any(self.has_instructions(h) for h, _, _ in phases if h.level == 3),
                "Workflow Modes": bool(titles & {"workflow modes", "workflow mode system"}),
                "Goal": "goal" in titles,
                "workflow-definition": any(line.strip() == "<workflow-definition>" for line in self.prose),
            }
        return {
            **checks,
            "Workflow Diagram": "workflow diagram" in titles,
            "IMPORTANT EXECUTION INSTRUCTIONS": "important execution instructions" in titles,
            "Notepad Template": bool(titles & {"0-notepad template", "notepad template"}),
        }


def required_sections(prompt: str) -> dict[str, bool]:
    return WorkflowDocument(prompt).required_sections()
