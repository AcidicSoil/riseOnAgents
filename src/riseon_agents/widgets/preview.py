"""Preview panel widget for showing generated configuration.

Implements T062-T063: User Story 3 - Preview Generated Configuration.
"""

from typing import Any

from rich.syntax import Syntax
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import Static

from riseon_agents.models.agent import PrimaryAgent, Subagent
from riseon_agents.models.generation import GenerationLevel
from riseon_agents.models.rule import Rule
from riseon_agents.models.skill import Skill


class PreviewPanel(Vertical):
    """Preview panel showing generated configuration for focused agent.

    Provides real-time preview of how the selected agent will be generated
    in Kilo Code format with syntax highlighting.
    """

    DEFAULT_CSS = """
    PreviewPanel {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    PreviewPanel > Static {
        width: 100%;
        height: 100%;
        overflow: auto scroll;
    }

    PreviewPanel .placeholder {
        color: $text-muted;
        text-align: center;
        content-align: center middle;
    }
    """

    current_preview = reactive("")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the preview panel."""
        super().__init__(*args, **kwargs)
        self.content_widget: Static | None = None
        self._current_node_type: str | None = None
        self._current_data: Any | None = None

    def compose(self) -> ComposeResult:
        """Compose the preview panel layout."""
        self.content_widget = Static(self._get_placeholder_text(), id="preview-content")
        yield self.content_widget

    def _get_placeholder_text(self) -> Text:
        """Get placeholder text when no agent is selected."""
        text = Text("Select an agent to preview generated configuration\n\n")
        text.append("Navigate the tree using arrow keys\n", style="dim")
        text.append("Press [Space] to toggle selection\n", style="dim")
        text.append("Press [g] to generate configuration", style="dim")
        return text

    def show_placeholder(self) -> None:
        """Show placeholder text."""
        if self.content_widget:
            self.content_widget.update(self._get_placeholder_text())

    def update_preview(
        self, node_type: str, data: Any, level: GenerationLevel = GenerationLevel.LOCAL
    ) -> None:
        """Update the preview for a selected node.

        Args:
            node_type: Type of node (primary_agent, subagent, rule, skill)
            data: The data object for the node
            level: Generation level (LOCAL or GLOBAL) for path display
        """
        self._current_node_type = node_type
        self._current_data = data

        if data is None:
            self.show_placeholder()
            return

        content = self._generate_preview_content(node_type, data, level)
        self.current_preview = content

        if self.content_widget:
            # Use syntax highlighting for YAML content
            if node_type in ("primary_agent", "subagent"):
                syntax = Syntax(content, "yaml", theme="monokai", line_numbers=True)
                self.content_widget.update(syntax)
            else:
                self.content_widget.update(Text(content))

    def _generate_preview_content(
        self, node_type: str, data: Any, level: GenerationLevel = GenerationLevel.LOCAL
    ) -> str:
        """Generate preview content based on node type.

        Args:
            node_type: Type of node
            data: Node data
            level: Generation level for path display

        Returns:
            Preview content as string.
        """
        if node_type == "primary_agent" and isinstance(data, PrimaryAgent):
            return self.generate_preview_for_agent(data, level)
        elif node_type == "subagent" and isinstance(data, Subagent):
            return self.generate_preview_for_subagent(data, level)
        elif node_type == "rule" and isinstance(data, Rule):
            return self.generate_preview_for_rule(data, level)
        elif node_type == "skill" and isinstance(data, Skill):
            return self.generate_preview_for_skill(data, level)
        else:
            return f"# Preview for {node_type}\n\nNo preview available for this node type."

    def generate_preview_for_agent(
        self, agent: PrimaryAgent, level: GenerationLevel = GenerationLevel.LOCAL
    ) -> str:
        """Generate preview for a PrimaryAgent.

        Shows the custom_modes.yaml entry format (US3-AC2).

        Args:
            agent: The PrimaryAgent to preview.
            level: Generation level for path display.

        Returns:
            Preview content as YAML string.
        """
        # T072: Show target path based on level
        path_prefix = "./.kilo/" if level == GenerationLevel.LOCAL else "~/.kilocode/"

        lines = [
            f"# Target: {path_prefix}custom_modes.yaml",
            f"# For agent: {agent.name}",
            "",
            "customModes:",
            f"  - slug: {agent.slug}",
            f"    name: {agent.display_name}",
            f"    description: {agent.description}",
            "    roleDefinition: |",
        ]

        # Add markdown body as literal block
        for line in agent.markdown_body.split("\n"):
            lines.append(f"      {line}")

        # Add groups based on permissions
        groups = self._map_permissions_to_groups(agent.permissions)
        if groups:
            lines.append("    groups:")
            for group in groups:
                lines.append(f"      - {group}")

        lines.append("")
        lines.append(f"# Total subagents: {len(agent.subagents)}")
        lines.append(f"# Total rules: {len(agent.rules)}")
        lines.append(f"# Total skills: {len(agent.skills)}")

        return "\n".join(lines)

    def generate_preview_for_subagent(
        self, subagent: Subagent, level: GenerationLevel = GenerationLevel.LOCAL
    ) -> str:
        """Generate preview for a Subagent.

        Shows the .kilo/agents/*.md format (US3-AC3).

        Args:
            subagent: The Subagent to preview.
            level: Generation level for path display.

        Returns:
            Preview content as Markdown/YAML frontmatter string.
        """
        # T072: Show target path based on level
        path_prefix = "./.kilo/" if level == GenerationLevel.LOCAL else "~/.kilocode/"

        lines = [
            "---",
            f"# File: {path_prefix}agents/{subagent.slug}.md",
            f"# Generated for: {subagent.parent_agent}/{subagent.name}",
            f"description: {subagent.description}",
            "mode: subagent",
            f"temperature: {subagent.temperature}",
            "permission:",
        ]

        # Add permissions
        if subagent.permissions:
            for perm_name, perm_level in subagent.permissions.items():
                lines.append(f"  {perm_name}: {perm_level.value}")
        else:
            lines.append("  edit: ask")
            lines.append("  bash: deny")

        lines.append("---")
        lines.append("")
        lines.append(subagent.markdown_body)

        return "\n".join(lines)

    def generate_preview_for_rule(
        self, rule: Rule, level: GenerationLevel = GenerationLevel.LOCAL
    ) -> str:
        """Generate preview for a Rule.

        Args:
            rule: The Rule to preview.
            level: Generation level for path display.

        Returns:
            Preview content as string.
        """
        # T072: Show target path based on level
        path_prefix = "./.kilo/" if level == GenerationLevel.LOCAL else "~/.kilocode/"

        lines = [
            f"# Target: {path_prefix}rules/{rule.filename}",
            f"# Rule: {rule.name}",
            "",
            rule.content,
        ]

        return "\n".join(lines)

    def generate_preview_for_skill(
        self, skill: Skill, level: GenerationLevel = GenerationLevel.LOCAL
    ) -> str:
        """Generate preview for a Skill.

        Args:
            skill: The Skill to preview.
            level: Generation level for path display.

        Returns:
            Preview content as string.
        """
        # T072: Show target path based on level
        path_prefix = "./.kilocode/" if level == GenerationLevel.LOCAL else "~/.kilocode/"

        lines = [
            f"# Target: {path_prefix}skills/{skill.name}/SKILL.md",
            f"# Skill: {skill.name}",
            f"# Description: {skill.description}",
            "",
            skill.content,
        ]

        return "\n".join(lines)

    def _map_permissions_to_groups(self, permissions: dict[str, Any]) -> list[str]:
        """Map agent permissions to Kilo Code groups.

        Args:
            permissions: Dictionary of permission names to levels.

        Returns:
            List of group names for Kilo Code.
        """
        from riseon_agents.models.agent import PermissionLevel

        groups = ["read"]  # Always include read

        if permissions.get("edit") == PermissionLevel.ALLOW:
            groups.append("edit")

        if permissions.get("bash") == PermissionLevel.ALLOW:
            groups.append("command")

        if permissions.get("webfetch") == PermissionLevel.ALLOW:
            groups.append("browser")

        if permissions.get("mcp") == PermissionLevel.ALLOW:
            groups.append("mcp")

        return groups

    def get_current_node_type(self) -> str | None:
        """Get the current node type being previewed.

        Returns:
            Node type string or None.
        """
        return self._current_node_type

    def get_current_data(self) -> Any | None:
        """Get the current data being previewed.

        Returns:
            Current data object or None.
        """
        return self._current_data

    def clear(self) -> None:
        """Clear the preview panel."""
        self._current_node_type = None
        self._current_data = None
        self.show_placeholder()
