"""Provider capability registry for multi-target generation.

Defines the compatibility surfaces supported by each provider target so the
rest of the generation layer can make decisions without scattered provider
conditionals.
"""

from dataclasses import dataclass, field
from enum import StrEnum


class ProviderTarget(StrEnum):
    """Supported provider targets for generation."""

    CODEX = "codex"
    GEMINI = "gemini"
    HERMES = "hermes"
    CLAUDE = "claude"
    COPILOT = "copilot"
    VSCODE = "vscode"
    PI = "pi"
    KILO = "kilo"


class ArtifactFormat(StrEnum):
    """File format used by a provider surface."""

    MARKDOWN = "markdown"
    MARKDOWN_FRONTMATTER = "markdown_frontmatter"
    TOML = "toml"


@dataclass(frozen=True)
class ProviderCapabilities:
    """Describes the compatibility surfaces supported by a provider target."""

    provider: ProviderTarget
    instruction_files: tuple[str, ...] = ()
    supports_instruction_frontmatter: bool = False
    skill_format: ArtifactFormat | None = None
    skill_extensions: tuple[str, ...] = ()
    agent_format: ArtifactFormat | None = None
    agent_required_fields: tuple[str, ...] = ()
    supports_identity_file: bool = False
    identity_filename: str | None = None
    supports_path_scoped_rules: bool = False
    output_locations: dict[str, str] = field(default_factory=dict)

    def supports_surface(self, surface: str) -> bool:
        """Return whether the provider supports a given compatibility surface."""
        return surface in self.output_locations


PROVIDER_CAPABILITIES: dict[ProviderTarget, ProviderCapabilities] = {
    ProviderTarget.CODEX: ProviderCapabilities(
        provider=ProviderTarget.CODEX,
        instruction_files=("AGENTS.md",),
        skill_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        skill_extensions=("openai-metadata",),
        agent_format=ArtifactFormat.TOML,
        agent_required_fields=("name", "description", "developer_instructions"),
        output_locations={
            "project_instructions": "AGENTS.md",
            "skills": ".agents/skills",
            "agents": ".codex/agents",
        },
    ),
    ProviderTarget.GEMINI: ProviderCapabilities(
        provider=ProviderTarget.GEMINI,
        instruction_files=("GEMINI.md", "AGENTS.md"),
        skill_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_required_fields=("name", "description"),
        output_locations={
            "project_instructions": "GEMINI.md",
            "skills": ".agents/skills",
            "agents": ".gemini/agents",
        },
    ),
    ProviderTarget.HERMES: ProviderCapabilities(
        provider=ProviderTarget.HERMES,
        instruction_files=(".hermes.md", "AGENTS.md"),
        skill_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        skill_extensions=("hermes-metadata",),
        supports_identity_file=True,
        identity_filename="SOUL.md",
        output_locations={
            "project_instructions": ".hermes.md",
            "identity": "SOUL.md",
            "skills": ".agents/skills",
        },
    ),
    ProviderTarget.CLAUDE: ProviderCapabilities(
        provider=ProviderTarget.CLAUDE,
        instruction_files=("CLAUDE.md",),
        skill_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_required_fields=("name", "description"),
        output_locations={
            "project_instructions": "CLAUDE.md",
            "skills": ".agents/skills",
            "agents": ".claude/agents",
        },
    ),
    ProviderTarget.COPILOT: ProviderCapabilities(
        provider=ProviderTarget.COPILOT,
        instruction_files=("AGENTS.md",),
        skill_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_required_fields=("name", "description", "tools"),
        supports_path_scoped_rules=True,
        output_locations={
            "project_instructions": "AGENTS.md",
            "skills": ".agents/skills",
            "agents": ".github/agents",
            "rules": ".github/instructions",
        },
    ),
    ProviderTarget.VSCODE: ProviderCapabilities(
        provider=ProviderTarget.VSCODE,
        instruction_files=("AGENTS.md",),
        skill_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_required_fields=("name", "description", "tools"),
        supports_path_scoped_rules=True,
        output_locations={
            "project_instructions": "AGENTS.md",
            "skills": ".agents/skills",
            "agents": ".github/agents",
            "rules": ".github/instructions",
        },
    ),
    ProviderTarget.PI: ProviderCapabilities(
        provider=ProviderTarget.PI,
        skill_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        output_locations={
            "skills": ".agents/skills",
        },
    ),
    ProviderTarget.KILO: ProviderCapabilities(
        provider=ProviderTarget.KILO,
        instruction_files=(),
        skill_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_format=ArtifactFormat.MARKDOWN_FRONTMATTER,
        agent_required_fields=("description",),
        output_locations={
            "modes": ".kilocode/custom_modes.yaml",
            "skills": ".kilocode/skills",
            "agents": ".kilo/agents",
            "rules": ".kilocode/rules",
        },
    ),
}


def get_provider_capabilities(provider: ProviderTarget | str) -> ProviderCapabilities:
    """Return the capabilities for the requested provider target."""
    target = provider if isinstance(provider, ProviderTarget) else ProviderTarget(provider)
    return PROVIDER_CAPABILITIES[target]
