"""Canonical model for project instruction documents."""

from __future__ import annotations

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
    def from_primary_agent(cls, agent: PrimaryAgent) -> ProjectInstructions:
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

    @classmethod
    def from_primary_agents(cls, agents: list[PrimaryAgent]) -> ProjectInstructions:
        """Create a single repository-wide instruction surface from primary agents."""
        if not agents:
            raise ValueError("At least one primary agent is required to build project instructions")

        if len(agents) == 1:
            return cls.from_primary_agent(agents[0])

        sections: list[str] = ["# Project Instructions", ""]
        metadata = {
            "source": "primary-agents",
            "agent_count": str(len(agents)),
        }

        for agent in agents:
            sections.append(f"## {agent.display_name}")
            sections.append("")
            sections.append(agent.markdown_body.strip())
            sections.append("")

        return cls(
            name="project-instructions",
            description="Repository-wide instructions aggregated from primary agents",
            body="\n".join(sections).rstrip(),
            metadata=metadata,
        )
