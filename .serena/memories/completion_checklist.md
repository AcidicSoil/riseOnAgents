# Completion checklist

Before considering a task done:
- Run targeted pytest coverage for changed areas first.
- Run broader relevant tests if interfaces or shared models changed.
- Run `ruff check` on touched files or `src tests` when feasible.
- Run `black --check src tests` or format touched files if needed.
- Run `mypy src/riseon_agents` when changes affect typed interfaces.
- Review CLI/app entrypoints and generator behavior if generation/parsing contracts changed.
- Summarize code changes and validation results clearly for the user.
