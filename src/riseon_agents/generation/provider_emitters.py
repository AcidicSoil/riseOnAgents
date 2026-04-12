"""Provider-native emitters for canonical compatibility surfaces."""

from pathlib import Path

import yaml

from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.models.generation import GenerationTarget
from riseon_agents.models.identity_spec import IdentitySpec
from riseon_agents.models.project_instructions import ProjectInstructions
from riseon_agents.models.skill_spec import SkillSpec


def emit_project_instructions(
    target: GenerationTarget,
    project_instructions: ProjectInstructions,
    provider: ProviderTarget,
) -> Path:
    """Emit provider-native project instructions as plain markdown."""
    output_path = target.provider_output_path(provider, "project_instructions")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(project_instructions.body.rstrip() + "\n", encoding="utf-8")
    return output_path


def emit_skill_surface(
    target: GenerationTarget,
    skill: SkillSpec,
    provider: ProviderTarget,
) -> Path:
    """Emit canonical SKILL.md content for a provider-supported skill surface."""
    skills_root = target.provider_output_path(provider, "skills")
    skill_dir = skills_root / skill.name
    skill_dir.mkdir(parents=True, exist_ok=True)

    output_path = skill_dir / "SKILL.md"
    output_path.write_text(_render_skill_markdown(skill), encoding="utf-8")
    return output_path


def emit_codex_agent_manifest(
    target: GenerationTarget,
    agent_profile: AgentProfile,
    provider: ProviderTarget,
) -> Path:
    """Emit a Codex-native TOML agent manifest."""
    if provider is not ProviderTarget.CODEX:
        raise ValueError(f"Unsupported provider for Codex agent manifest: {provider.value}")

    agents_root = target.provider_output_path(provider, "agents")
    output_path = agents_root / f"{agent_profile.name}.toml"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(_render_codex_agent_toml(agent_profile), encoding="utf-8")
    return output_path


def emit_gemini_agent_manifest(
    target: GenerationTarget,
    agent_profile: AgentProfile,
    provider: ProviderTarget,
) -> Path:
    """Emit a Gemini-native markdown agent manifest with YAML frontmatter."""
    if provider is not ProviderTarget.GEMINI:
        raise ValueError(f"Unsupported provider for Gemini agent manifest: {provider.value}")

    agents_root = target.provider_output_path(provider, "agents")
    output_path = agents_root / f"{agent_profile.name}.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(_render_gemini_agent_markdown(agent_profile), encoding="utf-8")
    return output_path


def emit_hermes_identity(
    target: GenerationTarget,
    identity: IdentitySpec,
    provider: ProviderTarget,
) -> Path:
    """Emit a Hermes-native identity file."""
    if provider is not ProviderTarget.HERMES:
        raise ValueError(f"Unsupported provider for Hermes identity: {provider.value}")

    output_path = target.provider_output_path(provider, "identity")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(identity.body.rstrip() + "\n", encoding="utf-8")
    return output_path


def _render_codex_agent_toml(agent_profile: AgentProfile) -> str:
    """Render a minimal TOML manifest for a Codex agent profile."""
    lines = [
        f'name = {_toml_string(agent_profile.name)}',
        f'description = {_toml_string(agent_profile.description)}',
        f'developer_instructions = {_toml_string(agent_profile.prompt)}',
    ]
    if agent_profile.tools:
        lines.append(f"tools = {_toml_list(agent_profile.tools)}")
    if agent_profile.mcp_servers:
        lines.append(f"mcp_servers = {_toml_list(agent_profile.mcp_servers)}")
    if agent_profile.model:
        lines.append(f'model = {_toml_string(agent_profile.model)}')
    if agent_profile.max_turns is not None:
        lines.append(f"max_turns = {agent_profile.max_turns}")
    if agent_profile.temperature is not None:
        lines.append(f"temperature = {agent_profile.temperature}")
    if agent_profile.permissions:
        lines.append("[permissions]")
        for key, value in agent_profile.permissions.items():
            lines.append(f"{key} = {_toml_string(value)}")

    return "\n".join(lines) + "\n"


def _render_gemini_agent_markdown(agent_profile: AgentProfile) -> str:
    """Render a Gemini markdown agent manifest with YAML frontmatter."""
    frontmatter: dict[str, object] = {
        "name": agent_profile.name,
        "description": agent_profile.description,
    }
    if agent_profile.tools:
        frontmatter["tools"] = agent_profile.tools
    if agent_profile.mcp_servers:
        frontmatter["mcpServers"] = agent_profile.mcp_servers
    if agent_profile.model:
        frontmatter["model"] = agent_profile.model
    if agent_profile.temperature is not None:
        frontmatter["temperature"] = agent_profile.temperature
    if agent_profile.max_turns is not None:
        frontmatter["max_turns"] = agent_profile.max_turns

    yaml_frontmatter = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    return f"---\n{yaml_frontmatter}\n---\n\n{agent_profile.prompt.rstrip()}\n"


def _toml_string(value: str) -> str:
    """Render a TOML basic string."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{escaped}"'


def _toml_list(values: list[str]) -> str:
    """Render a TOML array of strings."""
    rendered = ", ".join(_toml_string(value) for value in values)
    return f"[{rendered}]"


def _render_skill_markdown(skill: SkillSpec) -> str:
    """Render a canonical Agent-Skills-compatible SKILL.md file."""
    body = skill.body.strip()
    if body.startswith("---"):
        return body + "\n"

    frontmatter: dict[str, object] = {
        "name": skill.name,
        "description": skill.description,
    }
    if skill.license:
        frontmatter["license"] = skill.license
    if skill.tools:
        frontmatter["tools"] = skill.tools
    if skill.model:
        frontmatter["model"] = skill.model
    if skill.context:
        frontmatter["context"] = skill.context
    if skill.allowed_tools:
        frontmatter["allowed_tools"] = skill.allowed_tools
    if skill.disable_model_invocation:
        frontmatter["disable_model_invocation"] = skill.disable_model_invocation
    if skill.references:
        frontmatter["references"] = skill.references
    if skill.scripts:
        frontmatter["scripts"] = skill.scripts
    if skill.metadata:
        frontmatter["metadata"] = skill.metadata

    yaml_frontmatter = yaml.safe_dump(frontmatter, sort_keys=False).strip()
    return f"---\n{yaml_frontmatter}\n---\n\n{body}\n"
