# path: TICKET-160-skill-surface-support.md
---
ticket_id: "tkt_riseon_agents_skill_surface_support"
title: "Standardize-skill-surface-support"
agent: "codex"
done: false
goal: "RiseOn emits Agent-Skills-compatible SKILL.md outputs as the canonical reusable skill unit and applies provider extensions only where officially supported."
---

## Tasks
- Implement canonical `SKILL.md` generation from `SkillSpec` for the supported provider targets.
- Add provider-specific skill extensions only where the handoff explicitly calls for them, including Hermes-compatible skill metadata extensions when present.
- Add Pi/OpenClaw skill compatibility by generating Agent-Skills-compatible `SKILL.md` into `.agents/skills/` and optionally mirroring to `.pi/skills/` where requested.
- Preserve optional richer Codex skill metadata emission as a provider-specific extension path instead of a universal requirement.

## Acceptance criteria
- Skills round-trip through the canonical internal model without losing required fields.
- `SKILL.md` remains the canonical reusable unit across supported providers.
- Pi/OpenClaw support is delivered through skills compatibility first, without claiming stable custom-agent support.
- Provider-specific skill extensions remain additive and do not change the canonical skill contract.

## Tests
- uv run pytest tests/test_generators/test_codex.py -q
- uv run pytest tests/test_generators/test_hermes.py -q
- uv run pytest tests/test_generators/test_pi.py -q
- uv run pytest tests/test_golden_outputs.py -q

## Notes
- Source: "Use Agent-Skills-compatible SKILL.md as the canonical reusable unit."
- Source: "Pi and OpenClaw both align strongly with the Agent Skills model."
- Constraints:
  - Extend per provider only where officially supported.
  - Do not block the patch on Pi custom-agent manifests.
- Evidence:
  - Required core skill fields consistently verified: name and description.
- Dependencies:
  - TICKET-100-provider-capability-registry.md
  - TICKET-120-canonical-compatibility-models.md
- Unknowns:
  - Whether `.pi/skills/` mirroring is requested by project configuration.
