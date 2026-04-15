"""Tests for AgentRepository."""

from pathlib import Path

from riseon_agents.models.agent import PermissionLevel
from riseon_agents.parsing.repository import AgentRepository


class TestAgentRepository:
    """Tests for the AgentRepository class."""

    def test_discover_agents(self, agents_fixtures_dir: Path) -> None:
        """Test discovering agents from fixtures directory."""
        repo = AgentRepository(agents_fixtures_dir)
        result = repo.discover()

        assert result.success
        assert len(result.agents) >= 1

    def test_discover_agents_not_found(self, temp_dir: Path) -> None:
        """Test discovering agents from non-existent directory."""
        repo = AgentRepository(temp_dir / "nonexistent")
        result = repo.discover()

        assert len(result.agents) == 0
        assert len(result.warnings) > 0

    def test_load_primary_agent(self, agents_fixtures_dir: Path) -> None:
        """Test loading a primary agent with all fields."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        agent = repo.get_agent_by_name("test-primary")
        assert agent is not None
        assert agent.name == "test-primary"
        assert agent.description == "A test primary agent for unit testing"
        assert "read" in agent.tools
        assert agent.temperature == 0.1
        assert agent.steps == 40
        assert agent.permissions.get("edit") == PermissionLevel.ALLOW
        assert agent.permissions.get("bash") == PermissionLevel.DENY

    def test_load_subagents(self, agents_fixtures_dir: Path) -> None:
        """Test loading subagents for a primary agent."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        agent = repo.get_agent_by_name("test-primary")
        assert agent is not None
        assert len(agent.subagents) >= 2

        subagent_names = [s.name for s in agent.subagents]
        assert "test-subagent-1" in subagent_names
        assert "test-subagent-2" in subagent_names

    def test_subagent_properties(self, agents_fixtures_dir: Path) -> None:
        """Test subagent properties are loaded correctly."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        agent = repo.get_agent_by_name("test-primary")
        assert agent is not None

        subagent = next((s for s in agent.subagents if s.name == "test-subagent-1"), None)
        assert subagent is not None
        assert subagent.description == "First test subagent for validation"
        assert subagent.model_variant == "high"
        assert subagent.parent_agent == "test-primary"

    def test_load_rules(self, agents_fixtures_dir: Path) -> None:
        """Test loading rules for a primary agent."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        agent = repo.get_agent_by_name("test-primary")
        assert agent is not None
        # Should have at least the shared rule
        shared_rules = [r for r in agent.rules if r.is_shared]
        assert len(shared_rules) >= 1

    def test_load_skills(self, agents_fixtures_dir: Path) -> None:
        """Test loading skills for a primary agent."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        agent = repo.get_agent_by_name("test-primary")
        assert agent is not None
        assert len(agent.skills) >= 1

        skill = agent.skills[0]
        assert skill.name == "test-skill"
        assert "test skill" in skill.description.lower()

    def test_get_all_subagents(self, agents_fixtures_dir: Path) -> None:
        """Test getting all subagents across all agents."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        all_subagents = repo.get_all_subagents()
        assert len(all_subagents) >= 2

    def test_get_all_rules(self, agents_fixtures_dir: Path) -> None:
        """Test getting all rules across all agents."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        all_rules = repo.get_all_rules()
        assert len(all_rules) >= 1

    def test_get_all_skills(self, agents_fixtures_dir: Path) -> None:
        """Test getting all skills across all agents."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        all_skills = repo.get_all_skills()
        assert len(all_skills) >= 1

    def test_agent_not_found(self, agents_fixtures_dir: Path) -> None:
        """Test getting a non-existent agent."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        agent = repo.get_agent_by_name("nonexistent")
        assert agent is None

    def test_empty_agents_directory(self, temp_dir: Path) -> None:
        """Test discovering from empty directory."""
        agents_dir = temp_dir / "agents"
        agents_dir.mkdir()

        repo = AgentRepository(agents_dir)
        result = repo.discover()

        assert len(result.agents) == 0
        assert len(result.warnings) == 0  # Empty is not a warning

    def test_malformed_agent_generates_warning(self, temp_dir: Path) -> None:
        """Test that malformed agents generate warnings."""
        agents_dir = temp_dir / "agents"
        bad_agent_dir = agents_dir / "bad-agent"
        bad_agent_dir.mkdir(parents=True)

        # Create a malformed agent file (missing required fields)
        bad_file = bad_agent_dir / "bad-agent.agent.md"
        bad_file.write_text("""---
name: bad-agent
---

Missing description field.
""")

        repo = AgentRepository(agents_dir)
        result = repo.discover()

        assert len(result.warnings) > 0
        assert any("bad-agent" in str(w.path) for w in result.warnings)

    def test_get_project_instructions_returns_primary_agent_content(
        self, agents_fixtures_dir: Path
    ) -> None:
        """Repository should expose canonical project instructions."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        instructions = repo.get_project_instructions()

        assert len(instructions) == 1
        assert instructions[0].name == "test-primary"
        assert instructions[0].description == "A test primary agent for unit testing"
        assert instructions[0].body
        assert instructions[0].source_path is not None

    def test_get_project_instructions_aggregates_multiple_primary_agents(
        self, temp_agents_dir: Path
    ) -> None:
        """Repository should aggregate multiple primary agents into one project surface."""
        second_agent_dir = temp_agents_dir / "test-secondary"
        second_agent_dir.mkdir()
        (second_agent_dir / "test-secondary.agent.md").write_text(
            "---\n"
            "name: test-secondary\n"
            "description: Secondary test agent\n"
            "---\n\n"
            "# Test Secondary Agent\n\n"
            "Secondary project instructions.\n",
            encoding="utf-8",
        )

        repo = AgentRepository(temp_agents_dir)
        repo.discover()

        instructions = repo.get_project_instructions()

        assert len(instructions) == 1
        assert instructions[0].name == "project-instructions"
        assert instructions[0].description == (
            "Repository-wide instructions aggregated from primary agents"
        )
        assert "# Project Instructions" in instructions[0].body
        assert "## Test Primary" in instructions[0].body
        assert "## Test Secondary" in instructions[0].body

    def test_get_agent_profiles_returns_subagent_profiles(self, agents_fixtures_dir: Path) -> None:
        """Repository should expose canonical agent profiles from subagents."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        profiles = repo.get_agent_profiles()

        assert len(profiles) >= 2
        profile_names = [profile.name for profile in profiles]
        assert "test-subagent-1" in profile_names
        assert "test-subagent-2" in profile_names
        assert all(profile.prompt for profile in profiles)

    def test_get_skill_specs_returns_canonical_skills(self, agents_fixtures_dir: Path) -> None:
        """Repository should expose canonical skill specs."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        specs = repo.get_skill_specs()

        assert len(specs) >= 1
        assert specs[0].name == "test-skill"
        assert specs[0].description
        assert specs[0].body

    def test_get_rule_specs_returns_canonical_rules(self, agents_fixtures_dir: Path) -> None:
        """Repository should expose canonical rule specs."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        specs = repo.get_rule_specs()

        assert len(specs) >= 1
        assert all(spec.name for spec in specs)
        assert all(spec.body for spec in specs)

    def test_get_identity_specs_returns_empty_until_identity_surface_exists(
        self, agents_fixtures_dir: Path
    ) -> None:
        """Identity surface should remain empty until explicitly modeled in source."""
        repo = AgentRepository(agents_fixtures_dir)
        repo.discover()

        assert repo.get_identity_specs() == []
