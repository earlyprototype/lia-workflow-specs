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
_THEMATIC_BREAK = re.compile(r"([*_-])(?:[ \t]*\1){2,}")
_LIST_MARKERS = re.compile(r"(?:(?:[-+*]|\d+[.)]|\[[ xX]\])(?:[ \t]+|$))+")
_QUOTE_MARKER = re.compile(r" {0,3}>[ \t]?")
_EXPLICIT_PHASE = re.compile(r"phase\s+(\d+)[.:]\s*(\S.*)", re.IGNORECASE)
_NUMBERED_PHASE = re.compile(r"(\d+)[.:]\s*(\S.*)")


def _unquote(line: str, limit: int | None = None) -> tuple[int, str]:
    depth = offset = 0
    while depth != limit and (marker := _QUOTE_MARKER.match(line, offset)):
        depth += 1
        offset = marker.end()
    return depth, line[offset:]


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
        in_comment = False
        for number, line in enumerate(self.prose):
            depth, unquoted = _unquote(line)
            fence = re.fullmatch(r" {0,3}(`{3,}|~{3,})(.*)", unquoted)
            if fence and not in_comment:
                self._read_fence(number, depth, *fence.groups())
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
            try:
                end = markers.index("</workflow-definition>", start)
            except ValueError:
                # Older prompts end their phase definitions at the required diagram.
                end = next((h.line for h in self.headings if h.line >= start and h.level <= 2
                            and h.title.casefold() == "workflow diagram"), start)
            self.phase_lines = range(start, end)

    def _read_fence(self, start: int, quote_depth: int, marker: str, language: str):
        closing = re.compile(rf" {{0,3}}{marker}{marker[0]}*[ \t]*")
        content = []
        self.prose[start] = ""
        for index in range(start + 1, len(self.prose)):
            depth, code = _unquote(self.prose[index], quote_depth)
            if depth < quote_depth:
                break  # The blockquote ended before the closing fence.
            self.prose[index] = ""
            if closing.fullmatch(code):
                if not quote_depth:
                    self.fences.append(CodeBlock(start, language.strip().casefold(), "\n".join(content)))
                break
            content.append(code)

    def section_end(self, heading: Heading, *stop_titles: str) -> int:
        for following in self.headings:
            if following.line > heading.line and (
                following.level <= heading.level or following.title.casefold() in stop_titles
            ):
                return following.line
        return len(self.prose)

    def section_fences(self, *titles: str):
        for heading in self.headings:
            if heading.title.casefold() in titles:
                end = self.section_end(heading)
                yield from (block for block in self.fences if heading.line < block.line < end)

    def phase_headings(self):
        headings = [h for h in self.headings if h.line in self.phase_lines and h.level in {2, 3}]
        role_workflow = any(h.level == 2 and _EXPLICIT_PHASE.fullmatch(h.title) for h in headings)
        for heading in headings:
            match = _EXPLICIT_PHASE.fullmatch(heading.title)
            if not match and heading.level == 3 and not role_workflow:
                match = _NUMBERED_PHASE.fullmatch(heading.title)
            if match:
                yield heading, int(match[1]), match[2]

    def instruction_paragraphs(self, heading: Heading, end: int):
        """Join wrapped prose within each paragraph or list item."""
        paragraph = []
        for line in self.prose[heading.line + 1:end]:
            text = line.strip().lstrip("> \t")
            if text.startswith("#") or text == "</workflow-definition>" or _THEMATIC_BREAK.fullmatch(text):
                text = ""
            markers = _LIST_MARKERS.match(text)
            if paragraph and (not text or markers):
                yield " ".join(paragraph)
                paragraph = []
            if markers:
                text = text[markers.end():]
            if text:
                paragraph.append(text)
        if paragraph:
            yield " ".join(paragraph)

    def phase_errors(self):
        phases = list(self.phase_headings())
        for expected, (_, number, name) in enumerate(phases, start=1):
            if number != expected:
                yield f"Expected phase {expected}, observed {number} ({name})"
                break

        end = self.phase_lines.stop
        for heading, number, name in reversed(phases):
            if not any(self.instruction_paragraphs(heading, min(end, self.section_end(heading)))):
                yield f"Phase {number} ({name}) has no instructions"
            end = heading.line

    def structure_errors(self):
        yield from self.phase_errors()
        for heading in self.headings:
            if heading.title.casefold() != "important execution instructions":
                continue
            # spec.toml places its notepad at H2 after the H1 execution instructions.
            end = self.section_end(heading, "0-notepad template", "notepad template")
            if not any(self.instruction_paragraphs(heading, end)):
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
