"""Frontmatter parser for agent definition files.

Parses YAML frontmatter and Markdown body from agent .md files.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import frontmatter


@dataclass
class ParsedDocument:
    """Result of parsing a markdown document with YAML frontmatter."""

    frontmatter: dict[str, Any]
    body: str
    source_path: Path


class FrontmatterParser:
    """Parser for YAML frontmatter + Markdown documents."""

    def parse_file(self, path: Path) -> ParsedDocument:
        """Parse a markdown file with YAML frontmatter.

        Args:
            path: Path to the markdown file

        Returns:
            ParsedDocument with frontmatter dict and body string

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file cannot be parsed
        """
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        try:
            with open(path, encoding="utf-8") as f:
                post = frontmatter.load(f)
                return ParsedDocument(
                    frontmatter=dict(post.metadata),
                    body=post.content,
                    source_path=path,
                )
        except Exception as e:
            raise ValueError(f"Failed to parse {path}: {e}") from e

    def parse_string(self, content: str, source_path: Path | None = None) -> ParsedDocument:
        """Parse a string containing YAML frontmatter and Markdown.

        Args:
            content: The markdown content with YAML frontmatter
            source_path: Optional source path for the document

        Returns:
            ParsedDocument with frontmatter dict and body string

        Raises:
            ValueError: If the content cannot be parsed
        """
        try:
            post = frontmatter.loads(content)
            return ParsedDocument(
                frontmatter=dict(post.metadata),
                body=post.content,
                source_path=source_path or Path("<string>"),
            )
        except Exception as e:
            raise ValueError(f"Failed to parse content: {e}") from e

    def get_required_string(self, doc: ParsedDocument, key: str, context: str = "") -> str:
        """Get a required string value from frontmatter.

        Args:
            doc: The parsed document
            key: The frontmatter key to retrieve
            context: Additional context for error messages

        Returns:
            The string value

        Raises:
            ValueError: If the key is missing or not a string
        """
        value = doc.frontmatter.get(key)
        if value is None:
            ctx = f" ({context})" if context else ""
            raise ValueError(f"Missing required field '{key}'{ctx} in {doc.source_path}")
        if not isinstance(value, str):
            raise ValueError(f"Field '{key}' must be a string in {doc.source_path}")
        return value

    def get_optional_string(
        self, doc: ParsedDocument, key: str, default: str | None = None
    ) -> str | None:
        """Get an optional string value from frontmatter.

        Args:
            doc: The parsed document
            key: The frontmatter key to retrieve
            default: Default value if key is missing

        Returns:
            The string value or default
        """
        value = doc.frontmatter.get(key, default)
        if value is None:
            return default
        return str(value)

    def get_list(self, doc: ParsedDocument, key: str) -> list[Any]:
        """Get a list value from frontmatter.

        Args:
            doc: The parsed document
            key: The frontmatter key to retrieve

        Returns:
            The list value or empty list if missing
        """
        value = doc.frontmatter.get(key, [])
        if not isinstance(value, list):
            return [value] if value else []
        return value

    def get_dict(self, doc: ParsedDocument, key: str) -> dict[str, Any]:
        """Get a dict value from frontmatter.

        Args:
            doc: The parsed document
            key: The frontmatter key to retrieve

        Returns:
            The dict value or empty dict if missing
        """
        value = doc.frontmatter.get(key, {})
        if not isinstance(value, dict):
            return {}
        return value

    def get_float(self, doc: ParsedDocument, key: str, default: float) -> float:
        """Get a float value from frontmatter.

        Args:
            doc: The parsed document
            key: The frontmatter key to retrieve
            default: Default value if key is missing

        Returns:
            The float value or default
        """
        value = doc.frontmatter.get(key, default)
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    def get_int(self, doc: ParsedDocument, key: str, default: int) -> int:
        """Get an integer value from frontmatter.

        Args:
            doc: The parsed document
            key: The frontmatter key to retrieve
            default: Default value if key is missing

        Returns:
            The integer value or default
        """
        value = doc.frontmatter.get(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def get_bool(self, doc: ParsedDocument, key: str, default: bool) -> bool:
        """Get a boolean value from frontmatter.

        Args:
            doc: The parsed document
            key: The frontmatter key to retrieve
            default: Default value if key is missing

        Returns:
            The boolean value or default
        """
        value = doc.frontmatter.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1", "on")
        return bool(value)
