#!/usr/bin/env python3
"""
Interactive workflow starter example.

This script demonstrates how to use the MCP server to help users
choose and start a workflow interactively.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lia_workflow_mcp.server import (
    initialise_specs,
    call_tool,
    get_prompt,
    spec_collection,
)


def print_header():
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║            Lia Workflow Specs - Interactive Starter          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()


def print_menu():
    print("\nWhat would you like to do?")
    print()
    print("  1. Describe a task and get workflow recommendations")
    print("  2. Browse workflows by category")
    print("  3. Start a specific workflow")
    print("  4. Plan a workflow sequence for a project")
    print("  5. Exit")
    print()


async def task_recommendations():
    """Get workflow recommendations based on task description."""
    print("\nDescribe your task:")
    task = input("> ").strip()
    
    if not task:
        print("No task provided.")
        return
    
    result = await call_tool("recommend_workflow", {"task_description": task})
    print("\n" + result[0].text)
    
    print("\nWould you like to start one of these workflows? (Enter number or 'n'):")
    choice = input("> ").strip()
    
    if choice.isdigit():
        # Extract workflow name from recommendations
        recommendations = spec_collection.recommend_for_task(task)
        idx = int(choice) - 1
        if 0 <= idx < len(recommendations):
            await start_workflow(recommendations[idx].name, task)


async def browse_categories():
    """Browse workflows by category."""
    categories = spec_collection.get_categories()
    
    print("\nCategories:")
    for i, (cat, specs) in enumerate(sorted(categories.items()), 1):
        print(f"  {i}. {cat} ({len(specs)} workflows)")
    
    print("\nSelect a category (number):")
    choice = input("> ").strip()
    
    if not choice.isdigit():
        return
    
    idx = int(choice) - 1
    cat_list = sorted(categories.items())
    
    if 0 <= idx < len(cat_list):
        cat_name, spec_names = cat_list[idx]
        result = await call_tool("list_specs_by_category", {"category": cat_name})
        print("\n" + result[0].text)
        
        print("\nWould you like details on a specific workflow? (Enter name or 'n'):")
        spec_name = input("> ").strip()
        
        if spec_name and spec_name != 'n':
            result = await call_tool("get_spec_details", {"spec_name": spec_name})
            print("\n" + result[0].text)


async def start_workflow(spec_name: str = None, task: str = None):
    """Start a specific workflow."""
    if not spec_name:
        print("\nAvailable workflows:")
        for spec in sorted(spec_collection.specs, key=lambda s: s.name):
            print(f"  • {spec.name}")
        
        print("\nEnter workflow name:")
        spec_name = input("> ").strip()
    
    spec = spec_collection.get_by_name(spec_name)
    if not spec:
        print(f"Workflow '{spec_name}' not found.")
        return
    
    if not task:
        print(f"\nDescribe your task for the {spec_name} workflow:")
        task = input("> ").strip()
    
    print("\nExecution mode:")
    print("  1. Collaboration (interactive, with approval gates)")
    print("  2. Silent (autonomous execution)")
    mode_choice = input("> ").strip()
    mode = "silent" if mode_choice == "2" else "collaboration"
    
    # Get the workflow prompt
    messages = await get_prompt(f"start-{spec_name}", {
        "task": task,
        "mode": mode,
    })
    
    print("\n" + "=" * 60)
    print(f"STARTING {spec_name.upper()} WORKFLOW")
    print("=" * 60)
    print(f"\nTask: {task}")
    print(f"Mode: {mode}")
    print("\n--- Workflow Prompt ---")
    print(messages[0].content.text[:2000])
    if len(messages[0].content.text) > 2000:
        print("\n... (truncated, full prompt available via MCP)")
    
    print("\n--- End of Prompt ---")
    print("\nCopy this prompt to your AI assistant to begin the workflow.")


async def plan_sequence():
    """Plan a workflow sequence for a complex project."""
    print("\nDescribe your project or complex task:")
    project = input("> ").strip()
    
    if not project:
        print("No project description provided.")
        return
    
    result = await call_tool("suggest_workflow_sequence", {"task_description": project})
    print("\n" + result[0].text)
    
    # Get full planning prompt
    messages = await get_prompt("workflow-sequence", {"project": project})
    
    print("\n--- Full Planning Prompt ---")
    print(messages[0].content.text[:1500])
    print("\n... (use this prompt with your AI assistant for detailed planning)")


async def main():
    """Main interactive loop."""
    # Initialise
    specs_dir = os.environ.get("LIA_SPECS_DIR", str(Path(__file__).parent.parent.parent / "specs"))
    os.environ["LIA_SPECS_DIR"] = specs_dir
    initialise_specs()
    
    print_header()
    print(f"Loaded {len(spec_collection.specs)} workflow specs from {specs_dir}")
    
    while True:
        print_menu()
        choice = input("Select option: ").strip()
        
        if choice == "1":
            await task_recommendations()
        elif choice == "2":
            await browse_categories()
        elif choice == "3":
            await start_workflow()
        elif choice == "4":
            await plan_sequence()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    asyncio.run(main())
