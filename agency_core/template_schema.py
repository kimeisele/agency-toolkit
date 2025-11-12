"""
Template Schema - Define and validate data structures
FROZEN MODULE - Pure stdlib
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Type


@dataclass
class FieldDefinition:
    """Field definition in a template."""
    name: str
    type: Type
    required: bool = True
    default: Any = None
    description: str = ""


@dataclass
class TemplateDefinition:
    """Template definition."""
    name: str
    fields: List[FieldDefinition]
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class TemplateRegistry:
    """Registry for template definitions."""

    def __init__(self):
        self._templates: Dict[str, TemplateDefinition] = {}

    def register(self, template: TemplateDefinition) -> None:
        """Register a template."""
        self._templates[template.name] = template

    def get(self, name: str) -> Optional[TemplateDefinition]:
        """Get template by name."""
        return self._templates.get(name)

    def list(self) -> List[str]:
        """List all template names."""
        return list(self._templates.keys())

    def validate(self, template_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate data against template.
        Returns dict with 'valid' bool and 'errors' list.
        """
        template = self.get(template_name)
        if not template:
            return {
                'valid': False,
                'errors': [f"Template '{template_name}' not found"]
            }

        errors = []

        for field_def in template.fields:
            # Check required fields
            if field_def.required and field_def.name not in data:
                errors.append(f"Required field '{field_def.name}' missing")
                continue

            # Check type if value present
            if field_def.name in data:
                value = data[field_def.name]
                if value is not None and not isinstance(value, field_def.type):
                    errors.append(
                        f"Field '{field_def.name}' expects {field_def.type.__name__}, "
                        f"got {type(value).__name__}"
                    )

        return {
            'valid': len(errors) == 0,
            'errors': errors
        }


# Global registry
_registry = TemplateRegistry()


def define_template(
    name: str,
    fields: List[Dict[str, Any]],
    description: str = "",
    metadata: Optional[Dict[str, Any]] = None
) -> TemplateDefinition:
    """
    Define a new template.

    Args:
        name: Template name
        fields: List of field definitions, each with 'name', 'type', 'required', 'default', 'description'
        description: Template description
        metadata: Additional metadata
    """
    field_defs = []
    for f in fields:
        field_defs.append(FieldDefinition(
            name=f['name'],
            type=f.get('type', str),
            required=f.get('required', True),
            default=f.get('default'),
            description=f.get('description', '')
        ))

    template = TemplateDefinition(
        name=name,
        fields=field_defs,
        description=description,
        metadata=metadata or {}
    )

    _registry.register(template)
    return template


def validate_template_data(template_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate data against a template."""
    return _registry.validate(template_name, data)


def get_template(name: str) -> Optional[TemplateDefinition]:
    """Get template definition by name."""
    return _registry.get(name)


def list_templates() -> List[str]:
    """List all registered template names."""
    return _registry.list()
