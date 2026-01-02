"""
Workflow composition suggestions.

Provides OPTIONAL guidance for workflow sequences based on definitions
from specs/_common/workflow-triggers.toml.

IMPORTANT: Every spec is fully independent. These are suggestions only,
not dependencies. See docs/workflow-composition.md for full explanation.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import tomli
except ImportError:
    import tomllib as tomli


@dataclass
class WorkflowTrigger:
    """
    Defines composition hints for a workflow.
    
    All fields are SUGGESTIONS, not requirements. Every workflow
    can run independently with just a task description.
    """
    
    name: str
    on_complete: list[str] = field(default_factory=list)  # Suggested next steps
    can_chain_from: list[str] = field(default_factory=list)  # Often follows these
    typical_outputs: list[str] = field(default_factory=list)  # Common artefacts
    works_well_with: list[str] = field(default_factory=list)  # Helpful context (NOT required)


@dataclass
class WorkflowChain:
    """Defines a predefined workflow chain/sequence."""
    
    name: str
    description: str
    sequence: list[str]


class TriggerManager:
    """
    Manages workflow triggers and chaining logic.
    
    Loads trigger definitions from workflow-triggers.toml and provides
    methods for determining workflow sequences and recommendations.
    """
    
    def __init__(self, specs_dir: Optional[Path] = None):
        """
        Initialise the trigger manager.
        
        Args:
            specs_dir: Path to the specs directory. If None, uses LIA_SPECS_DIR
                      environment variable or auto-detects.
        """
        self.triggers: dict[str, WorkflowTrigger] = {}
        self.chains: dict[str, WorkflowChain] = {}
        
        if specs_dir:
            self._load_triggers(specs_dir)
    
    def _load_triggers(self, specs_dir: Path) -> None:
        """Load trigger definitions from workflow-triggers.toml."""
        triggers_file = specs_dir / "_common" / "workflow-triggers.toml"
        
        if not triggers_file.exists():
            return
        
        try:
            with open(triggers_file, "rb") as f:
                data = tomli.load(f)
            
            # Load chains
            chains_data = data.get("chains", {})
            for name, chain_info in chains_data.items():
                if isinstance(chain_info, dict):
                    self.chains[name] = WorkflowChain(
                        name=name,
                        description=chain_info.get("description", ""),
                        sequence=chain_info.get("sequence", []),
                    )
            
            # Load triggers
            triggers_data = data.get("triggers", {})
            for name, trigger_info in triggers_data.items():
                if name == "schema":
                    continue
                if isinstance(trigger_info, dict):
                    self.triggers[name] = WorkflowTrigger(
                        name=name,
                        on_complete=trigger_info.get("on_complete", []),
                        can_chain_from=trigger_info.get("can_chain_from", []),
                        # Support both old and new field names
                        typical_outputs=trigger_info.get("typical_outputs", trigger_info.get("provides", [])),
                        works_well_with=trigger_info.get("works_well_with", trigger_info.get("requires", [])),
                    )
        except Exception as e:
            print(f"Warning: Failed to load triggers: {e}")
    
    def get_suggested_next(self, current: str) -> list[str]:
        """
        Get suggested workflows to consider after the current one.
        
        Note: These are suggestions only, not requirements.
        
        Args:
            current: Name of the current/completed workflow.
            
        Returns:
            List of suggested follow-up workflow names.
        """
        trigger = self.triggers.get(current)
        if trigger:
            return trigger.on_complete
        return []
    
    # Alias for backwards compatibility
    get_next_workflows = get_suggested_next
    
    def get_common_predecessors(self, target: str) -> list[str]:
        """
        Get workflows that commonly precede this one.
        
        Note: Not prerequisites - any workflow can run standalone.
        
        Args:
            target: Name of the target workflow.
            
        Returns:
            List of workflows that often lead to this one.
        """
        trigger = self.triggers.get(target)
        if trigger:
            return trigger.can_chain_from
        return []
    
    # Alias for backwards compatibility
    get_previous_workflows = get_common_predecessors
    
    def get_typical_outputs(self, workflow: str) -> list[str]:
        """
        Get artefacts this workflow typically produces.
        
        Args:
            workflow: Name of the workflow.
            
        Returns:
            List of typical output types.
        """
        trigger = self.triggers.get(workflow)
        if trigger:
            return trigger.typical_outputs
        return []
    
    # Alias for backwards compatibility
    get_workflow_outputs = get_typical_outputs
    
    def get_helpful_context(self, workflow: str) -> list[str]:
        """
        Get context that helps this workflow (but is NOT required).
        
        Note: Workflow works fine without these - they're just helpful.
        
        Args:
            workflow: Name of the workflow.
            
        Returns:
            List of helpful context types.
        """
        trigger = self.triggers.get(workflow)
        if trigger:
            return trigger.works_well_with
        return []
    
    # Alias for backwards compatibility  
    get_workflow_inputs = get_helpful_context
    
    def find_chain_for_task(self, task_keywords: list[str]) -> Optional[WorkflowChain]:
        """
        Find a predefined chain that matches the task keywords.
        
        Args:
            task_keywords: Keywords from the task description.
            
        Returns:
            Matching WorkflowChain or None.
        """
        keyword_mappings = {
            "development": ["implement", "build", "feature", "code"],
            "quality": ["review", "security", "optimize", "quality"],
            "problem_solving": ["debug", "fix", "troubleshoot", "investigate"],
            "learning": ["learn", "understand", "study", "research"],
            "api_development": ["api", "endpoint", "integration", "rest"],
            "security_audit": ["security", "audit", "vulnerability", "secure"],
        }
        
        for chain_name, keywords in keyword_mappings.items():
            if any(kw in task_keywords for kw in keywords):
                chain = self.chains.get(chain_name)
                if chain:
                    return chain
        
        return None
    
    def build_custom_chain(
        self,
        start: str,
        end: Optional[str] = None,
        max_length: int = 5
    ) -> list[str]:
        """
        Build a custom workflow chain from start to optional end.
        
        Args:
            start: Starting workflow name.
            end: Optional ending workflow name.
            max_length: Maximum chain length.
            
        Returns:
            List of workflow names forming the chain.
        """
        chain = [start]
        current = start
        
        for _ in range(max_length - 1):
            next_workflows = self.get_next_workflows(current)
            
            if not next_workflows:
                break
            
            if end and end in next_workflows:
                chain.append(end)
                break
            
            # Pick the first recommended next workflow
            next_wf = next_workflows[0]
            if next_wf not in chain:  # Avoid cycles
                chain.append(next_wf)
                current = next_wf
            else:
                break
        
        return chain
    
    def get_all_chains(self) -> list[WorkflowChain]:
        """Get all predefined workflow chains."""
        return list(self.chains.values())
    
    def format_chain_info(self, chain: WorkflowChain) -> str:
        """Format a chain as a readable string."""
        return f"{chain.description}\n  Sequence: {' → '.join(chain.sequence)}"
