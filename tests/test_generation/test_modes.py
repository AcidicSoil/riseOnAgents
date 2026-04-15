"""Tests for custom_modes.yaml generation.

Covers T045: User Story 5 - Generate custom_modes.yaml.
"""

import pytest

from riseon_agents.generation.modes import ModesGenerator
from riseon_agents.models.agent import PermissionLevel, PrimaryAgent


class TestModesGenerator:
    """T045: Tests for custom_modes.yaml generation."""

    def test_generator_exists(self):
        """ModesGenerator can be instantiated."""
        generator = ModesGenerator()
        assert generator is not None

    def test_generate_single_agent(self, tmp_path):
        """Generate custom_modes.yaml for single agent."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect\n\nYou are an architect.",
            permissions={"edit": PermissionLevel.ALLOW},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        assert result.success
        assert len(result.files) == 1
        assert result.files[0].path.name == "custom_modes.yaml"

    def test_generate_multiple_agents(self, tmp_path):
        """Generate custom_modes.yaml for multiple agents."""
        agents = [
            PrimaryAgent(
                name="architect",
                description="Software architect",
                markdown_body="# Architect",
                permissions={},
                subagents=[],
                rules=[],
                skills=[],
            ),
            PrimaryAgent(
                name="developer",
                description="Software developer",
                markdown_body="# Developer",
                permissions={},
                subagents=[],
                rules=[],
                skills=[],
            ),
        ]

        generator = ModesGenerator()
        result = generator.generate(agents, tmp_path)

        assert result.success
        assert len(result.files) == 1

    def test_output_contains_agent_slug(self, tmp_path):
        """Generated file contains agent slug."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()
        assert "architect" in content

    def test_output_contains_description(self, tmp_path):
        """Generated file contains agent description."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect specialist",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()
        assert "Software architect specialist" in content

    def test_output_contains_markdown_body(self, tmp_path):
        """Generated file contains markdown body as roleDefinition."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Role\n\nYou are an expert.",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()
        assert "roleDefinition" in content
        assert "You are an expert" in content

    def test_permissions_map_to_groups(self, tmp_path):
        """Permissions map to appropriate groups."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={"edit": PermissionLevel.ALLOW, "bash": PermissionLevel.ALLOW},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()
        assert "groups" in content

    def test_empty_agents_list(self, tmp_path):
        """Handle empty agents list gracefully."""
        generator = ModesGenerator()
        result = generator.generate([], tmp_path)

        # Should have error files
        assert result.error_count > 0
        assert len(result.files) > 0

    def test_yaml_is_valid(self, tmp_path):
        """Generated YAML is valid."""
        import yaml

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        # Read content from file
        content = result.files[0].path.read_text()

        # Should be valid YAML
        try:
            yaml.safe_load(content)
        except yaml.YAMLError as e:
            pytest.fail(f"Generated YAML is invalid: {e}")

    def test_file_written_to_disk(self, tmp_path):
        """File is actually written to target directory."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = ModesGenerator()
        result = generator.generate([agent], tmp_path)

        output_path = tmp_path / "custom_modes.yaml"
        assert output_path.exists()
        assert output_path.read_text() == result.files[0].path.read_text()
