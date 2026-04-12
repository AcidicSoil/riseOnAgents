# Engineering Handoff RiseOn Agents

**Created:** 4/11/2026 17:46:22  
**Updated:** 4/11/2026 17:53:11  
**Exported:** 4/11/2026 18:09:09  
**Link:** [https://chatgpt.com/g/g-p-699e141c586c8191a60c161296bf2ae0-g-chat/c/69dacf3b-b510-83ea-9189-3e7cfa11a30a](https://chatgpt.com/g/g-p-699e141c586c8191a60c161296bf2ae0-g-chat/c/69dacf3b-b510-83ea-9189-3e7cfa11a30a)  

## Prompt:
your job is to generate a handoff for the engineering team to add codex and additional agent support for the following [RiseOn.Agents](https://github.com/daviholandas/RiseOn.Agents) 

Research the official supported frontmatter for codex, and other agent providers e.g. hermes-agent, gemini-cli, pi, and others so that each agent will be in full support and users will be able to utilize their agent of choice as needed after the pertinent support for each is patched in.

## Response:
I’m verifying the repo’s current instruction surface and the official instruction-file/frontmatter behavior for each agent before drafting the handoff. The main risk here is assuming parity where the providers actually diverge.

One concrete finding already: Codex and Gemini do **not** line up on the same primary instruction-file contract. Codex officially centers on `AGENTS.md`; Gemini CLI officially centers on `GEMINI.md`, though Gemini can be configured to also recognize `AGENTS.md`. That affects whether RiseOn should normalize to one canonical target or emit provider-native files per backend.

Thought for 5m 22s

Engineering-Handoff
-------------------

### Objective

Patch **RiseOn.Agents** so it can generate provider-native instruction assets for **Codex**, **Gemini CLI**, **Hermes Agent**, **Claude Code**, **GitHub Copilot / VS Code**, and **Pi/OpenClaw-compatible skills**, without forcing a fake universal frontmatter model where the providers do not actually share one.

### Executive-Decision

Do **not** model this as “one frontmatter schema for all agents.”

Model it as **three separate compatibility surfaces**:

1.  **Project-instructions**
    *   Repo/workspace guidance files such as `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.hermes.md`, `SOUL.md`.
    *   These are **not** universally frontmatter-driven.
    *   For Codex and AGENTS consumers, treat them as **plain markdown documents**, not typed YAML manifests.
2.  **Skills**
    *   This is the closest thing to a cross-provider standard.
    *   Use **Agent-Skills-compatible `SKILL.md`** as the canonical reusable unit.
    *   Extend per provider only where officially supported.
3.  **Custom-agents / subagents**
    *   These are **provider-specific manifests**.
    *   Codex uses **TOML**.
    *   Gemini / Claude / Copilot / VS Code use **markdown files with YAML frontmatter**.
    *   Hermes does not appear to expose the same custom-agent manifest contract in the official docs I reviewed.

Sources: [Visual Studio Code+7GitHub+7OpenAI Developers+7](https://github.com/daviholandas/RiseOn.Agents)

* * *

Current-State-of-RiseOn
-----------------------

RiseOn.Agents already has a useful canonical source layout:

*   `agents/{name}/{name}.agent.md`
*   `rules/`
*   `skills/`
*   `subagents/`

It currently targets **Kilo Code**, **OpenCode**, **GitHub Copilot**, and **Windsurf**. The repo also already depends on `python-frontmatter`, which means the codebase is already set up to parse markdown metadata where appropriate.

This is enough structure to add a provider-capability layer rather than redesigning the repository model from scratch.

Sources: [GitHub+3GitHub+3GitHub+3](https://github.com/daviholandas/RiseOn.Agents)

* * *

Recommended-Architecture
------------------------

### Canonical-IR

Introduce an internal provider-agnostic model with **separate entities**, not one merged markdown abstraction:

*   `ProjectInstructions`
    *   canonical content only
    *   no required frontmatter
    *   optional metadata for routing and scoping
*   `SkillSpec`
    *   based on Agent Skills
    *   canonical fields:
        *   `name`
        *   `description`
        *   `body`
        *   optional `tools`, `model`, `context`, `references`, `scripts`, provider extension bag
*   `AgentProfile`
    *   custom-agent/subagent abstraction
    *   canonical fields:
        *   `name`
        *   `description`
        *   `prompt`
        *   `tools`
        *   `mcp_servers`
        *   `model`
        *   `max_turns`
        *   provider extension bag
*   `IdentitySpec`
    *   for providers that split persona from repo context
    *   needed for Hermes `SOUL.md`
*   `RuleSpec`
    *   scoped instruction fragments
    *   used for Copilot path rules and future Cursor/experimental targets

### Provider-Capability-Registry

Add a registry like:

*   `instruction_files`
*   `supports_instruction_frontmatter`
*   `skill_format`
*   `skill_extensions`
*   `agent_format`
*   `agent_required_fields`
*   `supports_identity_file`
*   `supports_path_scoped_rules`
*   `output_locations`

This avoids scattered `if provider == ...` logic.

Sources: [Visual Studio Code+5OpenAI Developers+5Gemini CLI+5](https://developers.openai.com/codex/guides/agents-md)

* * *

Provider-Support-Matrix
-----------------------

### Codex

Implement:

*   `AGENTS.md` generation for project instructions
*   standard `SKILL.md` generation
*   optional `agents/openai.yaml` skill metadata emission when richer presentation is needed
*   `.codex/agents/*.toml` generation for custom agents

Important constraints:

*   **Do not invent YAML frontmatter for `AGENTS.md`.**
*   Codex documentation treats `AGENTS.md` as an open-format project instruction file.
*   Codex custom agents are **TOML**, not markdown-frontmatter manifests.
*   Codex skills use `SKILL.md`; optional OpenAI metadata lives separately in `agents/openai.yaml`.

### Gemini-CLI

Implement:

*   `GEMINI.md` generation as the provider-native instruction file
*   optional compatibility mode to also emit `AGENTS.md`
*   standard `SKILL.md` generation
*   `.gemini/agents/*.md` generation with YAML frontmatter for subagents
*   remote-agent output only if RiseOn explicitly models remote cards

Important constraints:

*   Gemini CLI can be configured to recognize alternate instruction filenames, including `AGENTS.md`, but `GEMINI.md` is the native target.
*   Gemini subagents officially require YAML frontmatter.

### Hermes-Agent

Implement:

*   `SOUL.md` generation for identity/persona
*   `.hermes.md` generation for highest-priority project context
*   optional `AGENTS.md` generation for interoperability mode
*   Hermes-compatible `SKILL.md` generation with Hermes metadata extensions when present

Important constraints:

*   Hermes separates **identity** (`SOUL.md`) from repo instructions.
*   Hermes loads project context from `.hermes.md` / `HERMES.md`, then `AGENTS.md`, then `CLAUDE.md`, then Cursor-style files.
*   Hermes skill metadata is markdown frontmatter-based, but project context is not a shared agent-profile schema.

### Claude-Code

Implement:

*   `CLAUDE.md` generation for project instructions
*   standard `SKILL.md` generation with Claude extensions where modeled
*   `.claude/agents/*.md` generation with YAML frontmatter

Important constraints:

*   `CLAUDE.md` is a plain instruction document, not a standardized frontmatter manifest.
*   Claude skills and Claude subagents both officially support YAML frontmatter.

### GitHub-Copilot / VS-Code

Implement:

*   `AGENTS.md` generation at repo root
*   `.github/agents/*.agent.md` generation for agent profiles
*   optional `.github/instructions/*.instructions.md` generation for path-scoped rules
*   optional `copilot-instructions.md` emission for repo-wide Copilot customization

Important constraints:

*   Copilot and VS Code both support `AGENTS.md`.
*   Copilot cloud/IDE custom agents use markdown files with YAML frontmatter.
*   Copilot path-scoped instructions use `.instructions.md` files with YAML frontmatter such as `applyTo`.

### Pi / OpenClaw

Implement now:

*   **skills compatibility first**
*   generate Agent-Skills-compatible `SKILL.md` into `.agents/skills/`
*   optionally mirror to `.pi/skills/` where requested

Do **not** block the overall patch on Pi custom-agent manifests unless the team locates an official stable schema during implementation.

Important constraints:

*   Pi and OpenClaw both align strongly with the Agent Skills model.
*   This is the safest official surface to support first.

Sources: [OpenClaw+19OpenAI Developers+19OpenAI Developers+19](https://developers.openai.com/codex/guides/agents-md)

* * *

Patch-Plan
----------

### Phase-1-Core-Refactor

Add provider generators:

*   `src/riseon_agents/generators/codex/`
*   `src/riseon_agents/generators/gemini/`
*   `src/riseon_agents/generators/hermes/`
*   `src/riseon_agents/generators/claude/`
*   `src/riseon_agents/generators/copilot/`
*   `src/riseon_agents/generators/vscode/`
*   `src/riseon_agents/generators/pi/`

Add a shared abstraction layer:

*   `provider_capabilities.py`
*   `models/project_instructions.py`
*   `models/skill_spec.py`
*   `models/agent_profile.py`
*   `models/identity_spec.py`

Refactor parsing so RiseOn stops assuming every generated artifact is “a markdown file with frontmatter.”

### Phase-2-Provider-Native-Emitters

Implement emitters per surface:

*   `emit_project_instructions(...)`
*   `emit_skill(...)`
*   `emit_agent_profile(...)`
*   `emit_identity(...)`
*   `emit_rules(...)`

Each provider decides which of these are valid and what file format they require.

### Phase-3-CLI-and-Config

Extend user-facing config so a project can request one or more targets:

*   `--target codex`
*   `--target gemini`
*   `--target hermes`
*   `--target claude`
*   `--target copilot`
*   `--target vscode`
*   `--target pi`

Add an option to generate **multi-target output** in a single run.

Example behavior:

*   `--target codex,gemini,hermes`
*   emits:
    *   `AGENTS.md`
    *   `GEMINI.md`
    *   `.hermes.md`
    *   `SOUL.md` if identity exists
    *   provider-specific agent/skill folders as applicable

### Phase-4-Validation

Add schema validators:

*   `validate_codex_agents_md()`
*   `validate_codex_toml_agent()`
*   `validate_gemini_agent_frontmatter()`
*   `validate_hermes_skill_frontmatter()`
*   `validate_claude_subagent_frontmatter()`
*   `validate_copilot_agent_frontmatter()`
*   `validate_pi_skill_frontmatter()`

Fail closed on required fields.

Sources: [GitHub+5OpenAI Developers+5Gemini CLI+5](https://developers.openai.com/codex/subagents)

* * *

Required-Behavior-By-Surface
----------------------------

### Project-Instructions

Canonical source should remain plain markdown content plus optional metadata for generator routing.

Do not require frontmatter here.

Provider mapping:

*   Codex → `AGENTS.md`
*   Gemini → `GEMINI.md`
*   Hermes → `.hermes.md` and optionally `AGENTS.md`
*   Claude → `CLAUDE.md`
*   Copilot / VS Code → `AGENTS.md`

### Skills

Use Agent-Skills-compatible `SKILL.md` as the canonical reusable object.

Canonical required fields:

*   `name`
*   `description`

Canonical optional fields:

*   `tools`
*   `model`
*   `context`
*   `allowed_tools`
*   `disable_model_invocation`
*   `references`
*   `scripts`
*   `metadata`

Provider-specific extensions should remain additive.

### Custom-Agents

Canonical `AgentProfile` should be rendered differently per provider:

*   Codex → TOML
*   Gemini → markdown + YAML frontmatter
*   Claude → markdown + YAML frontmatter
*   Copilot / VS Code → `.agent.md` / `.github/agents/*.agent.md`
*   Hermes → not first-class in this phase unless a verified official manifest contract is found
*   Pi → defer until official stable manifest schema is verified

Sources: [GitHub+7OpenAI Developers+7Gemini CLI+7](https://developers.openai.com/codex/skills)

* * *

Frontmatter-Research-Summary
----------------------------

### Officially-Verified

**Agent-Skills-style `SKILL.md`**

*   Required core fields consistently verified: `name`, `description`

**Gemini subagents**

*   YAML frontmatter required
*   verified fields include `name`, `description`, optional `kind`, `tools`, `mcpServers`, `model`, `temperature`, `max_turns`

**Claude subagents**

*   YAML frontmatter required
*   verified fields include `name`, `description`, optional tools/model/permissions/skills/hooks/memory/isolation fields

**Copilot / VS Code custom agents**

*   markdown with YAML frontmatter
*   verified core fields include `name`, `description`, `tools`; Copilot docs also describe `mcp-servers`

**Codex custom agents**

*   **not frontmatter**
*   TOML fields include `name`, `description`, `developer_instructions`, plus optional execution/model/MCP settings

### Officially-Not-A-Shared-Frontmatter-Surface

**AGENTS.md**

*   treat as open-format markdown instructions
*   no shared official YAML frontmatter contract verified for Codex/Copilot/AGENTS consumers

**CLAUDE.md**

*   treat as plain project memory/instructions

**GEMINI.md**

*   treat as plain project context unless Gemini-specific custom config handling is intentionally added later

### Under-Verified / Defer

*   Pi custom-agent manifest generation
*   Cursor rule-manifest generation as a first-class RiseOn target

Sources: [Claude API Docs+8OpenAI Developers+8OpenAI Developers+8](https://developers.openai.com/codex/guides/agents-md)

* * *

Implementation-Non-Goals
------------------------

Do not do any of these in the first patch:

*   do not create a fake universal AGENTS frontmatter spec
*   do not coerce Codex custom agents into markdown
*   do not merge Hermes `SOUL.md` into repo instructions
*   do not promise Pi custom-agent generation without a verified official schema
*   do not claim full Cursor parity until the team validates the official rule format from primary docs

Sources: [OpenAI Developers+2Hermes Agent+2](https://developers.openai.com/codex/subagents)

* * *

Acceptance-Criteria
-------------------

1.  RiseOn can generate provider-native outputs for:
    *   Codex
    *   Gemini CLI
    *   Hermes Agent
    *   Claude Code
    *   GitHub Copilot / VS Code
    *   Pi/OpenClaw skills
2.  Generated output matches each provider’s expected filename and format.
3.  Skills round-trip through canonical IR without losing required fields.
4.  Providers that support custom agents receive provider-native agent manifests.
5.  Providers that do not share a stable custom-agent schema are not misrepresented as supported.
6.  Multi-target generation works in one command.
7.  Validation errors clearly identify:
    *   missing required fields
    *   unsupported fields for target provider
    *   incompatible provider mapping attempts

* * *

Smoke-Tests
-----------

### RiseOn-Unit-Smoke-Tests

Use `uv`, not raw `python`.

```
uv run pytest tests/test_generators/test_codex.py -q
uv run pytest tests/test_generators/test_gemini.py -q
uv run pytest tests/test_generators/test_hermes.py -q
uv run pytest tests/test_generators/test_claude.py -q
uv run pytest tests/test_generators/test_copilot.py -q
uv run pytest tests/test_generators/test_vscode.py -q
uv run pytest tests/test_generators/test_pi.py -q
```

### Golden-File-Smoke-Tests

Add fixture projects and verify exact outputs:

```
uv run pytest tests/test_golden_outputs.py -q
```

Coverage targets:

*   `AGENTS.md` emitted for Codex/Copilot/VS Code
*   `GEMINI.md` emitted for Gemini
*   `.hermes.md` and `SOUL.md` emitted for Hermes when identity exists
*   `CLAUDE.md` emitted for Claude
*   `.codex/agents/*.toml` emitted for Codex agent profiles
*   `.gemini/agents/*.md` emitted for Gemini subagents
*   `.claude/agents/*.md` emitted for Claude subagents
*   `.github/agents/*.agent.md` emitted for Copilot

### Schema-Smoke-Tests

```
uv run pytest tests/test_validation.py -q
```

Minimum assertions:

*   Codex agent rejects markdown frontmatter source at output stage
*   Gemini agent requires `name` and `description`
*   Claude subagent requires `name` and `description`
*   Pi skill requires `name` and `description`

* * *

Suggested-Backlog
-----------------

### P0

*   provider capability registry
*   Codex generator
*   Gemini generator
*   Hermes generator
*   Claude generator
*   Copilot / VS Code generator
*   validation layer
*   golden output tests

### P1

*   Codex skill metadata via `agents/openai.yaml`
*   Copilot path-scoped instruction generation
*   Hermes metadata enrichment for skills
*   multi-target CLI UX polish

### P2

*   Pi custom-agent support if official schema is found
*   Cursor target after official rule/manifests are revalidated
*   remote Gemini agent generation

* * *

Bottom-Line
-----------

The correct design is **provider-native output from a shared internal model**, not a universal markdown-frontmatter abstraction.

The fastest safe path is:

1.  standardize **skills** on Agent Skills,
2.  treat **project instruction files** as provider-native documents,
3.  emit **custom agents** in each provider’s real format,
4.  defer under-verified surfaces instead of guessing.

Sources
-------

*   **RiseOn-current-structure-and-supported-targets**: [GitHub+3GitHub+3GitHub+3](https://github.com/daviholandas/RiseOn.Agents)
*   **Codex-project-instructions-and-fallback-files**: [OpenAI Developers+2OpenAI Developers+2](https://developers.openai.com/codex/guides/agents-md)
*   **Codex-skills-and-metadata**: [OpenAI Developers+2OpenAI Developers+2](https://developers.openai.com/codex/skills)
*   **Codex-custom-agents-TOML**: [OpenAI Developers](https://developers.openai.com/codex/subagents)
*   **Gemini-project-context-files**: [Gemini CLI](https://geminicli.com/docs/cli/gemini-md/)
*   **Gemini-skills**: [Gemini CLI](https://geminicli.com/docs/cli/creating-skills/)
*   **Gemini-subagents-and-remote-agents**: [Gemini CLI+1](https://geminicli.com/docs/core/subagents/)
*   **Hermes-context-loading-and-SOUL**: [Hermes Agent+3Hermes Agent+3Hermes Agent+3](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files/)
*   **Hermes-skills**: [Hermes Agent+2Hermes Agent+2](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills)
*   **Claude-project-memory**: [Claude API Docs](https://docs.anthropic.com/en/docs/claude-code/memory)
*   **Claude-skills**: [Claude API Docs+4Claude API Docs+4Claude API Docs+4](https://docs.anthropic.com/en/docs/claude-code/skills)
*   **Claude-subagents**: [Claude API Docs+2Claude+2](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
*   **GitHub-Copilot-and-VS-Code-agent-instructions**: [GitHub Docs+2GitHub Docs+2](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
*   **GitHub-Copilot-and-VS-Code-custom-agents**: [GitHub Docs+1](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/create-custom-agents)
*   **Pi-and-OpenClaw-skill-compatibility**: [GitHub+2OpenClaw+2](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md)

Ambiguity: 0.16  
Primary uncertainty remains Pi custom-agent manifests and Cursor-specific rule schema from official primary docs.

---

**Sources:**

- [GitHub - daviholandas/RiseOn.Agents · GitHub](https://github.com/daviholandas/RiseOn.Agents)
- [Custom instructions with AGENTS.md – Codex | OpenAI Developers](https://developers.openai.com/codex/guides/agents-md)
- [Provide context with GEMINI.md files | Gemini CLI](https://geminicli.com/docs/cli/gemini-md/)
- [Context Files | Hermes Agent](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files/)
- [How Claude remembers your project - Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Adding repository custom instructions for GitHub Copilot - GitHub Docs](https://docs.github.com/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)