"""Agent tree widget for displaying agent hierarchy.

Implements T027-T030: User Story 1 - View Agent Hierarchy.
"""

from dataclasses import dataclass, field
from typing import Any

from textual.widgets import Tree
from textual.widgets.tree import TreeNode

from riseon_agents.models.agent import PrimaryAgent, Subagent
from riseon_agents.models.rule import Rule
from riseon_agents.models.selection import SelectionState
from riseon_agents.models.skill import Skill


@dataclass
class AgentTreeNode:
    """Data associated with a tree node.

    Attributes:
        id: Unique identifier for the node
        label: Display label
        node_type: Type of node (primary_agent, subagent, rule, skill)
        state: Current selection state
        agent: Associated agent object (for primary_agent and subagent types)
        has_warning: Whether this node has a warning
        warnings: List of warning messages
    """

    id: str
    label: str
    node_type: str  # primary_agent, subagent, rule, skill
    state: SelectionState = field(default=SelectionState.UNSELECTED)
    agent: Any | None = None
    has_warning: bool = False
    warnings: list[str] = field(default_factory=list)

    def toggle(self) -> None:
        """Toggle selection state between UNSELECTED and SELECTED."""
        if self.state == SelectionState.UNSELECTED:
            self.state = SelectionState.SELECTED
        elif self.state == SelectionState.SELECTED:
            self.state = SelectionState.UNSELECTED
        # If PARTIAL, toggle to SELECTED
        elif self.state == SelectionState.PARTIAL:
            self.state = SelectionState.SELECTED

    def get_icon(self) -> str:
        """Get the icon for this node based on type and state.

        Returns:
            String containing the appropriate icon.
        """
        # Type icons
        type_icons = {
            "primary_agent": "◉",
            "subagent": "○",
            "rule": "▪",
            "skill": "★",
        }

        # Selection state icons
        state_icons = {
            SelectionState.UNSELECTED: "☐",
            SelectionState.SELECTED: "☑",
            SelectionState.PARTIAL: "◪",
        }

        type_icon = type_icons.get(self.node_type, "○")
        state_icon = state_icons.get(self.state, "☐")
        warning_icon = "⚠" if self.has_warning else ""

        parts = [state_icon, type_icon]
        if warning_icon:
            parts.append(warning_icon)

        return " ".join(parts)

    def get_label(self) -> str:
        """Get the full display label with icon."""
        icon = self.get_icon()
        return f"{icon} {self.label}"


class AgentTree(Tree):
    """Tree widget for displaying agent hierarchy.

    Extends Textual's Tree widget to provide agent-specific
    functionality including hierarchical display of Primary Agents,
    Subagents, Rules, and Skills.
    """

    DEFAULT_CSS = """
    AgentTree {
        width: 100%;
        height: 100%;
    }
    
    AgentTree > .tree--cursor {
        background: $surface-darken-1;
    }
    
    AgentTree > .tree--highlight {
        background: $surface-darken-2;
    }
    """

    BINDINGS = [
        ("space", "toggle_selection", "Toggle Selection"),
        ("a", "select_all", "Select All"),
        ("A", "deselect_all", "Deselect All"),
    ]

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the agent tree."""
        super().__init__("Agents", *args, **kwargs)
        self.root.expand()
        self._on_selection_changed: callable | None = None

    def set_on_selection_changed(self, callback: callable) -> None:
        """Set callback for when selection changes.

        Args:
            callback: Function to call when selection changes.
        """
        self._on_selection_changed = callback

    def _notify_selection_changed(self) -> None:
        """Notify that selection has changed."""
        if self._on_selection_changed:
            self._on_selection_changed()

    def populate_from_agents(self, agents: list[PrimaryAgent]) -> None:
        """Populate the tree from a list of PrimaryAgent objects.

        Args:
            agents: List of PrimaryAgent objects to display.
        """
        self.remove_children(self.root)

        for agent in agents:
            self._add_primary_agent(agent)

    def _add_primary_agent(self, agent: PrimaryAgent) -> TreeNode:
        """Add a Primary Agent node to the tree.

        Args:
            agent: The PrimaryAgent to add.

        Returns:
            The created TreeNode.
        """
        # Create node data
        has_warnings = hasattr(agent, "warnings") and bool(agent.warnings)
        warnings = getattr(agent, "warnings", [])

        node_data = AgentTreeNode(
            id=agent.name,
            label=agent.name.replace("-", " ").title(),
            node_type="primary_agent",
            agent=agent,
            has_warning=has_warnings,
            warnings=warnings,
        )

        # Add to tree
        node = self.root.add(node_data.get_label(), data=node_data)
        node.expand()

        # Add subagents
        if agent.subagents:
            subagents_node = node.add("Subagents")
            subagents_node.expand()
            for subagent in agent.subagents:
                self._add_subagent(subagents_node, subagent, agent.name)

        # Add rules
        if agent.rules:
            rules_node = node.add("Rules")
            rules_node.expand()
            for rule in agent.rules:
                self._add_rule(rules_node, rule)

        # Add skills
        if agent.skills:
            skills_node = node.add("Skills")
            skills_node.expand()
            for skill in agent.skills:
                self._add_skill(skills_node, skill)

        return node

    def _add_subagent(self, parent: TreeNode, subagent: Subagent, parent_name: str) -> TreeNode:
        """Add a Subagent node under a parent.

        Args:
            parent: Parent TreeNode.
            subagent: The Subagent to add.
            parent_name: Name of the parent agent.

        Returns:
            The created TreeNode.
        """
        node_data = AgentTreeNode(
            id=f"{parent_name}/{subagent.name}",
            label=subagent.name.replace("-", " ").title(),
            node_type="subagent",
            agent=subagent,
        )

        return parent.add(node_data.get_label(), data=node_data)

    def _add_rule(self, parent: TreeNode, rule: Rule) -> TreeNode:
        """Add a Rule node under a parent.

        Args:
            parent: Parent TreeNode.
            rule: The Rule to add.

        Returns:
            The created TreeNode.
        """
        node_data = AgentTreeNode(
            id=rule.name,
            label=rule.name.replace("-", " ").title(),
            node_type="rule",
        )

        return parent.add(node_data.get_label(), data=node_data)

    def _add_skill(self, parent: TreeNode, skill: Skill) -> TreeNode:
        """Add a Skill node under a parent.

        Args:
            parent: Parent TreeNode.
            skill: The Skill to add.

        Returns:
            The created TreeNode.
        """
        node_data = AgentTreeNode(
            id=skill.name,
            label=skill.name.replace("-", " ").title(),
            node_type="skill",
        )

        return parent.add(node_data.get_label(), data=node_data)

    def remove_children(self, node: TreeNode) -> None:
        """Remove all children from a node.

        Args:
            node: The node to clear.
        """
        # Textual's Tree doesn't have a direct clear method
        # We need to remove children one by one
        while node.children:
            child = node.children[-1]
            node.remove_child(child)

    def select_node(self, node: TreeNode) -> None:
        """Select a node and scroll to make it visible.

        Args:
            node: The node to select.
        """
        # Call parent class's select_node method
        Tree.select_node(self, node)
        self.scroll_to_node(node)

    def action_cursor_up(self) -> None:
        """Move cursor up."""
        super().action_cursor_up()

    def action_cursor_down(self) -> None:
        """Move cursor down."""
        super().action_cursor_down()

    def action_select_node(self) -> None:
        """Toggle expand/collapse on the current node."""
        if self.cursor_node is not None:
            self.cursor_node.toggle()

    def action_toggle_selection(self) -> None:
        """T039: Toggle selection on Space key with propagation."""
        if self.cursor_node is not None and self.cursor_node.data is not None:
            self.toggle_selection_with_propagation(self.cursor_node)
            self._update_all_labels()
            self._notify_selection_changed()

    def action_select_all(self) -> None:
        """Action handler for 'a' key to select all."""
        self.select_all()
        self._notify_selection_changed()

    def action_deselect_all(self) -> None:
        """Action handler for 'A' key to deselect all."""
        self.deselect_all()
        self._notify_selection_changed()

    def toggle_selection_with_propagation(self, node: TreeNode) -> None:
        """T039, T040: Toggle selection and propagate to children.

        Args:
            node: The node to toggle selection on.
        """
        if node.data is None:
            return

        # Toggle the node's selection state
        node.data.toggle()
        new_state = node.data.state

        # Propagate to all children (T040)
        self._propagate_selection_to_children(node, new_state)

        # Update parent state (T041)
        self._update_parent_state_recursive(node)

        # Update the node's label to reflect new state
        self._update_node_label(node)

    def _propagate_selection_to_children(self, node: TreeNode, state: SelectionState) -> None:
        """T040: Propagate selection state to all children recursively.

        Args:
            node: The parent node.
            state: The selection state to propagate.
        """
        for child in node.children:
            if child.data is not None:
                child.data.state = state
                self._update_node_label(child)
            # Always recurse to grandchildren, even if current child has no data
            self._propagate_selection_to_children(child, state)

    def _update_parent_state_recursive(self, node: TreeNode) -> None:
        """T041: Update parent state based on children.

        Args:
            node: The node whose parent needs updating.
        """
        # Find parent by traversing up
        parent = self._find_parent_node(node)
        if parent is None or parent.data is None:
            return

        # Calculate state based on children
        self._calculate_partial_state(parent)
        self._update_node_label(parent)

        # Continue up the tree
        self._update_parent_state_recursive(parent)

    def _find_parent_node(self, node: TreeNode) -> TreeNode | None:
        """Find the parent of a given node.

        Args:
            node: The child node.

        Returns:
            The parent TreeNode or None.
        """
        # Search from root to find parent
        return self._find_parent_recursive(self.root, node)

    def _find_parent_recursive(self, current: TreeNode, target: TreeNode) -> TreeNode | None:
        """Recursively search for parent of target node.

        Args:
            current: Current node being checked.
            target: The node to find parent for.

        Returns:
            The parent TreeNode or None.
        """
        for child in current.children:
            if child is target:
                return current
            result = self._find_parent_recursive(child, target)
            if result is not None:
                return result
        return None

    def _calculate_partial_state(self, node: TreeNode) -> None:
        """T041: Calculate if parent should show PARTIAL state.

        Args:
            node: The parent node to calculate state for.
        """
        if node.data is None:
            return

        # Get all descendant nodes with data (not just direct children)
        descendants = []
        self._collect_descendants_with_data(node, descendants, skip_self=True)

        if not descendants:
            return

        # Check states
        selected_count = sum(1 for n in descendants if n.data.state == SelectionState.SELECTED)
        unselected_count = sum(1 for n in descendants if n.data.state == SelectionState.UNSELECTED)
        total = len(descendants)

        if selected_count == total:
            node.data.state = SelectionState.SELECTED
        elif unselected_count == total:
            node.data.state = SelectionState.UNSELECTED
        else:
            node.data.state = SelectionState.PARTIAL

    def _collect_descendants_with_data(
        self, node: TreeNode, result: list, skip_self: bool = False
    ) -> None:
        """Collect all descendant nodes that have data.

        Args:
            node: Current node.
            result: List to collect nodes into.
            skip_self: If True, don't include the starting node.
        """
        if not skip_self and node.data is not None:
            result.append(node)

        for child in node.children:
            self._collect_descendants_with_data(child, result, skip_self=False)

    def _update_parent_state(self, node: TreeNode) -> None:
        """Update parent state for a single node (used in tests).

        Args:
            node: The node whose parent needs updating.
        """
        self._update_parent_state_recursive(node)

    def _update_node_label(self, node: TreeNode) -> None:
        """Update the visual label of a node to reflect current state.

        Args:
            node: The node to update.
        """
        if node.data is not None:
            node.label = node.data.get_label()

    def _update_all_labels(self) -> None:
        """Update all node labels in the tree."""
        self._update_labels_recursive(self.root)

    def _update_labels_recursive(self, node: TreeNode) -> None:
        """Recursively update labels.

        Args:
            node: Current node to update.
        """
        self._update_node_label(node)
        for child in node.children:
            self._update_labels_recursive(child)

    def select_all(self) -> None:
        """T043: Bulk select all agents."""
        for node in self.root.children:
            if node.data is not None:
                node.data.state = SelectionState.SELECTED
                self._propagate_selection_to_children(node, SelectionState.SELECTED)
        self._update_all_labels()

    def deselect_all(self) -> None:
        """T043: Bulk deselect all agents."""
        for node in self.root.children:
            if node.data is not None:
                node.data.state = SelectionState.UNSELECTED
                self._propagate_selection_to_children(node, SelectionState.UNSELECTED)
        self._update_all_labels()

    def get_selected_count(self) -> int:
        """T044: Get count of selected agents (excluding section headers).

        Returns:
            Number of selected agent nodes.
        """
        return self._count_selected_recursive(self.root)

    def get_total_count(self) -> int:
        """T044: Get total count of selectable agents (excluding section headers).

        Returns:
            Total number of agent nodes that can be selected.
        """
        return self._count_total_recursive(self.root)

    def _count_total_recursive(self, node: TreeNode) -> int:
        """Recursively count total selectable nodes.

        Args:
            node: Current node to check.

        Returns:
            Count of selectable nodes.
        """
        count = 0
        for child in node.children:
            # Only count nodes that have data (actual agents, not section headers)
            if child.data is not None:
                count += 1
            count += self._count_total_recursive(child)
        return count

    def _count_selected_recursive(self, node: TreeNode) -> int:
        """Recursively count selected nodes.

        Args:
            node: Current node to check.

        Returns:
            Count of selected nodes.
        """
        count = 0
        for child in node.children:
            if child.data is not None and child.data.state == SelectionState.SELECTED:
                count += 1
            count += self._count_selected_recursive(child)
        return count

    def scroll_to_node(self, node: TreeNode) -> None:
        """Scroll to make a node visible.

        Args:
            node: The node to scroll to.
        """
        # Textual's tree should auto-scroll, but we can force it if needed
        self.scroll_to_line(self.get_node_line(node))

    def get_node_line(self, node: TreeNode) -> int:
        """Get the line number for a node.

        Args:
            node: The node to find.

        Returns:
            The line number (approximate for scrolling).
        """
        # This is a simplified implementation
        # In practice, Textual handles this automatically
        return 0
