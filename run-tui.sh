#!/bin/bash
# Execution RiseOn.Agents TUI
# Usage: ./run-tui.sh

cd "$(dirname "$0")"
source .venv/bin/activate
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
python -m riseon_agents
