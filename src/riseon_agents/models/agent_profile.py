"""Canonical model for provider-agnostic custom agents and subagents."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from riseon_agents.models.agent import Subagent


@dataclass(frozen=True)
class AgentProfile:
    """Provider-agnostic representation of an agent manifest."""

    name: str
    description: str
    prompt: str
    tools: list[str] = field(default_factory=list)
    mcp_servers: list[str] = field(default_factory=list)
    model: str | None = None
    max_turns: int | None = None
    temperature: float | None = None
    permissions: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, str] = field(default_factory=dict)
    source_path: Path | None = None
    provider_extensions: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_subagent(cls, subagent: Subagent) -> "AgentProfile":
        """Create a canonical agent profile from a subagent."""
        metadata = {"source": "subagent", "target": subagent.target}
        if subagent.parent_agent is not None:
            metadata["parent_agent"] = subagent.parent_agent

        return cls(
            name=subagent.name,
            description=subagent.description,
            prompt=subagent.markdown_body,
            tools=list(subagent.tools),
            model=subagent.model_variant,
            max_turns=subagent.steps,
            temperature=subagent.temperature,
            permissions={key: value.value for key, value in subagent.permissions.items()},
            metadata=metadata,
            source_path=subagent.source_path,
        )
