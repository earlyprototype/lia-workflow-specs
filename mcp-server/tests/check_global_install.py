"""Launch the global installer's generated config and read the index over stdio."""

import asyncio
import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from mcp import ClientSession, StdioServerParameters, stdio_client


async def check_install():
    config_path = Path(__file__).resolve().parents[1] / "config/generated-config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    entry = config["mcpServers"]["lia-workflow-specs"]
    assert Path(entry["command"]) == Path(sys.executable), entry["command"]
    specs_dir = Path(entry["env"]["LIA_SPECS_DIR"]).expanduser()
    assert specs_dir == Path.home() / ".lia" / "specs"
    assert (specs_dir / "development/dev.toml").is_file()

    with TemporaryDirectory() as project:
        os.environ["PATH"] = project
        params = StdioServerParameters(**entry, cwd=project)
        async with stdio_client(params) as streams, ClientSession(*streams) as client:
            await client.initialize()
            result = await client.read_resource("specs://index")
            assert result.contents[0].mimeType == "application/json"
            catalog = json.loads(result.contents[0].text)
            assert len(catalog["specs"]) == catalog["total_specs"] == 19
            resources = (await client.list_resources()).resources
            tools = (await client.list_tools()).tools
            prompts = (await client.list_prompts()).prompts
            assert len(resources) > 30
            assert len(tools) >= 10
            assert sum(p.name.startswith("start-") for p in prompts) == 19
            search = await client.call_tool("search_specs", {"query": "security"})
            assert not search.isError and "security" in search.content[0].text.lower()
            recommendation = await client.call_tool("recommend_workflow", {"task_description": "implement a feature"})
            assert not recommendation.isError and "dev" in recommendation.content[0].text.lower()
            print(f"Discovered {len(resources)} resources, {len(tools)} tools and {len(prompts)} prompts")


if __name__ == "__main__":
    asyncio.run(asyncio.wait_for(check_install(), timeout=30))
