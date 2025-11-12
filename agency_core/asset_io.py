"""
Asset IO - File operations for various formats
FROZEN MODULE - Pure stdlib, no external dependencies
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def read_file(path: Union[str, Path], encoding: str = 'utf-8') -> str:
    """Read text file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding=encoding)


def write_file(path: Union[str, Path], content: str, encoding: str = 'utf-8') -> None:
    """Write text file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)


def read_image(path: Union[str, Path]) -> bytes:
    """Read image file as bytes."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    return path.read_bytes()


def write_image(path: Union[str, Path], data: bytes) -> None:
    """Write image file from bytes."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def read_csv(path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Read CSV file as list of dictionaries."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")

    with path.open('r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv(path: Union[str, Path], data: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> None:
    """Write CSV file from list of dictionaries."""
    if not data:
        return

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if fieldnames is None:
        fieldnames = list(data[0].keys())

    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def read_json(path: Union[str, Path]) -> Any:
    """Read JSON file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"JSON not found: {path}")

    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: Union[str, Path], data: Any, indent: int = 2) -> None:
    """Write JSON file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def write_pdf(path: Union[str, Path], content: bytes) -> None:
    """Write PDF file from bytes."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def read_pdf(path: Union[str, Path]) -> bytes:
    """Read PDF file as bytes."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {path}")
    return path.read_bytes()
