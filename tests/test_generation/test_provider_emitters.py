"""Tests for provider emitters: skills and project instructions surfaces."""

from pathlib import Path

from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.generation.provider_emitters import (
    emit_project_instructions,
    emit_skill_surface,
)
from riseon_agents.models.generation import GenerationTarget
from riseon_agents.models.project_instructions import ProjectInstructions
from riseon_agents.models.skill_spec import SkillSpec


class TestProviderEmitters:
    """Tests for the generation of provider-specific skill and project instruction outputs."""

    def test_emit_skill_surface(self, temp_dir: Path) -> None:
        """Skill surfaces should emit canonical SKILL.md files under provider skill roots."""
        skill = SkillSpec(
            name="test-skill",
            description="Test skill description",
            body="# Test Skill Body",
            metadata={"author": "Test Author"},
        )

        target = GenerationTarget.local(temp_dir)

        output_path = emit_skill_surface(target, skill, ProviderTarget.CODEX)
        assert output_path == temp_dir / ".agents" / "skills" / "test-skill" / "SKILL.md"
        assert output_path.exists()
        content = output_path.read_text(encoding="utf-8")
        assert "name: test-skill" in content
        assert "description: Test skill description" in content
        assert "# Test Skill Body" in content

        gemini_path = emit_skill_surface(target, skill, ProviderTarget.GEMINI)
        assert gemini_path == temp_dir / ".agents" / "skills" / "test-skill" / "SKILL.md"
        assert gemini_path.exists()

    def test_emit_project_instructions(self, temp_dir: Path) -> None:
        """Project instructions should use provider-native filenames."""
        project_instructions = ProjectInstructions(
            name="test-project",
            description="Test project instructions",
            body="# Test Project Instructions Body",
            metadata={"author": "Test Author"},
        )

        target = GenerationTarget.local(temp_dir)

        codex_path = emit_project_instructions(target, project_instructions, ProviderTarget.CODEX)
        assert codex_path == temp_dir / "AGENTS.md"
        assert codex_path.exists()
        assert codex_path.read_text(encoding="utf-8") == "# Test Project Instructions Body\n"

        gemini_path = emit_project_instructions(target, project_instructions, ProviderTarget.GEMINI)
        assert gemini_path == temp_dir / "GEMINI.md"
        assert gemini_path.exists()

        hermes_path = emit_project_instructions(target, project_instructions, ProviderTarget.HERMES)
        assert hermes_path == temp_dir / ".hermes.md"
        assert hermes_path.exists()
