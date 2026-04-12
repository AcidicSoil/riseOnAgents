"""Tests for selection state models."""

import pytest

from riseon_agents.models.selection import SelectableNode, SelectionState


class TestSelectionState:
    """Tests for the SelectionState enum."""

    def test_selection_state_values(self) -> None:
        """Test that all selection states exist."""
        assert SelectionState.UNSELECTED is not None
        assert SelectionState.SELECTED is not None
        assert SelectionState.PARTIAL is not None

    def test_selection_states_are_distinct(self) -> None:
        """Test that selection states are distinct."""
        states = [SelectionState.UNSELECTED, SelectionState.SELECTED, SelectionState.PARTIAL]
        assert len(set(states)) == 3


class TestSelectableNode:
    """Tests for the SelectableNode dataclass."""

    def test_create_minimal_node(self) -> None:
        """Test creating a node with minimal required fields."""
        node = SelectableNode(
            node_id="node-1",
            label="Test Node",
            node_type="primary",
        )
        assert node.node_id == "node-1"
        assert node.label == "Test Node"
        assert node.node_type == "primary"
        assert node.state == SelectionState.UNSELECTED

    def test_create_full_node(self) -> None:
        """Test creating a node with all fields."""
        node = SelectableNode(
            node_id="node-1",
            label="Test Node",
            node_type="subagent",
            state=SelectionState.SELECTED,
            parent_id="parent-1",
            children_ids=["child-1", "child-2"],
            data={"key": "value"},
        )
        assert node.state == SelectionState.SELECTED
        assert node.parent_id == "parent-1"
        assert node.children_ids == ["child-1", "child-2"]
        assert node.data == {"key": "value"}

    def test_node_requires_id(self) -> None:
        """Test that node requires an ID."""
        with pytest.raises(ValueError, match="Node ID cannot be empty"):
            SelectableNode(node_id="", label="Test", node_type="primary")

    def test_node_requires_label(self) -> None:
        """Test that node requires a label."""
        with pytest.raises(ValueError, match="Node label cannot be empty"):
            SelectableNode(node_id="node-1", label="", node_type="primary")

    def test_node_requires_valid_type(self) -> None:
        """Test that node requires a valid type."""
        with pytest.raises(ValueError, match="Invalid node_type"):
            SelectableNode(node_id="node-1", label="Test", node_type="invalid")

    def test_valid_node_types(self) -> None:
        """Test all valid node types."""
        for node_type in ["primary", "subagent", "rule", "skill"]:
            node = SelectableNode(node_id="node-1", label="Test", node_type=node_type)
            assert node.node_type == node_type

    def test_is_leaf_property(self) -> None:
        """Test the is_leaf property."""
        leaf = SelectableNode(node_id="leaf", label="Leaf", node_type="skill")
        assert leaf.is_leaf is True

        parent = SelectableNode(
            node_id="parent",
            label="Parent",
            node_type="primary",
            children_ids=["child-1"],
        )
        assert parent.is_leaf is False

    def test_is_selected_property(self) -> None:
        """Test the is_selected property."""
        node = SelectableNode(node_id="node-1", label="Test", node_type="primary")
        assert node.is_selected is False

        node.state = SelectionState.SELECTED
        assert node.is_selected is True

        node.state = SelectionState.PARTIAL
        assert node.is_selected is False

    def test_is_partial_property(self) -> None:
        """Test the is_partial property."""
        node = SelectableNode(node_id="node-1", label="Test", node_type="primary")
        assert node.is_partial is False

        node.state = SelectionState.PARTIAL
        assert node.is_partial is True

    def test_toggle_unselected_to_selected(self) -> None:
        """Test toggling from unselected to selected."""
        node = SelectableNode(node_id="node-1", label="Test", node_type="primary")
        assert node.state == SelectionState.UNSELECTED

        new_state = node.toggle()
        assert new_state == SelectionState.SELECTED
        assert node.state == SelectionState.SELECTED

    def test_toggle_selected_to_unselected(self) -> None:
        """Test toggling from selected to unselected."""
        node = SelectableNode(
            node_id="node-1",
            label="Test",
            node_type="primary",
            state=SelectionState.SELECTED,
        )

        new_state = node.toggle()
        assert new_state == SelectionState.UNSELECTED
        assert node.state == SelectionState.UNSELECTED

    def test_toggle_partial_to_selected(self) -> None:
        """Test toggling from partial to selected (selects all)."""
        node = SelectableNode(
            node_id="node-1",
            label="Test",
            node_type="primary",
            state=SelectionState.PARTIAL,
        )

        new_state = node.toggle()
        assert new_state == SelectionState.SELECTED
        assert node.state == SelectionState.SELECTED

    def test_get_selection_icon(self) -> None:
        """Test getting selection icons."""
        node = SelectableNode(node_id="node-1", label="Test", node_type="primary")

        node.state = SelectionState.UNSELECTED
        assert node.get_selection_icon() == "\u2610"  # Empty checkbox

        node.state = SelectionState.SELECTED
        assert node.get_selection_icon() == "\u2611"  # Checked checkbox

        node.state = SelectionState.PARTIAL
        assert node.get_selection_icon() == "\u25ea"  # Partial square

    def test_default_values(self) -> None:
        """Test default values for optional fields."""
        node = SelectableNode(node_id="node-1", label="Test", node_type="primary")
        assert node.state == SelectionState.UNSELECTED
        assert node.parent_id is None
        assert node.children_ids == []
        assert node.data is None
