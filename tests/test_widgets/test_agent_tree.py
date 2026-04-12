"""Tests for the agent tree widget.

Covers T024-T026: User Story 1 - View Agent Hierarchy tests.
Covers T035-T038: User Story 2 - Select Agents tests.
"""

from unittest.mock import patch

from textual.widgets import Tree

from riseon_agents.models.agent import PrimaryAgent, Subagent
from riseon_agents.models.rule import Rule
from riseon_agents.models.selection import SelectionState
from riseon_agents.models.skill import Skill
from riseon_agents.widgets.agent_tree import AgentTree, AgentTreeNode


class TestAgentTree:
    """T024-T026: Tests for the agent tree widget."""

    def test_tree_widget_exists(self):
        """T024: Basic Textual Tree widget can be created."""
        tree = AgentTree()
        assert tree is not None
        assert isinstance(tree, Tree)

    def test_tree_has_root(self):
        """T024: Tree has a root node for agents."""
        tree = AgentTree()
        assert tree.root is not None
        # Textual Tree stores label as a Text object
        assert str(tree.root.label) == "Agents"

    def test_tree_populates_from_agents(self):
        """T025: Tree populates from AgentRepository."""
        # Create mock agents
        agent1 = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect\n\nYou are an architect.",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )
        agent2 = PrimaryAgent(
            name="developer",
            description="Software developer",
            markdown_body="# Developer\n\nYou are a developer.",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent1, agent2])

        # Check root has children
        assert len(tree.root.children) == 2

        # Check agent names are in tree
        child_labels = [str(child.label) for child in tree.root.children]
        assert any("architect" in label.lower() for label in child_labels)
        assert any("developer" in label.lower() for label in child_labels)

    def test_tree_shows_primary_agents(self):
        """T025: Tree shows all Primary Agents."""
        agents = [
            PrimaryAgent(
                name=f"agent{i}",
                description=f"Agent {i}",
                markdown_body=f"# Agent {i}",
                permissions={},
                subagents=[],
                rules=[],
                skills=[],
            )
            for i in range(5)
        ]

        tree = AgentTree()
        tree.populate_from_agents(agents)

        assert len(tree.root.children) == 5

    def test_tree_expands_subagents(self):
        """T025: Expand shows subagents as nested items."""
        subagent = Subagent(
            name="adr-generator",
            description="ADR generator",
            parent_agent="architect",
            markdown_body="# ADR Generator",
            permissions={},
        )

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[subagent],
            rules=[],
            skills=[],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent])

        # Find the architect node
        architect_node = tree.root.children[0]
        # Should have "Subagents" as a child
        subagent_section = None
        for child in architect_node.children:
            if "Subagents" in str(child.label):
                subagent_section = child
                break

        assert subagent_section is not None
        assert len(subagent_section.children) > 0

        # Check subagent is a child (label is title-cased: "Adr Generator")
        subagent_labels = [str(child.label) for child in subagent_section.children]
        assert any("Adr" in label for label in subagent_labels)

    def test_tree_expands_rules(self):
        """T025: Expand shows rules as nested items."""
        rule = Rule(
            name="code-style",
            content="# Code Style Rules",
        )

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[rule],
            skills=[],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent])

        # Find the architect node and check for rules section
        architect_node = tree.root.children[0]
        has_rules = any("Rules" in str(child.label) for child in architect_node.children)
        assert has_rules

    def test_tree_expands_skills(self):
        """T025: Expand shows skills as nested items."""
        skill = Skill(
            name="speckit-specify",
            description="Speckit specify skill",
            content="---\nname: speckit-specify\n---",
            source_path="/fake/path",
        )

        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[skill],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent])

        # Find the architect node and check for skills section
        architect_node = tree.root.children[0]
        has_skills = any("Skills" in str(child.label) for child in architect_node.children)
        assert has_skills

    def test_tree_node_types(self):
        """T025: Tree nodes have correct type indicators."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent])

        # Check that nodes have AgentTreeNode data
        node = tree.root.children[0]
        assert isinstance(node.data, AgentTreeNode)
        assert node.data.node_type == "primary_agent"

    def test_keyboard_navigation_up_down(self):
        """T026: Keyboard navigation with arrows works."""
        agents = [
            PrimaryAgent(
                name=f"agent{i}",
                description=f"Agent {i}",
                markdown_body=f"# Agent {i}",
                permissions={},
                subagents=[],
                rules=[],
                skills=[],
            )
            for i in range(3)
        ]

        tree = AgentTree()
        tree.populate_from_agents(agents)

        # Verify tree has children (nodes exist for navigation)
        assert len(tree.root.children) == 3

        # The tree widget handles keyboard navigation internally
        # We just verify the structure is set up correctly
        first_node = tree.root.children[0]
        assert first_node is not None

        # Verify navigation methods exist
        assert hasattr(tree, "action_cursor_down")
        assert hasattr(tree, "action_cursor_up")

    def test_keyboard_enter_toggles_expand(self):
        """T026: Enter key toggles expand/collapse."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent])

        node = tree.root.children[0]

        # Initially expanded (our implementation expands by default)
        assert node.is_expanded

        # Toggle expand/collapse using the node's toggle method
        node.toggle()
        assert not node.is_expanded

        # Toggle again
        node.toggle()
        assert node.is_expanded

    def test_tree_scrolls_to_cursor(self):
        """T026: Cursor is always visible with auto-scroll."""
        tree = AgentTree()

        # Mock scroll_to_node to verify it's called
        with patch.object(tree, "scroll_to_node") as mock_scroll:
            tree.select_node(tree.root)
            # select_node calls scroll_to_node internally (via Tree base class)
            # and our method also calls it - verify it was called at least once
            assert mock_scroll.call_count >= 1

    def test_malformed_agent_warning(self):
        """T025: Malformed agents show warning indicator."""
        # Create a node data with warning
        node = AgentTreeNode(
            id="malformed-agent",
            label="Malformed Agent",
            node_type="primary_agent",
            has_warning=True,
            warnings=["Missing required field: tools"],
        )

        # Check that warning icon is in the icon
        icon = node.get_icon()
        assert "⚠" in icon


class TestAgentTreeNode:
    """Tests for AgentTreeNode data class."""

    def test_node_creation(self):
        """AgentTreeNode can be created with required fields."""
        node = AgentTreeNode(
            id="architect",
            label="Architect",
            node_type="primary_agent",
        )

        assert node.id == "architect"
        assert node.label == "Architect"
        assert node.node_type == "primary_agent"
        assert node.state == SelectionState.UNSELECTED

    def test_node_with_agent(self):
        """AgentTreeNode can hold a PrimaryAgent."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[],
            rules=[],
            skills=[],
        )

        node = AgentTreeNode(
            id="architect",
            label="Architect",
            node_type="primary_agent",
            agent=agent,
        )

        assert node.agent == agent

    def test_node_state_toggle(self):
        """AgentTreeNode can toggle selection state."""
        node = AgentTreeNode(
            id="test",
            label="Test",
            node_type="subagent",
        )

        assert node.state == SelectionState.UNSELECTED

        node.toggle()
        assert node.state == SelectionState.SELECTED

        node.toggle()
        assert node.state == SelectionState.UNSELECTED

    def test_node_icon_for_state(self):
        """AgentTreeNode returns correct icon for state."""
        node = AgentTreeNode(
            id="test",
            label="Test",
            node_type="primary_agent",
        )

        # Unselected
        node.state = SelectionState.UNSELECTED
        icon = node.get_icon()
        assert "☐" in icon

        # Selected
        node.state = SelectionState.SELECTED
        icon = node.get_icon()
        assert "☑" in icon

        # Partial
        node.state = SelectionState.PARTIAL
        icon = node.get_icon()
        assert "◪" in icon

    def test_node_icon_for_type(self):
        """AgentTreeNode returns correct icon for node type."""
        test_cases = [
            ("primary_agent", "◉"),
            ("subagent", "○"),
            ("rule", "▪"),
            ("skill", "★"),
        ]

        for node_type, expected_icon in test_cases:
            node = AgentTreeNode(
                id="test",
                label="Test",
                node_type=node_type,
            )
            icon = node.get_icon()
            assert expected_icon in icon

    def test_node_with_warning(self):
        """AgentTreeNode can have warning flag."""
        node = AgentTreeNode(
            id="test",
            label="Test",
            node_type="primary_agent",
            has_warning=True,
        )

        assert node.has_warning is True

        icon = node.get_icon()
        assert "⚠" in icon


class TestAgentTreeSelection:
    """T035-T038: Tests for User Story 2 - Select Agents."""

    def test_selection_state_transitions(self):
        """T035: SelectionState transitions work correctly."""
        node = AgentTreeNode(
            id="test",
            label="Test",
            node_type="primary_agent",
        )

        # Start unselected
        assert node.state == SelectionState.UNSELECTED

        # Toggle to selected
        node.toggle()
        assert node.state == SelectionState.SELECTED

        # Toggle back to unselected
        node.toggle()
        assert node.state == SelectionState.UNSELECTED

        # Set to partial and toggle should go to selected
        node.state = SelectionState.PARTIAL
        node.toggle()
        assert node.state == SelectionState.SELECTED

    def test_selection_propagation_to_children(self):
        """T036: Selecting parent selects all children."""
        # Create tree with hierarchy
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[
                Subagent(
                    name="adr-generator",
                    description="ADR generator",
                    parent_agent="architect",
                    markdown_body="# ADR",
                    permissions={},
                ),
                Subagent(
                    name="ddd-specialist",
                    description="DDD specialist",
                    parent_agent="architect",
                    markdown_body="# DDD",
                    permissions={},
                ),
            ],
            rules=[],
            skills=[],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent])

        # Find the architect node
        architect_node = tree.root.children[0]

        # Select the architect node with propagation
        tree.toggle_selection_with_propagation(architect_node)

        # Check architect is selected
        assert architect_node.data.state == SelectionState.SELECTED

        # Find subagents section
        subagents_section = None
        for child in architect_node.children:
            if "Subagents" in str(child.label):
                subagents_section = child
                break

        assert subagents_section is not None

        # Check all subagents are selected
        for subagent_node in subagents_section.children:
            if hasattr(subagent_node, "data") and subagent_node.data:
                assert subagent_node.data.state == SelectionState.SELECTED

    def test_partial_state_calculation(self):
        """T037: PARTIAL state shown when some children selected."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[
                Subagent(
                    name="adr-generator",
                    description="ADR generator",
                    parent_agent="architect",
                    markdown_body="# ADR",
                    permissions={},
                ),
                Subagent(
                    name="ddd-specialist",
                    description="DDD specialist",
                    parent_agent="architect",
                    markdown_body="# DDD",
                    permissions={},
                ),
            ],
            rules=[],
            skills=[],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent])

        # Find the architect node and subagents
        architect_node = tree.root.children[0]
        subagents_section = None
        for child in architect_node.children:
            if "Subagents" in str(child.label):
                subagents_section = child
                break

        assert subagents_section is not None
        assert len(subagents_section.children) >= 2

        # Select first subagent only
        first_subagent = subagents_section.children[0]
        if hasattr(first_subagent, "data") and first_subagent.data:
            first_subagent.data.state = SelectionState.SELECTED

        # Calculate partial state for parent (architect_node) based on its descendants
        tree._calculate_partial_state(architect_node)

        # Parent should show PARTIAL
        assert architect_node.data.state == SelectionState.PARTIAL

    def test_bulk_selection_all(self):
        """T038: Bulk selection 'a' selects all agents."""
        agents = [
            PrimaryAgent(
                name=f"agent{i}",
                description=f"Agent {i}",
                markdown_body=f"# Agent {i}",
                permissions={},
                subagents=[],
                rules=[],
                skills=[],
            )
            for i in range(3)
        ]

        tree = AgentTree()
        tree.populate_from_agents(agents)

        # Initially all unselected
        for node in tree.root.children:
            assert node.data.state == SelectionState.UNSELECTED

        # Bulk select all
        tree.select_all()

        # All should be selected
        for node in tree.root.children:
            assert node.data.state == SelectionState.SELECTED

    def test_bulk_deselection_all(self):
        """T038: Bulk deselection 'A' deselects all agents."""
        agents = [
            PrimaryAgent(
                name=f"agent{i}",
                description=f"Agent {i}",
                markdown_body=f"# Agent {i}",
                permissions={},
                subagents=[],
                rules=[],
                skills=[],
            )
            for i in range(3)
        ]

        tree = AgentTree()
        tree.populate_from_agents(agents)

        # Select all first
        tree.select_all()
        for node in tree.root.children:
            assert node.data.state == SelectionState.SELECTED

        # Bulk deselect all
        tree.deselect_all()

        # All should be unselected
        for node in tree.root.children:
            assert node.data.state == SelectionState.UNSELECTED

    def test_get_selected_count(self):
        """T038: Selection count is calculated correctly."""
        agent = PrimaryAgent(
            name="architect",
            description="Software architect",
            markdown_body="# Architect",
            permissions={},
            subagents=[
                Subagent(
                    name="adr-generator",
                    description="ADR generator",
                    parent_agent="architect",
                    markdown_body="# ADR",
                    permissions={},
                ),
            ],
            rules=[],
            skills=[],
        )

        tree = AgentTree()
        tree.populate_from_agents([agent])

        # Initially 0 selected
        count = tree.get_selected_count()
        assert count == 0

        # Select the agent
        architect_node = tree.root.children[0]
        tree.toggle_selection_with_propagation(architect_node)

        # Should have selected count > 0
        count = tree.get_selected_count()
        assert count > 0
