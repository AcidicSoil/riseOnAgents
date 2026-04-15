"""Tests for KiloCodeGenerator orchestrator.

Covers T049: User Story 5 - Test generator orchestration.
Covers T074, T075: User Story 6 - Test YAML and Markdown validation.
"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from riseon_agents.generation.generator import KiloCodeGenerator
from riseon_agents.models.agent import PrimaryAgent, Subagent
from riseon_agents.models.generation import (
    FileStatus,
    GenerationLevel,
    GenerationResult,
    ValidationStatus,
)
from riseon_agents.models.rule import Rule
from riseon_agents.models.skill import Skill


class TestKiloCodeGenerator:
    """T049: Tests for generator orchestrator."""

    def test_generator_exists(self):
        """KiloCodeGenerator can be instantiated."""
        generator = KiloCodeGenerator()
        assert generator is not None

    def test_generate_requires_selection(self, tmp_path):
        """Generation requires at least one selected agent."""
        generator = KiloCodeGenerator()
        result = generator.generate([], GenerationLevel.LOCAL, tmp_path)

        # Should have errors
        assert result.error_count > 0

    def test_generate_local_target(self, tmp_path):
        """Generate to Local target creates .kilo/ directory."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        # Mock the individual generators to avoid dependencies
        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            result = generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        assert result.error_count == 0

    def test_generate_global_target(self, tmp_path):
        """T069: Generate to Global target uses ~/.kilocode/ directory."""
        # Create agent with children so all generators are called
        subagent = Subagent(
            name="test-sub",
            description="Test subagent",
            parent_agent="architect",
            markdown_body="# Test",
            permissions={},
        )

        rule = Rule(
            name="test-rule",
            content="# Rule",
            is_shared=True,
        )

        skill = Skill(
            name="test-skill",
            description="Test skill",
            content="# Skill",
            source_path=tmp_path / "test-skill" / "SKILL.md",
        )

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[subagent],
            rules=[rule],
            skills=[skill],
        )

        generator = KiloCodeGenerator()

        # Track the paths passed to generators
        captured_paths = {}

        def capture_modes(_agents, path):
            captured_paths["modes"] = path
            return MagicMock(error_count=0, files=[])

        def capture_subagents(_subagents, path):
            captured_paths["subagents"] = path
            return MagicMock(error_count=0, files=[])

        def capture_rules(_rules, path):
            captured_paths["rules"] = path
            return MagicMock(error_count=0, files=[])

        def capture_skills(_skills, path):
            captured_paths["skills"] = path
            return MagicMock(error_count=0, files=[])

        with (
            patch.object(generator.modes_gen, "generate", side_effect=capture_modes),
            patch.object(generator.subagents_gen, "generate", side_effect=capture_subagents),
            patch.object(generator.rules_gen, "generate", side_effect=capture_rules),
            patch.object(generator.skills_gen, "generate", side_effect=capture_skills),
        ):
            generator.generate([agent], GenerationLevel.GLOBAL, tmp_path)

        # Verify global paths are used (generators get parent dir, not subdirs)
        home = Path.home()
        assert captured_paths["modes"] == home / ".kilocode"
        assert captured_paths["subagents"] == home / ".kilocode"
        assert captured_paths["rules"] == home / ".kilocode"
        assert captured_paths["skills"] == home / ".kilocode"

    def test_local_vs_global_path_differences(self, tmp_path):
        """T069: Local and Global targets use different base paths."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        local_paths = {}
        global_paths = {}

        def make_capture(storage):
            def capture(_agents_or_items, path):
                storage["path"] = path
                return MagicMock(error_count=0, files=[])

            return capture

        # Test LOCAL
        with (
            patch.object(generator.modes_gen, "generate", side_effect=make_capture(local_paths)),
            patch.object(
                generator.subagents_gen, "generate", side_effect=make_capture(local_paths)
            ),
            patch.object(generator.rules_gen, "generate", side_effect=make_capture(local_paths)),
            patch.object(generator.skills_gen, "generate", side_effect=make_capture(local_paths)),
        ):
            generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        # Test GLOBAL
        with (
            patch.object(generator.modes_gen, "generate", side_effect=make_capture(global_paths)),
            patch.object(
                generator.subagents_gen, "generate", side_effect=make_capture(global_paths)
            ),
            patch.object(generator.rules_gen, "generate", side_effect=make_capture(global_paths)),
            patch.object(generator.skills_gen, "generate", side_effect=make_capture(global_paths)),
        ):
            generator.generate([agent], GenerationLevel.GLOBAL, tmp_path)

        # Verify paths are different
        assert (
            local_paths["path"] == tmp_path / ".kilo"
            or local_paths["path"] == tmp_path / ".kilocode"
        )
        assert global_paths["path"] == Path.home() / ".kilocode"

    def test_generate_creates_directories(self, tmp_path):
        """Generation creates necessary directories."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        # Check .kilo directory was created
        kilo_dir = tmp_path / ".kilo"
        assert kilo_dir.exists()

    def test_result_contains_file_list(self, tmp_path):
        """Generation result contains list of generated files."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        # Create a mock file
        mock_file = MagicMock()
        mock_file.path = tmp_path / "custom_modes.yaml"
        mock_file.status = FileStatus.CREATED

        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[mock_file])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            result = generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        assert len(result.files) > 0

    def test_error_handling(self, tmp_path):
        """Handle errors during generation gracefully."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        with patch.object(generator.modes_gen, "generate") as mock_modes:
            mock_modes.side_effect = Exception("Generation failed")

            result = generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

        assert result.error_count > 0
        assert "Generation failed" in "; ".join(
            [f.error_message for f in result.error_files if f.error_message]
        )

    def test_overwrite_existing_files(self, tmp_path):
        """Overwrite existing files when requested."""
        # Create an existing file
        kilo_dir = tmp_path / ".kilo"
        kilo_dir.mkdir()
        existing_file = kilo_dir / "custom_modes.yaml"
        existing_file.write_text("old content")

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        generator = KiloCodeGenerator()

        # Create a mock file
        mock_file = MagicMock()
        mock_file.path = existing_file
        mock_file.status = FileStatus.UPDATED
        mock_file.content = "new content"

        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[mock_file])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            result = generator.generate([agent], GenerationLevel.LOCAL, tmp_path, overwrite=True)

        assert result.error_count == 0

    def test_collects_all_agent_children(self, tmp_path):
        """Generator collects subagents, rules, and skills from agents."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# ADR",
            permissions={},
        )

        rule = Rule(
            name="code-style",
            content="# Code Style",
            is_shared=True,
        )

        skill = Skill(
            name="my-skill",
            description="My skill",
            content="# Skill",
            source_path=tmp_path / "my-skill" / "SKILL.md",
        )

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[subagent],
            rules=[rule],
            skills=[skill],
        )

        generator = KiloCodeGenerator()

        with (
            patch.object(generator.modes_gen, "generate") as mock_modes,
            patch.object(generator.subagents_gen, "generate") as mock_subagents,
            patch.object(generator.rules_gen, "generate") as mock_rules,
            patch.object(generator.skills_gen, "generate") as mock_skills,
        ):
            mock_modes.return_value = MagicMock(error_count=0, files=[])
            mock_subagents.return_value = MagicMock(error_count=0, files=[])
            mock_rules.return_value = MagicMock(error_count=0, files=[])
            mock_skills.return_value = MagicMock(error_count=0, files=[])

            generator.generate([agent], GenerationLevel.LOCAL, tmp_path)

            # Verify that all generators were called
            mock_modes.assert_called_once()
            mock_subagents.assert_called_once()
            mock_rules.assert_called_once()
            mock_skills.assert_called_once()


class TestYAMLValidation:
    """T074: Tests for YAML validation (User Story 6)."""

    def test_validate_yaml_valid_file(self, tmp_path):
        """Valid YAML file passes validation."""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("""
key: value
list:
  - item1
  - item2
nested:
  key: value
""")

        generator = KiloCodeGenerator()
        result = generator.validate_yaml(yaml_file)

        assert result.is_valid is True
        assert result.status == ValidationStatus.PASS
        assert len(result.errors) == 0

    def test_validate_yaml_invalid_syntax(self, tmp_path):
        """Invalid YAML syntax fails validation with error location."""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("""
key: value
  invalid_indent: value
another_key: value
""")

        generator = KiloCodeGenerator()
        result = generator.validate_yaml(yaml_file)

        assert result.is_valid is False
        assert result.status == ValidationStatus.FAIL
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "yaml_syntax"
        # Should have line number info
        assert result.errors[0].line_number is not None

    def test_validate_yaml_missing_file(self, tmp_path):
        """Non-existent file fails validation."""
        yaml_file = tmp_path / "nonexistent.yaml"

        generator = KiloCodeGenerator()
        result = generator.validate_yaml(yaml_file)

        assert result.is_valid is False
        assert result.status == ValidationStatus.FAIL
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "file_not_found"

    def test_validate_yaml_complex_structure(self, tmp_path):
        """Complex YAML structures are validated correctly."""
        yaml_file = tmp_path / "custom_modes.yaml"
        yaml_file.write_text("""customModes:
  - slug: test-mode
    name: Test Mode
    description: A test mode
    roleDefinition: |
      Multi-line
      content here
    groups:
      - read
      - - edit
        - fileRegex: ".*"
""")

        generator = KiloCodeGenerator()
        result = generator.validate_yaml(yaml_file)

        assert result.is_valid is True
        assert result.status == ValidationStatus.PASS


class TestMarkdownValidation:
    """T075: Tests for Markdown validation (User Story 6)."""

    def test_validate_markdown_valid_file(self, tmp_path):
        """Valid Markdown file with frontmatter passes validation."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
name: test-agent
description: Test agent
---

# Test Agent

This is the agent content.
""")

        generator = KiloCodeGenerator()
        result = generator.validate_markdown(md_file)

        assert result.is_valid is True
        assert result.status == ValidationStatus.PASS
        assert len(result.errors) == 0

    def test_validate_markdown_no_frontmatter(self, tmp_path):
        """Markdown without frontmatter is valid."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""# Test Content

This is just regular markdown.
""")

        generator = KiloCodeGenerator()
        result = generator.validate_markdown(md_file)

        assert result.is_valid is True
        assert result.status == ValidationStatus.PASS

    def test_validate_markdown_empty_file(self, tmp_path):
        """Empty Markdown file fails validation."""
        md_file = tmp_path / "test.md"
        md_file.write_text("")

        generator = KiloCodeGenerator()
        result = generator.validate_markdown(md_file)

        assert result.is_valid is False
        assert result.status == ValidationStatus.FAIL
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "empty_file"

    def test_validate_markdown_invalid_frontmatter_yaml(self, tmp_path):
        """Invalid frontmatter YAML fails validation."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
name: test-agent
  invalid: yaml here
---

# Content
""")

        generator = KiloCodeGenerator()
        result = generator.validate_markdown(md_file)

        assert result.is_valid is False
        assert result.status == ValidationStatus.FAIL
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "frontmatter_yaml"

    def test_validate_markdown_unclosed_frontmatter(self, tmp_path):
        """Unclosed frontmatter fails validation."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
name: test-agent

# Content without closing frontmatter
""")

        generator = KiloCodeGenerator()
        result = generator.validate_markdown(md_file)

        assert result.is_valid is False
        assert result.status == ValidationStatus.FAIL
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "frontmatter_unclosed"

    def test_validate_markdown_no_content_after_frontmatter(self, tmp_path):
        """Markdown with only frontmatter fails validation."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
name: test-agent
---
""")

        generator = KiloCodeGenerator()
        result = generator.validate_markdown(md_file)

        assert result.is_valid is False
        assert result.status == ValidationStatus.FAIL
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "no_content"

    def test_validate_markdown_missing_file(self, tmp_path):
        """Non-existent Markdown file fails validation."""
        md_file = tmp_path / "nonexistent.md"

        generator = KiloCodeGenerator()
        result = generator.validate_markdown(md_file)

        assert result.is_valid is False
        assert result.status == ValidationStatus.FAIL
        assert len(result.errors) == 1
        assert result.errors[0].error_type == "file_not_found"


class TestGenerationValidation:
    """Tests for validating generated files."""

    def test_validate_generation_result_adds_validation_results(self, tmp_path):
        """Validation results are added to generation result."""
        # Create some test files
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("key: value\n")

        md_file = tmp_path / "test.md"
        md_file.write_text("# Test\n")

        # Create a generation result with these files
        result = GenerationResult()
        from riseon_agents.models.generation import GeneratedFile

        result.files.append(
            GeneratedFile(
                path=yaml_file,
                status=FileStatus.CREATED,
            )
        )
        result.files.append(
            GeneratedFile(
                path=md_file,
                status=FileStatus.CREATED,
            )
        )

        generator = KiloCodeGenerator()
        generator.validate_generation_result(result)

        # Should have validation results
        assert len(result.validation_results) == 2
        assert result.validation_passed is True

    def test_generation_result_summary_includes_validation(self, tmp_path):
        """Generation summary includes validation status."""
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("key: value\n")

        result = GenerationResult()
        from riseon_agents.models.generation import GeneratedFile

        result.files.append(
            GeneratedFile(
                path=yaml_file,
                status=FileStatus.CREATED,
            )
        )

        generator = KiloCodeGenerator()
        generator.validate_generation_result(result)

        summary = result.get_summary()
        assert "Validation" in summary
        assert "passed" in summary.lower()
