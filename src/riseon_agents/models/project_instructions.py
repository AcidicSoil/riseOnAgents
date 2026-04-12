"""Canonical model for project instruction documents."""

from dataclasses import dataclass, field
from pathlib import Path

from riseon_agents.models.agent import PrimaryAgent


@dataclass(frozen=True)
class ProjectInstructions:
    """Provider-agnostic project instruction content."""

    name: str
    description: str
    body: str
    metadata: dict[str, str] = field(default_factory=dict)
    source_path: Path | None = None

    @classmethod
    def from_primary_agent(cls, agent: PrimaryAgent) -> "ProjectInstructions":
        """Create canonical project instructions from a primary agent."""
        metadata = {"source": "primary-agent"}
        if agent.source_path is not None:
            metadata["source_path"] = str(agent.source_path)

        return cls(
            name=agent.name,
            description=agent.description,
            body=agent.markdown_body,
            metadata=metadata,
            source_path=agent.source_path,
        )
