"""Codex-specific emitter for agent manifests in TOML format."""

from pathlib import Path
import toml
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.models.generation import GenerationTarget


def emit_codex_agent_manifest(
    target: GenerationTarget,
    agent_profile: AgentProfile,
    provider: ProviderTarget,
) -> Path:
    """Emit a Codex agent manifest as a TOML file at the appropriate path."""
    if provider != ProviderTarget.CODEX:
        raise ValueError(f"Unsupported provider for agent manifest: {provider}")

    output_path = target.provider_output_path(provider, "agents") / f"{agent_profile.name}.toml"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    agent_data = {
        "name": agent_profile.name,
        "description": agent_profile.description,
        "developer_instructions": agent_profile.prompt,
        "tools": agent_profile.tools,
        "mcp_servers": agent_profile.mcp_servers,
        "model": agent_profile.model,
        "max_turns": agent_profile.max_turns,
        "temperature": agent_profile.temperature,
        "permissions": agent_profile.permissions,
    }

    with open(output_path, "w") as f:
        toml.dump(agent_data, f)

    return output_path