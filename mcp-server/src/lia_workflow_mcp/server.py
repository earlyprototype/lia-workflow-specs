"""
MCP Server for Lia Workflow Specs.

Provides resources and tools for remote agent access to workflow specifications.
This server enables AI agents to discover, read, validate, and execute
systematic development workflows through the Model Context Protocol (MCP).

Features:
    - 37+ resources for accessing spec content and metadata
    - 11+ tools for searching, recommending, and validating specs
    - 20+ prompt templates for starting workflow sessions
    - Workflow chaining based on trigger definitions

Example:
    Configure in Claude Desktop:
    
    ```json
    {
      "mcpServers": {
        "lia-workflow-specs": {
          "command": "python3",
          "args": ["-m", "lia_workflow_mcp.server"],
          "env": {"LIA_SPECS_DIR": "/path/to/specs"}
        }
      }
    }
    ```
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
    Prompt,
    PromptMessage,
    PromptArgument,
)

from .models import SpecCollection, SpecCategory, WorkflowSpec
from .triggers import TriggerManager


# Initialise MCP server
server = Server("lia-workflow-specs")

# Global spec collection and trigger manager
spec_collection = SpecCollection()
trigger_manager = TriggerManager()


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
    """
    Initialise the spec collection and trigger manager.
    
    Loads all workflow specs from the specs directory and configures
    the trigger manager for workflow chaining recommendations.
    """
    global trigger_manager
    specs_dir = get_specs_directory()
    spec_collection.load_from_directory(specs_dir)
    trigger_manager = TriggerManager(specs_dir)


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
# PROMPTS
# ============================================================================

@server.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List all available prompt templates."""
    prompts = []
    
    # Add workflow starter prompts for each spec
    for spec in spec_collection.specs:
        prompts.append(Prompt(
            name=f"start-{spec.name}",
            description=f"Start a {spec.name} workflow session",
            arguments=[
                PromptArgument(
                    name="task",
                    description="Description of your task or goal",
                    required=True,
                ),
                PromptArgument(
                    name="mode",
                    description="Execution mode: 'collaboration' or 'silent'",
                    required=False,
                ),
            ],
        ))
    
    # Add general helper prompts
    prompts.extend([
        Prompt(
            name="choose-workflow",
            description="Help me choose the right workflow for my task",
            arguments=[
                PromptArgument(
                    name="task",
                    description="Description of what you want to accomplish",
                    required=True,
                ),
            ],
        ),
        Prompt(
            name="workflow-sequence",
            description="Plan a sequence of workflows for a complex project",
            arguments=[
                PromptArgument(
                    name="project",
                    description="Description of the project or complex task",
                    required=True,
                ),
            ],
        ),
        Prompt(
            name="resume-workflow",
            description="Resume an interrupted workflow session",
            arguments=[
                PromptArgument(
                    name="workflow",
                    description="Name of the workflow to resume",
                    required=True,
                ),
                PromptArgument(
                    name="task_name",
                    description="Task name (directory name under .lia/)",
                    required=True,
                ),
            ],
        ),
    ])
    
    return prompts


@server.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> list[PromptMessage]:
    """Get a specific prompt with arguments filled in."""
    args = arguments or {}
    
    # Handle workflow starter prompts
    if name.startswith("start-"):
        spec_name = name[6:]  # Remove "start-" prefix
        spec = spec_collection.get_by_name(spec_name)
        
        if not spec:
            return [PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"Error: Workflow '{spec_name}' not found.",
                ),
            )]
        
        task = args.get("task", "")
        mode = args.get("mode", "collaboration")
        
        # Build the prompt
        prompt_text = f"""# Starting {spec.name} Workflow

## Task
{task}

## Mode
{mode.title()} Mode

## Instructions
You are now operating as a {spec.name} workflow agent. Follow the systematic workflow defined below.

{spec.prompt}

---

**Begin the workflow now.** Start with Phase 1, creating the necessary directory structure and `0-notepad.md` file.
"""
        
        return [PromptMessage(
            role="user",
            content=TextContent(type="text", text=prompt_text),
        )]
    
    # Handle choose-workflow prompt
    elif name == "choose-workflow":
        task = args.get("task", "")
        recommendations = spec_collection.recommend_for_task(task)
        
        rec_text = "\n".join([
            f"- **{r.name}**: {r.description[:80]}..."
            for r in recommendations
        ])
        
        prompt_text = f"""# Help Me Choose a Workflow

## My Task
{task}

## Recommended Workflows
Based on your task, here are the recommended workflows:

{rec_text}

## All Available Workflows
{generate_quick_reference()}

Please help me choose the best workflow for my task and explain why.
"""
        
        return [PromptMessage(
            role="user",
            content=TextContent(type="text", text=prompt_text),
        )]
    
    # Handle workflow-sequence prompt
    elif name == "workflow-sequence":
        project = args.get("project", "")
        sequence = suggest_workflow_sequence(project)
        
        prompt_text = f"""# Plan Workflow Sequence

## Project Description
{project}

## Suggested Sequence
{sequence}

Please help me refine this workflow sequence for my project. Consider:
1. Are there any workflows I should add or remove?
2. Is the order optimal?
3. What deliverables should flow between workflows?
"""
        
        return [PromptMessage(
            role="user",
            content=TextContent(type="text", text=prompt_text),
        )]
    
    # Handle resume-workflow prompt
    elif name == "resume-workflow":
        workflow = args.get("workflow", "")
        task_name = args.get("task_name", "")
        
        spec = spec_collection.get_by_name(workflow)
        if not spec:
            return [PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"Error: Workflow '{workflow}' not found.",
                ),
            )]
        
        prompt_text = f"""# Resume {workflow} Workflow

## Task
{task_name}

## Instructions
You are resuming an interrupted {workflow} workflow session.

1. First, read the existing files in `.lia/{workflow}/{task_name}/`:
   - `0-notepad.md` - Review captured insights and assumptions
   - Any phase documents (1-*.md, 2-*.md, etc.)

2. Determine which phase was last completed

3. Resume from the next incomplete phase

## Workflow Definition
{spec.prompt}

---

**Please read the existing workflow files and determine where to resume.**
"""
        
        return [PromptMessage(
            role="user",
            content=TextContent(type="text", text=prompt_text),
        )]
    
    else:
        return [PromptMessage(
            role="user",
            content=TextContent(
                type="text",
                text=f"Unknown prompt: {name}",
            ),
        )]


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
        Tool(
            name="get_execution_guide",
            description="Get a step-by-step execution guide for a workflow, including what to do at each phase and how to handle approvals.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_name": {
                        "type": "string",
                        "description": "Name of the spec to get execution guide for",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["collaboration", "silent"],
                        "description": "Execution mode (default: collaboration)",
                    },
                },
                "required": ["spec_name"],
            },
        ),
        Tool(
            name="get_phase_checklist",
            description="Get a detailed checklist for a specific phase of a workflow, including constraints and deliverables.",
            inputSchema={
                "type": "object",
                "properties": {
                    "spec_name": {
                        "type": "string",
                        "description": "Name of the spec",
                    },
                    "phase_number": {
                        "type": "integer",
                        "description": "Phase number (1-based)",
                    },
                },
                "required": ["spec_name", "phase_number"],
            },
        ),
        Tool(
            name="suggest_workflow_sequence",
            description="Suggest a sequence of workflows for a complex task that may require multiple workflows.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_description": {
                        "type": "string",
                        "description": "Description of the complex task",
                    },
                },
                "required": ["task_description"],
            },
        ),
        Tool(
            name="get_workflow_chain",
            description="Get the recommended workflow chain starting from a specific workflow, based on trigger definitions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_workflow": {
                        "type": "string",
                        "description": "Name of the starting workflow",
                    },
                    "end_workflow": {
                        "type": "string",
                        "description": "Optional target end workflow",
                    },
                },
                "required": ["start_workflow"],
            },
        ),
        Tool(
            name="list_workflow_chains",
            description="List all predefined workflow chains for common development patterns.",
            inputSchema={
                "type": "object",
                "properties": {},
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
    
    elif name == "get_execution_guide":
        spec_name = arguments.get("spec_name", "")
        mode = arguments.get("mode", "collaboration")
        
        spec = spec_collection.get_by_name(spec_name)
        if not spec:
            return [TextContent(type="text", text=f"Spec '{spec_name}' not found.")]
        
        guide = generate_execution_guide(spec, mode)
        return [TextContent(type="text", text=guide)]
    
    elif name == "get_phase_checklist":
        spec_name = arguments.get("spec_name", "")
        phase_number = arguments.get("phase_number", 1)
        
        spec = spec_collection.get_by_name(spec_name)
        if not spec:
            return [TextContent(type="text", text=f"Spec '{spec_name}' not found.")]
        
        checklist = generate_phase_checklist(spec, phase_number)
        return [TextContent(type="text", text=checklist)]
    
    elif name == "suggest_workflow_sequence":
        task_desc = arguments.get("task_description", "")
        sequence = suggest_workflow_sequence(task_desc)
        return [TextContent(type="text", text=sequence)]
    
    elif name == "get_workflow_chain":
        start = arguments.get("start_workflow", "")
        end = arguments.get("end_workflow")
        
        chain = trigger_manager.build_custom_chain(start, end)
        if not chain or chain == [start]:
            # Fallback to next workflows
            next_wfs = trigger_manager.get_next_workflows(start)
            if next_wfs:
                chain = [start] + next_wfs[:2]
        
        output = [
            f"# Workflow Chain from {start}",
            "",
            f"**Sequence**: {' → '.join(chain)}",
            "",
            "## Chain Details",
            "",
        ]
        
        for wf in chain:
            outputs = trigger_manager.get_workflow_outputs(wf)
            inputs = trigger_manager.get_workflow_inputs(wf)
            output.append(f"### {wf}")
            if inputs:
                output.append(f"- **Requires**: {', '.join(inputs)}")
            if outputs:
                output.append(f"- **Provides**: {', '.join(outputs)}")
            output.append("")
        
        return [TextContent(type="text", text="\n".join(output))]
    
    elif name == "list_workflow_chains":
        chains = trigger_manager.get_all_chains()
        
        if not chains:
            return [TextContent(
                type="text",
                text="No predefined chains found. Ensure specs/_common/workflow-triggers.toml exists.",
            )]
        
        output = [
            "# Predefined Workflow Chains",
            "",
            "These are common workflow sequences for typical development patterns:",
            "",
        ]
        
        for chain in chains:
            output.append(f"## {chain.name.replace('_', ' ').title()}")
            output.append(f"{chain.description}")
            output.append(f"")
            output.append(f"**Sequence**: {' → '.join(chain.sequence)}")
            output.append("")
        
        return [TextContent(type="text", text="\n".join(output))]
    
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


def generate_execution_guide(spec: WorkflowSpec, mode: str = "collaboration") -> str:
    """Generate a step-by-step execution guide for a workflow."""
    is_silent = mode == "silent"
    
    output = [
        f"# Execution Guide: {spec.name}",
        f"**Mode**: {mode.title()}",
        "",
        "## Before Starting",
        "",
        "1. Create the workflow directory: `.lia/{workflow}/{task_name}/`",
        "2. Create `0-notepad.md` for capturing insights",
        "3. Read relevant existing documentation",
        "",
        "## Workflow Execution",
        "",
    ]
    
    for phase in spec.phases:
        output.append(f"### Phase {phase.number}: {phase.name}")
        output.append("")
        
        # Extract constraints for this phase from the prompt if possible
        output.append("**Actions:**")
        output.append(f"- Create phase output file: `{phase.number}-*.md`")
        output.append("- Complete all phase requirements")
        output.append("- Document findings and decisions")
        output.append("")
        
        if is_silent:
            output.append("**Silent Mode:**")
            output.append("- Record all assumptions in `0-notepad.md`")
            output.append("- Proceed automatically to next phase")
        else:
            output.append("**Collaboration Mode:**")
            output.append("- Present completed work to user")
            output.append("- Request explicit approval")
            output.append("- Iterate based on feedback until approved")
            output.append("- Only proceed after receiving approval")
        output.append("")
    
    output.extend([
        "## Completion",
        "",
        "- Ensure all phase documents are complete",
        "- Review `0-notepad.md` for captured insights",
        "- Provide summary of completed work",
    ])
    
    return "\n".join(output)


def generate_phase_checklist(spec: WorkflowSpec, phase_number: int) -> str:
    """Generate a detailed checklist for a specific phase."""
    phase = None
    for p in spec.phases:
        if p.number == phase_number:
            phase = p
            break
    
    if not phase:
        return f"Phase {phase_number} not found in {spec.name}. Available phases: {len(spec.phases)}"
    
    output = [
        f"# Phase {phase.number}: {phase.name}",
        f"**Workflow**: {spec.name}",
        "",
        "## Checklist",
        "",
        f"- [ ] Create output file: `.lia/{spec.name}/{{task_name}}/{phase.number}-*.md`",
        "- [ ] Analyse requirements for this phase",
        "- [ ] Document all findings",
        "- [ ] Review for completeness",
        "- [ ] Request user approval (Collaboration mode)",
        "- [ ] Iterate on feedback if needed",
        "- [ ] Receive explicit approval before proceeding",
        "",
        "## Common Constraints",
        "",
        "- MUST complete all required documentation",
        "- MUST NOT proceed without user approval (Collaboration mode)",
        "- MUST record assumptions in notepad (Silent mode)",
        "- SHOULD capture insights in `0-notepad.md`",
        "",
        "## Tips",
        "",
        f"- Focus only on Phase {phase.number} tasks",
        "- Don't jump ahead to later phases",
        "- Ask clarifying questions if requirements are unclear",
        "- Document decisions and rationale",
    ]
    
    return "\n".join(output)


def suggest_workflow_sequence(task_description: str) -> str:
    """Suggest a sequence of workflows for a complex task."""
    task_lower = task_description.lower()
    
    sequences = []
    
    # Pattern matching for common task sequences
    if "new feature" in task_lower or "build" in task_lower or "implement" in task_lower:
        if "design" in task_lower or "plan" in task_lower:
            sequences.append({
                "name": "Full Feature Development",
                "steps": [
                    ("spec", "Create requirements and design documents"),
                    ("dev", "Implement the feature"),
                    ("test", "Design and implement tests"),
                    ("review", "Conduct code review"),
                ],
            })
        else:
            sequences.append({
                "name": "Quick Implementation",
                "steps": [
                    ("dev", "Implement the feature"),
                    ("test", "Write tests"),
                ],
            })
    
    if "bug" in task_lower or "fix" in task_lower or "debug" in task_lower:
        sequences.append({
            "name": "Bug Fix Workflow",
            "steps": [
                ("troubleshoot", "Diagnose the issue"),
                ("dev", "Implement the fix"),
                ("test", "Verify the fix with tests"),
            ],
        })
    
    if "security" in task_lower or "audit" in task_lower:
        sequences.append({
            "name": "Security Assessment",
            "steps": [
                ("security", "Conduct security assessment"),
                ("review", "Review security-related code"),
                ("dev", "Implement security improvements"),
            ],
        })
    
    if "performance" in task_lower or "slow" in task_lower or "optimize" in task_lower:
        sequences.append({
            "name": "Performance Optimization",
            "steps": [
                ("optimize", "Profile and identify bottlenecks"),
                ("dev", "Implement optimizations"),
                ("test", "Validate performance improvements"),
            ],
        })
    
    if "learn" in task_lower or "understand" in task_lower:
        if "legacy" in task_lower or "existing" in task_lower:
            sequences.append({
                "name": "Codebase Understanding",
                "steps": [
                    ("wtf", "Understand mysterious/legacy code"),
                    ("review", "Review code quality"),
                    ("docs", "Document findings"),
                ],
            })
        else:
            sequences.append({
                "name": "Learning Path",
                "steps": [
                    ("research", "Research the technology"),
                    ("learn", "Project-based learning"),
                    ("docs", "Document learnings"),
                ],
            })
    
    if "research" in task_lower or "evaluate" in task_lower or "compare" in task_lower:
        sequences.append({
            "name": "Technology Evaluation",
            "steps": [
                ("research", "Research and evaluate options"),
                ("architecture", "Design integration approach"),
                ("integrate", "Implement integration"),
            ],
        })
    
    if "api" in task_lower or "integration" in task_lower:
        sequences.append({
            "name": "API Development",
            "steps": [
                ("spec", "Define API requirements"),
                ("integrate", "Design and implement API"),
                ("test", "Create API tests"),
                ("docs", "Document API"),
            ],
        })
    
    # Default suggestion if no specific pattern matched
    if not sequences:
        sequences.append({
            "name": "General Development",
            "steps": [
                ("spec", "Define requirements (if complex)"),
                ("dev", "Implement solution"),
                ("review", "Review code quality"),
            ],
        })
    
    # Build output
    output = [
        f"# Suggested Workflow Sequences",
        f"**Task**: {task_description}",
        "",
    ]
    
    for i, seq in enumerate(sequences, 1):
        output.append(f"## Option {i}: {seq['name']}")
        output.append("")
        for j, (workflow, purpose) in enumerate(seq['steps'], 1):
            output.append(f"{j}. **{workflow}** - {purpose}")
        output.append("")
    
    output.extend([
        "## Tips",
        "",
        "- Start with the first workflow in the sequence",
        "- Complete each workflow before moving to the next",
        "- Artifacts from earlier workflows feed into later ones",
        "- You can skip workflows if not needed for your task",
    ])
    
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
