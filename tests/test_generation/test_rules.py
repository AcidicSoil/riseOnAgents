"""Tests for rules generation.

Covers T047: User Story 5 - Generate rule files.
"""



from riseon_agents.generation.rules import RulesGenerator
from riseon_agents.models.rule import Rule


class TestRulesGenerator:
    """T047: Tests for rules generation."""

    def test_generator_exists(self):
        """RulesGenerator can be instantiated."""
        generator = RulesGenerator()
        assert generator is not None

    def test_generate_shared_rule(self, tmp_path):
        """Generate shared rule file."""
        rule = Rule(
            name="code-style",
            content="# Code Style Rules",
            is_shared=True,
        )

        generator = RulesGenerator()
        result = generator.generate([rule], tmp_path)

        assert result.success
        assert len(result.files) == 1
        assert result.files[0].path.name == "code-style.md"

    def test_generate_mode_specific_rule(self, tmp_path):
        """Generate mode-specific rule file."""
        rule = Rule(
            name="architect-specific",
            content="# Architect Rules",
            is_shared=False,
            mode_slug="architect",
        )

        generator = RulesGenerator()
        result = generator.generate([rule], tmp_path)

        assert result.success
        # Should be in rules-architect/ subdirectory
        assert "rules-architect" in str(result.files[0].path)

    def test_shared_rules_go_to_rules_dir(self, tmp_path):
        """Shared rules go to .kilo/rules/ directory."""
        rule = Rule(
            name="shared-rule",
            content="# Shared",
            is_shared=True,
        )

        generator = RulesGenerator()
        result = generator.generate([rule], tmp_path)

        # Should be in rules/ subdirectory
        assert "rules" in str(result.files[0].path)
        assert "rules-architect" not in str(result.files[0].path)

    def test_content_preserved(self, tmp_path):
        """Rule content is preserved exactly."""
        content = "# Rule Title\n\n- Item 1\n- Item 2"
        rule = Rule(
            name="my-rule",
            content=content,
            is_shared=True,
        )

        generator = RulesGenerator()
        result = generator.generate([rule], tmp_path)

        # Read content from file
        assert result.files[0].path.read_text() == content

    def test_generate_multiple_rules(self, tmp_path):
        """Generate multiple rule files."""
        rules = [
            Rule(name="rule1", content="# Rule 1", is_shared=True),
            Rule(name="rule2", content="# Rule 2", is_shared=True),
        ]

        generator = RulesGenerator()
        result = generator.generate(rules, tmp_path)

        # Check success by error_count
        assert result.error_count == 0
        assert len(result.files) == 2

    def test_empty_rules_list(self, tmp_path):
        """Handle empty rules list gracefully."""
        generator = RulesGenerator()
        result = generator.generate([], tmp_path)

        # Should have error files
        assert result.error_count > 0
        assert len(result.files) > 0

    def test_file_written_to_disk(self, tmp_path):
        """Rule file is actually written to target directory."""
        rule = Rule(
            name="test-rule",
            content="# Test Rule",
            is_shared=True,
        )

        generator = RulesGenerator()
        result = generator.generate([rule], tmp_path)

        assert result.files[0].path.exists()
        assert result.files[0].path.read_text() == "# Test Rule"
