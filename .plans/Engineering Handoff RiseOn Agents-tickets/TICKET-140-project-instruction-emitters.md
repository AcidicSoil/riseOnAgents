# path: TICKET-140-project-instruction-emitters.md
---
ticket_id: "tkt_riseon_agents_project_instruction_emitters"
title: "Emit-provider-native-project-instructions"
agent: "codex"
done: false
goal: "RiseOn emits provider-native project instruction files with the correct filenames and without inventing a shared frontmatter contract."
---

## Tasks
- Implement project-instruction emitters for Codex, Gemini CLI, Hermes Agent, Claude Code, GitHub Copilot, and VS Code.
- Map provider-native filenames as described in the handoff: `AGENTS.md`, `GEMINI.md`, `.hermes.md`, `CLAUDE.md`, and repo-root `AGENTS.md` for Copilot and VS Code.
- Ensure project instruction outputs are emitted as plain markdown documents unless the target surface explicitly requires another format.

## Acceptance criteria
- Codex emits `AGENTS.md` as an open-format markdown instruction file.
- Gemini emits `GEMINI.md`, with optional compatibility-mode support for also emitting `AGENTS.md`.
- Hermes emits `.hermes.md`; Claude emits `CLAUDE.md`; Copilot and VS Code emit `AGENTS.md`.
- No project-instruction emitter invents YAML frontmatter for surfaces the handoff treats as plain instruction documents.

## Tests
- uv run pytest tests/test_golden_outputs.py -q
- uv run pytest tests/test_generators/test_codex.py -q
- uv run pytest tests/test_generators/test_gemini.py -q
- uv run pytest tests/test_generators/test_hermes.py -q
- uv run pytest tests/test_generators/test_claude.py -q
- uv run pytest tests/test_generators/test_copilot.py -q
- uv run pytest tests/test_generators/test_vscode.py -q

## Notes
- Source: "Do not invent YAML frontmatter for AGENTS.md."
- Source: "Codex officially centers on AGENTS.md; Gemini CLI officially centers on GEMINI.md."
- Constraints:
  - Treat AGENTS.md, GEMINI.md, and CLAUDE.md as provider-native instruction documents.
  - Hermes project context is separate from identity.
- Evidence:
  - The handoff distinguishes project instructions from skills and custom agents.
- Dependencies:
  - TICKET-100-provider-capability-registry.md
  - TICKET-120-canonical-compatibility-models.md
- Unknowns: Not provided
