"""Canonical model for provider-specific identity content."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class IdentitySpec:
    """Provider-agnostic identity or persona content."""

    name: str
    body: str
    metadata: dict[str, str] = field(default_factory=dict)
    source_path: Path | None = None
