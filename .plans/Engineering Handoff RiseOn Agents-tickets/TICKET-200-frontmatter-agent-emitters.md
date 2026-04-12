# path: TICKET-200-frontmatter-agent-emitters.md
---
ticket_id: "tkt_riseon_agents_frontmatter_agent_emitters"
title: "Emit-frontmatter-agent-manifests"
agent: "codex"
done: false
goal: "RiseOn emits provider-native markdown agent manifests with YAML frontmatter for Gemini CLI, Claude Code, GitHub Copilot, and VS Code."
---

## Tasks
- Implement `.gemini/agents/*.md` generation with YAML frontmatter for Gemini subagents.
- Implement `.claude/agents/*.md` generation with YAML frontmatter for Claude subagents.
- Implement `.github/agents/*.agent.md` generation with YAML frontmatter for GitHub Copilot and VS Code agent profiles.
- Map the canonical agent profile fields into each target’s required and optional frontmatter fields without assuming cross-provider field parity.

## Acceptance criteria
- Gemini, Claude, Copilot, and VS Code agent outputs are emitted as markdown files with YAML frontmatter in the provider-native locations named in the handoff.
- Required core fields are preserved for each supported target.
- Provider-specific fields remain scoped to the relevant emitter instead of leaking into a shared manifest contract.

## Tests
- uv run pytest tests/test_generators/test_gemini.py -q
- uv run pytest tests/test_generators/test_claude.py -q
- uv run pytest tests/test_generators/test_copilot.py -q
- uv run pytest tests/test_generators/test_vscode.py -q
- uv run pytest tests/test_validation.py -q
- uv run pytest tests/test_golden_outputs.py -q

## Notes
- Source: "Gemini / Claude / Copilot / VS Code use markdown files with YAML frontmatter."
- Constraints:
  - Do not claim Hermes exposes the same custom-agent manifest contract in this phase.
  - Do not assume a universal field set beyond the canonical mapping layer.
- Evidence:
  - The handoff verifies markdown plus YAML frontmatter for Gemini subagents, Claude subagents, and Copilot or VS Code custom agents.
- Dependencies:
  - TICKET-100-provider-capability-registry.md
  - TICKET-120-canonical-compatibility-models.md
- Unknowns:
  - Remote Gemini agent output should remain out of scope unless RiseOn explicitly models remote cards.
