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


@pytest.mark.parametrize("workflow, heading, next_heading, number", [
    ("development/dev.toml", "### 1.", "### 2.", 1),
    ("research/recon.toml", "## PHASE 2:", "## PHASE 3:", 2),
])
def test_each_declared_phase_needs_instructions(global_install, workflow, heading, next_heading, number):
    path = global_install / workflow
    text = path.read_text(encoding="utf-8")
    start = text.index("\n", text.index("\n" + heading) + 1)
    end = text.index("\n" + next_heading, start)
    path.write_text(text[:start] + "\n\n```text\nExample only\n```\n" + text[end:], encoding="utf-8")

    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 1, result.stdout
    diagnostic = next(line.lower() for line in result.stdout.splitlines() if path.name in line)
    assert f"phase {number}" in diagnostic and "instruction" in diagnostic


def replace_final_phase(catalog, phase):
    path = catalog / "development/spec.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("### 3. Create Task List")
    end = text.index("## Troubleshooting", start)
    if phase is None:
        text = text.replace("### Design Complexity", "### 3. Design Complexity", 1)
        phase = ""
    path.write_text(text[:start] + phase + "\n\n" + text[end:], encoding="utf-8")
    return path


@pytest.mark.parametrize("phase", [
    pytest.param("", id="removed"),
    pytest.param(None, id="numbered-troubleshooting"),
    pytest.param("### 3. Publish Design\nSend the design for review.", id="unrelated-phase"),
    pytest.param("### 3. Publish Design\nSend the design and the existing 3-tasks.md.", id="unrelated-delivery"),
    pytest.param("### 3. Create Task List\nRead the existing 3-tasks.md.", id="input-only"),
    pytest.param("### 3. Create Task List\nCreate a release summary using the existing 3-tasks.md as input.",
                 id="summary-from-task-list"),
    pytest.param("### 3. Create Task List\nWrite a summary using the checklist in `3-tasks.md`.",
                 id="checklist-as-source"),
    pytest.param("### 3. Create Task List\nWrite 2-design.md using the existing 3-tasks.md as input.",
                 id="write-design"),
    pytest.param("### 3. Create Task List\nDo not write 3-tasks.md.", id="prohibited-write"),
    pytest.param("### 3. Create Task List\nDo not write the task list to a file named `3-tasks.md`.",
                 id="prohibited-named-file"),
    pytest.param("### 3. Create Task List\nWrite the task list using a file named `3-tasks.md`.",
                 id="named-input-file"),
    pytest.param("### 3. Create Task List\n- The model MUST NOT\n  create `3-tasks.md`.", id="wrapped-prohibition"),
    pytest.param("### 3. Create Task List\n- Write the task list to\n- `3-tasks.md` is an input.", id="separate-bullets"),
    pytest.param("### 3. Create Task List\nWrite tasks to 3-tasks.md.bak.", id="wrong-file"),
    pytest.param("### 3. Create Task List\nWrite `3-tasks.md backup`.", id="quoted-wrong-file"),
    pytest.param("### 3. Create Task List\nReview the design.\n<!-- Write 3-tasks.md. -->", id="comment"),
    pytest.param("### 3. Create Task List\nWrite 3-tasks.md.\n### 4. Publish Design\nSend the design.", id="not-final"),
])
def test_catalog_requires_walkthrough_task_list_phase(global_install, phase):
    path = replace_final_phase(global_install, phase)

    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 1, result.stdout
    assert any(path.name in line and "phase 3" in line.lower() and "3-tasks.md" in line
               for line in result.stdout.splitlines()), result.stdout


@pytest.mark.parametrize("target", ["file", "directory", "standalone"])
def test_installed_copy_requires_walkthrough_task_list_phase(global_install, tmp_path, target):
    path = replace_final_phase(global_install, "")
    if target == "standalone":
        path = shutil.copyfile(path, tmp_path / path.name)
    result = validate(global_install if target == "directory" else path, "-q")
    assert result.returncode == 1, result.stdout
    assert any(path.name in line and "phase 3" in line.lower() and "3-tasks.md" in line
               for line in result.stdout.splitlines()), result.stdout


def test_unrelated_standalone_workflow_can_use_spec_filename(tmp_path):
    path = tmp_path / "spec.toml"
    shutil.copyfile(ROOT / "specs/quality/architecture.toml", path)
    result = validate(path, "-q")
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("instruction", [
    "Write\n`3-tasks.md`.",
    "Write the implementation tasks to\n`3-tasks.md`.",
    "- The model MUST save the task list to\n  `.lia/specs/{feature_name}/3-tasks.md`.",
    "Write a numbered checklist to `3-tasks.md`.",
    pytest.param("Write the task list to a file named `3-tasks.md`.", id="named-file"),
    "Save the prioritized implementation tasks in `3-tasks.md`.",
    "**Output:** `3-tasks.md`",
    "__Deliverable__: `3-tasks.md`",
])
def test_catalog_accepts_task_list_destination(global_install, instruction):
    replace_final_phase(global_install, "### 3. Create Task List\n" + instruction)
    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("workflow, following, body, valid", [
    ("strategy/innovate", "## Innovation Techniques and Methods", "", False),
    ("strategy/innovate", "## Innovation Techniques and Methods", "<!-- draft -->\n```text\nExample instructions\n```", False),
    ("strategy/innovate", "## Innovation Techniques and Methods", "***", False),
    ("strategy/innovate", "## Innovation Techniques and Methods", "  _ _ _\n- - - -", False),
    ("strategy/innovate", "## Innovation Techniques and Methods", "- [ ]", False),
    ("strategy/innovate", "## Innovation Techniques and Methods", ">", False),
    pytest.param("strategy/innovate", "## Innovation Techniques and Methods",
                 "> ```\n> ```", False, id="empty-quoted-fence"),
    pytest.param("strategy/innovate", "## Innovation Techniques and Methods",
                 "> > ~~~~text\n> > Example only.\n> > ~~~~", False, id="nested-quoted-fence"),
    pytest.param("strategy/innovate", "## Innovation Techniques and Methods",
                 "> ```text\n> Example only.\n\nAsk for feedback.", True, id="instruction-after-quote"),
    ("strategy/innovate", "## Innovation Techniques and Methods", "> Ask for feedback.", True),
    ("strategy/innovate", "## Innovation Techniques and Methods", "-\n*\n+\n1.\n2) [x]", False),
    ("strategy/innovate", "## Innovation Techniques and Methods", "### Collaboration Mode\nAsk for feedback.", True),
    ("development/dev", "## 0-Notepad Template", "", False),
    ("development/spec", "## 0-Notepad Template", "", False),
    ("development/spec", "## 0-Notepad Template", "## Collaboration Mode\nAsk the user to approve each document.", True),
])
def test_catalog_requires_execution_instructions(global_install, workflow, following, body, valid):
    path = global_install / f"{workflow}.toml"
    text = path.read_text(encoding="utf-8")
    heading = re.search(r"^#+ Important Execution Instructions$", text, re.IGNORECASE | re.MULTILINE)
    assert heading
    start = heading.end()
    end = text.index(following, start)
    path.write_text(text[:start] + f"\n{body}\n" + text[end:], encoding="utf-8")

    result = validate(global_install, "--catalog", "-q")
    if valid:
        assert result.returncode == 0, result.stdout
        return
    assert result.returncode == 1, result.stdout
    assert any(path.name in line and "execution instructions" in line.lower()
               and "add" in line.lower() for line in result.stdout.splitlines()), result.stdout


@pytest.mark.asyncio
@pytest.mark.parametrize("closed", [True, False], ids=["closed", "unclosed"])
async def test_numbered_technique_after_definition_is_not_a_phase(global_install, closed):
    path = global_install / "strategy/innovate.toml"
    text = path.read_text(encoding="utf-8")
    heading = "### Creative Thinking Approaches"
    assert text.index(heading) > text.index("</workflow-definition>")
    if not closed:
        text = text.replace("</workflow-definition>", "")
    number = 1 if closed else 6
    path.write_text(text.replace(heading, f"### {number}. Creative Thinking Approaches"), encoding="utf-8")

    server.initialise_specs()
    phases, = await server.call_tool("get_workflow_phases", {"spec_name": "innovate"})
    assert re.findall(r"^(\d+)\. ", phases.text, re.MULTILINE) == list("12345")
    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("workflow, heading, following, replacement, expected, observed", [
    ("knowledge/docs.toml", "### 3.", "### 4.", None, 3, 4),
    ("knowledge/docs.toml", "### 3.", "### 4.", "### 2.", 3, 2),
    ("development/dev.toml", "### 1.", "### 2.", "### 0.", 1, 0),
    ("research/recon.toml", "## PHASE 2:", "## PHASE 3:", "## PHASE 3:", 2, 3),
])
def test_catalog_reports_phase_number_out_of_sequence(
    global_install, workflow, heading, following, replacement, expected, observed
):
    path = global_install / workflow
    text = path.read_text(encoding="utf-8")
    start = text.index(heading)
    if replacement is None:
        text = text[:start] + text[text.index(following, start):]
    else:
        text = text.replace(heading, replacement, 1)
    path.write_text(text, encoding="utf-8")

    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 1, result.stdout
    assert any(path.name in line and f"expected phase {expected}" in line.lower()
               and f"observed {observed}" in line.lower() for line in result.stdout.splitlines())


@pytest.mark.parametrize("body, valid", [
    ("<!-- Implementation instructions go here. -->", False),
    ("<!-- Draft instructions\n### 9. Example phase\nImplement it.\n-->", False),
    ("<!-- Draft\nnotes --> Implement the feature. <!-- End of note -->", True),
    ("Remove the literal `<!--` marker.", True),
])
def test_phase_body_excludes_html_comments(global_install, body, valid):
    path = global_install / "development/dev.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("\n", text.index("### 3. Implementation"))
    end = text.index("### 4.", start)
    path.write_text(text[:start] + f"\n{body}\n" + text[end:], encoding="utf-8")
    result = validate(path, "-q")
    if valid:
        assert result.returncode == 0, result.stdout
    else:
        assert result.returncode == 1, result.stdout
        assert any(path.name in line and "Phase 3" in line and "no instructions" in line
                   for line in result.stdout.splitlines())


@pytest.mark.parametrize("workflow, introduction", [
    ("development/dev.toml", "## Your Role\nGuide the implementation."),
    ("research/recon.toml", "## Goal\nSurvey the project landscape."),
])
def test_optional_introduction_preserves_phase_format(global_install, workflow, introduction):
    path = global_install / workflow
    text = path.read_text(encoding="utf-8")
    start = text.index("\n## ")
    path.write_text(text[:start] + f"\n{introduction}\n" + text[start:], encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 0, result.stdout


def test_numbered_subheading_in_role_phase_is_a_task(global_install):
    path = global_install / "research/recon.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("### Tasks", text.index("## PHASE 1:"))
    text = text[:start] + text[start:].replace("### Tasks", "### 1. Scope the search", 1)
    path.write_text(text, encoding="utf-8")
    server.initialise_specs()
    recon = server.spec_collection.get_by_name("recon")
    assert [phase.number for phase in recon.phases] == [1, 2, 3, 4, 5, 6]
    result = validate(path, "-q")
    assert result.returncode == 0, result.stdout


@pytest.mark.asyncio
async def test_numbered_role_deliverable_is_not_a_phase(global_install):
    path = global_install / "research/recon.toml"
    text = path.read_text(encoding="utf-8")
    heading = "### landscape-analysis.md"
    assert text.index(heading) > text.index("## PHASE 6:")
    path.write_text(text.replace(heading, "### 1. landscape-analysis.md"), encoding="utf-8")

    server.initialise_specs()
    phases, = await server.call_tool("get_workflow_phases", {"spec_name": "recon"})
    assert re.findall(r"^(\d+)\. ", phases.text, re.MULTILINE) == list("123456")
    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 0, result.stdout


def test_nested_phase_cannot_supply_its_parent_instructions(global_install):
    path = global_install / "research/recon.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("\n", text.index("## PHASE 1:"))
    end = text.index("## PHASE 2:", start)
    path.write_text(text[:start] + "\n\n#" + text[end:], encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 1, result.stdout
    assert any(path.name in line and "Phase 1" in line and "no instructions" in line
               for line in result.stdout.splitlines())


@pytest.mark.asyncio
async def test_contributor_phase_headings_are_discoverable(global_install):
    path = global_install / "development/dev.toml"
    text = path.read_text(encoding="utf-8")
    text, count = re.subn(r"^### (\d+)\. ", r"### Phase \1: ", text, flags=re.MULTILINE)
    assert count == 7
    path.write_text(text, encoding="utf-8")

    server.initialise_specs()
    phases = await server.call_tool("get_workflow_phases", {"spec_name": "dev"})
    assert re.findall(r"^(\d+)\. ", phases[0].text, re.MULTILINE) == list("1234567")
    result = validate(path, "-q")
    assert result.returncode == 0, result.stdout


@pytest.mark.parametrize("field, value", [("metadata", "17"), ("config.resumable", '"yes"')])
def test_catalog_reports_schema_field(global_install, field, value):
    path = global_install / "development/dev.toml"
    text = path.read_text(encoding="utf-8")
    path.write_text(f"{field} = {value}\n" + text, encoding="utf-8")
    result = validate(global_install, "--catalog", "-q")
    assert result.returncode == 1, result.stdout
    assert any(path.name in line and field in line for line in result.stdout.splitlines())


@pytest.mark.parametrize("replacement", [
    "",
    "```mermaid\n   \n```",
    "```mermaid\ngraph TD\n%% phases pending\n```",
    "```mermaid\nsequenceDiagram\n```",
    "```mermaid\ngraph TD\nclassDef step fill:#fff\n```",
    "```mermaid\ngraph TD; style A fill:#fff\n```",
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


def test_mermaid_accepts_declared_workflow_elements():
    diagrams = [
        "graph TD; Plan; style Plan fill:#fff",
        "sequenceDiagram\n  User->>Lia: Start",
        'stateDiagram-v2\n  state "Plan the work" as Plan',
        "journey\n  section Review\n    Check requirements: 5: Team",
    ]
    result = subprocess.run(
        ["node", str(ROOT / "tools/parse-mermaid.mjs")], input=json.dumps(diagrams),
        capture_output=True, encoding="utf-8", check=True,
    )
    assert json.loads(result.stdout) == [None] * len(diagrams)


@pytest.mark.asyncio
async def test_mcp_reports_scope_for_unparsed_mermaid(global_install):
    path = global_install / "development/dev.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("graph TD", text.index("## Workflow Diagram"))
    end = text.index("\n```", start)
    path.write_text(text[:start] + "graph TD\n  A --> B[unfinished" + text[end:], encoding="utf-8")

    server.initialise_specs()
    report, = await server.call_tool("validate_spec", {"spec_name": "dev"})
    assert "VALID" not in report.text
    assert "Mermaid syntax" in report.text and "tools/spec-validator.py" in report.text
    result = validate(path, "-q")
    assert result.returncode == 1
    assert "Invalid Mermaid" in result.stdout


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


def test_accepts_shipped_base_notepad(global_install):
    base = (ROOT / "templates/base-workflow.toml").read_text(encoding="utf-8")
    start = base.index("# ```markdown", base.index("# NOTEPAD TEMPLATE"))
    end = base.index("\n# ```", start) + len("\n# ```")
    notepad = "\n".join(line[1:].removeprefix(" ") for line in base[start:end].splitlines())

    path = global_install / "development/dev.toml"
    text = path.read_text(encoding="utf-8")
    start = text.index("```markdown", text.index("## 0-Notepad Template"))
    end = text.index("\n```", start) + len("\n```")
    path.write_text(text[:start] + notepad + text[end:], encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 0, result.stdout


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
