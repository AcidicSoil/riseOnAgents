# Suggested commands

## Setup
- `python3.11 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -e ".[dev]"`

## Run
- `./run-tui.sh`
- `export PYTHONPATH=src:$PYTHONPATH && python -m riseon_agents`
- `riseon-agents`

## Test
- `PYTHONPATH=src pytest tests/ -v`
- `PYTHONPATH=src pytest tests/test_generation/test_generator.py -v`
- `PYTHONPATH=src pytest tests/test_parsing/ -v`

## Quality
- `ruff check src tests`
- `ruff check --fix src tests`
- `black src tests`
- `black --check src tests`
- `mypy src/riseon_agents`

## Full validation
- `ruff check src tests && black --check src tests && mypy src/riseon_agents && PYTHONPATH=src pytest tests/ -v`

## Linux utilities
- `git status`, `git diff`, `git grep`, `find`, `ls`, `cd`, `sed`, `grep`
