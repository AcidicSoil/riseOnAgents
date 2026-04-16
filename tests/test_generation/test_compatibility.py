from pathlib import Path

from riseon_agents.generation.compatibility import CompatibilityGenerator
from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.models.generation import GenerationTarget
from riseon_agents.models.identity_spec import IdentitySpec
from riseon_agents.models.project_instructions import ProjectInstructions
from riseon_agents.models.skill_spec import SkillSpec


class TestProviderCompatibilityGeneration:
    """Tests for Codex, Gemini, and Hermes compatibility generation."""

    def test_generate_codex_agent_manifest(self, temp_dir: Path) -> None:
        """Codex agent manifests should be emitted with validator-compatible TOML content."""
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
            provider_extensions={
                "approval_policy": "never",
                "permissions": {
                    "trusted": {
                        "network": {
                            "mode": "limited",
                            "enabled": True,
                            "domains": {"example.com": "allow"},
                        }
                    }
                },
                "default_permissions": "trusted",
            },
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
        assert 'approval_policy = "never"' in toml_content
        assert 'default_permissions = "trusted"' in toml_content
        assert "[permissions.trusted.network]" in toml_content
        assert 'mode = "limited"' in toml_content
        assert "enabled = true" in toml_content
        assert 'mcp_servers = ["server1"]' not in toml_content
        assert 'perm1 = "value1"' not in toml_content

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

    def test_generate_hermes_project_context_and_identity(self, temp_dir: Path) -> None:
        """Hermes should emit separate project context and identity surfaces."""
        instructions = [
            ProjectInstructions(
                name="test-project",
                description="Hermes context",
                body="# Hermes Context\n\nProject guidance.",
            )
        ]
        identities = [
            IdentitySpec(
                name="test-identity",
                body="# Soul\n\nYou are the Hermes identity.",
            )
        ]

        target = GenerationTarget.local(temp_dir)
        generator = CompatibilityGenerator()
        result = generator.generate(
            target=target,
            providers=[ProviderTarget.HERMES],
            project_instructions=instructions,
            skills=[],
            agent_profiles=[],
            identity_specs=identities,
        )

        assert result.error_count == 0
        paths = {generated.path for generated in result.files}
        assert temp_dir / ".hermes.md" in paths
        assert temp_dir / "SOUL.md" in paths
        assert (temp_dir / ".hermes.md").read_text(encoding="utf-8") == (
            "# Hermes Context\n\nProject guidance.\n"
        )
        assert (temp_dir / "SOUL.md").read_text(encoding="utf-8") == (
            "# Soul\n\nYou are the Hermes identity.\n"
        )

    def test_generate_multi_target_agent_and_hermes_surfaces(self, temp_dir: Path) -> None:
        """A single run should emit Codex manifests and Hermes context or identity files."""
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
        instructions = [
            ProjectInstructions(
                name="test-project",
                description="Hermes context",
                body="# Hermes Context\n\nProject guidance.",
            )
        ]
        identities = [
            IdentitySpec(
                name="test-identity",
                body="# Soul\n\nYou are the Hermes identity.",
            )
        ]

        target = GenerationTarget.local(temp_dir)
        generator = CompatibilityGenerator()
        result = generator.generate(
            target=target,
            providers=[ProviderTarget.CODEX, ProviderTarget.HERMES],
            project_instructions=instructions,
            skills=[],
            agent_profiles=[agent_profile],
            identity_specs=identities,
        )

        assert result.error_count == 0
        paths = {generated.path for generated in result.files}
        assert temp_dir / ".codex" / "agents" / "test-agent.toml" in paths
        assert temp_dir / ".hermes.md" in paths
        assert temp_dir / "SOUL.md" in paths

    def test_generate_multi_target_shared_skills_are_not_duplicated(self, temp_dir: Path) -> None:
        """Shared output paths should be reported once even across multiple providers."""
        skill = SkillSpec(
            name="test-skill",
            description="Test skill description",
            body="# Test Skill",
        )

        target = GenerationTarget.local(temp_dir)
        generator = CompatibilityGenerator()
        result = generator.generate(
            target=target,
            providers=[ProviderTarget.CODEX, ProviderTarget.GEMINI],
            project_instructions=[],
            skills=[skill],
            agent_profiles=[],
        )

        skill_path = temp_dir / ".agents" / "skills" / "test-skill" / "SKILL.md"
        matches = [generated for generated in result.files if generated.path == skill_path]

        assert skill_path.exists()
        assert len(matches) == 1
