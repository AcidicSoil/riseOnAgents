"""Main Textual application.

Implements T032: User Story 1 - Create KiloGeneratorApp.
"""

from pathlib import Path

from textual.app import App

from riseon_agents.parsing.repository import AgentRepository
from riseon_agents.screens.dialogs import EmptyAgentsDialog
from riseon_agents.screens.main import MainScreen
from riseon_agents.widgets.help_overlay import HelpOverlay


class KiloGeneratorApp(App):
    """Main application for the Kilo Code Configuration Generator.

    This app provides a TUI for viewing agent hierarchies, selecting
    agents, and generating Kilo Code configuration files.
    """

    TITLE = "RiseOn.Agents - Kilo Code Generator"
    SUB_TITLE = "Generate Kilo Code configurations from agent definitions"

    CSS = """
    Screen {
        align: center middle;
    }
    
    #loading {
        text-align: center;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("?", "help", "Help"),
    ]

    def __init__(self) -> None:
        """Initialize the application."""
        super().__init__()
        self.agent_repository: AgentRepository | None = None
        self.agents_path: Path = Path("agents")

    def on_mount(self) -> None:
        """Handle application mount event."""
        # Set up the agent repository
        self.agent_repository = AgentRepository(self.agents_path)

        # Check if agents folder exists and has content
        if not self._check_agents_folder():
            self.push_screen(EmptyAgentsDialog(), self._on_empty_agents_dismiss)
            return

        # Load agents and show main screen
        self._load_agents_and_show_main()

    def _check_agents_folder(self) -> bool:
        """Check if the agents folder exists and has agent definitions.

        Returns:
            True if agents folder exists and has content, False otherwise.
        """
        if not self.agents_path.exists():
            return False

        if not self.agents_path.is_dir():
            return False

        # Check for any .agent.md files
        try:
            for item in self.agents_path.iterdir():
                if item.is_dir():
                    # Check for primary agent file
                    agent_file = item / f"{item.name}.agent.md"
                    if agent_file.exists():
                        return True
        except (OSError, PermissionError):
            return False

        return False

    def _load_agents_and_show_main(self) -> None:
        """Load agents from repository and display the main screen."""
        try:
            # Discover all agents
            primary_agents = self.agent_repository.discover_agents()

            # Create and push main screen
            main_screen = MainScreen()
            self.push_screen(main_screen)

            # Populate the tree
            if main_screen.agent_tree:
                main_screen.agent_tree.populate_from_agents(primary_agents)

        except Exception as e:
            # Show error screen
            from riseon_agents.screens.dialogs import ErrorDialog

            self.push_screen(
                ErrorDialog(
                    title="Error Loading Agents",
                    message=f"Failed to load agents: {e}",
                    actions=[("Exit", "exit")],
                ),
                self._on_error_dismiss,
            )

    def _on_empty_agents_dismiss(self, result: str | None) -> None:
        """Handle dismiss of empty agents dialog.

        Args:
            result: The button that was pressed.
        """
        self.exit()

    def _on_error_dismiss(self, result: str | None) -> None:
        """Handle dismiss of error dialog.

        Args:
            result: The button that was pressed.
        """
        self.exit()

    def action_help(self) -> None:
        """T084: Show help overlay with keyboard shortcuts."""
        self.push_screen(HelpOverlay())
