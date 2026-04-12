# path: TICKET-180-codex-custom-agent-toml.md
---
ticket_id: "tkt_riseon_agents_codex_custom_agent_toml"
title: "Emit-codex-custom-agent-toml"
agent: "codex"
done: false
goal: "RiseOn emits Codex custom agents in the provider-native TOML format under `.codex/agents/`."
---

## Tasks
- Implement Codex custom-agent generation from `AgentProfile` into `.codex/agents/*.toml`.
- Map the canonical agent fields into the Codex TOML shape described in the handoff, including `name`, `description`, and `developer_instructions`, with optional execution, model, and MCP settings when present.
- Ensure Codex custom-agent output is isolated from markdown-frontmatter agent emitters.

## Acceptance criteria
- Codex custom-agent manifests are generated as TOML files under `.codex/agents/`.
- Codex custom-agent output does not use markdown files or YAML frontmatter.
- Unsupported field mappings fail validation instead of being silently coerced.

## Tests
- uv run pytest tests/test_generators/test_codex.py -q
- uv run pytest tests/test_validation.py -q
- uv run pytest tests/test_golden_outputs.py -q

## Notes
- Source: "Codex custom agents are TOML, not markdown-frontmatter manifests."
- Constraints:
  - Do not coerce Codex custom agents into markdown.
- Evidence:
  - The handoff names `.codex/agents/*.toml` as the provider-native output location.
- Dependencies:
  - TICKET-100-provider-capability-registry.md
  - TICKET-120-canonical-compatibility-models.md
- Unknowns: Not provided
