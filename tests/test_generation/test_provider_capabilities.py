"""Tests for the provider capability registry."""

from riseon_agents.generation import ArtifactFormat, ProviderTarget, get_provider_capabilities


class TestProviderCapabilities:
    """Tests for provider capability metadata."""

    def test_codex_uses_toml_agents(self) -> None:
        """Codex should expose TOML custom-agent support."""
        capabilities = get_provider_capabilities(ProviderTarget.CODEX)

        assert capabilities.instruction_files == ("AGENTS.md",)
        assert capabilities.agent_format == ArtifactFormat.TOML
        assert capabilities.output_locations["agents"] == ".codex/agents"
        assert capabilities.agent_required_fields == (
            "name",
            "description",
            "developer_instructions",
        )

    def test_hermes_identity_is_separate_surface(self) -> None:
        """Hermes should declare separate identity support."""
        capabilities = get_provider_capabilities("hermes")

        assert capabilities.supports_identity_file is True
        assert capabilities.identity_filename == "SOUL.md"
        assert capabilities.output_locations["project_instructions"] == ".hermes.md"
        assert capabilities.supports_surface("identity") is True

    def test_pi_only_declares_skill_surface(self) -> None:
        """Pi support should remain skill-only until more is verified."""
        capabilities = get_provider_capabilities(ProviderTarget.PI)

        assert capabilities.skill_format == ArtifactFormat.MARKDOWN_FRONTMATTER
        assert capabilities.output_locations == {"skills": ".agents/skills"}
        assert capabilities.agent_format is None
        assert capabilities.supports_identity_file is False
