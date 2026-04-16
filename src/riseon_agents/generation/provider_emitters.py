"""Provider-native emitters for canonical compatibility surfaces."""

from pathlib import Path
from typing import Any

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
    """Render a Codex TOML manifest using only Codex-compatible structures."""
    lines = [
        f"name = {_toml_string(agent_profile.name)}",
        f"description = {_toml_string(agent_profile.description)}",
        f"developer_instructions = {_toml_string(agent_profile.prompt)}",
    ]
    if agent_profile.model:
        lines.append(f"model = {_toml_string(agent_profile.model)}")

    provider_extensions = agent_profile.provider_extensions

    if isinstance(
        nickname_candidates := provider_extensions.get("nickname_candidates"), list
    ) and all(isinstance(candidate, str) for candidate in nickname_candidates):
        lines.append(f"nickname_candidates = {_toml_list(nickname_candidates)}")

    if isinstance(reasoning_effort := provider_extensions.get("model_reasoning_effort"), str):
        lines.append(f"model_reasoning_effort = {_toml_string(reasoning_effort)}")

    if isinstance(sandbox_mode := provider_extensions.get("sandbox_mode"), str):
        lines.append(f"sandbox_mode = {_toml_string(sandbox_mode)}")

    if (approval_policy := provider_extensions.get("approval_policy")) is not None:
        if isinstance(approval_policy, str):
            lines.append(f"approval_policy = {_toml_string(approval_policy)}")
        elif isinstance(approval_policy, dict):
            lines.append("")
            lines.append("[approval_policy]")
            _append_toml_mapping(lines, approval_policy, parent_key="approval_policy")

    if isinstance(approvals_reviewer := provider_extensions.get("approvals_reviewer"), str):
        lines.append(f"approvals_reviewer = {_toml_string(approvals_reviewer)}")

    if isinstance(default_permissions := provider_extensions.get("default_permissions"), str):
        lines.append(f"default_permissions = {_toml_string(default_permissions)}")

    if isinstance(allow_login_shell := provider_extensions.get("allow_login_shell"), bool):
        lines.append(f"allow_login_shell = {_toml_bool(allow_login_shell)}")

    if isinstance(web_search := provider_extensions.get("web_search"), bool):
        lines.append(f"web_search = {_toml_bool(web_search)}")

    for top_level_table in (
        "sandbox_workspace_write",
        "mcp_servers",
        "skills",
        "permissions",
        "features",
    ):
        value = provider_extensions.get(top_level_table)
        if isinstance(value, dict) and value:
            lines.append("")
            lines.append(f"[{top_level_table}]")
            _append_toml_mapping(lines, value, parent_key=top_level_table)

    return "\n".join(lines).rstrip() + "\n"


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


def _toml_bool(value: bool) -> str:
    """Render a TOML boolean."""
    return "true" if value else "false"


def _toml_value(value: Any) -> str:
    """Render a TOML scalar or inline value."""
    if isinstance(value, bool):
        return _toml_bool(value)
    if isinstance(value, int | float):
        return str(value)
    if isinstance(value, str):
        return _toml_string(value)
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return _toml_list(value)
    if isinstance(value, dict):
        items: list[str] = []
        for key, item in value.items():
            if not isinstance(key, str):
                continue
            items.append(f"{key} = {_toml_value(item)}")
        return "{ " + ", ".join(items) + " }"
    raise TypeError(f"Unsupported TOML value type: {type(value).__name__}")


def _append_toml_mapping(lines: list[str], mapping: dict[str, Any], parent_key: str) -> None:
    """Append TOML key-values or nested tables for a mapping."""
    scalar_items: list[tuple[str, Any]] = []
    nested_mappings: list[tuple[str, dict[str, Any]]] = []
    array_tables: list[tuple[str, list[dict[str, Any]]]] = []

    for key, value in mapping.items():
        if not isinstance(key, str):
            continue
        if isinstance(value, dict):
            nested_mappings.append((key, value))
        elif isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
            array_tables.append((key, value))
        else:
            scalar_items.append((key, value))

    for key, value in scalar_items:
        lines.append(f"{key} = {_toml_value(value)}")

    for key, nested in nested_mappings:
        lines.append("")
        lines.append(f"[{parent_key}.{key}]")
        _append_toml_mapping(lines, nested, parent_key=f"{parent_key}.{key}")

    for key, entries in array_tables:
        for entry in entries:
            lines.append("")
            lines.append(f"[[{parent_key}.{key}]]")
            _append_toml_mapping(lines, entry, parent_key=f"{parent_key}.{key}")


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
