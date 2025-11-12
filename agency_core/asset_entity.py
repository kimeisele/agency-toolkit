"""
Asset Entity - CRUD operations for assets
FROZEN MODULE - Pure stdlib
"""

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Asset:
    """Base asset entity."""
    id: str
    type: str
    data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = asdict(self)
        result['created_at'] = self.created_at.isoformat()
        result['updated_at'] = self.updated_at.isoformat()
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Asset':
        """Create from dictionary."""
        data = data.copy()
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


class AssetRegistry:
    """Registry for asset entities."""

    def __init__(self):
        self._assets: Dict[str, Asset] = {}

    def create(self, asset_type: str, data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Asset:
        """Create a new asset."""
        now = datetime.utcnow()
        asset = Asset(
            id=str(uuid.uuid4()),
            type=asset_type,
            data=data,
            created_at=now,
            updated_at=now,
            metadata=metadata or {}
        )
        self._assets[asset.id] = asset
        return asset

    def get(self, asset_id: str) -> Optional[Asset]:
        """Get asset by ID."""
        return self._assets.get(asset_id)

    def update(self, asset_id: str, data: Dict[str, Any]) -> Optional[Asset]:
        """Update asset data."""
        asset = self._assets.get(asset_id)
        if not asset:
            return None

        asset.data.update(data)
        asset.updated_at = datetime.utcnow()
        return asset

    def delete(self, asset_id: str) -> bool:
        """Delete asset by ID."""
        if asset_id in self._assets:
            del self._assets[asset_id]
            return True
        return False

    def list_by_type(self, asset_type: str) -> List[Asset]:
        """List all assets of a specific type."""
        return [a for a in self._assets.values() if a.type == asset_type]

    def list_all(self) -> List[Asset]:
        """List all assets."""
        return list(self._assets.values())


# Global registry
_registry = AssetRegistry()


def create_asset(asset_type: str, data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> Asset:
    """Create a new asset."""
    return _registry.create(asset_type, data, metadata)


def get_asset(asset_id: str) -> Optional[Asset]:
    """Get asset by ID."""
    return _registry.get(asset_id)


def update_asset(asset_id: str, data: Dict[str, Any]) -> Optional[Asset]:
    """Update asset data."""
    return _registry.update(asset_id, data)


def delete_asset_entity(asset_id: str) -> bool:
    """Delete asset by ID."""
    return _registry.delete(asset_id)


def list_assets_by_type(asset_type: str) -> List[Asset]:
    """List all assets of a specific type."""
    return _registry.list_by_type(asset_type)


def list_all_assets() -> List[Asset]:
    """List all assets."""
    return _registry.list_all()
