# path: TICKET-280-review-deferred-provider-surfaces.md
---
ticket_id: "tkt_riseon_agents_review_deferred_provider_surfaces"
title: "Review-deferred-provider-surfaces"
agent: "user"
done: false
goal: "A human reviews the shipped provider support against the handoff’s non-goals, deferred items, and acceptance criteria before broader rollout."
---

## Tasks
- Review the generated provider support against the handoff acceptance criteria for Codex, Gemini CLI, Hermes Agent, Claude Code, GitHub Copilot, VS Code, and Pi/OpenClaw skills.
- Confirm that under-verified surfaces were deferred rather than represented as fully supported.
- Decide whether to schedule the carry-forward backlog items named in the handoff after the initial patch lands.

## Acceptance criteria
- A reviewer confirms the initial patch meets the handoff acceptance criteria without overstating unsupported provider surfaces.
- Deferred items are explicitly tracked rather than implied as completed.
- Rollout is not blocked by Pi custom-agent support or Cursor-specific rule manifests unless official schemas are verified.

## Tests
- Verify generated outputs for each enabled provider match the expected filenames and formats.
- Verify deferred items remain out of scope for the initial patch unless separately implemented.

## Notes
- Source: "Do not block the overall patch on Pi custom-agent manifests unless the team locates an official stable schema during implementation."
- Source: "Do not claim full Cursor parity until the team validates the official rule format from primary docs."
- Constraints:
  - Non-goals and deferred surfaces must stay clearly marked.
- Evidence:
  - Suggested backlog includes Codex skill metadata via `agents/openai.yaml`, Copilot path-scoped instruction generation, Hermes metadata enrichment, Pi custom-agent support if an official schema is found, and Cursor target validation.
- Dependencies:
  - TICKET-260-validation-and-golden-tests.md
- Unknowns: Not provided
