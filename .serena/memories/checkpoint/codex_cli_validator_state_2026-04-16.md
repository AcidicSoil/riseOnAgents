# Checkpoint: Codex CLI + validator state (2026-04-16)

## What was completed
- Added provider-native CLI generation in `src/riseon_agents/__main__.py`.
- `python -m riseon_agents --target codex` now generates Codex artifacts from canonical `agents/`.
- CLI supports repeated/comma-separated `--target`, `--agents-dir`, `--output-dir`, `--global-output`, and `--list-targets`.
- No-target behavior still launches the TUI.

## Project instruction aggregation
- Added repo-wide project instruction aggregation in `src/riseon_agents/models/project_instructions.py` via `ProjectInstructions.from_primary_agents(...)`.
- `AgentRepository.get_project_instructions()` now returns a single aggregated instruction surface instead of one per primary agent.
- This prevents multiple primary agents from racing to overwrite one provider instruction file like `AGENTS.md`.

## Multi-target compatibility generation
- `CompatibilityGenerator` in `src/riseon_agents/generation/compatibility.py` was updated to dedupe emitted artifacts by `(surface, path)`.
- Root cause fixed: shared skill paths such as `.agents/skills/.../SKILL.md` were being reported twice when multiple providers shared the same output path.
- Regression test was added in `tests/test_generation/test_compatibility.py`.

## Codex validator-driven fix
- User asked to run `scripts/validate-codex-agent.py` against generated Codex TOML and fix root causes of malformations.
- Validator initially failed on generated `.codex/agents/*.toml` because legacy generic permissions were being emitted as flat string values under `[permissions]`, e.g. `permissions.edit = "allow"`, which the validator rejects.
- Root cause: `_render_codex_agent_toml(...)` in `src/riseon_agents/generation/provider_emitters.py` serialized generic `AgentProfile.permissions` and `AgentProfile.mcp_servers` as if Codex accepted those legacy shapes.

## Codex emitter changes
- Tightened `_render_codex_agent_toml(...)` so it emits only Codex-compatible fields by default.
- It no longer serializes incompatible legacy generic shapes like:
  - flat `[permissions]` with string values
  - string-array `mcp_servers`
  - generic `tools`, `max_turns`, `temperature` for Codex manifests unless deliberately modeled later
- Added provider-native TOML helpers in `provider_emitters.py`:
  - `_toml_bool(...)`
  - `_toml_value(...)`
  - `_append_toml_mapping(...)`
- Added structured provider-specific support through `AgentProfile.provider_extensions`.
- Updated `src/riseon_agents/models/agent_profile.py` so `provider_extensions` is typed as `dict[str, Any]` instead of `dict[str, str]`.
- Codex-native structured fields can now be passed via `provider_extensions` for things like:
  - `approval_policy`
  - `approvals_reviewer`
  - `default_permissions`
  - `permissions`
  - `mcp_servers`
  - `sandbox_workspace_write`
  - `features`
  - etc.

## Validator result after fix
- Freshly generated Codex manifests now pass:
  - `uv run scripts/validate-codex-agent.py <generated/.codex/agents>`
  - `uv run scripts/validate-codex-agent.py --strict-keys <generated/.codex/agents>`
- Both normal and strict validation returned 0 errors and 0 warnings.

## Tests added/updated
- New file: `tests/test_cli.py`
  - target parsing
  - Codex CLI generation
  - target listing
- Updated `tests/test_parsing/test_repository.py`
  - asserts single aggregated project instruction surface
  - added multi-primary-agent aggregation case
- Updated `tests/test_generation/test_compatibility.py`
  - Codex compatibility expectations now reflect validator-compatible TOML
  - includes dedupe regression test for shared skill outputs
- Updated `tests/test_generation/test_provider_emitters.py`
  - Codex emitter expectations now reflect validator-compatible TOML and use `provider_extensions`

## Current repo validation state at checkpoint
- `uv run ruff check src tests` ✅
- `uv run black --check src tests` ✅
- `uv run mypy src/riseon_agents` ✅
- `uv run python -m pytest tests/ -q` ✅
- Full suite status at checkpoint: `191 passed`

## Most relevant changed files
- `src/riseon_agents/__main__.py`
- `src/riseon_agents/generation/compatibility.py`
- `src/riseon_agents/generation/provider_emitters.py`
- `src/riseon_agents/models/agent_profile.py`
- `src/riseon_agents/models/project_instructions.py`
- `src/riseon_agents/parsing/repository.py`
- `tests/test_cli.py`
- `tests/test_generation/test_compatibility.py`
- `tests/test_generation/test_provider_emitters.py`
- `tests/test_parsing/test_repository.py`

## Recommended next step
- Implement a first-class provider-native validation layer in the app/generation flow (not just the external script), starting with Codex.
- After that, extend the same CLI/dev-workflow polish to Claude/Copilot/Hermes and define provider-tailored composition rather than generic aggregation where needed.
