"""Provider-native emitters for canonical compatibility surfaces."""

from pathlib import Path

import yaml

from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.models.generation import GenerationTarget
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
