"""Offline checks for the published catalog and its two entry points."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from mcp.shared.memory import create_connected_server_and_client_session

from lia_workflow_mcp import server
from lia_workflow_mcp.models import SpecCollection


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
            resource = await client.read_resource(f"specs://{item['category']}/{item['name']}")
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
        cwd=ROOT, capture_output=True, encoding="utf-8",
    )


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


@pytest.mark.parametrize("prompt", ['"   "', '[]', '{content = 12}', '"Only a title"'])
def test_malformed_prompt_has_file_diagnostic(tmp_path, prompt):
    path = tmp_path / "broken.toml"
    path.write_text(f'description = "Example workflow description"\nprompt = {prompt}', encoding="utf-8")
    result = validate(path, "-q")
    assert result.returncode == 1
    assert "broken.toml" in result.stdout
    assert "prompt" in result.stdout.lower() or "section" in result.stdout.lower()
    assert "Traceback" not in result.stderr
