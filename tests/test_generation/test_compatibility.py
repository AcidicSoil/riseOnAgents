"""Tests for compatibility generation for provider agent manifests."""

from pathlib import Path

from riseon_agents.generation.compatibility import CompatibilityGenerator
from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.models.generation import GenerationTarget


class TestProviderAgentManifestGeneration:
    """Tests for Codex and Gemini agent manifest generation."""

    def test_generate_codex_agent_manifest(self, temp_dir: Path) -> None:
        """Codex agent manifests should be emitted with the correct path and TOML content."""
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
            metadata={"key": "value"},
            source_path=None,
        )

        target = GenerationTarget.local(temp_dir)
        generator = CompatibilityGenerator()
        result = generator.generate(
            target=target,
            providers=[ProviderTarget.CODEX],
            project_instructions=[],
            skills=[],
            agent_profiles=[agent_profile],
        )

        assert result.error_count == 0
        paths = {generated.path for generated in result.files}
        codex_agent_path = temp_dir / ".codex" / "agents" / "test-agent.toml"
        assert codex_agent_path in paths
        assert codex_agent_path.exists()

        toml_content = codex_agent_path.read_text(encoding="utf-8")
        assert 'name = "test-agent"' in toml_content
        assert 'description = "Test agent description"' in toml_content
        assert 'developer_instructions = "# Test Agent Prompt"' in toml_content
        assert 'model = "test-model"' in toml_content
        assert 'max_turns = 10' in toml_content

    def test_generate_gemini_agent_manifest(self, temp_dir: Path) -> None:
        """Gemini agent manifests should be emitted with markdown frontmatter content."""
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
        generator = CompatibilityGenerator()
        result = generator.generate(
            target=target,
            providers=[ProviderTarget.GEMINI],
            project_instructions=[],
            skills=[],
            agent_profiles=[agent_profile],
        )

        assert result.error_count == 0
        paths = {generated.path for generated in result.files}
        gemini_agent_path = temp_dir / ".gemini" / "agents" / "test-agent.md"
        assert gemini_agent_path in paths
        assert gemini_agent_path.exists()

        content = gemini_agent_path.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert "name: test-agent" in content
        assert "description: Test agent description" in content
        assert "mcpServers:" in content
        assert "max_turns: 10" in content
        assert "# Test Agent Prompt" in content

    def test_generate_multi_target_agent_manifests(self, temp_dir: Path) -> None:
        """A single run should emit both Codex and Gemini agent manifests."""
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
        generator = CompatibilityGenerator()
        result = generator.generate(
            target=target,
            providers=[ProviderTarget.CODEX, ProviderTarget.GEMINI],
            project_instructions=[],
            skills=[],
            agent_profiles=[agent_profile],
        )

        assert result.error_count == 0
        paths = {generated.path for generated in result.files}
        assert temp_dir / ".codex" / "agents" / "test-agent.toml" in paths
        assert temp_dir / ".gemini" / "agents" / "test-agent.md" in paths
