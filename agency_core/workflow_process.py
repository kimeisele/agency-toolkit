"""
Workflow Process - Multi-step workflow execution
FROZEN MODULE - Pure stdlib
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class WorkflowStep:
    """Single step in a workflow."""
    name: str
    func: Callable[[Any], Any]
    description: str = ""


@dataclass
class Workflow:
    """Workflow definition."""
    name: str
    steps: List[WorkflowStep]
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def execute(self, input_data: Any) -> Any:
        """Execute workflow steps sequentially."""
        result = input_data
        for step in self.steps:
            result = step.func(result)
        return result


class WorkflowRegistry:
    """Registry for workflows."""

    def __init__(self):
        self._workflows: Dict[str, Workflow] = {}

    def register(self, workflow: Workflow) -> None:
        """Register a workflow."""
        self._workflows[workflow.name] = workflow

    def get(self, name: str) -> Optional[Workflow]:
        """Get workflow by name."""
        return self._workflows.get(name)

    def list(self) -> List[str]:
        """List all workflow names."""
        return list(self._workflows.keys())

    def execute(self, workflow_name: str, input_data: Any) -> Any:
        """Execute a workflow by name."""
        workflow = self.get(workflow_name)
        if not workflow:
            raise ValueError(f"Workflow '{workflow_name}' not found")
        return workflow.execute(input_data)


# Global registry
_registry = WorkflowRegistry()


def define_workflow(
    name: str,
    steps: List[Dict[str, Any]],
    description: str = "",
    metadata: Optional[Dict[str, Any]] = None
) -> Workflow:
    """
    Define a new workflow.

    Args:
        name: Workflow name
        steps: List of steps, each with 'name', 'func', 'description'
        description: Workflow description
        metadata: Additional metadata
    """
    workflow_steps = []
    for step_def in steps:
        workflow_steps.append(WorkflowStep(
            name=step_def['name'],
            func=step_def['func'],
            description=step_def.get('description', '')
        ))

    workflow = Workflow(
        name=name,
        steps=workflow_steps,
        description=description,
        metadata=metadata or {}
    )

    _registry.register(workflow)
    return workflow


def execute_workflow(workflow_name: str, input_data: Any) -> Any:
    """Execute a workflow."""
    return _registry.execute(workflow_name, input_data)


def get_workflow(name: str) -> Optional[Workflow]:
    """Get workflow by name."""
    return _registry.get(name)


def list_workflows() -> List[str]:
    """List all registered workflow names."""
    return _registry.list()
