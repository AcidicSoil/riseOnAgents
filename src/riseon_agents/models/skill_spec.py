"""Canonical model for provider-agnostic skill definitions."""

from dataclasses import dataclass, field
from pathlib import Path

from riseon_agents.models.skill import Skill


@dataclass(frozen=True)
class SkillSpec:
    """Provider-agnostic representation of a reusable skill."""

    name: str
    description: str
    body: str
    license: str | None = None
    tools: list[str] = field(default_factory=list)
    model: str | None = None
    context: str | None = None
    allowed_tools: list[str] = field(default_factory=list)
    disable_model_invocation: bool = False
    references: list[str] = field(default_factory=list)
    scripts: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    source_path: Path | None = None
    source_dir: Path | None = None

    @classmethod
    def from_skill(cls, skill: Skill) -> "SkillSpec":
        """Create a canonical skill spec from the current skill model."""
        references = ["references/"] if skill.has_references else []
        scripts = ["scripts/"] if skill.has_scripts else []
        metadata = dict(skill.metadata)
        metadata.setdefault("source", "skill")

        return cls(
            name=skill.name,
            description=skill.description,
            body=skill.content,
            license=skill.license,
            references=references,
            scripts=scripts,
            metadata=metadata,
            source_path=skill.source_path,
            source_dir=skill.source_dir,
        )
