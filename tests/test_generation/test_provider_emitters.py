"""Tests for provider emitters: skills and project instructions surfaces."""

from pathlib import Path

from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.generation.provider_emitters import (
    emit_codex_agent_manifest,
    emit_gemini_agent_manifest,
    emit_hermes_identity,
    emit_project_instructions,
    emit_skill_surface,
)
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.models.generation import GenerationTarget
from riseon_agents.models.identity_spec import IdentitySpec
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

    def test_emit_codex_agent_manifest(self, temp_dir: Path) -> None:
        """Codex agent manifests should use the native TOML path and fields."""
        agent_profile = AgentProfile(
            name="test-agent",
            description="Test agent description",
            prompt="# Test Agent Prompt",
            tools=["tool1", "tool2"],
            mcp_servers=["server1"],
            model="test-model",
            max_turns=10,
            temperature=0.7,
            permissions={"perm1": "value1"},
        )

        target = GenerationTarget.local(temp_dir)
        output_path = emit_codex_agent_manifest(target, agent_profile, ProviderTarget.CODEX)

        assert output_path == temp_dir / ".codex" / "agents" / "test-agent.toml"
        assert output_path.exists()

        content = output_path.read_text(encoding="utf-8")
        assert 'name = "test-agent"' in content
        assert 'description = "Test agent description"' in content
        assert 'developer_instructions = "# Test Agent Prompt"' in content
        assert 'tools = ["tool1", "tool2"]' in content

    def test_emit_gemini_agent_manifest(self, temp_dir: Path) -> None:
        """Gemini agent manifests should use markdown with YAML frontmatter."""
        agent_profile = AgentProfile(
            name="test-agent",
            description="Test agent description",
            prompt="# Test Agent Prompt",
            tools=["tool1", "tool2"],
            mcp_servers=["server1"],
            model="test-model",
            max_turns=10,
            temperature=0.7,
        )

        target = GenerationTarget.local(temp_dir)
        output_path = emit_gemini_agent_manifest(target, agent_profile, ProviderTarget.GEMINI)

        assert output_path == temp_dir / ".gemini" / "agents" / "test-agent.md"
        assert output_path.exists()

        content = output_path.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert "name: test-agent" in content
        assert "description: Test agent description" in content
        assert "mcpServers:" in content
        assert "max_turns: 10" in content
        assert "# Test Agent Prompt" in content

    def test_emit_hermes_identity(self, temp_dir: Path) -> None:
        """Hermes identity should emit to SOUL.md as a separate surface."""
        identity = IdentitySpec(
            name="test-identity",
            body="# Soul\n\nYou are the Hermes identity.",
            metadata={"author": "Test Author"},
        )

        target = GenerationTarget.local(temp_dir)
        output_path = emit_hermes_identity(target, identity, ProviderTarget.HERMES)

        assert output_path == temp_dir / "SOUL.md"
        assert output_path.exists()
        assert output_path.read_text(encoding="utf-8") == "# Soul\n\nYou are the Hermes identity.\n"
