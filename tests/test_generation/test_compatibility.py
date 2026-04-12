"""Tests for provider-native compatibility generation."""

from pathlib import Path

from riseon_agents.generation.compatibility import CompatibilityGenerator
from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.models.generation import GenerationTarget
from riseon_agents.models.project_instructions import ProjectInstructions
from riseon_agents.models.skill_spec import SkillSpec


class TestCompatibilityGenerator:
    """Tests for compatibility surface generation."""

    def test_generate_multi_provider_project_instructions_and_skills(self, temp_dir: Path) -> None:
        """A single run should emit provider-native instructions plus shared skills."""
        generator = CompatibilityGenerator()
        target = GenerationTarget.local(temp_dir)

        instructions = [
            ProjectInstructions(
                name="test-project",
                description="Test project instructions",
                body="# Project Instructions",
            )
        ]
        skills = [
            SkillSpec(
                name="test-skill",
                description="Test skill description",
                body="# Skill Body",
            )
        ]

        result = generator.generate(
            target=target,
            providers=[ProviderTarget.CODEX, ProviderTarget.GEMINI, ProviderTarget.HERMES],
            project_instructions=instructions,
            skills=skills,
        )

        assert result.error_count == 0
        paths = {generated.path for generated in result.files}
        assert temp_dir / "AGENTS.md" in paths
        assert temp_dir / "GEMINI.md" in paths
        assert temp_dir / ".hermes.md" in paths
        assert temp_dir / ".agents" / "skills" / "test-skill" / "SKILL.md" in paths

    def test_generate_reports_unsupported_surface(self, temp_dir: Path) -> None:
        """Providers without a surface should produce a clear error entry."""
        generator = CompatibilityGenerator()
        target = GenerationTarget.local(temp_dir)

        instructions = [
            ProjectInstructions(
                name="test-project",
                description="Test project instructions",
                body="# Project Instructions",
            )
        ]

        result = generator.generate(
            target=target,
            providers=[ProviderTarget.PI],
            project_instructions=instructions,
            skills=[],
        )

        assert result.error_count == 1
        assert result.files[0].error_message == (
            "Provider 'pi' does not support project instructions"
        )
