"""Dialog screens for the TUI.

Implements T033: User Story 1 - Error screens for missing/empty agents folder.
Implements T078, T079: User Story 6 - Show validation results with file and line info.
"""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static

from riseon_agents.models.generation import ValidationError


class ErrorDialog(ModalScreen[str | None]):
    """Generic error dialog with message and actions.

    Attributes:
        title: Dialog title
        message: Error message to display
        actions: List of (label, action_id) tuples for buttons
    """

    DEFAULT_CSS = """
    ErrorDialog {
        align: center middle;
    }

    ErrorDialog > Container {
        width: 60;
        height: auto;
        max-height: 20;
        border: solid $error;
        background: $surface;
        padding: 1 2;
    }

    ErrorDialog > Container > Label {
        text-align: center;
        text-style: bold;
        color: $error;
        margin-bottom: 1;
    }

    ErrorDialog > Container > Static {
        text-align: center;
        margin-bottom: 1;
    }

    ErrorDialog > Container > Vertical {
        height: auto;
        align: center middle;
    }

    ErrorDialog > Container > Vertical > Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        title: str,
        message: str,
        actions: list[tuple[str, str]] | None = None,
    ) -> None:
        """Initialize the error dialog.

        Args:
            title: Dialog title.
            message: Error message to display.
            actions: List of (label, action_id) tuples for buttons.
                     Defaults to [("OK", "ok")].
        """
        super().__init__()
        self.title = title
        self.message = message
        self.actions = actions or [("OK", "ok")]

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        with Container():
            yield Label(f"⚠ {self.title}")
            yield Static(self.message)

            with Vertical():
                for label, action_id in self.actions:
                    yield Button(label, id=action_id)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        self.dismiss(event.button.id)


class EmptyAgentsDialog(ErrorDialog):
    """Dialog shown when agents folder is empty or missing."""

    def __init__(self) -> None:
        """Initialize the empty agents dialog."""
        super().__init__(
            title="No Agents Found",
            message=(
                "The agents/ folder is empty or missing.\n\n"
                "Please create agent definitions in the agents/ folder "
                "before running this tool."
            ),
            actions=[
                ("Exit", "exit"),
            ],
        )


class ConfirmDialog(ModalScreen[str | None]):
    """Confirmation dialog with Yes/No options.

    Attributes:
        title: Dialog title
        message: Message to display
    """

    DEFAULT_CSS = """
    ConfirmDialog {
        align: center middle;
    }

    ConfirmDialog > Container {
        width: 60;
        height: auto;
        max-height: 20;
        border: solid $primary;
        background: $surface;
        padding: 1 2;
    }

    ConfirmDialog > Container > Label {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    ConfirmDialog > Container > Static {
        text-align: center;
        margin-bottom: 1;
    }

    ConfirmDialog > Container > Vertical {
        height: auto;
        align: center middle;
    }

    ConfirmDialog > Container > Vertical > Button {
        margin: 0 1;
    }
    """

    def __init__(self, title: str, message: str) -> None:
        """Initialize the confirmation dialog.

        Args:
            title: Dialog title.
            message: Message to display.
        """
        super().__init__()
        self.title = title
        self.message = message

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        with Container():
            yield Label(self.title or "")
            yield Static(self.message)

            with Vertical():
                yield Button("Yes", id="yes", variant="primary")
                yield Button("No", id="no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press."""
        self.dismiss(event.button.id)


class ResultDialog(ModalScreen[str]):
    """Dialog showing generation results with validation.

    Implements T078, T079: User Story 6 - Show validation results with file and line info.

    Attributes:
        title: Dialog title
        summary: Summary text to display
        validation_errors: Optional list of validation errors to display
    """

    DEFAULT_CSS = """
    ResultDialog {
        align: center middle;
    }

    ResultDialog > Container {
        width: 80;
        height: auto;
        max-height: 40;
        border: solid $success;
        background: $surface;
        padding: 1 2;
    }

    ResultDialog.error > Container {
        border: solid $error;
    }

    ResultDialog > Container > Label {
        text-align: center;
        text-style: bold;
        color: $success;
        margin-bottom: 1;
    }

    ResultDialog.error > Container > Label {
        color: $error;
    }

    ResultDialog > Container > Static.summary {
        margin-bottom: 1;
    }

    ResultDialog > Container > Static.errors {
        color: $error;
        margin-bottom: 1;
        max-height: 15;
    }

    ResultDialog > Container > Button {
        margin: 1 auto;
    }
    """

    def __init__(
        self,
        title: str,
        summary: str,
        validation_errors: list[ValidationError] | None = None,
    ) -> None:
        """Initialize the result dialog.

        Args:
            title: Dialog title.
            summary: Summary text to display.
            validation_errors: Optional list of validation errors to display.
        """
        super().__init__()
        self.title = title
        self.summary = summary
        self.validation_errors = validation_errors or []

    def compose(self) -> ComposeResult:
        """Compose the dialog."""
        # Set error class if there are validation errors
        if self.validation_errors:
            self.add_class("error")

        with Container():
            # Show checkmark for success, warning for validation errors
            icon = "⚠" if self.validation_errors else "✓"
            yield Label(f"{icon} {self.title}")
            yield Static(self.summary, classes="summary")

            # Show validation errors if present
            if self.validation_errors:
                error_text = self._format_validation_errors()
                yield Static(error_text, classes="errors")

            yield Button("OK", id="ok", variant="primary")

    def _format_validation_errors(self) -> str:
        """Format validation errors for display.

        Returns:
            Formatted string with error details.
        """
        lines = ["Validation Errors:"]
        lines.append("")

        for i, error in enumerate(self.validation_errors[:10], 1):  # Limit to first 10
            location = str(error.file_path.name)
            if error.line_number is not None:
                location += f":{error.line_number}"
                if error.column is not None:
                    location += f":{error.column}"

            lines.append(f"{i}. {location}")
            lines.append(f"   {error.message}")
            lines.append("")

        if len(self.validation_errors) > 10:
            lines.append(f"... and {len(self.validation_errors) - 10} more errors")

        return "\n".join(lines)

    def on_button_pressed(self, _event: Button.Pressed) -> None:
        """Handle button press."""
        self.dismiss("ok")
