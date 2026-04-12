"""Help overlay widget for displaying keyboard shortcuts.

Implements T084: User Story - Help System with keyboard shortcuts.
"""

from textual.app import ComposeResult
from textual.containers import Container, Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static


class HelpOverlay(ModalScreen):
    """Help overlay displaying keyboard shortcuts and usage information.

    Shows all available keyboard shortcuts organized by category,
    accessible via the '?' key.
    """

    DEFAULT_CSS = """
    HelpOverlay {
        align: center middle;
    }
    
    HelpOverlay > Container {
        width: 70;
        height: auto;
        max-height: 35;
        border: solid $primary;
        background: $surface;
        padding: 1 2;
    }
    
    HelpOverlay > Container > Label {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
        color: $primary;
    }
    
    HelpOverlay > Container > Grid {
        grid-size: 2;
        grid-gutter: 1;
        margin-bottom: 1;
    }
    
    HelpOverlay > Container > Grid > Static.key {
        text-style: bold;
        color: $text-accent;
        content-align: right middle;
    }
    
    HelpOverlay > Container > Grid > Static.desc {
        color: $text;
    }
    
    HelpOverlay > Container > Static.category {
        text-style: bold;
        color: $success;
        margin-top: 1;
        margin-bottom: 1;
    }
    
    HelpOverlay > Container > Button {
        margin: 1 auto;
    }
    """

    BINDINGS = [
        ("escape", "dismiss", "Close Help"),
        ("q", "dismiss", "Close Help"),
    ]

    # Define keyboard shortcuts by category
    SHORTCUTS = {
        "Navigation": [
            ("↑/↓", "Navigate up/down in tree"),
            ("←/→", "Collapse/expand tree nodes"),
            ("Tab", "Switch between panels"),
            ("Enter/Space", "Toggle selection"),
        ],
        "Selection": [
            ("Space", "Select/deselect agent"),
            ("a", "Select all agents"),
            ("A", "Deselect all agents"),
        ],
        "Generation": [
            ("g", "Generate configuration files"),
            ("l", "Toggle Local/Global target"),
        ],
        "General": [
            ("?", "Show/hide this help"),
            ("q", "Quit application"),
        ],
    }

    def compose(self) -> ComposeResult:
        """Compose the help overlay."""
        with Container():
            yield Label("⌨ Keyboard Shortcuts")

            for category, shortcuts in self.SHORTCUTS.items():
                yield Static(f"\n{category}", classes="category")

                for key, description in shortcuts:
                    with Grid():
                        yield Static(f"{key}", classes="key")
                        yield Static(description, classes="desc")

            yield Button("Close (Esc)", id="close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        if event.button.id == "close":
            self.dismiss()

    def action_dismiss(self) -> None:
        """Dismiss the overlay."""
        self.dismiss()
