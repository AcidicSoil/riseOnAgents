"""CLI entrypoints for the RiseOn.Agents application.

Usage:
    python -m riseon_agents
    riseon-agents
    python -m riseon_agents --target codex
    python -m riseon_agents --target codex,gemini --agents-dir ./agents --output-dir .
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from riseon_agents.generation import CompatibilityGenerator, KiloCodeGenerator, ProviderTarget
from riseon_agents.models.generation import GenerationLevel, GenerationResult, GenerationTarget
from riseon_agents.parsing.repository import AgentRepository


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="riseon-agents",
        description="Generate provider-native AI agent configuration from the canonical agents/ tree.",
    )
    parser.add_argument(
        "--target",
        "-t",
        action="append",
        default=[],
        help=(
            "Generation target(s). Repeat the flag or pass a comma-separated list, "
            "for example '--target codex,gemini' or '--target codex --target kilo'."
        ),
    )
    parser.add_argument(
        "--agents-dir",
        default="agents",
        help="Path to the canonical agents directory. Defaults to ./agents.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Local output directory. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--global-output",
        action="store_true",
        help="Write output to the global user target instead of the local output directory.",
    )
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="Print the supported target names and exit.",
    )
    return parser


def parse_targets(raw_targets: list[str]) -> list[ProviderTarget]:
    """Parse repeated or comma-separated target arguments into provider targets."""
    parsed: list[ProviderTarget] = []
    seen: set[ProviderTarget] = set()

    for raw_target in raw_targets:
        for chunk in raw_target.split(","):
            normalized = chunk.strip().lower()
            if not normalized:
                continue
            target = ProviderTarget(normalized)
            if target not in seen:
                seen.add(target)
                parsed.append(target)

    return parsed


def _merge_generation_results(destination: GenerationResult, source: GenerationResult) -> None:
    """Merge generated file and validation details into a destination result."""
    destination.files.extend(source.files)
    destination.validation_results.extend(source.validation_results)
    if source.interrupted:
        destination.interrupted = True


def run_generation(
    targets: list[ProviderTarget],
    agents_dir: Path,
    output_dir: Path,
    global_output: bool,
) -> int:
    """Generate configuration for the selected provider targets."""
    repository = AgentRepository(agents_dir)
    load_result = repository.discover()

    for warning in load_result.warnings:
        print(f"warning: {warning.message}", file=sys.stderr)

    if not load_result.agents:
        print(f"No agents were discovered in {agents_dir}", file=sys.stderr)
        return 1

    level = GenerationLevel.GLOBAL if global_output else GenerationLevel.LOCAL
    target = (
        GenerationTarget.global_()
        if global_output
        else GenerationTarget.local(output_dir.resolve())
    )
    overall = GenerationResult(target=target)

    remaining_targets = list(targets)
    if ProviderTarget.KILO in remaining_targets:
        kilo_result = KiloCodeGenerator().generate(
            load_result.agents,
            level,
            output_dir.resolve(),
            overwrite=True,
        )
        _merge_generation_results(overall, kilo_result)
        remaining_targets = [
            provider for provider in remaining_targets if provider is not ProviderTarget.KILO
        ]

    if remaining_targets:
        compatibility_result = CompatibilityGenerator().generate(
            target=target,
            providers=remaining_targets,
            project_instructions=repository.get_project_instructions(),
            skills=repository.get_skill_specs(),
            agent_profiles=repository.get_agent_profiles(),
            identity_specs=repository.get_identity_specs(),
        )
        _merge_generation_results(overall, compatibility_result)

    print(overall.get_summary())
    for generated in overall.files:
        print(f"[{generated.status.value}] {generated.path}")
        if generated.error_message:
            print(f"  {generated.error_message}")

    return 0 if overall.success else 1


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the CLI application."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_targets:
        for target in ProviderTarget:
            print(target.value)
        return 0

    try:
        targets = parse_targets(args.target)
    except ValueError as exc:
        parser.error(str(exc))

    if targets:
        return run_generation(
            targets=targets,
            agents_dir=Path(args.agents_dir),
            output_dir=Path(args.output_dir),
            global_output=args.global_output,
        )

    from riseon_agents.app import KiloGeneratorApp

    app = KiloGeneratorApp()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
