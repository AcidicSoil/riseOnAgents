"""Skill data model for RiseOn.Agents.

Defines the Skill dataclass that represents reusable knowledge modules.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Skill:
    """Skill definition (maps to Kilo Code Skills).

    Represents a reusable knowledge module.
    Parsed from {agent-name}/skills/*/SKILL.md files.
    """

    # Identity (from SKILL.md frontmatter)
    name: str  # Max 64 chars, [a-z0-9-]+
    description: str  # Max 1024 chars

    # Content
    content: str  # Full SKILL.md content including frontmatter

    # Optional metadata
    license: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)

    # Resources
    has_scripts: bool = False  # Has scripts/ directory
    has_references: bool = False  # Has references/ directory
    has_assets: bool = False  # Has assets/ directory

    # Metadata
    source_path: Path | None = None  # Path to SKILL.md
    source_dir: Path | None = None  # Path to skill directory

    # Validation pattern for skill names
    _NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

    def __post_init__(self) -> None:
        """Validate skill data after initialization."""
        if not self.name:
            raise ValueError("Skill name cannot be empty")
        if len(self.name) > 64:
            raise ValueError(f"Skill name must be <= 64 chars, got {len(self.name)}")
        if not self._NAME_PATTERN.match(self.name):
            raise ValueError(
                f"Skill name '{self.name}' must match pattern [a-z0-9-]+ "
                "and not start or end with hyphen"
            )
        if self.name.startswith("-") or self.name.endswith("-"):
            raise ValueError(f"Skill name '{self.name}' must not start or end with hyphen")
        if not self.description:
            raise ValueError("Skill description cannot be empty")
        if len(self.description) > 1024:
            raise ValueError(
                f"Skill description must be <= 1024 chars, got {len(self.description)}"
            )

    @property
    def dir_name(self) -> str:
        """Get the directory name for this skill."""
        return self.name
