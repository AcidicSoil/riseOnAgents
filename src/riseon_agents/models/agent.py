"""Agent data models for RiseOn.Agents.

Defines the PrimaryAgent and Subagent dataclasses that represent agent definitions
parsed from the agents/ folder.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class PermissionLevel(Enum):
    """Permission level for agent capabilities."""

    ALLOW = "allow"
    ASK = "ask"
    DENY = "deny"


@dataclass
class PrimaryAgent:
    """Primary agent definition (maps to Kilo Code Custom Mode).

    Represents a top-level agent that can have subagents, rules, and skills.
    Parsed from {agent-name}/{agent-name}.agent.md files.
    """

    # Identity
    name: str  # Unique identifier (slug)
    description: str  # Short description for UI

    # Content
    markdown_body: str  # Instructions (becomes roleDefinition)

    # Configuration
    tools: list[str] = field(default_factory=list)
    temperature: float = 0.1
    steps: int = 40
    permissions: dict[str, PermissionLevel] = field(default_factory=dict)
    handoffs: list[str] = field(default_factory=list)  # subagent names

    # Children
    subagents: list[Subagent] = field(default_factory=list)
    rules: list[Rule] = field(default_factory=list)
    skills: list[Skill] = field(default_factory=list)

    # Metadata
    source_path: Path | None = None

    @property
    def slug(self) -> str:
        """Generate Kilo Code compatible slug."""
        return self.name.lower().replace("_", "-")

    @property
    def display_name(self) -> str:
        """Generate human-readable display name."""
        return self.name.replace("-", " ").replace("_", " ").title()

    def __post_init__(self) -> None:
        """Validate agent data after initialization."""
        if not self.name:
            raise ValueError("Agent name cannot be empty")
        if not self.description:
            raise ValueError("Agent description cannot be empty")
        if not self.markdown_body:
            raise ValueError("Agent markdown_body cannot be empty")


@dataclass
class Subagent:
    """Subagent definition (maps to Kilo Code Custom Subagent).

    Represents a specialized agent invoked by primary agents.
    Parsed from {agent-name}/subagents/*.agent.md files.
    """

    # Identity
    name: str  # Unique identifier
    description: str  # What the agent does

    # Content
    markdown_body: str  # System prompt instructions

    # Configuration
    tools: list[str] = field(default_factory=list)
    temperature: float = 0.1
    steps: int = 15
    permissions: dict[str, PermissionLevel] = field(default_factory=dict)
    model_variant: str | None = None  # e.g., "high", "low", "medium"
    target: str = "opencode"  # Target platform

    # Metadata
    source_path: Path | None = None
    parent_agent: str | None = None  # Name of parent primary agent

    @property
    def slug(self) -> str:
        """Generate Kilo Code compatible slug."""
        return self.name.lower().replace("_", "-")

    @property
    def display_name(self) -> str:
        """Generate human-readable display name."""
        return self.name.replace("-", " ").replace("_", " ").title()

    def __post_init__(self) -> None:
        """Validate subagent data after initialization."""
        if not self.name:
            raise ValueError("Subagent name cannot be empty")
        if not self.description:
            raise ValueError("Subagent description cannot be empty")
        if not self.markdown_body:
            raise ValueError("Subagent markdown_body cannot be empty")
        if self.model_variant is not None and self.model_variant not in (
            "high",
            "low",
            "medium",
        ):
            raise ValueError(
                f"Invalid model_variant '{self.model_variant}'. "
                "Must be 'high', 'low', 'medium', or None."
            )


# Forward references for type hints
from riseon_agents.models.rule import Rule as Rule  # noqa: E402, F401
from riseon_agents.models.skill import Skill as Skill  # noqa: E402, F401
