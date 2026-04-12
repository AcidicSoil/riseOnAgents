# RiseOn.Agents overview

- Purpose: canonical agent-definition framework that generates platform-specific AI coding agent configs from a single source of truth, with a Textual TUI and CLI entrypoint.
- Stack: Python 3.11+, Textual, Rich, PyYAML, python-frontmatter; pytest/pytest-asyncio/pytest-cov for tests; Ruff, Black, MyPy for quality.
- Package layout: `src/riseon_agents/` for app, parsing, generation, models, and CLI; `tests/` for generation/parsing/UI coverage; `.plans/` for engineering handoffs and ticket stacks.
- Entrypoints: `python -m riseon_agents`, `riseon-agents`, and `./run-tui.sh`.
- Current work style: strict typing, dataclass-heavy models, docstrings, deterministic generator/parsing behavior, tests updated alongside code.
