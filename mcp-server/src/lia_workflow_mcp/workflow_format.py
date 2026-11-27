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


# Backtick spans can contain literal HTML comment delimiters.
_CODE_OR_COMMENT = re.compile(
    r"(?<!`)(?P<ticks>`+)(?!`).*?(?<!`)(?P=ticks)(?!`)|<!--.*?(?:(?P<close>-->)|$)"
)


def _without_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    if in_comment:
        _, close, line = line.partition("-->")
        if not close:
            return "", True

    visible = []
    start = 0
    for match in _CODE_OR_COMMENT.finditer(line):
        if match["ticks"]:
            continue
        visible.append(line[start:match.start()])
        if not match["close"]:
            return "".join(visible), True
        start = match.end()
    return "".join(visible) + line[start:], False


class WorkflowDocument:
    """Index Markdown headings and closed fences by their position in the prompt."""

    def __init__(self, prompt: str):
        self.headings: list[Heading] = []
        self.fences: list[CodeBlock] = []
        self.prose = dedent(prompt).splitlines()
        lines = iter(enumerate(self.prose))
        in_comment = False
        for number, line in lines:
            fence = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", line)
            if fence and not in_comment:
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
                continue
            if in_comment or "<!--" in line:
                line, in_comment = _without_comments(line, in_comment)
                self.prose[number] = line
            if heading := re.fullmatch(r" {0,3}(#{1,6})[ \t]+(.+?)\s*", line):
                title = re.sub(r"[ \t]+#+$", "", heading[2]).strip()
                self.headings.append(Heading(number, len(heading[1]), title))

        markers = [line.strip() for line in self.prose]
        self.phase_lines = range(len(markers))
        if "<workflow-definition>" in markers:
            start = markers.index("<workflow-definition>") + 1
            end = next((i for i in range(start, len(markers)) if markers[i] == "</workflow-definition>"),
                       len(markers))
            self.phase_lines = range(start, end)

    def section_end(self, heading: Heading) -> int:
        return next((h.line for h in self.headings if h.line > heading.line and h.level <= heading.level),
                    len(self.prose))

    def section_fences(self, *titles: str):
        for heading in self.headings:
            if heading.title.casefold() in titles:
                end = self.section_end(heading)
                yield from (block for block in self.fences if heading.line < block.line < end)

    def phase_headings(self):
        role_phase_end = 0
        for heading in self.headings:
            if heading.line not in self.phase_lines or heading.level not in {2, 3}:
                continue
            # Within a role phase, a bare numbered subheading introduces a task.
            prefix = r"phase\s+" if heading.level == 2 or heading.line < role_phase_end else r"(?:phase\s+)?"
            match = re.fullmatch(prefix + r"(\d+)[.:]\s*(\S.*)", heading.title, re.IGNORECASE)
            if match:
                if heading.level == 2:
                    role_phase_end = self.section_end(heading)
                yield heading, int(match[1]), match[2]

    def _has_instructions(self, heading: Heading, end: int) -> bool:
        body = self.prose[heading.line + 1:end]
        return any(line.strip() and line.strip() not in {"---", "</workflow-definition>"}
                   and not line.lstrip().startswith("#") for line in body)

    def phase_errors(self):
        phases = list(self.phase_headings())
        for expected, (_, number, name) in enumerate(phases, start=1):
            if number != expected:
                yield f"Expected phase {expected}, observed {number} ({name})"
                break

        end = self.phase_lines.stop
        for heading, number, name in reversed(phases):
            if not self._has_instructions(heading, min(end, self.section_end(heading))):
                yield f"Phase {number} ({name}) has no instructions"
            end = heading.line

    def structure_errors(self):
        yield from self.phase_errors()
        for heading in self.headings:
            if (heading.title.casefold() == "important execution instructions"
                    and not self._has_instructions(heading, self.section_end(heading))):
                yield "Add instructions to the Important Execution Instructions section"

    def required_sections(self) -> dict[str, bool]:
        titles = {h.title.casefold() for h in self.headings}
        first_phase = next(self.phase_headings(), None)
        if first_phase and first_phase[0].level == 2:
            checks = {"Your Role": "your role" in titles}
        else:
            checks = {
                "Numbered workflow phase": first_phase is not None,
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
