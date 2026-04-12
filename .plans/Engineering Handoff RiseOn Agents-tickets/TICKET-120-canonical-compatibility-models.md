# path: TICKET-120-canonical-compatibility-models.md
---
ticket_id: "tkt_riseon_agents_canonical_compatibility_models"
title: "Separate-canonical-compatibility-models"
agent: "codex"
done: false
goal: "RiseOn represents project instructions, skills, custom agents, identity files, and rules as distinct internal models instead of one merged markdown-frontmatter abstraction."
---

## Tasks
- Introduce the canonical internal models described in the handoff: ProjectInstructions, SkillSpec, AgentProfile, IdentitySpec, and RuleSpec.
- Refactor parsing and generation plumbing so project instruction files can remain plain markdown while provider-native agent manifests and skills use their own formats.
- Stop assuming every generated artifact is a markdown file with frontmatter.

## Acceptance criteria
- Internal models exist for the distinct compatibility surfaces named in the handoff.
- Generation code can route plain markdown, YAML-frontmatter markdown, and TOML outputs without coercing them into a single shape.
- Existing repository structure can be mapped into the new internal models without losing source content needed for generation.

## Tests
- uv run pytest tests/test_generators/test_codex.py -q
- uv run pytest tests/test_generators/test_gemini.py -q
- uv run pytest tests/test_generators/test_hermes.py -q
- uv run pytest tests/test_generators/test_claude.py -q
- uv run pytest tests/test_generators/test_copilot.py -q
- uv run pytest tests/test_generators/test_vscode.py -q
- uv run pytest tests/test_generators/test_pi.py -q

## Notes
- Source: "Introduce an internal provider-agnostic model with separate entities, not one merged markdown abstraction."
- Constraints:
  - Preserve the current canonical source layout.
  - Do not force project instruction files into typed YAML manifests.
- Evidence:
  - Current layout includes agents, rules, skills, and subagents.
  - The repo already depends on python-frontmatter where markdown metadata is appropriate.
- Dependencies:
  - TICKET-100-provider-capability-registry.md
- Unknowns: Not provided
