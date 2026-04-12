# Style and conventions

- Python 3.11+ typing is required: use built-in generics (`list[str]`, `dict[str, str]`) and `|` unions.
- Keep Ruff/Black line length to 100 characters.
- Organize imports into stdlib, third-party, local groups.
- Use `snake_case` for functions/modules/variables, `PascalCase` for classes, `UPPER_CASE` for constants.
- Prefer dataclasses for structured data and `field(default_factory=...)` for mutable defaults.
- Add docstrings for modules, classes, and non-trivial methods; use triple double quotes.
- Use explicit exception handling and informative messages.
- Keep implementations test-driven where possible, update tests with each feature slice, and preserve backward compatibility or update all references.
