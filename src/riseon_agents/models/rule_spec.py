"""Canonical model for provider-agnostic rule definitions."""

from dataclasses import dataclass, field
from pathlib import Path

from riseon_agents.models.rule import Rule


@dataclass(frozen=True)
class RuleSpec:
    """Provider-agnostic representation of a rule surface."""

    name: str
    body: str
    apply_to: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    source_path: Path | None = None
    is_shared: bool = True
    mode_slug: str | None = None

    @classmethod
    def from_rule(cls, rule: Rule) -> "RuleSpec":
        """Create a canonical rule spec from the current rule model."""
        metadata = {"source": "rule"}
        if rule.mode_slug is not None:
            metadata["mode_slug"] = rule.mode_slug

        return cls(
            name=rule.name,
            body=rule.content,
            apply_to=rule.mode_slug,
            metadata=metadata,
            source_path=rule.source_path,
            is_shared=rule.is_shared,
            mode_slug=rule.mode_slug,
        )
