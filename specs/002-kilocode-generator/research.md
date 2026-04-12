# Research: Kilo Code Configuration Generator

**Feature Branch**: `002-kilocode-generator`  
**Date**: 2026-03-30  
**Status**: Complete

## Research Questions

### RQ-001: TUI Framework Choice - Textual vs Rich

**Decision**: Use Textual (built on Rich) as the primary TUI framework

**Rationale**:
- Textual provides full-featured widget library including Tree widget with built-in keyboard navigation
- Tree widget supports expand/collapse, cursor navigation, and node selection out of the box
- Rich handles terminal rendering and styling (Textual dependency)
- Constitution mandates "Textual/Rich framework" - Textual satisfies both

**Alternatives Considered**:
- Rich only: Lacks interactive widgets needed for tree selection
- Urwid: Older API, less modern aesthetics
- Blessed/Curses: Lower-level, more boilerplate

**Key Findings from Textual Documentation**:
- Tree widget has built-in BINDINGS for navigation (up/down/left/right arrows)
- Space toggles node expansion, Enter selects
- `expand()`, `collapse()`, `toggle()`, `expand_all()` methods available
- TreeNode supports `add()` for children, `add_leaf()` for terminals
- Custom data can be attached via generic type: `Tree[MyDataType]`

### RQ-002: Tri-State Selection Implementation

**Decision**: Implement custom SelectableTree widget extending Textual's Tree

**Rationale**:
- Textual Tree doesn't have built-in checkbox/selection state
- Need to track: SELECTED, UNSELECTED, PARTIAL states
- Parent nodes must show PARTIAL when some children selected

**Implementation Approach**:
1. Create `SelectionState` enum: `SELECTED`, `UNSELECTED`, `PARTIAL`
2. Extend `TreeNode` with selection state property
3. Override Space binding to toggle selection (not expansion)
4. Propagate selection changes up (to parents) and down (to children)
5. Use Unicode symbols for visual state: ☑ (selected), ☐ (unselected), ◪ (partial)

**Alternatives Considered**:
- Separate checkbox column: More complex layout, harder to maintain
- Selection stored outside tree: Breaks encapsulation, harder to sync

### RQ-003: Kilo Code Configuration Format

**Decision**: Generate YAML format for all configuration files

**Rationale**:
- Kilo Code documentation states "YAML is now the preferred format"
- YAML supports comments, multi-line strings, better readability
- JSON still supported but deprecated for new configurations

**Key Mappings from Research**:

| RiseOn.Agents Source | Kilo Code Target | Format |
|---------------------|------------------|--------|
| `{agent}.agent.md` frontmatter | `custom_modes.yaml` entry | YAML |
| `subagents/*.agent.md` | `.kilo/agents/*.md` | Markdown with YAML frontmatter |
| `rules/_shared/*.md` | `.kilo/rules/*.md` | Markdown |
| `rules/{mode}/*.md` | `.kilo/rules-{slug}/*.md` | Markdown |
| `skills/*/SKILL.md` | `.kilocode/skills/*/SKILL.md` | Markdown with YAML frontmatter |

**custom_modes.yaml Schema** (from Kilo docs):
```yaml
customModes:
  - slug: mode-slug          # Required: [a-zA-Z0-9-]+
    name: Mode Display Name  # Required: shown in UI
    description: Short desc  # Required: shown in mode selector
    roleDefinition: |        # Required: system prompt content
      Multi-line role definition...
    whenToUse: When to use   # Optional: for orchestrator
    customInstructions: |    # Optional: additional instructions
      Instructions...
    groups:                  # Required: tool permissions
      - read
      - - edit
        - fileRegex: \.md$
          description: Markdown only
      - command
```

**Subagent Markdown Schema** (from Kilo docs):
```yaml
---
description: What the agent does
mode: subagent
model: provider/model-id  # Optional
temperature: 0.1          # Optional
permission:
  edit: deny
  bash: deny
---

# Agent Instructions

Markdown body becomes the system prompt...
```

### RQ-004: TUI Layout Design

**Decision**: 2-panel layout (Tree + Preview) with bottom action bar

**Rationale**:
- Tree panel (left, 40%): Agent hierarchy with selection
- Preview panel (right, 60%): Generated configuration preview
- Bottom bar: Generation level toggle (Local/Global), action buttons
- Simpler than 3-panel, focuses on primary workflow

**Layout Structure**:
```
┌─────────────────────────────────────────────────────────────┐
│ RiseOn.Agents - Kilo Code Generator                    [?] │
├──────────────────────┬──────────────────────────────────────┤
│ ◉ architect          │ Preview: custom_modes.yaml          │
│   ├── ☑ adr-generator│ ─────────────────────────────────── │
│   ├── ☐ ddd-special. │ customModes:                        │
│   └── ◪ ...          │   - slug: architect                 │
│ ○ software-engineer  │     name: Architect                 │
│   └── ...            │     description: ...                │
│ ○ devops-engineer    │     roleDefinition: |               │
│   └── ...            │       You are a Senior...           │
├──────────────────────┴──────────────────────────────────────┤
│ [●] Local  ○ Global  │  Selected: 3/31  │  [Generate] [Q] │
└─────────────────────────────────────────────────────────────┘
```

**Alternatives Considered**:
- 3-panel (tree + details + preview): Too crowded for terminal
- Tabs for preview types: Adds navigation complexity
- Modal dialogs for preview: Breaks flow

### RQ-005: Data Model Choice

**Decision**: Use Python dataclasses with type hints

**Rationale**:
- Lightweight, no external dependencies
- Built into Python 3.7+
- Good IDE support and mypy integration
- Constitution requires type hints and mypy validation

**Alternatives Considered**:
- Pydantic: Heavier dependency, validation overkill for this use case
- attrs: Extra dependency, similar to dataclasses
- Named tuples: Immutable, less flexible for tree state

### RQ-006: Generation Strategy

**Decision**: Direct string building with template-like structure

**Rationale**:
- YAML output is relatively simple and structured
- Avoids Jinja2 dependency
- PyYAML for YAML serialization ensures valid output
- Markdown files can use f-strings with proper escaping

**Generation Flow**:
1. Parse source agent definitions (YAML frontmatter + Markdown body)
2. Transform to internal data model
3. Map to Kilo Code schema
4. Serialize to YAML/Markdown using PyYAML + direct string

**Alternatives Considered**:
- Jinja2 templates: Extra dependency, overkill for this scope
- String concatenation: Error-prone for YAML
- YAML dump only: Less control over formatting

### RQ-007: Agent Frontmatter Schema Mapping

**Decision**: Map RiseOn.Agents frontmatter to Kilo Code format

**Source Schema (RiseOn.Agents)**:
```yaml
# Primary Agent
name: architect
description: Senior software architect...
tools: ['search', 'read', 'edit', 'mcp', ...]
temperature: 0.1
steps: 40
permissions:
  edit: 'allow'
  bash: 'deny'
  webfetch: 'allow'
handoffs:
  - agent: adr-generator
  - agent: ddd-specialist

# Subagent
name: adr-generator
description: Expert agent for creating ADRs...
tools: ['mcp', 'read', 'edit', 'search', ...]
modelVariant: 'high'
target: 'opencode'
mode: 'subagent'
temperature: 0.1
steps: 15
permissions:
  edit: 'allow'
  bash: 'deny'
```

**Target Schema (Kilo Code)**:

For Custom Mode (from Primary Agent):
```yaml
customModes:
  - slug: architect
    name: Architect
    description: Senior software architect...
    roleDefinition: |
      # (Markdown body from .agent.md)
    groups:
      - read
      - - edit
        - fileRegex: .*
      - command  # if bash permission exists
```

For Custom Subagent (from Subagent):
```yaml
---
description: Expert agent for creating ADRs...
mode: subagent
temperature: 0.1
permission:
  edit: allow
  bash: deny
---

# (Markdown body from .agent.md)
```

**Tool Mapping**:
| RiseOn tools | Kilo groups |
|--------------|-------------|
| read, search | read |
| edit | edit |
| bash (if allowed) | command |
| mcp | mcp |
| webfetch | browser |

### RQ-008: File Discovery Pattern

**Decision**: Recursive glob-based discovery with validation

**Pattern**:
```
agents/
├── {agent-name}/
│   ├── {agent-name}.agent.md      # Primary agent definition
│   ├── subagents/                  # Optional
│   │   └── *.agent.md             # Subagent definitions
│   ├── rules/                      # Optional
│   │   └── *.md                   # Rule files
│   └── skills/                     # Optional
│       └── */SKILL.md             # Skill definitions
```

**Discovery Algorithm**:
1. Glob `agents/*/*.agent.md` for primary agents
2. For each primary, check for `subagents/` directory
3. Glob `agents/{name}/subagents/*.agent.md` for subagents
4. Glob `agents/{name}/rules/*.md` for rules
5. Glob `agents/{name}/skills/*/SKILL.md` for skills

## Dependencies

### Required
| Package | Version | Purpose |
|---------|---------|---------|
| textual | >=0.47.0 | TUI framework |
| rich | >=13.0.0 | Terminal rendering (Textual dep) |
| pyyaml | >=6.0 | YAML parsing and serialization |
| python-frontmatter | >=1.0 | Markdown frontmatter parsing |

### Development
| Package | Version | Purpose |
|---------|---------|---------|
| pytest | >=7.0 | Testing framework |
| pytest-asyncio | >=0.21 | Async test support for Textual |
| ruff | >=0.1.0 | Linting |
| black | >=23.0 | Formatting |
| mypy | >=1.0 | Type checking |

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Textual API changes | Medium | Pin to specific version range |
| Complex tri-state logic | Medium | Comprehensive unit tests |
| YAML formatting edge cases | Low | Use PyYAML for serialization |
| Large agent hierarchies | Low | Lazy loading, virtualization in Tree |

## Open Questions (Resolved)

1. ~~What is the Global config path?~~ → `~/.kilocode/` (confirmed in docs)
2. ~~YAML or JSON for custom_modes?~~ → YAML preferred (confirmed in docs)
3. ~~How to handle tool permissions mapping?~~ → groups array with regex options
4. ~~Skills location in Kilo Code?~~ → `.kilocode/skills/` or `~/.kilocode/skills/`
