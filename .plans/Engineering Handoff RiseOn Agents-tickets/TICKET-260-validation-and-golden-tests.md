# path: TICKET-260-validation-and-golden-tests.md
---
ticket_id: "tkt_riseon_agents_validation_and_golden_tests"
title: "Add-validation-and-golden-tests"
agent: "codex"
done: false
goal: "RiseOn fails closed on invalid provider mappings and has golden and smoke coverage for the provider-native outputs introduced by this patch."
---

## Tasks
- Implement provider-native validators for project instructions, skills, and agent manifests where the handoff explicitly calls for them.
- Add schema and output validation covering Codex TOML agents, Gemini agent frontmatter, Hermes skill metadata behavior, Claude subagent frontmatter, Copilot or VS Code agent frontmatter, and Pi skill requirements.
- Add golden-file coverage that verifies the expected filenames, locations, and formats for each supported provider target.
- Add smoke tests using the command set listed in the handoff.

## Acceptance criteria
- Validation errors clearly identify missing required fields, unsupported fields for the target provider, and incompatible provider mapping attempts.
- Golden tests cover the provider-native outputs named in the handoff.
- Codex markdown-frontmatter agent output is rejected at validation or output time.
- Pi support validation is limited to the skill surface unless a verified custom-agent schema is added later.

## Tests
- uv run pytest tests/test_validation.py -q
- uv run pytest tests/test_golden_outputs.py -q
- uv run pytest tests/test_generators/test_codex.py -q
- uv run pytest tests/test_generators/test_gemini.py -q
- uv run pytest tests/test_generators/test_hermes.py -q
- uv run pytest tests/test_generators/test_claude.py -q
- uv run pytest tests/test_generators/test_copilot.py -q
- uv run pytest tests/test_generators/test_vscode.py -q
- uv run pytest tests/test_generators/test_pi.py -q

## Notes
- Source: "Fail closed on required fields."
- Source: "Validation errors clearly identify missing required fields, unsupported fields for target provider, incompatible provider mapping attempts."
- Constraints:
  - Do not claim support for under-verified custom-agent surfaces.
- Evidence:
  - The handoff provides specific validator names, golden-file coverage, and smoke-test commands.
- Dependencies:
  - TICKET-140-project-instruction-emitters.md
  - TICKET-160-skill-surface-support.md
  - TICKET-180-codex-custom-agent-toml.md
  - TICKET-200-frontmatter-agent-emitters.md
  - TICKET-220-hermes-identity-and-context.md
  - TICKET-240-multi-target-cli-and-config.md
- Unknowns: Not provided
