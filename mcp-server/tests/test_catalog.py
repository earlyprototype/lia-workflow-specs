"""Offline checks for the published catalog and its two entry points."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from lia_workflow_mcp import server
from lia_workflow_mcp.models import SpecCollection
from mcp.shared.memory import create_connected_server_and_client_session

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def global_install(tmp_path, monkeypatch):
    home = tmp_path / "home"
    specs_dir = home / ".lia" / "specs"
    shutil.copytree(ROOT / "specs", specs_dir)
    project = tmp_path / "unrelated-project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.setenv("LIA_SPECS_DIR", "~/.lia/specs")
    monkeypatch.setattr(server, "spec_collection", SpecCollection())
    monkeypatch.setattr(server, "trigger_manager", None)
    return specs_dir


@pytest.mark.asyncio
async def test_global_install_serves_readme_catalog(global_install):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    advertised = set(re.findall(r"^([a-z-]+)\.toml\s+#", readme, re.MULTILINE))
    server.initialise_specs()
    async with create_connected_server_and_client_session(server.server) as client:
        index = await client.read_resource("specs://index")
        catalog = json.loads(index.contents[0].text)
        assert catalog["total_specs"] == len(advertised) == 19
        assert {item["name"] for item in catalog["specs"]} == advertised
        for item in catalog["specs"]:
            uri = f"specs://{item['category']}/{item['name']}"
            assert item["filepath"] == uri
            metadata = await client.read_resource(f"{uri}/metadata")
            assert json.loads(metadata.contents[0].text)["filepath"] == uri
            resource = await client.read_resource(uri)
            assert resource.contents[0].text.strip(), item["name"]
            starter = await client.get_prompt(f"start-{item['name']}", {"task": "Offline example"})
            assert resource.contents[0].text in starter.messages[0].content.text


@pytest.mark.parametrize("kind", ["missing", "file", "empty"])
def test_invalid_explicit_path_reports_remedy(global_install, monkeypatch, kind):
    path = global_install.parent / "wrong"
    if kind == "file":
        path.touch()
    if kind == "empty":
        path.mkdir()
    monkeypatch.setenv("LIA_SPECS_DIR", "~/.lia/wrong")
    with pytest.raises(ValueError) as exc:
        server.initialise_specs()
    assert str(path) in str(exc.value)
    assert "LIA_SPECS_DIR" in str(exc.value)
    assert "specs" in str(exc.value)


def validate(*args):
    return subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / "tools/spec-validator.py"), *args],
        cwd=ROOT, capture_output=True, encoding="utf-8", check=False,
    )


def test_unresolvable_home_reports_supplied_setting(global_install, monkeypatch):
    def missing_home(path):
        raise RuntimeError("Could not determine home directory.")

    monkeypatch.setattr(Path, "expanduser", missing_home)
    with pytest.raises(SystemExit) as error:
        server.main()
    assert "~/.lia/specs" in str(error.value)
    assert "LIA_SPECS_DIR" in str(error.value)
    assert "absolute" in str(error.value)


@pytest.mark.parametrize("workflow, first, end, example", [
    ("development/dev.toml", "### 1. Task Analysis", "## Workflow Diagram", "### 1. Sample"),
    ("research/recon.toml", "## PHASE 1: DEFINE", "## FINAL DELIVERABLE", "## PHASE 1: SAMPLE"),
])
def test_fenced_phase_cannot_replace_executable_phases(global_install, workflow, first, end, example):
    path = global_install / workflow
    text = path.read_text(encoding="utf-8")
    start = text.index(first)
    text = text[:start] + f"~~~~markdown\n{example}\nExample instructions.\n~~~~\n" + text[text.index(end, start):]
    path.write_text(text, encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 1 and path.name in result.stdout
    assert "phase" in result.stdout.lower()


def test_fenced_example_cannot_supply_goal(global_install):
    path = global_install / "development/dev.toml"
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("\n## Goal\n", "\n````markdown\n```\n## Goal\n````\n"), encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 1 and path.name in result.stdout
    assert "Goal" in result.stdout


@pytest.mark.parametrize("replacement", [
    "",
    "```mermaid\n   \n```",
    "```mermaid\ngraph TD\n%% phases pending\n```",
    "```mermaid\ngraph TD\n    B --> [*] : Update\n```",
    "```mermaid\ngraph LR\n    A --> B[unfinished\n```",
])
def test_diagram_must_parse_in_its_own_section(global_install, replacement):
    path = global_install / "strategy/innovate.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("```mermaid", text.index("## Workflow Diagram"))
    end = text.index("\n```", start) + len("\n```")
    example = "\n## Unrelated example\n```mermaid\ngraph LR\n    A --> B\n```\n"
    path.write_text(text[:start] + replacement + example + text[end:], encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 1 and path.name in result.stdout
    assert "diagram" in result.stdout.lower()


def test_unrelated_notepad_headings_rejected(global_install):
    path = global_install / "development/dev.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("```markdown", text.index("## 0-Notepad Template"))
    end = text.index("\n```", start)
    checklist = "```markdown\n## Release\n## Build\n## Sign\n## Publish\n## Notify"
    path.write_text(text[:start] + checklist + text[end:], encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 1 and path.name in result.stdout
    assert "USER NOTES" in result.stdout.upper()


def test_walkthrough_tasks_link_to_their_requirements():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    example = ROOT / "examples/feature-spec-example"
    assert f"]({example.relative_to(ROOT).as_posix()}/)" in readme
    walkthrough = (example / "README.md").read_text(encoding="utf-8")
    for artifact in ("0-notepad.md", "1-requirements.md", "2-design.md", "3-tasks.md"):
        assert f"]({artifact})" in walkthrough
        assert (example / artifact).read_text(encoding="utf-8").strip()

    requirements = (example / "1-requirements.md").read_text(encoding="utf-8")
    headings = re.findall(r"^### (Requirement \d+: .+)$", requirements, re.MULTILINE)
    anchors = {re.sub(r"[^\w -]", "", h.lower()).replace(" ", "-") for h in headings}
    tasks = (example / "3-tasks.md").read_text(encoding="utf-8")
    rows = [line for line in tasks.splitlines() if line.startswith("- [ ] ")]
    assert len(rows) == 18
    for row in rows:
        references = re.findall(r"\[([^\]]+)\]\(1-requirements\.md#([^)]+)\)", row)
        assert references, row
        for label, anchor in references:
            assert anchor in anchors
            numbers = re.findall(r"(\d+)\.\d+", label)
            assert numbers and all(anchor.startswith(f"requirement-{n}-") for n in numbers)


def test_validate_shipped_catalog():
    result = validate("specs", "-q")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Total files: 19" in result.stdout


def test_catalog_rejects_substitution_at_same_count(global_install):
    workflow = global_install / "research" / "recon.toml"
    workflow.rename(workflow.with_name("substitute.toml"))
    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 1
    assert "recon.toml" in result.stdout
    assert "substitute.toml" in result.stdout


@pytest.mark.parametrize("workflow", ["quality/constitution.toml", "research/recon.toml"])
def test_later_example_cannot_replace_notepad_template(global_install, workflow):
    path = global_install / workflow
    text = path.read_text(encoding="utf-8")
    heading = text.index("## NOTEPAD TEMPLATE")
    start = text.index("```markdown", heading)
    end = text.index("\n```", start) + len("\n```")
    assert "```markdown" in text[end:]
    path.write_text(text[:start] + text[end:], encoding="utf-8")

    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 1
    assert path.name in result.stdout
    assert "Notepad template incomplete" in result.stdout


@pytest.mark.parametrize("workflow", ["development/dev.toml", "quality/constitution.toml"])
@pytest.mark.parametrize("length, exit_code", [(19, 1), (20, 0)])
def test_description_minimum_length(global_install, workflow, length, exit_code):
    path = global_install / workflow
    text = path.read_text(encoding="utf-8")
    description = "x" * length
    text, count = re.subn(r'^description = ".*"$', f'description = "{description}"',
                          text, count=1, flags=re.MULTILINE)
    assert count == 1
    path.write_text(text, encoding="utf-8")

    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == exit_code, result.stdout
    if exit_code:
        assert path.name in result.stdout
        assert "description" in result.stdout.lower()
        assert "20" in result.stdout


@pytest.mark.parametrize("prompt", ['"   "', '[]', '{content = 12}', '"Only a title"'])
def test_malformed_prompt_has_file_diagnostic(tmp_path, prompt):
    path = tmp_path / "broken.toml"
    path.write_text(f'description = "Example workflow description"\nprompt = {prompt}', encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 1
    assert "broken.toml" in result.stdout
    assert "prompt" in result.stdout.lower() or "section" in result.stdout.lower()
    assert "Traceback" not in result.stderr
