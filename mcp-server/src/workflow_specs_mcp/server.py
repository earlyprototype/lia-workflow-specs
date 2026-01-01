"""
Workflow Specs MCP Server

MCP server implementation providing remote agent access to Lia Workflow Specifications.
Exposes resources for reading specs and tools for validation, search, and metadata.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)

from .spec_loader import SpecLoader

# Default specs directory - can be overridden via environment variable
DEFAULT_SPECS_DIR = Path(__file__).parent.parent.parent.parent / "specs"
SPECS_DIR = Path(os.environ.get("WORKFLOW_SPECS_DIR", DEFAULT_SPECS_DIR))

# Create the MCP server
server = Server("workflow-specs-mcp")

# Initialise spec loader
spec_loader = SpecLoader(SPECS_DIR)


# =============================================================================
# RESOURCES - For reading and listing specs
# =============================================================================


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List all available workflow spec resources."""
    resources = []

    # Add a resource for the specs catalogue
    resources.append(
        Resource(
            uri="specs://catalogue",
            name="Workflow Specs Catalogue",
            description="Complete catalogue of all available workflow specifications organised by category",
            mimeType="application/json",
        )
    )

    # Add resources for each category
    for category in spec_loader.get_categories():
        resources.append(
            Resource(
                uri=f"specs://category/{category}",
                name=f"Category: {category}",
                description=f"All workflow specs in the '{category}' category",
                mimeType="application/json",
            )
        )

    # Add resources for each individual spec
    for spec_path in spec_loader.discover_specs():
        metadata = spec_loader.extract_metadata(spec_path)
        if metadata:
            resources.append(
                Resource(
                    uri=f"specs://spec/{metadata.category}/{metadata.name}",
                    name=f"{metadata.name}.toml",
                    description=metadata.description[:200] if metadata.description else "",
                    mimeType="text/plain",
                )
            )

    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific workflow spec resource."""
    # Parse the URI
    if uri == "specs://catalogue":
        # Return full catalogue
        catalogue = spec_loader.get_specs_by_category()
        result = {}
        for category, specs in catalogue.items():
            result[category] = [
                {
                    "name": s.name,
                    "description": s.description,
                    "phases": s.phases,
                    "modes": s.modes,
                    "output_directory": s.output_directory,
                }
                for s in specs
            ]
        return json.dumps(result, indent=2)

    if uri.startswith("specs://category/"):
        # Return specs for a specific category
        category = uri.replace("specs://category/", "")
        specs_by_category = spec_loader.get_specs_by_category()
        if category in specs_by_category:
            specs = specs_by_category[category]
            result = [
                {
                    "name": s.name,
                    "description": s.description,
                    "path": s.path,
                    "phases": s.phases,
                    "constraints": s.constraints,
                    "modes": s.modes,
                }
                for s in specs
            ]
            return json.dumps(result, indent=2)
        return json.dumps({"error": f"Category '{category}' not found"})

    if uri.startswith("specs://spec/"):
        # Return a specific spec's content
        parts = uri.replace("specs://spec/", "").split("/")
        if len(parts) == 2:
            category, name = parts
            spec_path = SPECS_DIR / category / f"{name}.toml"
            content = spec_loader.get_spec_content(spec_path)
            if content:
                return content
        return f"Spec not found: {uri}"

    return f"Unknown resource: {uri}"


# =============================================================================
# TOOLS - For operations on specs
# =============================================================================


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools for working with workflow specs."""
    return [
        Tool(
            name="list_specs",
            description="List all available workflow specifications with their categories and basic metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Optional: Filter by category (development, quality, research, etc.)",
                    }
                },
            },
        ),
        Tool(
            name="get_spec",
            description="Get the full content and metadata of a specific workflow specification",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the spec (e.g., 'dev', 'spec', 'review')",
                    },
                    "category": {
                        "type": "string",
                        "description": "Category of the spec (e.g., 'development', 'quality')",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="get_spec_prompt",
            description="Get only the prompt content from a workflow specification (the actual instructions)",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the spec",
                    },
                    "category": {
                        "type": "string",
                        "description": "Category of the spec",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="validate_spec",
            description="Validate a workflow specification for correctness and completeness",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the spec to validate",
                    },
                    "category": {
                        "type": "string",
                        "description": "Category of the spec",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="search_specs",
            description="Search workflow specifications by keyword in name, description, or content",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional: Limit search to a specific category",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_spec_metadata",
            description="Get metadata about a specification including phases, constraints count, and structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the spec",
                    },
                    "category": {
                        "type": "string",
                        "description": "Category of the spec",
                    },
                },
                "required": ["name"],
            },
        ),
        Tool(
            name="get_categories",
            description="Get all available workflow spec categories",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="compare_specs",
            description="Compare two workflow specifications, showing their differences in structure and capabilities",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec1_name": {
                        "type": "string",
                        "description": "Name of the first spec",
                    },
                    "spec1_category": {
                        "type": "string",
                        "description": "Category of the first spec",
                    },
                    "spec2_name": {
                        "type": "string",
                        "description": "Name of the second spec",
                    },
                    "spec2_category": {
                        "type": "string",
                        "description": "Category of the second spec",
                    },
                },
                "required": ["spec1_name", "spec2_name"],
            },
        ),
        Tool(
            name="suggest_workflow",
            description="Suggest the most appropriate workflow specification based on a task description",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "Description of the task you want to accomplish",
                    }
                },
                "required": ["task_description"],
            },
        ),
        Tool(
            name="get_workflow_chain",
            description="Get the recommended workflow chain starting from a spec, showing what comes next",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_spec": {
                        "type": "string",
                        "description": "Name of the starting spec (e.g., 'spec', 'research')",
                    },
                    "depth": {
                        "type": "integer",
                        "description": "How many steps to show in the chain (default: 3)",
                    }
                },
                "required": ["start_spec"],
            },
        ),
        Tool(
            name="find_specs_that_provide",
            description="Find specs that provide a specific output (e.g., 'requirements.md', 'test_suite')",
            inputSchema={
                "type": "object",
                "properties": {
                    "output": {
                        "type": "string",
                        "description": "The output to search for",
                    }
                },
                "required": ["output"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls."""

    if name == "list_specs":
        category = arguments.get("category")
        specs_by_cat = spec_loader.get_specs_by_category()

        if category:
            if category in specs_by_cat:
                specs = specs_by_cat[category]
                result = {
                    "category": category,
                    "specs": [{"name": s.name, "description": s.description} for s in specs],
                }
            else:
                result = {"error": f"Category '{category}' not found"}
        else:
            result = {}
            for cat, specs in specs_by_cat.items():
                result[cat] = [{"name": s.name, "description": s.description} for s in specs]

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    if name == "get_spec":
        spec_name = arguments.get("name")
        category = arguments.get("category")

        spec_path = _find_spec(spec_name, category)
        if spec_path:
            content = spec_loader.get_spec_content(spec_path)
            if content:
                return [TextContent(type="text", text=content)]
        return [TextContent(type="text", text=f"Spec '{spec_name}' not found")]

    if name == "get_spec_prompt":
        spec_name = arguments.get("name")
        category = arguments.get("category")

        spec_path = _find_spec(spec_name, category)
        if spec_path:
            data = spec_loader.load_spec(spec_path)
            if data and "prompt" in data:
                return [TextContent(type="text", text=data["prompt"])]
        return [TextContent(type="text", text=f"Spec '{spec_name}' not found or has no prompt")]

    if name == "validate_spec":
        spec_name = arguments.get("name")
        category = arguments.get("category")

        spec_path = _find_spec(spec_name, category)
        if spec_path:
            result = spec_loader.validate_spec(spec_path)
            output = {
                "is_valid": result.is_valid,
                "errors": result.errors,
                "warnings": result.warnings,
                "info": result.info,
            }
            return [TextContent(type="text", text=json.dumps(output, indent=2))]
        return [TextContent(type="text", text=f"Spec '{spec_name}' not found")]

    if name == "search_specs":
        query = arguments.get("query", "")
        category = arguments.get("category")

        results = spec_loader.search_specs(query, category)
        output = [
            {
                "name": meta.name,
                "category": meta.category,
                "description": meta.description,
                "path": meta.path,
            }
            for _, meta in results
        ]
        return [TextContent(type="text", text=json.dumps(output, indent=2))]

    if name == "get_spec_metadata":
        spec_name = arguments.get("name")
        category = arguments.get("category")

        spec_path = _find_spec(spec_name, category)
        if spec_path:
            metadata = spec_loader.extract_metadata(spec_path)
            if metadata:
                output = {
                    "name": metadata.name,
                    "category": metadata.category,
                    "description": metadata.description,
                    "version": metadata.version,
                    "path": metadata.path,
                    "authors": metadata.authors,
                    "tags": metadata.tags,
                    "phases": metadata.phases,
                    "phase_count": len(metadata.phases),
                    "constraints": metadata.constraints,
                    "has_mermaid_diagram": metadata.has_mermaid_diagram,
                    "has_notepad_template": metadata.has_notepad_template,
                    "modes": metadata.modes,
                    "output_directory": metadata.output_directory,
                    "triggers": {
                        "on_complete": metadata.on_complete,
                        "can_chain_from": metadata.can_chain_from,
                        "provides": metadata.provides,
                        "requires": metadata.requires,
                    },
                }
                return [TextContent(type="text", text=json.dumps(output, indent=2))]
        return [TextContent(type="text", text=f"Spec '{spec_name}' not found")]

    if name == "get_categories":
        categories = spec_loader.get_categories()
        specs_by_cat = spec_loader.get_specs_by_category()
        output = {
            "categories": [
                {"name": cat, "spec_count": len(specs_by_cat.get(cat, []))} for cat in categories
            ]
        }
        return [TextContent(type="text", text=json.dumps(output, indent=2))]

    if name == "compare_specs":
        spec1_name = arguments.get("spec1_name")
        spec1_category = arguments.get("spec1_category")
        spec2_name = arguments.get("spec2_name")
        spec2_category = arguments.get("spec2_category")

        spec1_path = _find_spec(spec1_name, spec1_category)
        spec2_path = _find_spec(spec2_name, spec2_category)

        if not spec1_path:
            return [TextContent(type="text", text=f"Spec '{spec1_name}' not found")]
        if not spec2_path:
            return [TextContent(type="text", text=f"Spec '{spec2_name}' not found")]

        meta1 = spec_loader.extract_metadata(spec1_path)
        meta2 = spec_loader.extract_metadata(spec2_path)

        if meta1 and meta2:
            comparison = {
                "spec1": {
                    "name": meta1.name,
                    "category": meta1.category,
                    "phases": meta1.phases,
                    "phase_count": len(meta1.phases),
                    "constraints": meta1.constraints,
                    "modes": meta1.modes,
                },
                "spec2": {
                    "name": meta2.name,
                    "category": meta2.category,
                    "phases": meta2.phases,
                    "phase_count": len(meta2.phases),
                    "constraints": meta2.constraints,
                    "modes": meta2.modes,
                },
                "differences": {
                    "phase_count_diff": len(meta1.phases) - len(meta2.phases),
                    "must_constraint_diff": meta1.constraints.get("MUST", 0)
                    - meta2.constraints.get("MUST", 0),
                    "same_category": meta1.category == meta2.category,
                    "same_modes": set(meta1.modes) == set(meta2.modes),
                },
            }
            return [TextContent(type="text", text=json.dumps(comparison, indent=2))]
        return [TextContent(type="text", text="Could not extract metadata for comparison")]

    if name == "suggest_workflow":
        task_desc = arguments.get("task_description", "").lower()

        # Simple keyword matching for workflow suggestion
        suggestions = []

        keyword_mappings = {
            "dev": ["implement", "build", "code", "feature", "bug fix", "develop"],
            "spec": ["requirements", "design", "specification", "plan", "task list"],
            "test": ["test", "testing", "qa", "quality assurance", "automation"],
            "review": ["review", "code review", "quality", "assessment"],
            "troubleshoot": ["troubleshoot", "debug", "problem", "issue", "error"],
            "investigate": ["investigate", "crash", "data loss", "forensic", "recovery"],
            "research": ["research", "evaluate", "compare", "technology", "poc"],
            "learn": ["learn", "tutorial", "education", "skill", "training"],
            "innovate": ["innovate", "enhance", "improve", "creative", "ideas"],
            "security": ["security", "vulnerability", "audit", "hardening"],
            "optimize": ["optimize", "performance", "speed", "efficiency"],
            "architecture": ["architecture", "design", "system design", "structure"],
            "docs": ["document", "documentation", "knowledge", "readme"],
            "integrate": ["integrate", "api", "interface", "connect"],
            "wtf": ["mysterious", "legacy", "understand", "archaeology"],
        }

        for spec_name, keywords in keyword_mappings.items():
            if any(kw in task_desc for kw in keywords):
                # Find the spec
                spec_path = _find_spec(spec_name, None)
                if spec_path:
                    metadata = spec_loader.extract_metadata(spec_path)
                    if metadata:
                        suggestions.append(
                            {
                                "name": metadata.name,
                                "category": metadata.category,
                                "description": metadata.description,
                                "relevance": "high" if any(kw in task_desc for kw in keywords[:2]) else "medium",
                            }
                        )

        if not suggestions:
            # Default suggestion
            suggestions.append(
                {
                    "name": "dev",
                    "category": "development",
                    "description": "General development workflow",
                    "relevance": "fallback",
                }
            )

        output = {
            "task": task_desc,
            "suggestions": suggestions[:3],  # Return top 3 suggestions
        }
        return [TextContent(type="text", text=json.dumps(output, indent=2))]

    if name == "get_workflow_chain":
        start_spec = arguments.get("start_spec")
        depth = arguments.get("depth", 3)

        spec_path = _find_spec(start_spec, None)
        if not spec_path:
            return [TextContent(type="text", text=f"Spec '{start_spec}' not found")]

        # Build the chain
        chain = []
        visited = set()
        current_specs = [start_spec]

        for level in range(depth):
            next_specs = []
            for spec_name in current_specs:
                if spec_name in visited:
                    continue
                visited.add(spec_name)

                spec_path = _find_spec(spec_name, None)
                if spec_path:
                    metadata = spec_loader.extract_metadata(spec_path)
                    if metadata:
                        chain.append({
                            "level": level,
                            "spec": spec_name,
                            "category": metadata.category,
                            "on_complete": metadata.on_complete,
                            "provides": metadata.provides,
                        })
                        next_specs.extend(metadata.on_complete)
            current_specs = next_specs

        output = {
            "start": start_spec,
            "depth": depth,
            "chain": chain,
        }
        return [TextContent(type="text", text=json.dumps(output, indent=2))]

    if name == "find_specs_that_provide":
        output_search = arguments.get("output", "").lower()

        results = []
        for spec_path in spec_loader.discover_specs():
            metadata = spec_loader.extract_metadata(spec_path)
            if metadata:
                for provided in metadata.provides:
                    if output_search in provided.lower():
                        results.append({
                            "spec": metadata.name,
                            "category": metadata.category,
                            "provides": metadata.provides,
                            "matched": provided,
                        })
                        break

        return [TextContent(type="text", text=json.dumps(results, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


def _find_spec(name: str, category: str | None) -> Path | None:
    """Find a spec file by name and optional category."""
    if category:
        spec_path = SPECS_DIR / category / f"{name}.toml"
        if spec_path.exists():
            return spec_path
    else:
        # Search all categories
        for spec_path in spec_loader.discover_specs():
            if spec_path.stem == name:
                return spec_path
    return None


# =============================================================================
# PROMPTS - Workflow execution prompts
# =============================================================================


@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available prompts for workflow execution."""
    prompts = []

    for spec_path in spec_loader.discover_specs():
        metadata = spec_loader.extract_metadata(spec_path)
        if metadata:
            prompts.append(
                Prompt(
                    name=f"execute_{metadata.name}",
                    description=f"Execute the {metadata.name} workflow: {metadata.description[:100]}...",
                    arguments=[
                        PromptArgument(
                            name="task",
                            description="Description of the task to execute with this workflow",
                            required=True,
                        ),
                        PromptArgument(
                            name="mode",
                            description="Execution mode: 'collaboration' (default) or 'silent'",
                            required=False,
                        ),
                    ],
                )
            )

    return prompts


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Get a specific workflow prompt for execution."""
    # Extract spec name from prompt name (format: execute_<spec_name>)
    if not name.startswith("execute_"):
        return GetPromptResult(
            description="Unknown prompt",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=f"Unknown prompt: {name}"),
                )
            ],
        )

    spec_name = name.replace("execute_", "")
    spec_path = _find_spec(spec_name, None)

    if not spec_path:
        return GetPromptResult(
            description="Spec not found",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=f"Workflow spec '{spec_name}' not found"),
                )
            ],
        )

    data = spec_loader.load_spec(spec_path)
    if not data or "prompt" not in data:
        return GetPromptResult(
            description="Invalid spec",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(
                        type="text", text=f"Workflow spec '{spec_name}' has no prompt"
                    ),
                )
            ],
        )

    # Get arguments
    task = (arguments or {}).get("task", "")
    mode = (arguments or {}).get("mode", "collaboration")

    # Build the execution prompt
    workflow_prompt = data["prompt"]
    description = data.get("description", "")

    # Construct the full prompt
    full_prompt = f"""# Workflow Execution Request

## Workflow: {spec_name}
{description}

## Execution Mode: {mode.title()} Mode

## Task
{task}

---

# Workflow Instructions

{workflow_prompt}
"""

    return GetPromptResult(
        description=f"Execute {spec_name} workflow",
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=full_prompt),
            )
        ],
    )


# =============================================================================
# SERVER MAIN
# =============================================================================


async def run_server():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


def main():
    """Main entry point."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
