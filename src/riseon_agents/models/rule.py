"""Rule data model for RiseOn.Agents.

Defines the Rule dataclass that represents behavioral guidelines and guardrails.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Rule:
    """Rule definition (maps to Kilo Code Custom Rules).

    Represents a behavioral guideline or guardrail.
    Parsed from {agent-name}/rules/*.md files.
    """

    # Identity
    name: str  # Derived from filename

    # Content
    content: str  # Markdown content

    # Configuration
    is_shared: bool = True  # True = all modes, False = mode-specific
    mode_slug: str | None = None  # If not shared, which mode

    # Metadata
    source_path: Path | None = None

    def __post_init__(self) -> None:
        """Validate rule data after initialization."""
        if not self.name:
            raise ValueError("Rule name cannot be empty")
        if not self.content:
            raise ValueError("Rule content cannot be empty")
        if not self.is_shared and not self.mode_slug:
            raise ValueError("Mode-specific rules must have mode_slug set")

    @property
    def filename(self) -> str:
        """Generate the output filename for this rule."""
        return f"{self.name.lower().replace(' ', '-')}.md"
