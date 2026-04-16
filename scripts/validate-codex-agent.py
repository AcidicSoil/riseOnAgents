#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


REASONING_EFFORTS = {"minimal", "low", "medium", "high", "xhigh"}
SANDBOX_MODES = {"read-only", "workspace-write", "danger-full-access"}
APPROVAL_POLICIES = {"untrusted", "on-request", "never"}
APPROVAL_REVIEWERS = {"user", "guardian_subagent"}
NETWORK_MODES = {"limited", "full"}
DOMAIN_RULE_VALUES = {"allow", "deny"}
UNIX_SOCKET_RULE_VALUES = {"allow", "none"}
NICKNAME_RE = re.compile(r"^[A-Za-z0-9 _-]+$")
MALFORMED_AGENT_LINE_RE = re.compile(r"Ignoring malformed agent role definition:", re.IGNORECASE)

KNOWN_TOP_LEVEL_KEYS = {
    "name",
    "description",
    "developer_instructions",
    "nickname_candidates",
    "model",
    "model_reasoning_effort",
    "sandbox_mode",
    "sandbox_workspace_write",
    "mcp_servers",
    "skills",
    "approval_policy",
    "approvals_reviewer",
    "default_permissions",
    "permissions",
    "features",
    "allow_login_shell",
    "web_search",
}

GRANULAR_APPROVAL_KEYS = {
    "sandbox_approval",
    "rules",
    "mcp_elicitations",
    "request_permissions",
    "skill_approval",
}


@dataclass(slots=True)
class Issue:
    level: str
    code: str
    path: str
    message: str


@dataclass(slots=True)
class ValidationResult:
    path: Path
    issues: list[Issue]
    agent_name: str | None


def add_issue(
    issues: list[Issue],
    level: str,
    code: str,
    path: Path | str,
    message: str,
) -> None:
    issues.append(Issue(level=level, code=code, path=str(path), message=message))


def iter_candidate_files(paths: list[str]) -> list[Path]:
    candidates: list[Path] = []
    seen: set[Path] = set()

    input_paths = [Path(p).expanduser() for p in paths] if paths else [Path(".codex/agents")]

    for path in input_paths:
        if not path.exists():
            candidates.append(path)
            continue

        if path.is_file():
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                candidates.append(path)
            continue

        for file_path in sorted(path.rglob("*.toml")):
            resolved = file_path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                candidates.append(file_path)

    return candidates


def validate_string_field(
    data: dict[str, Any],
    field: str,
    file_path: Path,
    issues: list[Issue],
) -> None:
    value = data.get(field)
    if value is None:
        add_issue(issues, "error", "missing-required-field", file_path, f"missing required field `{field}`")
        return
    if not isinstance(value, str):
        add_issue(issues, "error", "invalid-type", file_path, f"`{field}` must be a string")
        return
    if not value.strip():
        add_issue(issues, "error", "empty-string", file_path, f"`{field}` must be non-empty")


def validate_nickname_candidates(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    if "nickname_candidates" not in data:
        return

    value = data["nickname_candidates"]
    if not isinstance(value, list):
        add_issue(issues, "error", "invalid-type", file_path, "`nickname_candidates` must be an array of strings")
        return
    if not value:
        add_issue(issues, "error", "empty-array", file_path, "`nickname_candidates` must be a non-empty array when provided")
        return

    seen: set[str] = set()
    for idx, item in enumerate(value):
        if not isinstance(item, str):
            add_issue(issues, "error", "invalid-type", file_path, f"`nickname_candidates[{idx}]` must be a string")
            continue
        if not item.strip():
            add_issue(issues, "error", "empty-string", file_path, f"`nickname_candidates[{idx}]` must be non-empty")
            continue
        if item in seen:
            add_issue(issues, "error", "duplicate-nickname", file_path, f"`nickname_candidates` contains duplicate value `{item}`")
        seen.add(item)
        if not NICKNAME_RE.fullmatch(item):
            add_issue(
                issues,
                "error",
                "invalid-nickname",
                file_path,
                f"`nickname_candidates[{idx}]` contains unsupported characters: `{item}`",
            )


def validate_reasoning_effort(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    if "model_reasoning_effort" not in data:
        return

    value = data["model_reasoning_effort"]
    if not isinstance(value, str):
        add_issue(issues, "error", "invalid-type", file_path, "`model_reasoning_effort` must be a string")
        return
    if value not in REASONING_EFFORTS:
        add_issue(
            issues,
            "error",
            "invalid-enum",
            file_path,
            "`model_reasoning_effort` must be one of: minimal, low, medium, high, xhigh",
        )


def validate_sandbox(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    sandbox_mode = data.get("sandbox_mode")
    if sandbox_mode is not None:
        if not isinstance(sandbox_mode, str):
            add_issue(issues, "error", "invalid-type", file_path, "`sandbox_mode` must be a string")
        elif sandbox_mode not in SANDBOX_MODES:
            add_issue(
                issues,
                "error",
                "invalid-enum",
                file_path,
                "`sandbox_mode` must be one of: read-only, workspace-write, danger-full-access",
            )

    workspace_cfg = data.get("sandbox_workspace_write")
    if workspace_cfg is None:
        return

    if not isinstance(workspace_cfg, dict):
        add_issue(issues, "error", "invalid-type", file_path, "`sandbox_workspace_write` must be a table")
        return

    if sandbox_mode != "workspace-write":
        add_issue(
            issues,
            "warning",
            "unused-workspace-write-config",
            file_path,
            "`sandbox_workspace_write` is set but `sandbox_mode` is not `workspace-write`",
        )

    for key, value in workspace_cfg.items():
        if key in {"exclude_slash_tmp", "exclude_tmpdir_env_var", "network_access"}:
            if not isinstance(value, bool):
                add_issue(issues, "error", "invalid-type", file_path, f"`sandbox_workspace_write.{key}` must be a boolean")
        elif key == "writable_roots":
            if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                add_issue(
                    issues,
                    "error",
                    "invalid-type",
                    file_path,
                    "`sandbox_workspace_write.writable_roots` must be an array of non-empty strings",
                )
        else:
            add_issue(
                issues,
                "warning",
                "unknown-workspace-write-key",
                file_path,
                f"unknown key under `sandbox_workspace_write`: `{key}`",
            )


def validate_mcp_servers(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    if "mcp_servers" not in data:
        return

    value = data["mcp_servers"]
    if not isinstance(value, dict):
        add_issue(issues, "error", "invalid-type", file_path, "`mcp_servers` must be a table")
        return

    for server_name, server_cfg in value.items():
        if not isinstance(server_cfg, dict):
            add_issue(issues, "error", "invalid-type", file_path, f"`mcp_servers.{server_name}` must be a table")
            continue
        if "url" in server_cfg and not isinstance(server_cfg["url"], str):
            add_issue(issues, "error", "invalid-type", file_path, f"`mcp_servers.{server_name}.url` must be a string")
        if "enabled" in server_cfg and not isinstance(server_cfg["enabled"], bool):
            add_issue(issues, "error", "invalid-type", file_path, f"`mcp_servers.{server_name}.enabled` must be a boolean")
        if "startup_timeout_sec" in server_cfg and not isinstance(server_cfg["startup_timeout_sec"], int):
            add_issue(
                issues,
                "error",
                "invalid-type",
                file_path,
                f"`mcp_servers.{server_name}.startup_timeout_sec` must be an integer",
            )


def validate_skills(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    if "skills" not in data:
        return

    value = data["skills"]
    if not isinstance(value, dict):
        add_issue(issues, "error", "invalid-type", file_path, "`skills` must be a table")
        return

    config_entries = value.get("config")
    if config_entries is None:
        add_issue(issues, "warning", "missing-skills-config", file_path, "`skills` is present without `[[skills.config]]` entries")
        return
    if not isinstance(config_entries, list):
        add_issue(issues, "error", "invalid-type", file_path, "`skills.config` must be an array of tables")
        return

    for idx, entry in enumerate(config_entries):
        if not isinstance(entry, dict):
            add_issue(issues, "error", "invalid-type", file_path, f"`skills.config[{idx}]` must be a table")
            continue
        path_value = entry.get("path")
        if not isinstance(path_value, str) or not path_value.strip():
            add_issue(issues, "error", "missing-required-field", file_path, f"`skills.config[{idx}].path` must be a non-empty string")
        if "enabled" in entry and not isinstance(entry["enabled"], bool):
            add_issue(issues, "error", "invalid-type", file_path, f"`skills.config[{idx}].enabled` must be a boolean")
        for key in entry:
            if key not in {"path", "enabled"}:
                add_issue(
                    issues,
                    "warning",
                    "unknown-skills-config-key",
                    file_path,
                    f"unknown key under `skills.config[{idx}]`: `{key}`",
                )


def validate_approval_policy(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    if "approval_policy" not in data:
        return

    value = data["approval_policy"]
    if isinstance(value, str):
        if value not in APPROVAL_POLICIES:
            add_issue(
                issues,
                "error",
                "invalid-enum",
                file_path,
                "`approval_policy` must be one of: untrusted, on-request, never, or a granular table",
            )
        return

    if not isinstance(value, dict):
        add_issue(issues, "error", "invalid-type", file_path, "`approval_policy` must be a string or a table")
        return

    if set(value.keys()) != {"granular"}:
        add_issue(
            issues,
            "error",
            "invalid-approval-policy-shape",
            file_path,
            "`approval_policy` table must use exactly `{ granular = { ... } }`",
        )
        return

    granular = value["granular"]
    if not isinstance(granular, dict):
        add_issue(issues, "error", "invalid-type", file_path, "`approval_policy.granular` must be a table")
        return

    for key, subvalue in granular.items():
        if key not in GRANULAR_APPROVAL_KEYS:
            add_issue(
                issues,
                "error",
                "unknown-granular-approval-key",
                file_path,
                f"unknown key under `approval_policy.granular`: `{key}`",
            )
            continue
        if not isinstance(subvalue, bool):
            add_issue(
                issues,
                "error",
                "invalid-type",
                file_path,
                f"`approval_policy.granular.{key}` must be a boolean",
            )

    missing = sorted(GRANULAR_APPROVAL_KEYS - set(granular.keys()))
    if missing:
        add_issue(
            issues,
            "warning",
            "partial-granular-approval-policy",
            file_path,
            f"`approval_policy.granular` is missing documented keys: {', '.join(missing)}",
        )


def validate_approvals_reviewer(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    if "approvals_reviewer" not in data:
        return

    value = data["approvals_reviewer"]
    if not isinstance(value, str):
        add_issue(issues, "error", "invalid-type", file_path, "`approvals_reviewer` must be a string")
        return
    if value not in APPROVAL_REVIEWERS:
        add_issue(
            issues,
            "error",
            "invalid-enum",
            file_path,
            "`approvals_reviewer` must be one of: user, guardian_subagent",
        )


def validate_default_permissions(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    if "default_permissions" not in data:
        return

    value = data["default_permissions"]
    if not isinstance(value, str):
        add_issue(issues, "error", "invalid-type", file_path, "`default_permissions` must be a string profile name")
        return
    if not value.strip():
        add_issue(issues, "error", "empty-string", file_path, "`default_permissions` must be non-empty")
        return

    permissions = data.get("permissions")
    if isinstance(permissions, dict) and value not in permissions:
        add_issue(
            issues,
            "warning",
            "undefined-default-permissions-profile",
            file_path,
            f"`default_permissions = \"{value}\"` but no matching `[permissions.{value}]` profile exists in this file",
        )


def validate_permissions_table(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    if "permissions" not in data:
        return

    permissions = data["permissions"]
    if not isinstance(permissions, dict):
        add_issue(
            issues,
            "error",
            "invalid-type",
            file_path,
            "`permissions` must be a table of named permission profiles, not a string or scalar",
        )
        return

    if not permissions:
        add_issue(issues, "warning", "empty-permissions-table", file_path, "`permissions` is present but empty")
        return

    for profile_name, profile_value in permissions.items():
        profile_path = f"{file_path} :: permissions.{profile_name}"
        if not isinstance(profile_value, dict):
            add_issue(
                issues,
                "error",
                "invalid-type",
                profile_path,
                f"`permissions.{profile_name}` must be a table, not `{type(profile_value).__name__}`",
            )
            continue

        network_cfg = profile_value.get("network")
        if network_cfg is None:
            continue

        if not isinstance(network_cfg, dict):
            add_issue(
                issues,
                "error",
                "invalid-type",
                profile_path,
                f"`permissions.{profile_name}.network` must be a table",
            )
            continue

        for key, value in network_cfg.items():
            dotted = f"`permissions.{profile_name}.network.{key}`"
            if key in {
                "enabled",
                "enable_socks5",
                "enable_socks5_udp",
                "allow_local_binding",
                "allow_upstream_proxy",
                "dangerously_allow_all_unix_sockets",
                "dangerously_allow_non_loopback_proxy",
            }:
                if not isinstance(value, bool):
                    add_issue(issues, "error", "invalid-type", profile_path, f"{dotted} must be a boolean")
            elif key == "mode":
                if not isinstance(value, str) or value not in NETWORK_MODES:
                    add_issue(issues, "error", "invalid-enum", profile_path, f"{dotted} must be one of: limited, full")
            elif key in {"proxy_url", "socks_url"}:
                if not isinstance(value, str) or not value.strip():
                    add_issue(issues, "error", "invalid-type", profile_path, f"{dotted} must be a non-empty string")
            elif key == "domains":
                if not isinstance(value, dict):
                    add_issue(issues, "error", "invalid-type", profile_path, f"{dotted} must be a table")
                    continue
                for domain_key, domain_value in value.items():
                    if not isinstance(domain_key, str) or not domain_key.strip():
                        add_issue(issues, "error", "invalid-type", profile_path, f"{dotted} keys must be non-empty strings")
                    if domain_value not in DOMAIN_RULE_VALUES:
                        add_issue(
                            issues,
                            "error",
                            "invalid-enum",
                            profile_path,
                            f"{dotted}[{domain_key!r}] must be `allow` or `deny`",
                        )
            elif key == "unix_sockets":
                if not isinstance(value, dict):
                    add_issue(issues, "error", "invalid-type", profile_path, f"{dotted} must be a table")
                    continue
                for socket_key, socket_value in value.items():
                    if not isinstance(socket_key, str) or not socket_key.strip():
                        add_issue(issues, "error", "invalid-type", profile_path, f"{dotted} keys must be non-empty strings")
                    if socket_value not in UNIX_SOCKET_RULE_VALUES:
                        add_issue(
                            issues,
                            "error",
                            "invalid-enum",
                            profile_path,
                            f"{dotted}[{socket_key!r}] must be `allow` or `none`",
                        )
            else:
                add_issue(
                    issues,
                    "warning",
                    "unknown-permissions-network-key",
                    profile_path,
                    f"unknown key under `permissions.{profile_name}.network`: `{key}`",
                )


def validate_filename_matches_name(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
) -> None:
    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        return

    normalized_file = re.sub(r"[^a-z0-9]", "", file_path.stem.lower())
    normalized_name = re.sub(r"[^a-z0-9]", "", name.lower())
    if normalized_file != normalized_name:
        add_issue(
            issues,
            "warning",
            "filename-name-mismatch",
            file_path,
            f"filename `{file_path.name}` does not roughly match agent name `{name}`; `name` is the source of truth",
        )


def validate_top_level_keys(
    data: dict[str, Any],
    file_path: Path,
    issues: list[Issue],
    strict_keys: bool,
) -> None:
    if not strict_keys:
        return

    for key in sorted(data):
        if key not in KNOWN_TOP_LEVEL_KEYS:
            add_issue(
                issues,
                "warning",
                "unknown-top-level-key",
                file_path,
                f"unknown top-level key `{key}` under best-effort custom-agent validation",
            )


def load_toml_file(file_path: Path, issues: list[Issue]) -> dict[str, Any] | None:
    if not file_path.exists():
        add_issue(issues, "error", "missing-file", file_path, "path does not exist")
        return None
    if not file_path.is_file():
        add_issue(issues, "error", "not-a-file", file_path, "path is not a file")
        return None
    if file_path.suffix != ".toml":
        add_issue(issues, "error", "wrong-extension", file_path, "expected a `.toml` file")
        return None

    try:
        raw = file_path.read_bytes()
    except OSError as exc:
        add_issue(issues, "error", "read-failed", file_path, f"failed to read file: {exc}")
        return None

    try:
        data = tomllib.loads(raw.decode("utf-8"))
    except UnicodeDecodeError as exc:
        add_issue(issues, "error", "decode-failed", file_path, f"file is not valid UTF-8: {exc}")
        return None
    except tomllib.TOMLDecodeError as exc:
        add_issue(issues, "error", "toml-parse-failed", file_path, f"invalid TOML: {exc}")
        return None

    if not isinstance(data, dict):
        add_issue(issues, "error", "invalid-root", file_path, "top-level TOML document must be a table")
        return None

    return data


def validate_agent_file(file_path: Path, strict_keys: bool) -> ValidationResult:
    issues: list[Issue] = []
    data = load_toml_file(file_path, issues)
    if data is None:
        return ValidationResult(path=file_path, issues=issues, agent_name=None)

    for field in ("name", "description", "developer_instructions"):
        validate_string_field(data, field, file_path, issues)

    validate_nickname_candidates(data, file_path, issues)
    validate_reasoning_effort(data, file_path, issues)
    validate_sandbox(data, file_path, issues)
    validate_mcp_servers(data, file_path, issues)
    validate_skills(data, file_path, issues)
    validate_approval_policy(data, file_path, issues)
    validate_approvals_reviewer(data, file_path, issues)
    validate_default_permissions(data, file_path, issues)
    validate_permissions_table(data, file_path, issues)
    validate_filename_matches_name(data, file_path, issues)
    validate_top_level_keys(data, file_path, issues, strict_keys)

    agent_name = data.get("name") if isinstance(data.get("name"), str) and data["name"].strip() else None
    return ValidationResult(path=file_path, issues=issues, agent_name=agent_name)


def validate_duplicate_agent_names(results: list[ValidationResult]) -> list[Issue]:
    issues: list[Issue] = []
    by_name: dict[str, list[Path]] = {}

    for result in results:
        if result.agent_name is None:
            continue
        by_name.setdefault(result.agent_name, []).append(result.path)

    for name, paths in sorted(by_name.items()):
        if len(paths) < 2:
            continue
        joined = ", ".join(str(path) for path in paths)
        for path in paths:
            add_issue(
                issues,
                "error",
                "duplicate-agent-name",
                path,
                f"agent name `{name}` appears in multiple files: {joined}",
            )

    return issues


def infer_live_root(paths: list[str]) -> Path | None:
    candidates = [Path(p).expanduser() for p in paths] if paths else [Path(".codex/agents")]

    for original in candidates:
        probe = original.resolve() if original.exists() else original
        for current in [probe, *probe.parents]:
            if current.name == ".codex":
                return current.parent
            maybe = current / ".codex"
            if maybe.is_dir():
                return current
    return None


def run_live_codex_check(
    codex_bin: str,
    root: Path,
    timeout_sec: int,
) -> list[Issue]:
    issues: list[Issue] = []

    if shutil.which(codex_bin) is None:
        add_issue(
            issues,
            "warning",
            "codex-not-found",
            root,
            f"`{codex_bin}` not found on PATH; skipped live Codex loader check",
        )
        return issues

    cmd = [
        codex_bin,
        "exec",
        "--sandbox",
        "read-only",
        "--ask-for-approval",
        "never",
        "Reply with OK and nothing else.",
    ]

    try:
        proc = subprocess.run(
            cmd,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout_sec,
            check=False,
        )
    except subprocess.TimeoutExpired:
        add_issue(
            issues,
            "warning",
            "live-codex-timeout",
            root,
            f"live Codex loader check timed out after {timeout_sec}s",
        )
        return issues
    except OSError as exc:
        add_issue(
            issues,
            "warning",
            "live-codex-launch-failed",
            root,
            f"failed to launch `{codex_bin}`: {exc}",
        )
        return issues

    combined_output = "\n".join(
        chunk for chunk in (proc.stdout, proc.stderr) if chunk
    )

    malformed_lines = [
        line.strip()
        for line in combined_output.splitlines()
        if MALFORMED_AGENT_LINE_RE.search(line)
    ]
    for line in malformed_lines:
        add_issue(
            issues,
            "error",
            "codex-loader-rejected-agent",
            root,
            line,
        )

    if not malformed_lines and proc.returncode != 0:
        add_issue(
            issues,
            "warning",
            "live-codex-nonzero-exit",
            root,
            f"`{' '.join(cmd)}` exited with code {proc.returncode}; no malformed-agent lines were detected",
        )

    return issues


def summarize(issues: list[Issue], checked_files: Iterable[Path]) -> dict[str, Any]:
    checked = [str(path) for path in checked_files]
    errors = sum(1 for issue in issues if issue.level == "error")
    warnings = sum(1 for issue in issues if issue.level == "warning")
    return {
        "ok": errors == 0,
        "checked_files": checked,
        "error_count": errors,
        "warning_count": warnings,
        "issues": [asdict(issue) for issue in issues],
    }


def print_human(summary: dict[str, Any]) -> None:
    print(f"checked files: {len(summary['checked_files'])}")
    print(f"errors: {summary['error_count']}")
    print(f"warnings: {summary['warning_count']}")
    print()

    if not summary["issues"]:
        print("all agent files passed validation")
        return

    for issue in summary["issues"]:
        print(f"[{issue['level'].upper()}] {issue['code']} :: {issue['path']}")
        print(f"  {issue['message']}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Codex custom agent TOML files under .codex/agents or explicit paths."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="files or directories to validate (defaults to .codex/agents)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit machine-readable JSON instead of human output",
    )
    parser.add_argument(
        "--strict-keys",
        action="store_true",
        help="warn on top-level keys outside the current best-effort allowlist",
    )
    parser.add_argument(
        "--fail-warn",
        action="store_true",
        help="return a non-zero exit code when warnings are present",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="also run a live `codex exec` loader smoke test from the inferred or provided repo root",
    )
    parser.add_argument(
        "--live-root",
        help="repo root to use for the live Codex loader check; defaults to inferred root",
    )
    parser.add_argument(
        "--codex-bin",
        default="codex",
        help="Codex executable to use for --live (default: codex)",
    )
    parser.add_argument(
        "--live-timeout-sec",
        type=int,
        default=60,
        help="timeout for the live Codex loader check in seconds (default: 60)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    files = iter_candidate_files(args.paths)

    if not files:
        summary = {
            "ok": False,
            "checked_files": [],
            "error_count": 1,
            "warning_count": 0,
            "issues": [
                {
                    "level": "error",
                    "code": "no-files-found",
                    "path": "",
                    "message": "no .toml files found to validate",
                }
            ],
        }
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print_human(summary)
        return 2

    results = [validate_agent_file(file_path, strict_keys=args.strict_keys) for file_path in files]
    issues: list[Issue] = []
    for result in results:
        issues.extend(result.issues)

    issues.extend(validate_duplicate_agent_names(results))

    if args.live:
        live_root = Path(args.live_root).expanduser() if args.live_root else infer_live_root(args.paths)
        if live_root is None:
            add_issue(
                issues,
                "warning",
                "live-root-not-found",
                "",
                "could not infer a repo root for --live; pass --live-root explicitly",
            )
        else:
            issues.extend(
                run_live_codex_check(
                    codex_bin=args.codex_bin,
                    root=live_root,
                    timeout_sec=args.live_timeout_sec,
                )
            )

    summary = summarize(issues, files)

    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_human(summary)

    if summary["error_count"] > 0:
        return 1
    if args.fail_warn and summary["warning_count"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))