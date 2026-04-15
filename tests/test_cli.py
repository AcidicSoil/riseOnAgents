from pathlib import Path

from riseon_agents.__main__ import main, parse_targets
from riseon_agents.generation.provider_capabilities import ProviderTarget


class TestCli:
    """Tests for provider-target CLI generation."""

    def test_parse_targets_supports_repeated_and_comma_separated_values(self) -> None:
        """CLI target parsing should deduplicate while preserving order."""
        targets = parse_targets(["codex,gemini", "codex", "kilo"])

        assert targets == [
            ProviderTarget.CODEX,
            ProviderTarget.GEMINI,
            ProviderTarget.KILO,
        ]

    def test_main_generates_codex_outputs(self, temp_agents_dir: Path, temp_dir: Path) -> None:
        """The CLI should generate Codex-native outputs from the canonical agents tree."""
        exit_code = main(
            [
                "--target",
                "codex",
                "--agents-dir",
                str(temp_agents_dir),
                "--output-dir",
                str(temp_dir),
            ]
        )

        assert exit_code == 0
        assert (temp_dir / "AGENTS.md").exists()
        assert (temp_dir / ".codex" / "agents" / "test-subagent-1.toml").exists()
        assert (temp_dir / ".codex" / "agents" / "test-subagent-2.toml").exists()
        assert (temp_dir / ".agents" / "skills" / "test-skill" / "SKILL.md").exists()

        agents_md = (temp_dir / "AGENTS.md").read_text(encoding="utf-8")
        assert "# Test Primary Agent" in agents_md

        codex_manifest = (temp_dir / ".codex" / "agents" / "test-subagent-1.toml").read_text(
            encoding="utf-8"
        )
        assert 'name = "test-subagent-1"' in codex_manifest
        assert 'developer_instructions = "# Test Subagent 1' in codex_manifest

    def test_main_lists_targets(self, capsys) -> None:
        """The CLI should print supported target names."""
        exit_code = main(["--list-targets"])

        assert exit_code == 0
        output = capsys.readouterr().out
        assert "codex" in output
        assert "gemini" in output
        assert "kilo" in output
