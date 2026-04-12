"""Generator for rule files.

Implements T052: User Story 5 - Generate rule files.
"""

from pathlib import Path

from riseon_agents.models.generation import FileStatus, GenerationResult
from riseon_agents.models.rule import Rule


class RulesGenerator:
    """Generator for rule files.

    Creates rule files in .kilo/rules/ (shared) or .kilo/rules-{mode}/ (mode-specific).
    """

    def generate(self, rules: list[Rule], target_dir: Path) -> GenerationResult:
        """Generate rule files for the given rules.

        Args:
            rules: List of Rule objects to generate files for.
            target_dir: Target directory for output.

        Returns:
            GenerationResult with the generated files.
        """
        result = GenerationResult()

        if not rules:
            result.add_file(
                path=target_dir / "rules",
                status=FileStatus.ERROR,
                error_message="No rules selected for generation",
            )
            return result

        for rule in rules:
            try:
                self._generate_rule_file(rule, target_dir, result)
            except Exception as e:
                result.add_file(
                    path=target_dir / f"{rule.name}.md",
                    status=FileStatus.ERROR,
                    error_message=f"Failed to generate {rule.name}: {e}",
                )

        return result

    def _generate_rule_file(self, rule: Rule, target_dir: Path, result: GenerationResult) -> None:
        """Generate a single rule file.

        Args:
            rule: Rule to generate file for.
            target_dir: Base target directory.
            result: GenerationResult to add file to.
        """
        # Determine target directory based on shared vs mode-specific
        if rule.is_shared:
            rules_dir = target_dir / "rules"
        else:
            mode_slug = rule.mode_slug or "default"
            rules_dir = target_dir / f"rules-{mode_slug}"

        # Create directory if needed
        rules_dir.mkdir(parents=True, exist_ok=True)

        # Write to file
        output_path = rules_dir / f"{rule.filename}"
        existed = output_path.exists()
        output_path.write_text(rule.content, encoding="utf-8")

        # Add to result
        result.add_file(
            path=output_path,
            status=FileStatus.UPDATED if existed else FileStatus.CREATED,
            existed_before=existed,
        )
