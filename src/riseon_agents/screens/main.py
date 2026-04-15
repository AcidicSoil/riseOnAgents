"""Main screen with tree + preview layout.

Implements T031: User Story 1 - View Agent Hierarchy.
Implements T044: User Story 2 - Selection count in status bar.
Implements T056-T057: User Story 5 - Generate action and progress.
"""

from pathlib import Path
from typing import Any

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, ProgressBar, Static

from riseon_agents.generation.generator import KiloCodeGenerator
from riseon_agents.models.agent import PrimaryAgent
from riseon_agents.models.generation import GenerationLevel, GenerationResult
from riseon_agents.widgets.agent_tree import AgentTree
from riseon_agents.widgets.help_overlay import HelpOverlay
from riseon_agents.widgets.preview import PreviewPanel


class MainScreen(Screen[None]):
    """Main screen with agent tree and preview panels.

    Provides a two-panel layout with the agent tree on the left
    and preview panel on the right (for US3).
    """

    DEFAULT_CSS = """
    MainScreen {
        layout: horizontal;
    }

    #tree-panel {
        width: 40%;
        height: 100%;
        border: solid $primary;
    }

    #preview-panel {
        width: 60%;
        height: 100%;
        border: solid $primary;
    }

    AgentTree {
        height: 100%;
        width: 100%;
    }

    #status-bar {
        height: 1;
        background: $surface-darken-1;
        color: $text;
        padding: 0 1;
        content-align: center middle;
    }

    #progress-bar {
        height: 1;
        margin: 0 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("g", "generate", "Generate"),
        ("l", "toggle_level", "Toggle Level"),
        ("?", "help", "Help"),
        ("tab", "focus_next", "Next Panel"),
    ]

    selected_count = reactive(0)
    generation_level = reactive(GenerationLevel.LOCAL)

    def __init__(self) -> None:
        """Initialize the main screen."""
        super().__init__()
        self.agent_tree: AgentTree | None = None
        self.preview_panel: PreviewPanel | None = None
        self.status_bar: Static | None = None
        self.progress_bar: ProgressBar | None = None
        self.generator = KiloCodeGenerator()

    def compose(self) -> ComposeResult:
        """Compose the screen layout."""
        yield Header()

        with Horizontal():
            # Tree panel (left side, 40%)
            with Vertical(id="tree-panel"):
                self.agent_tree = AgentTree()
                yield self.agent_tree

                # T044: Status bar showing selection count
                self.status_bar = Static("Selected: 0", id="status-bar")
                yield self.status_bar

                # T057: Progress bar for generation
                self.progress_bar = ProgressBar(id="progress-bar", total=100)
                self.progress_bar.display = False
                yield self.progress_bar

            # Preview panel (right side, 60%) - T064: PreviewPanel for US3
            with Vertical(id="preview-panel"):
                self.preview_panel = PreviewPanel()
                yield self.preview_panel

        yield Footer()

    def on_mount(self) -> None:
        """Handle screen mount event."""
        # Focus the tree by default
        if self.agent_tree:
            self.agent_tree.focus()
            # Set up callback for selection changes
            self.agent_tree.set_on_selection_changed(self.update_selection_count)
            # Initial count update
            self.update_selection_count()

    def on_tree_node_highlighted(self, event: Any) -> None:
        """T065: Update preview when tree node is highlighted (focused).

        Args:
            event: Tree node highlighted event.
        """
        if not self.preview_panel or not self.agent_tree:
            return

        node = event.node
        if node is None or node.data is None:
            self.preview_panel.show_placeholder()
            return

        # Get node type and data
        node_type = node.data.node_type if hasattr(node.data, "node_type") else None
        agent_data = node.data.agent if hasattr(node.data, "agent") else None

        if node_type and agent_data:
            # T072: Pass generation level to preview
            self.preview_panel.update_preview(node_type, agent_data, self.generation_level)
        else:
            self.preview_panel.show_placeholder()

    def watch_selected_count(self, count: int) -> None:
        """T044: Update status bar when selection count changes."""
        if self.status_bar:
            total = self._get_total_agent_count()
            level_str = "Local" if self.generation_level == GenerationLevel.LOCAL else "Global"
            self.status_bar.update(f"Selected: {count}/{total} | Target: {level_str}")

    def watch_generation_level(self, _level: GenerationLevel) -> None:
        """Update status bar when generation level changes."""
        if self.status_bar:
            self.selected_count = self.selected_count  # Trigger update

    def _get_total_agent_count(self) -> int:
        """Get total count of selectable agents in the tree."""
        if self.agent_tree is None:
            return 0
        return self.agent_tree.get_total_count()

    def update_selection_count(self) -> None:
        """Refresh the selection count from the tree."""
        if self.agent_tree:
            self.selected_count = self.agent_tree.get_selected_count()

    def action_help(self) -> None:
        """T084: Show help overlay with keyboard shortcuts."""
        self.app.push_screen(HelpOverlay())

    def action_toggle_level(self) -> None:
        """T070: Toggle generation level between Local and Global."""
        if self.generation_level == GenerationLevel.LOCAL:
            self.generation_level = GenerationLevel.GLOBAL
        else:
            self.generation_level = GenerationLevel.LOCAL

        # T072: Update preview to show new target paths
        if self.preview_panel:
            # Refresh the current preview if there's a node selected
            current_data = self.preview_panel.get_current_data()
            current_type = self.preview_panel.get_current_node_type()
            if current_data and current_type:
                self.preview_panel.update_preview(current_type, current_data, self.generation_level)

    def _get_target_path_display(self) -> str:
        """T071: Get the display string for current target path."""
        if self.generation_level == GenerationLevel.LOCAL:
            return "./.kilo/"
        else:
            return "~/.kilocode/"
        """T066: Toggle focus between tree and preview panels on Tab key."""
        if self.agent_tree and self.preview_panel:
            if self.agent_tree.has_focus:
                self.preview_panel.focus()
            else:
                self.agent_tree.focus()

    def action_focus_next(self) -> None:
        """T066: Toggle focus between tree and preview panels on Tab key."""
        if self.agent_tree and self.preview_panel:
            if self.agent_tree.has_focus:
                self.preview_panel.focus()
            else:
                self.agent_tree.focus()

    def action_generate(self) -> None:
        """T056: Generate configuration files for selected agents."""
        if not self.agent_tree:
            return

        # Get selected agents from tree
        selected_agents = self._get_selected_agents()

        if not selected_agents:
            self.app.push_screen(
                self._create_error_dialog(
                    "No agents selected. Please select at least one agent to generate."
                )
            )
            return

        # Show progress bar
        if self.progress_bar:
            self.progress_bar.display = True
            self.progress_bar.update(progress=0)

        # Check for existing files
        existing_files = self.generator.check_existing_files(
            selected_agents, self.generation_level, Path.cwd()
        )

        if existing_files:
            # T059: Show confirmation dialog for overwrite
            self.app.push_screen(
                self._create_confirm_dialog(existing_files),
                lambda confirmed: self._do_generate(selected_agents) if confirmed else None,
            )
        else:
            # Generate directly
            self._do_generate(selected_agents)

    def _do_generate(self, agents: list[PrimaryAgent]) -> None:
        """Perform the actual generation.

        Args:
            agents: List of selected PrimaryAgent objects.
        """
        try:
            # Update progress
            if self.progress_bar:
                self.progress_bar.update(progress=30)

            # Generate files
            result = self.generator.generate(
                agents,
                self.generation_level,
                Path.cwd(),
                overwrite=True,
            )

            # Update progress
            if self.progress_bar:
                self.progress_bar.update(progress=100)

            # T058: Show result dialog
            self.app.push_screen(self._create_result_dialog(result))

        except Exception as e:
            self.app.push_screen(self._create_error_dialog(f"Generation failed: {e}"))
        finally:
            # Hide progress bar
            if self.progress_bar:
                self.progress_bar.display = False

    def _get_selected_agents(self) -> list[PrimaryAgent]:
        """Get list of selected PrimaryAgent objects from tree.

        Returns:
            List of selected PrimaryAgent objects.
        """
        if not self.agent_tree:
            return []

        selected = []
        for node in self.agent_tree.root.children:
            if (
                node.data
                and node.data.agent
                and hasattr(node.data.agent, "subagents")
                and node.data.state.value >= 2
            ):
                # This is a PrimaryAgent
                selected.append(node.data.agent)

        return selected

    def _create_error_dialog(self, message: str) -> Any:
        """Create an error dialog.

        Args:
            message: Error message to display.

        Returns:
            ErrorDialog instance.
        """
        from riseon_agents.screens.dialogs import ErrorDialog

        return ErrorDialog(
            title="Generation Error",
            message=message,
        )

    def _create_confirm_dialog(self, existing_files: list[Path]) -> Any:
        """Create a confirmation dialog for overwrite.

        Args:
            existing_files: List of existing file paths.

        Returns:
            ConfirmDialog instance.
        """
        from riseon_agents.screens.dialogs import ConfirmDialog

        file_list = "\n".join([f"- {f.name}" for f in existing_files[:5]])
        if len(existing_files) > 5:
            file_list += f"\n... and {len(existing_files) - 5} more files"

        return ConfirmDialog(
            title="Overwrite Existing Files?",
            message=f"The following files already exist:\n\n{file_list}\n\nDo you want to overwrite them?",
        )

    def _create_result_dialog(self, result: GenerationResult) -> Any:
        """Create a result dialog for generation summary.

        Args:
            result: GenerationResult object.

        Returns:
            ResultDialog instance.
        """
        from riseon_agents.screens.dialogs import ResultDialog

        if result.success:
            created = result.created_count
            updated = result.updated_count

            summary = "Generation completed successfully!\n\n"
            summary += f"Files created: {created}\n"
            summary += f"Files updated: {updated}\n"
            summary += f"Total files: {len(result.files)}"

            # T078, T079: Pass validation errors if any
            validation_errors = (
                result.validation_errors if hasattr(result, "validation_errors") else []
            )

            return ResultDialog(
                title="Generation Complete",
                summary=summary,
                validation_errors=validation_errors,
            )
        error_messages = [file.error_message for file in result.error_files if file.error_message]
        error_summary = error_messages[0] if error_messages else "Unknown error"

        return ResultDialog(
            title="Generation Failed",
            summary=f"Generation failed:\n\n{error_summary}",
        )

    def get_agent_tree(self) -> AgentTree | None:
        """Get the agent tree widget.

        Returns:
            The AgentTree widget or None if not yet composed.
        """
        return self.agent_tree
