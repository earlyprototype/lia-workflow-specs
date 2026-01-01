"""
MCP Server for Lia Workflow Specs.

Provides resources and tools for remote agent access to workflow specifications.
"""

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    ResourceContents,
    TextResourceContents,
    Tool,
    TextContent,
)

from .models import SpecCollection, SpecCategory, WorkflowSpec


# Initialise MCP server
server = Server("lia-workflow-specs")

# Global spec collection
spec_collection = SpecCollection()


def get_specs_directory() -> Path:
    """Get the specs directory path from environment or default."""
    specs_dir = os.environ.get("LIA_SPECS_DIR")
    if specs_dir:
        return Path(specs_dir)
    
    # Default: look for specs directory relative to this file or workspace
    possible_paths = [
        Path(__file__).parent.parent.parent.parent / "specs",
        Path.cwd() / "specs",
        Path.home() / ".lia" / "specs",
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    return Path.cwd() / "specs"


def initialise_specs():
    """Initialise the spec collection."""
    specs_dir = get_specs_directory()
    spec_collection.load_from_directory(specs_dir)


# ============================================================================
# RESOURCES
# ============================================================================

@server.list_resources()
async def list_resources() -> list[Resource]:
    """List all available resources."""
    resources = []
    
    # Add index resource
    resources.append(Resource(
        uri="specs://index",
        name="Workflow Specs Index",
        description="Complete index of all available workflow specifications",
        mimeType="application/json",
    ))
    
    # Add categories resource
    resources.append(Resource(
        uri="specs://categories",
        name="Spec Categories",
        description="List of all spec categories and their workflows",
        mimeType="application/json",
    ))
    
    # Add individual spec resources
    for spec in spec_collection.specs:
        resources.append(Resource(
            uri=f"specs://{spec.category.value}/{spec.name}",
            name=f"{spec.name} Workflow Spec",
            description=spec.description[:100] + "..." if len(spec.description) > 100 else spec.description,
            mimeType="text/plain",
        ))
        
        # Add metadata resource for each spec
        resources.append(Resource(
            uri=f"specs://{spec.category.value}/{spec.name}/metadata",
            name=f"{spec.name} Metadata",
            description=f"Metadata and structure for {spec.name} workflow",
            mimeType="application/json",
        ))
    
    # Add summary resource
    resources.append(Resource(
        uri="specs://summary",
        name="Quick Reference Guide",
        description="Brief overview of all workflows and when to use them",
        mimeType="text/markdown",
    ))
    
    return resources


@server.read_resource()
async def read_resource(uri: str) -> ResourceContents:
    """Read a resource by URI."""
    
    # Parse URI
    if not uri.startswith("specs://"):
        raise ValueError(f"Invalid URI scheme: {uri}")
    
    path = uri[8:]  # Remove "specs://"
    
    # Handle index
    if path == "index":
        index_data = {
            "total_specs": len(spec_collection.specs),
            "categories": spec_collection.get_categories(),
            "specs": [spec.to_dict() for spec in spec_collection.specs],
        }
        return TextResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(index_data, indent=2),
        )
    
    # Handle categories
    if path == "categories":
        categories_data = spec_collection.get_categories()
        return TextResourceContents(
            uri=uri,
            mimeType="application/json",
            text=json.dumps(categories_data, indent=2),
        )
    
    # Handle summary
    if path == "summary":
        summary = generate_quick_reference()
        return TextResourceContents(
            uri=uri,
            mimeType="text/markdown",
            text=summary,
        )
    
    # Handle individual specs
    parts = path.split("/")
    
    if len(parts) >= 2:
        category = parts[0]
        spec_name = parts[1]
        is_metadata = len(parts) == 3 and parts[2] == "metadata"
        
        spec = spec_collection.get_by_name(spec_name)
        if not spec:
            raise ValueError(f"Spec not found: {spec_name}")
        
        if is_metadata:
            return TextResourceContents(
                uri=uri,
                mimeType="application/json",
                text=json.dumps(spec.to_dict(), indent=2),
            )
        else:
            return TextResourceContents(
                uri=uri,
                mimeType="text/plain",
                text=spec.prompt,
            )
    
    raise ValueError(f"Unknown resource: {uri}")


def generate_quick_reference() -> str:
    """Generate a quick reference guide for all workflows."""
    categories = spec_collection.get_categories()
    
    lines = [
        "# Lia Workflow Specs Quick Reference",
        "",
        "## Overview",
        f"Total workflows available: {len(spec_collection.specs)}",
        "",
    ]
    
    category_descriptions = {
        "development": "Build and implement features, fix bugs, and conduct testing",
        "quality": "Ensure code quality, security, and system architecture",
        "problem-solving": "Diagnose issues, investigate crashes, and troubleshoot",
        "research": "Conduct research, analyse papers, and evaluate technologies",
        "knowledge": "Create documentation and manage knowledge",
        "strategy": "Drive innovation and integration initiatives",
    }
    
    for category, spec_names in sorted(categories.items()):
        lines.append(f"## {category.replace('-', ' ').title()}")
        lines.append(category_descriptions.get(category, ""))
        lines.append("")
        
        for spec_name in sorted(spec_names):
            spec = spec_collection.get_by_name(spec_name)
            if spec:
                short_desc = spec.description[:80] + "..." if len(spec.description) > 80 else spec.description
                lines.append(f"- **{spec_name}**: {short_desc}")
        
        lines.append("")
    
    lines.extend([
        "## Quick Selection Guide",
        "",
        "| Task Type | Recommended Workflow |",
        "|-----------|---------------------|",
        "| Implement new feature | `spec` → `dev` |",
        "| Fix a bug | `troubleshoot` or `dev` |",
        "| Review code | `review` |",
        "| Security audit | `security` |",
        "| Performance issues | `optimize` |",
        "| Unknown code | `wtf` |",
        "| Crash investigation | `investigate` |",
        "| Write documentation | `docs` |",
        "| Research technology | `research` |",
        "| Read academic paper | `paper` |",
        "| Learn new skills | `learn` |",
        "| Enhance features | `innovate` |",
        "| Design architecture | `architecture` |",
        "| Build API | `integrate` |",
        "| Plan tests | `test` |",
    ])
    
    return "\n".join(lines)


# ============================================================================
# TOOLS
# ============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="search_specs",
            description="Search workflow specifications by keyword. Returns matching specs with descriptions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search keyword or phrase to find relevant specs",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="recommend_workflow",
            description="Get workflow recommendations based on a task description. Returns the best matching workflows for your task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "Description of what you want to accomplish",
                    },
                },
                "required": ["task_description"],
            },
        ),
        Tool(
            name="get_spec_details",
            description="Get detailed information about a specific workflow spec including phases and constraints.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_name": {
                        "type": "string",
                        "description": "Name of the spec (e.g., 'dev', 'spec', 'review')",
                    },
                },
                "required": ["spec_name"],
            },
        ),
        Tool(
            name="list_specs_by_category",
            description="List all workflow specs in a specific category.",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Category name (development, quality, problem-solving, research, knowledge, strategy)",
                        "enum": ["development", "quality", "problem-solving", "research", "knowledge", "strategy"],
                    },
                },
                "required": ["category"],
            },
        ),
        Tool(
            name="get_workflow_phases",
            description="Get the list of phases for a specific workflow spec.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_name": {
                        "type": "string",
                        "description": "Name of the spec to get phases for",
                    },
                },
                "required": ["spec_name"],
            },
        ),
        Tool(
            name="validate_spec",
            description="Validate a workflow spec file for required sections and formatting.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_name": {
                        "type": "string",
                        "description": "Name of the spec to validate",
                    },
                },
                "required": ["spec_name"],
            },
        ),
        Tool(
            name="get_spec_prompt",
            description="Get the full prompt text for a workflow spec, ready to use with an AI agent.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_name": {
                        "type": "string",
                        "description": "Name of the spec to get the prompt for",
                    },
                },
                "required": ["spec_name"],
            },
        ),
        Tool(
            name="compare_specs",
            description="Compare two workflow specs to understand their differences and use cases.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec1": {
                        "type": "string",
                        "description": "Name of the first spec",
                    },
                    "spec2": {
                        "type": "string",
                        "description": "Name of the second spec",
                    },
                },
                "required": ["spec1", "spec2"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent]:
    """Handle tool calls."""
    
    if name == "search_specs":
        query = arguments.get("query", "")
        results = spec_collection.search(query)
        
        if not results:
            return [TextContent(
                type="text",
                text=f"No specs found matching '{query}'",
            )]
        
        output = [f"Found {len(results)} spec(s) matching '{query}':\n"]
        for spec in results:
            output.append(f"**{spec.name}** ({spec.category.value})")
            output.append(f"  {spec.description[:100]}...")
            output.append("")
        
        return [TextContent(type="text", text="\n".join(output))]
    
    elif name == "recommend_workflow":
        task_desc = arguments.get("task_description", "")
        recommendations = spec_collection.recommend_for_task(task_desc)
        
        if not recommendations:
            return [TextContent(
                type="text",
                text=f"No specific recommendations for: {task_desc}\n\nTry browsing categories or searching for specific keywords.",
            )]
        
        output = [f"Recommended workflows for: '{task_desc}'\n"]
        for i, spec in enumerate(recommendations, 1):
            output.append(f"{i}. **{spec.name}** ({spec.category.value})")
            output.append(f"   {spec.description}")
            output.append(f"   Phases: {len(spec.phases)}")
            output.append("")
        
        return [TextContent(type="text", text="\n".join(output))]
    
    elif name == "get_spec_details":
        spec_name = arguments.get("spec_name", "")
        spec = spec_collection.get_by_name(spec_name)
        
        if not spec:
            return [TextContent(
                type="text",
                text=f"Spec '{spec_name}' not found. Available specs: {', '.join(s.name for s in spec_collection.specs)}",
            )]
        
        return [TextContent(type="text", text=spec.get_summary())]
    
    elif name == "list_specs_by_category":
        category_name = arguments.get("category", "")
        try:
            category = SpecCategory(category_name)
        except ValueError:
            return [TextContent(
                type="text",
                text=f"Invalid category: {category_name}. Valid categories: {', '.join(c.value for c in SpecCategory)}",
            )]
        
        specs = spec_collection.get_by_category(category)
        
        if not specs:
            return [TextContent(
                type="text",
                text=f"No specs found in category: {category_name}",
            )]
        
        output = [f"Specs in category '{category_name}':\n"]
        for spec in specs:
            output.append(f"- **{spec.name}**: {spec.description[:80]}...")
        
        return [TextContent(type="text", text="\n".join(output))]
    
    elif name == "get_workflow_phases":
        spec_name = arguments.get("spec_name", "")
        spec = spec_collection.get_by_name(spec_name)
        
        if not spec:
            return [TextContent(
                type="text",
                text=f"Spec '{spec_name}' not found.",
            )]
        
        if not spec.phases:
            return [TextContent(
                type="text",
                text=f"No phases extracted for '{spec_name}'. The spec may use a different format.",
            )]
        
        output = [f"Phases for {spec_name} workflow:\n"]
        for phase in spec.phases:
            output.append(f"{phase.number}. {phase.name}")
        
        return [TextContent(type="text", text="\n".join(output))]
    
    elif name == "validate_spec":
        spec_name = arguments.get("spec_name", "")
        spec = spec_collection.get_by_name(spec_name)
        
        if not spec:
            return [TextContent(
                type="text",
                text=f"Spec '{spec_name}' not found.",
            )]
        
        validation_results = validate_spec_content(spec)
        return [TextContent(type="text", text=validation_results)]
    
    elif name == "get_spec_prompt":
        spec_name = arguments.get("spec_name", "")
        spec = spec_collection.get_by_name(spec_name)
        
        if not spec:
            return [TextContent(
                type="text",
                text=f"Spec '{spec_name}' not found.",
            )]
        
        return [TextContent(type="text", text=spec.prompt)]
    
    elif name == "compare_specs":
        spec1_name = arguments.get("spec1", "")
        spec2_name = arguments.get("spec2", "")
        
        spec1 = spec_collection.get_by_name(spec1_name)
        spec2 = spec_collection.get_by_name(spec2_name)
        
        if not spec1:
            return [TextContent(type="text", text=f"Spec '{spec1_name}' not found.")]
        if not spec2:
            return [TextContent(type="text", text=f"Spec '{spec2_name}' not found.")]
        
        comparison = compare_specs(spec1, spec2)
        return [TextContent(type="text", text=comparison)]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}",
        )]


def validate_spec_content(spec: WorkflowSpec) -> str:
    """Validate a spec and return results."""
    errors = []
    warnings = []
    passed = []
    
    # Check required sections
    required_sections = [
        "Workflow Mode System",
        "Goal",
        "workflow-definition",
        "IMPORTANT EXECUTION INSTRUCTIONS",
        "0-Notepad Template",
    ]
    
    for section in required_sections:
        if section in spec.prompt:
            passed.append(f"✓ Found required section: {section}")
        else:
            errors.append(f"✗ Missing required section: {section}")
    
    # Check for Mermaid diagram
    if "```mermaid" in spec.prompt.lower():
        passed.append("✓ Contains Mermaid workflow diagram")
    else:
        warnings.append("⚠ No Mermaid diagram found")
    
    # Check MUST constraints
    must_count = len(re.findall(r"\bMUST\b", spec.prompt))
    if must_count > 0:
        passed.append(f"✓ Contains {must_count} MUST constraints")
    else:
        warnings.append("⚠ No MUST constraints found")
    
    # Check phases
    if spec.phases:
        passed.append(f"✓ Has {len(spec.phases)} defined phases")
    else:
        warnings.append("⚠ No phases detected")
    
    # Build output
    output = [f"# Validation Results for {spec.name}\n"]
    
    if errors:
        output.append("## Errors")
        output.extend(errors)
        output.append("")
    
    if warnings:
        output.append("## Warnings")
        output.extend(warnings)
        output.append("")
    
    if passed:
        output.append("## Passed Checks")
        output.extend(passed)
        output.append("")
    
    status = "❌ INVALID" if errors else ("⚠️ VALID with warnings" if warnings else "✅ VALID")
    output.append(f"\n**Status**: {status}")
    
    return "\n".join(output)


def compare_specs(spec1: WorkflowSpec, spec2: WorkflowSpec) -> str:
    """Compare two specs and return a comparison."""
    output = [
        f"# Comparison: {spec1.name} vs {spec2.name}",
        "",
        "## Overview",
        "",
        f"| Aspect | {spec1.name} | {spec2.name} |",
        "|--------|------------|------------|",
        f"| Category | {spec1.category.value} | {spec2.category.value} |",
        f"| Phases | {len(spec1.phases)} | {len(spec2.phases)} |",
        f"| Tags | {', '.join(spec1.tags[:3])} | {', '.join(spec2.tags[:3])} |",
        "",
        "## Descriptions",
        "",
        f"**{spec1.name}**: {spec1.description[:150]}...",
        "",
        f"**{spec2.name}**: {spec2.description[:150]}...",
        "",
        "## When to Use Each",
        "",
    ]
    
    # Add use case recommendations
    use_cases = {
        "dev": "Implementing features, fixing bugs, building systems",
        "spec": "Creating requirements and design documents before implementation",
        "test": "Designing and implementing testing strategies",
        "review": "Conducting thorough code reviews",
        "troubleshoot": "Diagnosing and resolving technical issues",
        "investigate": "Forensic analysis after crashes or data loss",
        "security": "Security assessments and vulnerability testing",
        "optimize": "Performance optimization and profiling",
        "architecture": "System design and architectural decisions",
        "research": "Technology evaluation and proof of concepts",
        "learn": "Project-based learning and skill development",
        "paper": "Academic paper analysis and synthesis",
        "docs": "Documentation creation and knowledge management",
        "innovate": "Creative enhancement and feature innovation",
        "integrate": "API development and system integration",
        "wtf": "Understanding mysterious or legacy code",
    }
    
    output.append(f"**Use {spec1.name}** when: {use_cases.get(spec1.name, spec1.description[:100])}")
    output.append("")
    output.append(f"**Use {spec2.name}** when: {use_cases.get(spec2.name, spec2.description[:100])}")
    
    return "\n".join(output)


def main():
    """Main entry point for the MCP server."""
    # Initialise specs
    initialise_specs()
    
    print(f"Loaded {len(spec_collection.specs)} workflow specs", file=__import__("sys").stderr)
    
    # Run the server
    async def run():
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )
    
    asyncio.run(run())


if __name__ == "__main__":
    main()
