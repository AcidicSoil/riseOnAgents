# path: TICKET-100-provider-capability-registry.md
---
ticket_id: "tkt_riseon_agents_provider_capability_registry"
title: "Establish-provider-capability-registry"
agent: "codex"
done: false
goal: "RiseOn has a single capability registry that describes which compatibility surfaces each target provider supports and where each output belongs."
---

## Tasks
- Add a provider capability registry that captures, per provider, the supported instruction files, skill format, agent format, required agent fields, identity support, path-scoped rule support, and output locations.
- Encode the target providers called out in the handoff: Codex, Gemini CLI, Hermes Agent, Claude Code, GitHub Copilot, VS Code, and Pi/OpenClaw skills.
- Replace scattered provider conditionals with registry-backed capability lookups where generation decisions are made.

## Acceptance criteria
- A single registry defines the provider-specific capability surface used by generation code.
- The registry distinguishes project instructions, skills, custom agents/subagents, identity files, and rules instead of treating them as one shared format.
- Provider support that is under-verified is represented as unsupported or deferred rather than implied.

## Tests
- uv run pytest tests/test_generators/test_codex.py -q
- uv run pytest tests/test_generators/test_gemini.py -q
- uv run pytest tests/test_generators/test_hermes.py -q
- uv run pytest tests/test_generators/test_claude.py -q
- uv run pytest tests/test_generators/test_copilot.py -q
- uv run pytest tests/test_generators/test_vscode.py -q
- uv run pytest tests/test_generators/test_pi.py -q

## Notes
- Source: "Add a registry like: instruction_files, supports_instruction_frontmatter, skill_format, skill_extensions, agent_format, agent_required_fields, supports_identity_file, supports_path_scoped_rules, output_locations."
- Constraints:
  - Do not model all providers as one shared frontmatter schema.
  - Do not misrepresent under-verified surfaces as supported.
- Evidence:
  - Providers diverge across plain markdown instructions, SKILL.md, TOML agents, and markdown plus YAML frontmatter agents.
- Dependencies: Not provided
- Unknowns:
  - Pi custom-agent manifest generation remains under-verified.
  - Cursor-specific rule schema remains under-verified.
