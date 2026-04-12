"""Tests for subagent .md generation.

Covers T046: User Story 5 - Generate subagent .md files.
"""



from riseon_agents.generation.subagents import SubagentsGenerator
from riseon_agents.models.agent import PermissionLevel, Subagent


class TestSubagentsGenerator:
    """T046: Tests for subagent .md generation."""

    def test_generator_exists(self):
        """SubagentsGenerator can be instantiated."""
        generator = SubagentsGenerator()
        assert generator is not None

    def test_generate_single_subagent(self, tmp_path):
        """Generate .md file for single subagent."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# ADR Generator",
            permissions={"edit": PermissionLevel.ALLOW},
        )

        generator = SubagentsGenerator()
        result = generator.generate([subagent], tmp_path)

        assert result.error_count == 0
        assert len(result.files) == 1
        assert result.files[0].path.name == "adr-generator.md"

    def test_generate_multiple_subagents(self, tmp_path):
        """Generate .md files for multiple subagents."""
        subagents = [
            Subagent(
                name="adr-generator",
                description="ADR generator",
                parent_agent="architect",
                markdown_body="# ADR",
                permissions={},
            ),
            Subagent(
                name="ddd-specialist",
                description="DDD specialist",
                parent_agent="architect",
                markdown_body="# DDD",
                permissions={},
            ),
        ]

        generator = SubagentsGenerator()
        result = generator.generate(subagents, tmp_path)

        assert result.error_count == 0
        assert len(result.files) == 2

    def test_output_has_frontmatter(self, tmp_path):
        """Generated file has YAML frontmatter."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# ADR Generator",
            permissions={},
        )

        generator = SubagentsGenerator()
        result = generator.generate([subagent], tmp_path)

        content = result.files[0].path.read_text()
        assert content.startswith("---")
        assert "mode: subagent" in content

    def test_output_contains_description(self, tmp_path):
        """Generated file contains description."""
        subagent = Subagent(
            name="adr-generator",
            description="Creates ADRs",
            parent_agent="architect",
            markdown_body="# ADR",
            permissions={},
        )

        generator = SubagentsGenerator()
        result = generator.generate([subagent], tmp_path)

        content = result.files[0].path.read_text()
        assert "Creates ADRs" in content

    def test_output_contains_markdown_body(self, tmp_path):
        """Generated file contains markdown body."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# Instructions\n\nCreate ADRs",
            permissions={},
        )

        generator = SubagentsGenerator()
        result = generator.generate([subagent], tmp_path)

        content = result.files[0].path.read_text()
        # After frontmatter, should have markdown body
        parts = content.split("---")
        assert len(parts) >= 3
        assert "Create ADRs" in parts[2]

    def test_permissions_mapped(self, tmp_path):
        """Permissions are mapped to frontmatter."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# ADR",
            permissions={"edit": PermissionLevel.ALLOW, "bash": PermissionLevel.DENY},
        )

        generator = SubagentsGenerator()
        result = generator.generate([subagent], tmp_path)

        content = result.files[0].path.read_text()
        assert "permission:" in content
        assert "edit: allow" in content
        assert "bash: deny" in content

    def test_empty_subagents_list(self, tmp_path):
        """Handle empty subagents list gracefully."""
        generator = SubagentsGenerator()
        result = generator.generate([], tmp_path)

        assert result.error_count > 0
        assert len(result.files) > 0

    def test_files_written_to_agents_subdir(self, tmp_path):
        """Files written to .kilo/agents/ subdirectory."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# ADR",
            permissions={},
        )

        generator = SubagentsGenerator()
        result = generator.generate([subagent], tmp_path)

        # Check path includes agents/ subdirectory
        assert "agents" in str(result.files[0].path)

    def test_temperature_included(self, tmp_path):
        """Temperature is included in frontmatter."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# ADR",
            permissions={},
            temperature=0.1,
        )

        generator = SubagentsGenerator()
        result = generator.generate([subagent], tmp_path)

        content = result.files[0].path.read_text()
        assert "temperature: 0.1" in content
