"""Tests for compatibility generation for Codex agent manifests."""

from pathlib import Path
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.generation.compatibility import CompatibilityGenerator
from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.models.generation import GenerationTarget
from riseon_agents.models.agent_profile import AgentProfile


class TestCodexAgentManifestGeneration:
    """Tests for the generation of Codex-specific agent manifest files."""

    def test_generate_codex_agent_manifest(self, temp_dir: Path) -> None:
        """Test that Codex agent manifests are emitted with the correct paths and content."""
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
        assert temp_dir / ".codex" / "agents" / "test-agent.toml" in paths

        codex_agent_path = temp_dir / ".codex" / "agents" / "test-agent.toml"
        assert codex_agent_path.exists()

        with open(codex_agent_path, "r") as f:
            toml_content = f.read()

        assert "name = 'test-agent'" in toml_content
        assert "description = 'Test agent description'" in toml_content
        assert "developer_instructions = '# Test Agent Prompt'" in toml_content
        assert "description = 'Test agent description'" in toml_content
        assert "developer_instructions = '# Test Agent Prompt'" in toml_content
        assert "developer_instructions = "# Test Agent Prompt"" in toml_content
