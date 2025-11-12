"""
Content Transform - Data transformations
FROZEN MODULE - Pure stdlib
"""

from typing import Any, Callable, Dict, List, Optional


class Transform:
    """Transform definition."""

    def __init__(self, name: str, source_type: str, target_type: str, func: Callable[[Any], Any]):
        self.name = name
        self.source_type = source_type
        self.target_type = target_type
        self.func = func

    def apply(self, data: Any) -> Any:
        """Apply transformation."""
        return self.func(data)


class TransformRegistry:
    """Registry for transforms."""

    def __init__(self):
        self._transforms: Dict[str, Transform] = {}

    def register(self, transform: Transform) -> None:
        """Register a transform."""
        self._transforms[transform.name] = transform

    def get(self, name: str) -> Optional[Transform]:
        """Get transform by name."""
        return self._transforms.get(name)

    def list(self) -> List[str]:
        """List all transform names."""
        return list(self._transforms.keys())

    def apply(self, transform_name: str, data: Any) -> Any:
        """Apply a transform by name."""
        transform = self.get(transform_name)
        if not transform:
            raise ValueError(f"Transform '{transform_name}' not found")
        return transform.apply(data)


# Global registry
_registry = TransformRegistry()


def define_transform(
    name: str,
    source_type: str,
    target_type: str,
    func: Callable[[Any], Any]
) -> Transform:
    """
    Define a new transform.

    Args:
        name: Transform name
        source_type: Source data type (descriptive)
        target_type: Target data type (descriptive)
        func: Transform function
    """
    transform = Transform(name, source_type, target_type, func)
    _registry.register(transform)
    return transform


def apply_transform(transform_name: str, data: Any) -> Any:
    """Apply a transform to data."""
    return _registry.apply(transform_name, data)


def get_transform(name: str) -> Optional[Transform]:
    """Get transform by name."""
    return _registry.get(name)


def list_transforms() -> List[str]:
    """List all registered transform names."""
    return _registry.list()
