#!/usr/bin/env python3
"""
Basic usage example for Lia Workflow Specs MCP Server.

This script demonstrates how to interact with the MCP server programmatically.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lia_workflow_mcp.server import (
    initialise_specs,
    list_resources,
    read_resource,
    list_tools,
    call_tool,
    list_prompts,
    get_prompt,
    spec_collection,
)


async def demo_resources():
    """Demonstrate resource access."""
    print("\n" + "=" * 60)
    print("RESOURCES")
    print("=" * 60)
    
    # List all resources
    resources = await list_resources()
    print(f"\nTotal resources available: {len(resources)}")
    print("\nFirst 10 resources:")
    for r in resources[:10]:
        print(f"  • {r.uri}")
        print(f"    {r.description[:50]}...")
    
    # Read the summary resource
    print("\n--- Reading specs://summary ---")
    summary = await read_resource("specs://summary")
    print(summary.text[:500] + "...")
    
    # Read a specific spec's metadata
    print("\n--- Reading specs://development/dev/metadata ---")
    metadata = await read_resource("specs://development/dev/metadata")
    print(metadata.text[:400] + "...")


async def demo_tools():
    """Demonstrate tool usage."""
    print("\n" + "=" * 60)
    print("TOOLS")
    print("=" * 60)
    
    # List all tools
    tools = await list_tools()
    print(f"\nTotal tools available: {len(tools)}")
    for t in tools:
        print(f"  • {t.name}: {t.description[:50]}...")
    
    # Search for specs
    print("\n--- Tool: search_specs('testing') ---")
    result = await call_tool("search_specs", {"query": "testing"})
    print(result[0].text)
    
    # Get recommendations
    print("\n--- Tool: recommend_workflow('fix a bug') ---")
    result = await call_tool("recommend_workflow", {
        "task_description": "I need to fix a bug in the authentication system"
    })
    print(result[0].text)
    
    # Get spec details
    print("\n--- Tool: get_spec_details('troubleshoot') ---")
    result = await call_tool("get_spec_details", {"spec_name": "troubleshoot"})
    print(result[0].text)
    
    # Get execution guide
    print("\n--- Tool: get_execution_guide('spec', 'collaboration') ---")
    result = await call_tool("get_execution_guide", {
        "spec_name": "spec",
        "mode": "collaboration"
    })
    print(result[0].text[:600] + "...")
    
    # Suggest workflow sequence
    print("\n--- Tool: suggest_workflow_sequence('build a new API') ---")
    result = await call_tool("suggest_workflow_sequence", {
        "task_description": "I need to build a new REST API with security review"
    })
    print(result[0].text)


async def demo_prompts():
    """Demonstrate prompt templates."""
    print("\n" + "=" * 60)
    print("PROMPTS")
    print("=" * 60)
    
    # List all prompts
    prompts = await list_prompts()
    print(f"\nTotal prompts available: {len(prompts)}")
    print("\nWorkflow starter prompts:")
    for p in prompts:
        if p.name.startswith("start-"):
            print(f"  • {p.name}: {p.description}")
    
    print("\nHelper prompts:")
    for p in prompts:
        if not p.name.startswith("start-"):
            print(f"  • {p.name}: {p.description}")
    
    # Get a specific prompt
    print("\n--- Prompt: choose-workflow ---")
    messages = await get_prompt("choose-workflow", {
        "task": "I need to refactor our database layer for better performance"
    })
    print(messages[0].content.text[:800] + "...")
    
    # Get a workflow starter prompt
    print("\n--- Prompt: start-dev ---")
    messages = await get_prompt("start-dev", {
        "task": "Implement user profile editing feature",
        "mode": "collaboration"
    })
    print(messages[0].content.text[:600] + "...")


async def demo_collection():
    """Demonstrate direct collection access."""
    print("\n" + "=" * 60)
    print("SPEC COLLECTION")
    print("=" * 60)
    
    print(f"\nTotal specs: {len(spec_collection.specs)}")
    
    print("\nCategories:")
    for cat, specs in sorted(spec_collection.get_categories().items()):
        print(f"  {cat}: {', '.join(sorted(specs))}")
    
    print("\nSearching for 'security':")
    results = spec_collection.search("security")
    for r in results:
        print(f"  • {r.name}: {r.description[:50]}...")
    
    print("\nRecommendations for 'implement new feature':")
    recs = spec_collection.recommend_for_task("implement new feature")
    for r in recs:
        print(f"  • {r.name} ({r.category.value})")


async def main():
    """Run all demos."""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║       Lia Workflow Specs MCP Server - Usage Examples         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    
    # Initialise specs
    specs_dir = os.environ.get("LIA_SPECS_DIR", str(Path(__file__).parent.parent.parent / "specs"))
    os.environ["LIA_SPECS_DIR"] = specs_dir
    print(f"\nLoading specs from: {specs_dir}")
    initialise_specs()
    print(f"Loaded {len(spec_collection.specs)} specs")
    
    # Run demos
    await demo_collection()
    await demo_resources()
    await demo_tools()
    await demo_prompts()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
