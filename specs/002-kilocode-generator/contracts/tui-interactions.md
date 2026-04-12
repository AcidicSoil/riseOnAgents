# TUI Interaction Contracts

**Feature Branch**: `002-kilocode-generator`  
**Date**: 2026-03-30

This document defines the user interaction contracts for the RiseOn.Agents TUI.

## 1. Application Lifecycle

### Contract: Application Launch

**Trigger**: User runs `riseon-agents` command

**Behavior**:
1. Application starts and shows loading indicator
2. Scans `agents/` directory for agent definitions
3. Builds agent hierarchy tree
4. Displays main screen with tree populated

**Success Criteria**:
- Main screen visible within 2 seconds (SC-001)
- Tree shows all discovered agents
- Default selection: none selected

**Error Handling**:
- If `agents/` folder missing: Show error screen with guidance
- If `agents/` folder empty: Show empty state with guidance
- If parsing fails: Show warning on affected agent, continue loading others

### Contract: Application Exit

**Trigger**: User presses `q` or `Ctrl+C`

**Behavior**:
1. If generation in progress: Show confirmation dialog
2. If unsaved selections: Exit immediately (no persistence)
3. Clean terminal restoration

**Success Criteria**:
- Terminal restored to pre-launch state
- No orphan processes

## 2. Tree Navigation

### Contract: Keyboard Navigation

| Key | Action |
|-----|--------|
| `↑` / `k` | Move cursor up |
| `↓` / `j` | Move cursor down |
| `←` / `h` | Collapse node / move to parent |
| `→` / `l` | Expand node / move to first child |
| `Enter` | Toggle expand/collapse |
| `Space` | Toggle selection |
| `Home` | Jump to first node |
| `End` | Jump to last node |
| `PageUp` | Move up one page |
| `PageDown` | Move down one page |

**Success Criteria**:
- Navigation is smooth and responsive
- Cursor position always visible (auto-scroll)
- Visual feedback on every action

### Contract: Mouse Navigation

| Action | Behavior |
|--------|----------|
| Click on node | Move cursor to node |
| Double-click on node | Toggle expand/collapse |
| Click on checkbox | Toggle selection |
| Scroll wheel | Scroll tree view |

**Success Criteria**:
- Mouse and keyboard can be used interchangeably
- Click targets are large enough (minimum 1 character height)

## 3. Selection System

### Contract: Single Selection Toggle

**Trigger**: User presses `Space` on a node

**Behavior for Leaf Node (Subagent, Rule, Skill)**:
1. Toggle state: UNSELECTED → SELECTED → UNSELECTED
2. Update parent node state accordingly

**Behavior for Parent Node (Primary Agent)**:
1. If UNSELECTED: Select self + all children → SELECTED
2. If SELECTED: Deselect self + all children → UNSELECTED
3. If PARTIAL: Select self + all children → SELECTED

**Parent State Calculation**:
- All children UNSELECTED → Parent UNSELECTED
- All children SELECTED → Parent SELECTED
- Mixed children states → Parent PARTIAL

**Success Criteria**:
- State change visible immediately
- Selection count updates in status bar
- Preview panel updates if focused node is selected

### Contract: Bulk Selection

| Key | Action |
|-----|--------|
| `a` | Select all agents |
| `A` (Shift+a) | Deselect all agents |
| `Ctrl+a` | Select all (alternative) |

**Success Criteria**:
- All nodes change state immediately
- Selection count reflects total

## 4. Preview Panel

### Contract: Preview Display

**Trigger**: User navigates to a node in the tree

**Behavior**:
1. If node is a Primary Agent:
   - Show generated `custom_modes.yaml` entry
   - Include slug, name, description, roleDefinition, groups
2. If node is a Subagent:
   - Show generated `.kilo/agents/{name}.md` content
   - Include frontmatter and markdown body
3. If node is a Rule:
   - Show rule content as-is
4. If node is a Skill:
   - Show SKILL.md content as-is

**Success Criteria**:
- Preview updates within 500ms (SC-004)
- Syntax highlighting for YAML/Markdown
- Preview reflects current generation level (Local/Global paths)

### Contract: Preview Scrolling

| Key | Action (when preview focused) |
|-----|-------------------------------|
| `↑` / `↓` | Scroll preview content |
| `PageUp` / `PageDown` | Scroll one page |
| `Home` / `End` | Jump to start/end |

**Tab Navigation**:
- `Tab`: Move focus from tree to preview
- `Shift+Tab`: Move focus from preview to tree

## 5. Generation Level

### Contract: Level Toggle

**Trigger**: User presses `l` or clicks Local/Global toggle

**Behavior**:
1. Toggle between Local and Global
2. Update target path display
3. Update preview panel paths

**Visual States**:
- Local: `[●] Local  ○ Global` - Target: `./.kilo/`
- Global: `○ Local  [●] Global` - Target: `~/.kilocode/`

**Success Criteria**:
- Toggle is instantaneous
- Preview paths update immediately

## 6. Generation

### Contract: Generate Action

**Trigger**: User presses `g` or clicks [Generate] button

**Preconditions**:
- At least one agent selected

**Behavior**:
1. Check for existing files at target location
2. If conflicts found: Show overwrite confirmation dialog
3. Generate files with progress indicator
4. Show generation summary

**Overwrite Dialog**:
```
┌─────────────────────────────────────────────┐
│ Existing Files Found                        │
│                                             │
│ The following files will be overwritten:    │
│ - .kilo/custom_modes.yaml                   │
│ - .kilo/agents/adr-generator.md             │
│                                             │
│ [Overwrite All] [Skip Existing] [Cancel]    │
└─────────────────────────────────────────────┘
```

**Progress Display**:
```
Generating... [████████░░░░░░░░░░░░] 40%
Writing: .kilo/agents/ddd-specialist.md
```

**Success Summary**:
```
┌─────────────────────────────────────────────┐
│ Generation Complete                         │
│                                             │
│ Created: 5 files                            │
│ Updated: 2 files                            │
│ Skipped: 1 file                             │
│                                             │
│ Files written to: ./.kilo/                  │
│                                             │
│ [OK]                                        │
└─────────────────────────────────────────────┘
```

**Success Criteria**:
- Full generation completes in under 10 seconds (SC-005)
- Zero data loss on cancel (SC-007)
- Clear summary of actions taken

### Contract: Generation Interruption

**Trigger**: User presses `Ctrl+C` during generation

**Behavior**:
1. Stop writing new files
2. Complete current file write (atomic)
3. Show partial summary
4. Clean up any temp files

**Partial Summary**:
```
┌─────────────────────────────────────────────┐
│ Generation Interrupted                      │
│                                             │
│ Completed: 3 files                          │
│ Not started: 4 files                        │
│                                             │
│ [OK]                                        │
└─────────────────────────────────────────────┘
```

## 7. Help System

### Contract: Help Display

**Trigger**: User presses `?` or `F1`

**Behavior**: Show help overlay with keyboard shortcuts

```
┌─────────────────────────────────────────────┐
│ Keyboard Shortcuts                          │
│                                             │
│ Navigation                                  │
│   ↑/↓      Move cursor                      │
│   ←/→      Collapse/Expand                  │
│   Enter    Toggle expand                    │
│   Tab      Switch panel focus               │
│                                             │
│ Selection                                   │
│   Space    Toggle selection                 │
│   a        Select all                       │
│   A        Deselect all                     │
│                                             │
│ Actions                                     │
│   l        Toggle Local/Global              │
│   g        Generate files                   │
│   q        Quit                             │
│   ?        This help                        │
│                                             │
│ Press any key to close                      │
└─────────────────────────────────────────────┘
```

## 8. Error States

### Contract: Error Display

**Error Types and Handling**:

| Error | Display | Recovery |
|-------|---------|----------|
| agents/ missing | Full screen error | User creates folder, restarts |
| Parse error | Warning icon on node | User fixes file, restarts |
| Permission denied | Modal dialog | User fixes permissions |
| Disk full | Modal dialog | User frees space, retry |

**Error Modal**:
```
┌─────────────────────────────────────────────┐
│ ⚠ Error                                     │
│                                             │
│ Cannot write to .kilo/custom_modes.yaml     │
│                                             │
│ Permission denied. Please check write       │
│ permissions for the target directory.       │
│                                             │
│ [Retry] [Change Target] [Cancel]            │
└─────────────────────────────────────────────┘
```

## 9. Visual Indicators

### Selection State Icons

| State | Icon | Color |
|-------|------|-------|
| Unselected | ☐ | dim gray |
| Selected | ☑ | green |
| Partial | ◪ | yellow |

### Node Type Icons

| Type | Icon | Color |
|------|------|-------|
| Primary Agent | ◉ | blue |
| Subagent | ○ | cyan |
| Rule | ▪ | gray |
| Skill | ★ | yellow |
| Warning | ⚠ | orange |

### Status Bar Elements

```
│ [●] Local  ○ Global  │  Selected: 3/31  │  [Generate] [?] [Q] │
```

- Generation level toggle (left)
- Selection count (center)
- Action buttons (right)
