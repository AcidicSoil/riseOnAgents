# path: TICKET-220-hermes-identity-and-context.md
---
ticket_id: "tkt_riseon_agents_hermes_identity_and_context"
title: "Emit-hermes-identity-and-context"
agent: "codex"
done: false
goal: "RiseOn supports Hermes by emitting separate identity and project-context outputs that preserve the provider’s distinct loading model."
---

## Tasks
- Implement `SOUL.md` generation from `IdentitySpec` for Hermes identity or persona content.
- Implement `.hermes.md` generation for highest-priority Hermes project context.
- Support optional `AGENTS.md` interoperability output for Hermes mode without collapsing identity and project context into one file.
- Ensure Hermes-compatible skill metadata extensions are routed through the skill surface rather than the project-context surface.

## Acceptance criteria
- Hermes output can emit both `.hermes.md` and `SOUL.md` when the relevant source content exists.
- Hermes identity and project-context outputs are represented as separate surfaces.
- Hermes support does not rely on a fake shared custom-agent manifest schema.

## Tests
- uv run pytest tests/test_generators/test_hermes.py -q
- uv run pytest tests/test_golden_outputs.py -q
- uv run pytest tests/test_validation.py -q

## Notes
- Source: "Hermes separates identity (`SOUL.md`) from repo instructions."
- Source: "Hermes loads project context from `.hermes.md` / `HERMES.md`, then `AGENTS.md`, then `CLAUDE.md`, then Cursor-style files."
- Constraints:
  - Do not merge `SOUL.md` into repo instructions.
- Evidence:
  - The handoff calls out Hermes as a distinct compatibility surface with identity support.
- Dependencies:
  - TICKET-100-provider-capability-registry.md
  - TICKET-120-canonical-compatibility-models.md
  - TICKET-160-skill-surface-support.md
- Unknowns: Not provided
