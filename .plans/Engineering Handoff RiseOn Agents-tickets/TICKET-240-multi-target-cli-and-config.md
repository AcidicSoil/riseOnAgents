# path: TICKET-240-multi-target-cli-and-config.md
---
ticket_id: "tkt_riseon_agents_multi_target_cli_and_config"
title: "Add-multi-target-cli-and-config"
agent: "codex"
done: false
goal: "Users can request one or more provider targets in a single run and receive the correct provider-native output set."
---

## Tasks
- Extend user-facing configuration and CLI handling to accept one or more target providers in a single invocation.
- Support the explicit targets named in the handoff: codex, gemini, hermes, claude, copilot, vscode, and pi.
- Wire multi-target execution so the correct project-instruction, skill, custom-agent, identity, and rule emitters run only for providers that support those surfaces.

## Acceptance criteria
- A single run can emit outputs for multiple providers.
- Multi-target generation respects provider-native filenames and formats rather than forcing a lowest-common-denominator output.
- Unsupported mapping attempts produce clear errors.

## Tests
- uv run pytest tests/test_golden_outputs.py -q
- uv run pytest tests/test_validation.py -q

## Notes
- Source: "Add an option to generate multi-target output in a single run."
- Source: "Example behavior: `--target codex,gemini,hermes`."
- Constraints:
  - Only emit surfaces the selected target provider actually supports.
- Evidence:
  - The handoff explicitly calls for multi-target output in one command.
- Dependencies:
  - TICKET-140-project-instruction-emitters.md
  - TICKET-160-skill-surface-support.md
  - TICKET-180-codex-custom-agent-toml.md
  - TICKET-200-frontmatter-agent-emitters.md
  - TICKET-220-hermes-identity-and-context.md
- Unknowns: Not provided
