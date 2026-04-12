"""Generator for subagent .md files.

Implements T051: User Story 5 - Generate subagent .md files.
"""

from pathlib import Path

from riseon_agents.models.agent import Subagent
from riseon_agents.models.generation import FileStatus, GenerationResult


class SubagentsGenerator:
    """Generator for subagent .md files.

    Creates individual .md files for each subagent in the .kilo/agents/ directory.
    """

    def generate(self, subagents: list[Subagent], target_dir: Path) -> GenerationResult:
        """Generate .md files for the given subagents.

        Args:
            subagents: List of Subagent objects to generate files for.
            target_dir: Target directory for output.

        Returns:
            GenerationResult with the generated files.
        """
        result = GenerationResult()

        if not subagents:
            result.add_file(
                path=target_dir / "agents",
                status=FileStatus.ERROR,
                error_message="No subagents selected for generation",
            )
            return result

        # Create agents subdirectory
        agents_dir = target_dir / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)

        for subagent in subagents:
            try:
                self._generate_subagent_file(subagent, agents_dir, result)
            except Exception as e:
                result.add_file(
                    path=agents_dir / f"{subagent.slug}.md",
                    status=FileStatus.ERROR,
                    error_message=f"Failed to generate {subagent.name}: {e}",
                )

        return result

    def _generate_subagent_file(
        self, subagent: Subagent, agents_dir: Path, result: GenerationResult
    ) -> None:
        """Generate a single subagent .md file.

        Args:
            subagent: Subagent to generate file for.
            agents_dir: Directory to write file to.
            result: GenerationResult to add file to.
        """
        # Generate content
        content = self._generate_content(subagent)

        # Write to file
        output_path = agents_dir / f"{subagent.slug}.md"
        existed = output_path.exists()
        output_path.write_text(content, encoding="utf-8")

        # Add to result
        result.add_file(
            path=output_path,
            status=FileStatus.UPDATED if existed else FileStatus.CREATED,
            existed_before=existed,
        )

    def _generate_content(self, subagent: Subagent) -> str:
        """Generate the content for a subagent .md file.

        Args:
            subagent: Subagent to generate content for.

        Returns:
            Content as string.
        """
        lines = [
            "---",
            "# RiseOn.Agents Generated Subagent",
            f"# Source: {subagent.parent_agent}/subagents/{subagent.slug}.agent.md",
            f"description: {subagent.description}",
            "mode: subagent",
            f"temperature: {subagent.temperature}",
            "permission:",
        ]

        # Add permissions
        if subagent.permissions:
            for perm_name, perm_level in subagent.permissions.items():
                lines.append(f"  {perm_name}: {perm_level.value}")
        else:
            # Default permissions
            lines.append("  edit: ask")
            lines.append("  bash: deny")

        lines.append("---")
        lines.append("")

        # Add markdown body
        lines.append(subagent.markdown_body)

        return "\n".join(lines)
