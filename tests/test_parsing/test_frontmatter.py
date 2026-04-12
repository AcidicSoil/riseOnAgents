"""Tests for frontmatter parser."""

from pathlib import Path

import pytest

from riseon_agents.parsing.frontmatter import FrontmatterParser, ParsedDocument


class TestFrontmatterParser:
    """Tests for the FrontmatterParser class."""

    @pytest.fixture
    def parser(self) -> FrontmatterParser:
        """Create a parser instance."""
        return FrontmatterParser()

    def test_parse_string_basic(self, parser: FrontmatterParser) -> None:
        """Test parsing a basic frontmatter string."""
        content = """---
name: test
description: A test document
---

# Test Content

Some markdown body.
"""
        doc = parser.parse_string(content)

        assert doc.frontmatter["name"] == "test"
        assert doc.frontmatter["description"] == "A test document"
        assert "# Test Content" in doc.body
        assert "Some markdown body." in doc.body

    def test_parse_string_no_frontmatter(self, parser: FrontmatterParser) -> None:
        """Test parsing a string without frontmatter."""
        content = """# Just Markdown

No frontmatter here.
"""
        doc = parser.parse_string(content)

        assert doc.frontmatter == {}
        assert "# Just Markdown" in doc.body

    def test_parse_string_complex_yaml(self, parser: FrontmatterParser) -> None:
        """Test parsing complex YAML frontmatter."""
        content = """---
name: complex
tools:
  - read
  - edit
  - search
permissions:
  edit: allow
  bash: deny
temperature: 0.5
---

Body content.
"""
        doc = parser.parse_string(content)

        assert doc.frontmatter["name"] == "complex"
        assert doc.frontmatter["tools"] == ["read", "edit", "search"]
        assert doc.frontmatter["permissions"] == {"edit": "allow", "bash": "deny"}
        assert doc.frontmatter["temperature"] == 0.5

    def test_parse_file(self, parser: FrontmatterParser, temp_dir: Path) -> None:
        """Test parsing a file."""
        test_file = temp_dir / "test.md"
        test_file.write_text("""---
name: file-test
---

File content.
""")
        doc = parser.parse_file(test_file)

        assert doc.frontmatter["name"] == "file-test"
        assert doc.source_path == test_file

    def test_parse_file_not_found(self, parser: FrontmatterParser, temp_dir: Path) -> None:
        """Test parsing a non-existent file."""
        with pytest.raises(FileNotFoundError):
            parser.parse_file(temp_dir / "nonexistent.md")

    def test_get_required_string(self, parser: FrontmatterParser) -> None:
        """Test getting a required string value."""
        doc = ParsedDocument(
            frontmatter={"name": "test"},
            body="",
            source_path=Path("test.md"),
        )

        assert parser.get_required_string(doc, "name") == "test"

    def test_get_required_string_missing(self, parser: FrontmatterParser) -> None:
        """Test getting a missing required string."""
        doc = ParsedDocument(
            frontmatter={},
            body="",
            source_path=Path("test.md"),
        )

        with pytest.raises(ValueError, match="Missing required field 'name'"):
            parser.get_required_string(doc, "name")

    def test_get_optional_string(self, parser: FrontmatterParser) -> None:
        """Test getting an optional string value."""
        doc = ParsedDocument(
            frontmatter={"name": "test"},
            body="",
            source_path=Path("test.md"),
        )

        assert parser.get_optional_string(doc, "name") == "test"
        assert parser.get_optional_string(doc, "missing") is None
        assert parser.get_optional_string(doc, "missing", "default") == "default"

    def test_get_list(self, parser: FrontmatterParser) -> None:
        """Test getting a list value."""
        doc = ParsedDocument(
            frontmatter={"tools": ["read", "edit"], "single": "value"},
            body="",
            source_path=Path("test.md"),
        )

        assert parser.get_list(doc, "tools") == ["read", "edit"]
        assert parser.get_list(doc, "single") == ["value"]
        assert parser.get_list(doc, "missing") == []

    def test_get_dict(self, parser: FrontmatterParser) -> None:
        """Test getting a dict value."""
        doc = ParsedDocument(
            frontmatter={"permissions": {"edit": "allow"}},
            body="",
            source_path=Path("test.md"),
        )

        assert parser.get_dict(doc, "permissions") == {"edit": "allow"}
        assert parser.get_dict(doc, "missing") == {}

    def test_get_float(self, parser: FrontmatterParser) -> None:
        """Test getting a float value."""
        doc = ParsedDocument(
            frontmatter={"temperature": 0.5, "invalid": "not-a-number"},
            body="",
            source_path=Path("test.md"),
        )

        assert parser.get_float(doc, "temperature", 0.1) == 0.5
        assert parser.get_float(doc, "missing", 0.1) == 0.1
        assert parser.get_float(doc, "invalid", 0.1) == 0.1

    def test_get_int(self, parser: FrontmatterParser) -> None:
        """Test getting an integer value."""
        doc = ParsedDocument(
            frontmatter={"steps": 40, "invalid": "not-a-number"},
            body="",
            source_path=Path("test.md"),
        )

        assert parser.get_int(doc, "steps", 10) == 40
        assert parser.get_int(doc, "missing", 10) == 10
        assert parser.get_int(doc, "invalid", 10) == 10

    def test_get_bool(self, parser: FrontmatterParser) -> None:
        """Test getting a boolean value."""
        doc = ParsedDocument(
            frontmatter={
                "enabled": True,
                "disabled": False,
                "yes_str": "yes",
                "no_str": "no",
            },
            body="",
            source_path=Path("test.md"),
        )

        assert parser.get_bool(doc, "enabled", False) is True
        assert parser.get_bool(doc, "disabled", True) is False
        assert parser.get_bool(doc, "yes_str", False) is True
        assert parser.get_bool(doc, "no_str", True) is False
        assert parser.get_bool(doc, "missing", True) is True
