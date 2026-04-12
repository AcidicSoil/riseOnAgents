# Quickstart: Kilo Code Configuration Generator

**Feature Branch**: `002-kilocode-generator`  
**Date**: 2026-03-30

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Terminal with Unicode support (most modern terminals)
- agents/ folder with agent definitions (already exists in this repo)

## Setup (Development)

### 1. Clone and Navigate

```bash
cd /path/to/RiseOn.Agents
```

### 2. Create Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e ".[dev]"
```

Or manually:
```bash
pip install textual>=0.47.0 rich>=13.0.0 pyyaml>=6.0 python-frontmatter>=1.0
pip install pytest pytest-asyncio ruff black mypy  # dev dependencies
```

### 4. Verify Installation

```bash
riseon-agents --version
# Expected: riseon-agents 0.1.0
```

## Running the TUI

### Launch

```bash
riseon-agents
```

Or during development:
```bash
python -m riseon_agents
```

### First Launch

1. TUI loads and scans `agents/` folder
2. You see a tree with all 5 Primary Agents
3. Expand any agent to see subagents, rules, skills

## Basic Workflow

### 1. Navigate the Tree

```
↑/↓    Move up/down
←/→    Collapse/Expand
Enter  Toggle expand
```

### 2. Select Agents

```
Space  Toggle selection
a      Select all
A      Deselect all
```

### 3. Choose Generation Level

```
l      Toggle Local/Global

Local:  ./.kilo/ (project)
Global: ~/.kilocode/ (user)
```

### 4. Generate

```
g      Generate selected agents
```

### 5. Exit

```
q      Quit
```

## Generated Files

After generation, you'll have:

```
# Local mode
.kilo/
├── custom_modes.yaml      # Primary agents as Custom Modes
├── agents/
│   ├── adr-generator.md   # Subagent definitions
│   ├── ddd-specialist.md
│   └── ...
├── rules/                 # Shared rules
│   └── ...
└── rules-architect/       # Mode-specific rules
    └── ...

.kilocode/
└── skills/               # Skills
    └── ...
```

## Testing with Kilo Code

1. Install Kilo Code extension in JetBrains IDE
2. Open a project with generated `.kilo/` folder
3. Check if custom modes appear in mode selector
4. Test subagent invocation with `@agent-name`

## Development Commands

### Run Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=riseon_agents --cov-report=html
```

### Lint Code

```bash
ruff check src/
black --check src/
```

### Type Check

```bash
mypy src/
```

### Format Code

```bash
black src/
ruff check --fix src/
```

## Project Structure

```
src/riseon_agents/
├── __init__.py
├── __main__.py           # Entry point
├── app.py                # Textual App class
├── models/
│   ├── __init__.py
│   ├── agent.py          # PrimaryAgent, Subagent dataclasses
│   ├── rule.py           # Rule dataclass
│   ├── skill.py          # Skill dataclass
│   └── selection.py      # SelectionState, SelectableNode
├── parsing/
│   ├── __init__.py
│   ├── frontmatter.py    # YAML frontmatter parser
│   └── repository.py     # AgentRepository discovery
├── generation/
│   ├── __init__.py
│   ├── modes.py          # custom_modes.yaml generator
│   ├── subagents.py      # Subagent .md generator
│   ├── rules.py          # Rules generator
│   └── skills.py         # Skills generator
├── widgets/
│   ├── __init__.py
│   ├── agent_tree.py     # SelectableTree widget
│   └── preview.py        # Preview panel widget
└── screens/
    ├── __init__.py
    ├── main.py           # Main screen
    └── dialogs.py        # Confirmation dialogs

tests/
├── conftest.py           # pytest fixtures
├── test_models/
├── test_parsing/
├── test_generation/
└── test_widgets/
```

## Troubleshooting

### TUI doesn't render correctly

- Ensure terminal supports Unicode
- Try: `export TERM=xterm-256color`
- Check terminal dimensions (minimum 80x24)

### agents/ folder not found

- Run from repository root
- Or specify: `riseon-agents --agents-path /path/to/agents`

### Permission denied on generation

- Check write permissions on target directory
- Try Global level if Local doesn't work
- Or: `sudo chown -R $USER ~/.kilocode`

### Generated files not recognized by Kilo Code

- Verify Kilo Code extension version
- Check YAML syntax with: `python -c "import yaml; yaml.safe_load(open('.kilo/custom_modes.yaml'))"`
- Reload IDE window after generation

## Next Steps

1. Run `riseon-agents` and explore the TUI
2. Generate configurations for a test project
3. Verify in Kilo Code IDE extension
4. Report issues or suggestions
