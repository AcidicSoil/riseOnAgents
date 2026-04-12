"""Tests for agent data models."""

import pytest

from riseon_agents.models.agent import PermissionLevel, PrimaryAgent, Subagent


class TestPermissionLevel:
    """Tests for the PermissionLevel enum."""

    def test_permission_values(self) -> None:
        """Test that all permission levels have correct values."""
        assert PermissionLevel.ALLOW.value == "allow"
        assert PermissionLevel.ASK.value == "ask"
        assert PermissionLevel.DENY.value == "deny"

    def test_permission_from_string(self) -> None:
        """Test creating permission level from string."""
        assert PermissionLevel("allow") == PermissionLevel.ALLOW
        assert PermissionLevel("ask") == PermissionLevel.ASK
        assert PermissionLevel("deny") == PermissionLevel.DENY


class TestPrimaryAgent:
    """Tests for the PrimaryAgent dataclass."""

    def test_create_minimal_agent(self) -> None:
        """Test creating an agent with minimal required fields."""
        agent = PrimaryAgent(
            name="test-agent",
            description="A test agent",
            markdown_body="# Test Agent\n\nInstructions here.",
        )
        assert agent.name == "test-agent"
        assert agent.description == "A test agent"
        assert agent.markdown_body == "# Test Agent\n\nInstructions here."

    def test_create_full_agent(self) -> None:
        """Test creating an agent with all fields."""
        agent = PrimaryAgent(
            name="full-agent",
            description="A full agent",
            markdown_body="# Full Agent",
            tools=["read", "edit", "search"],
            temperature=0.2,
            steps=50,
            permissions={"edit": PermissionLevel.ALLOW, "bash": PermissionLevel.DENY},
            handoffs=["subagent-1", "subagent-2"],
        )
        assert agent.tools == ["read", "edit", "search"]
        assert agent.temperature == 0.2
        assert agent.steps == 50
        assert agent.permissions["edit"] == PermissionLevel.ALLOW
        assert agent.handoffs == ["subagent-1", "subagent-2"]

    def test_agent_slug(self) -> None:
        """Test the slug property."""
        agent = PrimaryAgent(
            name="Test_Agent",
            description="Test",
            markdown_body="# Test",
        )
        assert agent.slug == "test-agent"

    def test_agent_display_name(self) -> None:
        """Test the display_name property."""
        agent = PrimaryAgent(
            name="test-agent",
            description="Test",
            markdown_body="# Test",
        )
        assert agent.display_name == "Test Agent"

    def test_agent_requires_name(self) -> None:
        """Test that agent requires a name."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            PrimaryAgent(name="", description="Test", markdown_body="# Test")

    def test_agent_requires_description(self) -> None:
        """Test that agent requires a description."""
        with pytest.raises(ValueError, match="description cannot be empty"):
            PrimaryAgent(name="test", description="", markdown_body="# Test")

    def test_agent_requires_markdown_body(self) -> None:
        """Test that agent requires markdown body."""
        with pytest.raises(ValueError, match="markdown_body cannot be empty"):
            PrimaryAgent(name="test", description="Test", markdown_body="")

    def test_agent_default_values(self) -> None:
        """Test default values for optional fields."""
        agent = PrimaryAgent(
            name="test",
            description="Test",
            markdown_body="# Test",
        )
        assert agent.tools == []
        assert agent.temperature == 0.1
        assert agent.steps == 40
        assert agent.permissions == {}
        assert agent.handoffs == []
        assert agent.subagents == []
        assert agent.rules == []
        assert agent.skills == []
        assert agent.source_path is None


class TestSubagent:
    """Tests for the Subagent dataclass."""

    def test_create_minimal_subagent(self) -> None:
        """Test creating a subagent with minimal required fields."""
        subagent = Subagent(
            name="test-subagent",
            description="A test subagent",
            markdown_body="# Test Subagent\n\nInstructions here.",
        )
        assert subagent.name == "test-subagent"
        assert subagent.description == "A test subagent"

    def test_create_full_subagent(self) -> None:
        """Test creating a subagent with all fields."""
        subagent = Subagent(
            name="full-subagent",
            description="A full subagent",
            markdown_body="# Full Subagent",
            tools=["read", "edit"],
            temperature=0.3,
            steps=20,
            permissions={"edit": PermissionLevel.ALLOW},
            model_variant="high",
            target="opencode",
            parent_agent="primary-agent",
        )
        assert subagent.model_variant == "high"
        assert subagent.target == "opencode"
        assert subagent.parent_agent == "primary-agent"

    def test_subagent_slug(self) -> None:
        """Test the slug property."""
        subagent = Subagent(
            name="Test_Subagent",
            description="Test",
            markdown_body="# Test",
        )
        assert subagent.slug == "test-subagent"

    def test_subagent_invalid_model_variant(self) -> None:
        """Test that invalid model_variant raises error."""
        with pytest.raises(ValueError, match="Invalid model_variant"):
            Subagent(
                name="test",
                description="Test",
                markdown_body="# Test",
                model_variant="invalid",
            )

    def test_subagent_valid_model_variants(self) -> None:
        """Test valid model_variant values."""
        for variant in ["high", "low", "medium", None]:
            subagent = Subagent(
                name="test",
                description="Test",
                markdown_body="# Test",
                model_variant=variant,
            )
            assert subagent.model_variant == variant

    def test_subagent_default_values(self) -> None:
        """Test default values for optional fields."""
        subagent = Subagent(
            name="test",
            description="Test",
            markdown_body="# Test",
        )
        assert subagent.tools == []
        assert subagent.temperature == 0.1
        assert subagent.steps == 15
        assert subagent.permissions == {}
        assert subagent.model_variant is None
        assert subagent.target == "opencode"
        assert subagent.parent_agent is None
