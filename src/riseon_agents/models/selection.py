"""Selection state models for RiseOn.Agents TUI.

Defines the tri-state selection system used in the agent tree.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass


class SelectionState(Enum):
    """Tri-state selection for tree nodes."""

    UNSELECTED = auto()  # Not selected
    SELECTED = auto()  # Fully selected
    PARTIAL = auto()  # Some children selected


@dataclass
class SelectableNode:
    """Tree node with selection state.

    Represents a node in the agent tree that can be selected.
    """

    # Node identity
    node_id: str  # Unique within tree
    label: str  # Display text
    node_type: str  # "primary", "subagent", "rule", "skill"

    # Selection
    state: SelectionState = SelectionState.UNSELECTED

    # Hierarchy
    parent_id: str | None = None
    children_ids: list[str] = field(default_factory=list)

    # Data reference - stores the actual model object
    data: Any = None  # PrimaryAgent | Subagent | Rule | Skill | None

    def __post_init__(self) -> None:
        """Validate node data after initialization."""
        if not self.node_id:
            raise ValueError("Node ID cannot be empty")
        if not self.label:
            raise ValueError("Node label cannot be empty")
        if self.node_type not in ("primary", "subagent", "rule", "skill"):
            raise ValueError(
                f"Invalid node_type '{self.node_type}'. "
                "Must be 'primary', 'subagent', 'rule', or 'skill'."
            )

    @property
    def is_leaf(self) -> bool:
        """Check if this node is a leaf (no children)."""
        return len(self.children_ids) == 0

    @property
    def is_selected(self) -> bool:
        """Check if this node is selected."""
        return self.state == SelectionState.SELECTED

    @property
    def is_partial(self) -> bool:
        """Check if this node has partial selection."""
        return self.state == SelectionState.PARTIAL

    def toggle(self) -> SelectionState:
        """Toggle selection state.

        Returns the new state after toggling.
        - UNSELECTED -> SELECTED
        - SELECTED -> UNSELECTED
        - PARTIAL -> SELECTED (selects all)
        """
        if self.state == SelectionState.UNSELECTED:
            self.state = SelectionState.SELECTED
        elif self.state == SelectionState.SELECTED:
            self.state = SelectionState.UNSELECTED
        else:  # PARTIAL -> select all
            self.state = SelectionState.SELECTED
        return self.state

    def get_selection_icon(self) -> str:
        """Get the Unicode icon for current selection state."""
        icons = {
            SelectionState.UNSELECTED: "\u2610",  # Empty checkbox
            SelectionState.SELECTED: "\u2611",  # Checked checkbox
            SelectionState.PARTIAL: "\u25ea",  # Partially filled square
        }
        return icons[self.state]
