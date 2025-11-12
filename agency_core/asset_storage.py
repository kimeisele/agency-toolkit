"""
Asset Storage - In-memory key-value store with persistence
FROZEN MODULE - Pure stdlib
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class AssetStore:
    """Thread-safe in-memory asset storage."""

    def __init__(self, storage_path: Optional[Path] = None):
        self._storage: Dict[str, Any] = {}
        self._storage_path = storage_path or Path('.agency_storage.json')
        self._load()

    def _load(self) -> None:
        """Load storage from disk."""
        if self._storage_path.exists():
            try:
                with self._storage_path.open('r') as f:
                    self._storage = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._storage = {}

    def _save(self) -> None:
        """Save storage to disk."""
        try:
            with self._storage_path.open('w') as f:
                json.dump(self._storage, f, indent=2, default=str)
        except IOError:
            pass  # Fail silently on write errors

    def store(self, key: str, value: Any) -> None:
        """Store asset by key."""
        self._storage[key] = value
        self._save()

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve asset by key."""
        return self._storage.get(key)

    def delete(self, key: str) -> bool:
        """Delete asset by key. Returns True if deleted."""
        if key in self._storage:
            del self._storage[key]
            self._save()
            return True
        return False

    def list(self, prefix: str = '') -> List[str]:
        """List all keys with optional prefix filter."""
        if prefix:
            return [k for k in self._storage.keys() if k.startswith(prefix)]
        return list(self._storage.keys())

    def clear(self) -> None:
        """Clear all storage."""
        self._storage.clear()
        self._save()


# Global store instance
_store = AssetStore()


def store_asset(key: str, asset: Any) -> None:
    """Store an asset."""
    _store.store(key, asset)


def retrieve_asset(key: str) -> Optional[Any]:
    """Retrieve an asset."""
    return _store.retrieve(key)


def delete_asset(key: str) -> bool:
    """Delete an asset."""
    return _store.delete(key)


def list_assets(prefix: str = '') -> List[str]:
    """List all asset keys."""
    return _store.list(prefix)


def clear_storage() -> None:
    """Clear all storage."""
    _store.clear()
