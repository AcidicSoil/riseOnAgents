# RiseOn.Agents Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-03-30

## Active Technologies

- Python 3.11+ + Textual >=0.47.0, Rich >=13.0.0, PyYAML >=6.0, python-frontmatter >=1.0 (002-kilocode-generator)

## Project Structure

```text
src/
tests/
```

## Build/Lint/Test Commands

**Setup (one-time):**
```bash
# Create virtual environment (if not exists)
python3.11 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

**Run the TUI application:**
```bash
./run-tui.sh
# OR manually:
export PYTHONPATH=src:$PYTHONPATH
python -m riseon_agents
```

**Run all tests:**
```bash
PYTHONPATH=src pytest tests/ -v
```

**Run a single test file:**
```bash
PYTHONPATH=src pytest tests/test_generation/test_generator.py -v
```

**Run a single test class:**
```bash
PYTHONPATH=src pytest tests/test_generation/test_generator.py::TestYAMLValidation -v
```

**Run a single test method:**
```bash
PYTHONPATH=src pytest tests/test_generation/test_generator.py::TestYAMLValidation::test_validate_yaml_valid_file -v
```

**Lint and format:**
```bash
# Check code with ruff
ruff check src tests

# Fix auto-fixable issues
ruff check --fix src tests

# Format with black
black src tests

# Type check with mypy (strict)
mypy src/riseon_agents
```

**Full validation (run before commits):**
```bash
ruff check src tests && black --check src tests && mypy src/riseon_agents && PYTHONPATH=src pytest tests/ -v
```

## Code Style

### Python 3.11+ Standards

**Type Hints (Required):**
- Use Python 3.11+ syntax: `list[str]`, `dict[str, int]`, `str | None`
- Avoid `from typing import List, Dict, Optional` (use built-in generics)
- All function parameters and return types must be annotated
- Use `|` for unions instead of `Union` or `Optional`
- Example: `def process(items: list[str]) -> dict[str, int] | None:`

**Imports Organization:**
```python
"""Module docstring here."""

# 1. Standard library imports
from pathlib import Path
from enum import Enum

# 2. Third-party imports (alphabetical)
import yaml
from textual.widgets import Tree

# 3. Local imports (alphabetical, grouped by package)
from riseon_agents.models.agent import PrimaryAgent
from riseon_agents.models.generation import GenerationResult
```

**Formatting:**
- Line length: 100 characters (enforced by ruff/black)
- Use double quotes for strings
- Trailing commas in multi-line collections
- Black handles all formatting - don't fight it

**Naming Conventions:**
- `snake_case` for functions, variables, modules
- `PascalCase` for classes
- `UPPER_CASE` for constants and enums
- Private methods/attributes prefix with `_`
- Test classes: `Test<ClassName>`
- Test methods: `test_<description>`

**Docstrings:**
- Use triple double quotes: `"""Docstring here."""`
- Module docstrings at the top of each file
- Class docstrings explaining purpose
- Method docstrings with Args and Returns sections:
```python
def validate_yaml(self, file_path: Path) -> ValidationResult:
    """Validate a YAML file for syntax errors.

    Implements T076: User Story 6 - YAML validation.

    Args:
        file_path: Path to the YAML file to validate.

    Returns:
        ValidationResult with status and any errors found.
    """
```

**Task References in Comments:**
- Prefix implementation comments with task IDs:
```python
# T073: Use GenerationTarget for path resolution
if level == GenerationLevel.LOCAL:
    target = GenerationTarget.local(base_dir)
```

**Error Handling:**
- Use specific exception types, not bare `except:`
- Provide context in error messages
- Use `result.add_error()` pattern for accumulating errors
- Don't swallow exceptions silently

**Dataclasses:**
- Use `@dataclass` for data containers
- Use `field(default_factory=list)` for mutable defaults
- Include type hints on all fields

**Test Patterns:**
```python
class TestClassName:
    """T###: Brief description of what's being tested."""

    def test_specific_behavior(self, tmp_path):
        """Description of what this test verifies."""
        # Arrange
        instance = ClassName()
        
        # Act
        result = instance.method()
        
        # Assert
        assert result.expected_value == actual_value
```

## Linting Configuration

**Ruff settings** (from pyproject.toml):
- Line length: 100
- Target Python: 3.11
- Enabled: E, W, F, I (isort), B (bugbear), C4, UP, ARG, SIM
- First-party package: `riseon_agents`

**MyPy settings** (strict mode):
- `disallow_untyped_defs = true`
- `disallow_incomplete_defs = true`
- `no_implicit_optional = true`
- Ignores missing imports for: frontmatter, textual, rich

## Recent Changes

- 002-kilocode-generator: Added Python 3.11+ + Textual >=0.47.0, Rich >=13.0.0, PyYAML >=6.0, python-frontmatter >=1.0
- Phase 9: Added HelpOverlay widget (? key), permission error handling, generation interruption cleanup
- All 166 tests passing, 91 tasks complete across 9 phases

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
