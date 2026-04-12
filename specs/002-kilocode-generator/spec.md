# Feature Specification: Kilo Code Configuration Generator

**Feature Branch**: `002-kilocode-generator`  
**Created**: 2026-03-30  
**Status**: Draft  
**Input**: User description: "RiseOn.Agents TUI for generating Kilo Code configurations from centralized agent definitions"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Agent Hierarchy (Priority: P1)

As a developer, I want to see the complete hierarchy of all defined agents so that I can understand what will be generated and make informed selections.

**Why this priority**: This is the foundation of the TUI - users must be able to visualize what agents exist before they can select or generate anything. Without this, no other functionality is useful.

**Independent Test**: Can be fully tested by launching the TUI and navigating through the agent tree. Delivers value by providing visibility into the agent structure.

**Acceptance Scenarios**:

1. **Given** the TUI is launched, **When** the main screen loads, **Then** I see a tree view showing all 5 Primary Agents (architect, software-engineer, devops-engineer, product-manager, product-owner)
2. **Given** I am viewing the agent tree, **When** I expand a Primary Agent, **Then** I see its subagents, rules, and skills as nested items
3. **Given** I am viewing the agent tree, **When** I navigate using keyboard (arrow keys), **Then** I can move through the hierarchy smoothly
4. **Given** an agent folder is missing or malformed, **When** the TUI loads, **Then** I see a warning indicator on that agent without crashing

---

### User Story 2 - Select Agents for Generation (Priority: P1)

As a developer, I want to select which agents and subagents to include in the generation so that I can customize the output for my specific project needs.

**Why this priority**: Selection is essential for generation. Users need control over what gets generated rather than forcing all-or-nothing.

**Independent Test**: Can be tested by selecting/deselecting agents and verifying the selection state persists. Delivers value by enabling customization.

**Acceptance Scenarios**:

1. **Given** I am viewing the agent tree, **When** I press space/enter on an agent, **Then** it toggles between selected and unselected (visual indicator changes)
2. **Given** I select a Primary Agent, **When** the selection is applied, **Then** all its subagents are also selected by default
3. **Given** I deselect a subagent, **When** viewing the parent agent, **Then** the parent shows a partial selection indicator
4. **Given** I have made selections, **When** I view the selection summary, **Then** I see a count of selected agents/subagents

---

### User Story 3 - Preview Generated Configuration (Priority: P2)

As a developer, I want to preview the configuration files before they are generated so that I can verify the output matches my expectations.

**Why this priority**: Preview prevents mistakes and builds confidence. Important but secondary to basic navigation and selection.

**Independent Test**: Can be tested by selecting an agent and viewing its preview panel. Delivers value by showing exactly what will be generated.

**Acceptance Scenarios**:

1. **Given** I have selected an agent, **When** I focus on it in the tree, **Then** I see a preview panel showing the generated configuration
2. **Given** I am viewing a Primary Agent preview, **When** the preview loads, **Then** I see the custom_modes.yaml entry format
3. **Given** I am viewing a Subagent preview, **When** the preview loads, **Then** I see the .kilo/agents/*.md file format
4. **Given** I am viewing a preview, **When** I scroll within the preview panel, **Then** I can see the complete generated content

---

### User Story 4 - Choose Generation Level (Priority: P2)

As a developer, I want to choose between Local (project) and Global (user) configuration so that I can control where the generated files are placed.

**Why this priority**: This is a key differentiator in the feature scope. Must be available before generation but not needed for basic navigation.

**Independent Test**: Can be tested by switching between Local/Global and verifying the target path changes. Delivers value by supporting different use cases.

**Acceptance Scenarios**:

1. **Given** I am ready to generate, **When** I view generation options, **Then** I see a toggle/selector for Local vs Global
2. **Given** I select Local, **When** I view the target path, **Then** it shows the current project directory (e.g., `./.kilo/`)
3. **Given** I select Global, **When** I view the target path, **Then** it shows `~/.kilocode/` directory
4. **Given** I switch between Local and Global, **When** viewing the preview, **Then** the file paths in preview update accordingly

---

### User Story 5 - Generate Configuration Files (Priority: P1)

As a developer, I want to generate the Kilo Code configuration files so that my AI coding assistant recognizes and uses my custom agents.

**Why this priority**: This is the core deliverable - the actual generation. Equal priority with navigation and selection as the three together form the MVP.

**Independent Test**: Can be tested by triggering generation and verifying files are created in the correct location with correct content.

**Acceptance Scenarios**:

1. **Given** I have selected agents and chosen a generation level, **When** I trigger generation, **Then** the system creates the appropriate files
2. **Given** generation is in progress, **When** files are being written, **Then** I see a progress indicator showing current status
3. **Given** generation completes successfully, **When** viewing results, **Then** I see a summary of files created with their paths
4. **Given** target files already exist, **When** I trigger generation, **Then** I am prompted to confirm before overwriting

---

### User Story 6 - Validate Configuration Format (Priority: P3)

As a developer, I want the system to validate the generated configuration so that I know the output will work with Kilo Code.

**Why this priority**: Validation improves reliability but is an enhancement over basic generation. Users can manually verify initially.

**Independent Test**: Can be tested by generating configs and viewing validation results. Delivers value by catching errors before deployment.

**Acceptance Scenarios**:

1. **Given** generation is complete, **When** validation runs, **Then** I see a validation report with pass/fail status
2. **Given** a configuration has format errors, **When** validation runs, **Then** I see specific error messages with locations
3. **Given** all configurations are valid, **When** viewing the validation summary, **Then** I see a success confirmation

---

### Edge Cases

- What happens when the agents/ folder is empty or missing?
  - Display a clear error message guiding user to create agent definitions first
- What happens when an agent definition has invalid YAML frontmatter?
  - Show warning on that specific agent, allow generation of others
- What happens when the user doesn't have write permissions to the target directory?
  - Display permission error with suggested resolution (run with elevated permissions or choose different location)
- What happens when generation is interrupted (e.g., Ctrl+C)?
  - Clean up partial files, show what was completed vs. incomplete
- What happens when Global configuration directory doesn't exist?
  - Create the directory structure automatically with user confirmation

## Requirements *(mandatory)*

### Functional Requirements

**Agent Parsing**
- **FR-001**: System MUST parse agent definition files with YAML frontmatter and Markdown body
- **FR-002**: System MUST discover all agents recursively from the agents/ folder
- **FR-003**: System MUST extract agent metadata from frontmatter (name, description, tools, modelVariant, target, mode, temperature, steps, permissions, handoffs)
- **FR-004**: System MUST identify relationships between Primary Agents and their Subagents

**TUI Navigation**
- **FR-005**: System MUST display agents in a hierarchical tree view
- **FR-006**: System MUST support keyboard navigation (arrows, enter, space, tab)
- **FR-007**: System MUST provide visual feedback for current focus and selection state
- **FR-008**: System MUST support expanding/collapsing tree nodes

**Selection**
- **FR-009**: System MUST allow selecting/deselecting individual agents and subagents
- **FR-010**: System MUST support bulk selection (select all, deselect all)
- **FR-011**: System MUST visually indicate partial selection on parent nodes

**Preview**
- **FR-012**: System MUST display a real-time preview of generated configuration for selected agent (see SC-004: <500ms)
- **FR-013**: System MUST update preview when selection or generation level changes

**Generation**
- **FR-014**: System MUST generate custom_modes.yaml from Primary Agent definitions
- **FR-015**: System MUST generate .kilo/agents/*.md files from Subagent definitions
- **FR-016**: System MUST generate .kilo/rules/ from shared rules
- **FR-017**: System MUST generate .kilo/rules-{mode}/ from mode-specific rules
- **FR-018**: System MUST generate .kilocode/skills/ from skill definitions
- **FR-019**: System MUST support Local (project) generation level
- **FR-020**: System MUST support Global (user config) generation level targeting `~/.kilocode/`

**Overwrite Handling**
- **FR-021**: System MUST detect existing configuration files before generation
- **FR-022**: System MUST prompt user for confirmation before overwriting existing files
- **FR-023**: System MUST provide options: overwrite, skip, or cancel generation

**Validation**
- **FR-024**: System MUST validate generated YAML syntax
- **FR-025**: System MUST validate generated Markdown structure
- **FR-026**: System MUST report validation errors with specific file and line information

### Key Entities

- **Primary Agent**: Top-level agent definition with identity, guardrails, and handoff registry. Contains subagents, rules, and skills. Maps to Kilo Code Custom Mode.
  - Required frontmatter: `name`, `description`, `tools`, `modelVariant`, `target`, `mode` (= 'primary'), `temperature`, `steps`, `permissions`, `handoffs`
- **Subagent**: Specialized agent invoked on-demand by Primary Agent. Has specific permissions and focused context. Maps to Kilo Code Custom Subagent.
  - Required frontmatter: `name`, `description`, `tools`, `modelVariant`, `target`, `mode` (= 'subagent'), `temperature`, `steps`, `permissions`
- **Rule**: Behavioral guideline or guardrail. Can be shared (all modes) or mode-specific. Maps to Kilo Code Custom Rules.
- **Skill**: Reusable knowledge module loaded on-demand. Maps to Kilo Code Skills.
- **Generation Level**: Target location for generated files - Local (project `./.kilo/`) or Global (user `~/.kilocode/`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can view the complete agent hierarchy within 2 seconds of launching the TUI
- **SC-002**: Users can select agents and generate configurations in under 1 minute for a typical workflow
- **SC-003**: 100% of generated configurations pass Kilo Code format validation
- **SC-004**: Users can preview any agent's generated configuration in under 500ms
- **SC-005**: Generation of all 5 Primary Agents with 26 Subagents completes in under 10 seconds
- **SC-006**: Users report the TUI as "intuitive" in usability testing (target: 80% positive rating)
- **SC-007**: Zero data loss when overwrite confirmation is declined (existing files remain intact)

## Clarifications

### Session 2026-03-30

- Q: What is the Global configuration directory path for Kilo Code? → A: `~/.kilocode`
- Q: What are the required fields in agent definition YAML frontmatter? → A: Document existing schema (Primary: name, description, tools, modelVariant, target, mode, temperature, steps, permissions, handoffs; Subagent: same without handoffs)

## Assumptions

- Users have the agents/ folder with valid agent definitions already created
- Users have Kilo Code extension installed in their JetBrains IDE (for testing generated configs)
- The TUI will run in modern terminal emulators with Unicode and color support
- Users have basic familiarity with terminal applications and keyboard navigation
- Network connectivity is not required (all operations are local file-based)
- The Kilo Code configuration format follows the official documentation at https://kilo.ai/docs/customize
- Global configuration path follows Kilo Code's standard user configuration location (`~/.kilocode/`)
