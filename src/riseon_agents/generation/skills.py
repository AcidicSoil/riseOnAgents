"""Generator for skill files.

Creates skill directories with SKILL.md in .kilocode/skills/ directory.
"""

from datetime import UTC, datetime
from pathlib import Path

from riseon_agents.models.generation import FileStatus, GenerationResult
from riseon_agents.models.skill import Skill


class SkillsGenerator:
    """Generator for skill files.

    Creates skill directories with SKILL.md in .kilocode/skills/ directory.
    """

    def generate(self, skills: list[Skill], target_dir: Path) -> GenerationResult:
        """Generate skill files for the given skills.

        Args:
            skills: List of Skill objects to generate files for.
            target_dir: Target directory for output.

        Returns:
            GenerationResult with the generated files.
        """
        result = GenerationResult()

        if not skills:
            result.add_file(
                path=target_dir / "skills",
                status=FileStatus.ERROR,
                error_message="No skills selected for generation",
            )
            return result

        skills_dir = target_dir / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)

        for skill in skills:
            try:
                self._generate_skill_files(skill, skills_dir, result)
            except Exception as e:
                result.add_file(
                    path=skills_dir / skill.name / "SKILL.md",
                    status=FileStatus.ERROR,
                    error_message=f"Failed to generate {skill.name}: {e}",
                )

        return result

    def _generate_skill_files(
        self, skill: Skill, skills_dir: Path, result: GenerationResult
    ) -> None:
        """Generate files for a single skill.

        Args:
            skill: Skill to generate files for.
            skills_dir: Base skills directory.
            result: GenerationResult to add files to.
        """
        skill_dir = skills_dir / skill.name
        skill_dir.mkdir(parents=True, exist_ok=True)

        content = self._generate_skill_content(skill)
        skill_path = skill_dir / "SKILL.md"
        existed = skill_path.exists()
        skill_path.write_text(content, encoding="utf-8")

        result.add_file(
            path=skill_path,
            status=FileStatus.UPDATED if existed else FileStatus.CREATED,
            existed_before=existed,
        )

        if skill.source_dir and skill.source_dir.exists():
            if skill.has_scripts:
                scripts_src = skill.source_dir / "scripts"
                if scripts_src.exists():
                    scripts_dst = skill_dir / "scripts"
                    self._copy_directory(scripts_src, scripts_dst)
                    result.add_file(path=scripts_dst, status=FileStatus.CREATED)

            if skill.has_references:
                refs_src = skill.source_dir / "references"
                if refs_src.exists():
                    refs_dst = skill_dir / "references"
                    self._copy_directory(refs_src, refs_dst)
                    result.add_file(path=refs_dst, status=FileStatus.CREATED)

            if skill.has_assets:
                assets_src = skill.source_dir / "assets"
                if assets_src.exists():
                    assets_dst = skill_dir / "assets"
                    self._copy_directory(assets_src, assets_dst)
                    result.add_file(path=assets_dst, status=FileStatus.CREATED)

    def _generate_skill_content(self, skill: Skill) -> str:
        """Generate the content for SKILL.md with added metadata.

        Args:
            skill: Skill to generate content for.

        Returns:
            Content as string.
        """
        lines: list[str] = []
        generated_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")

        if skill.content.startswith("---"):
            parts = skill.content.split("---", 2)
            if len(parts) >= 2:
                lines.append("---")
                lines.append(parts[1].strip())
                lines.append("metadata:")
                lines.append("  source: riseon-agents")
                lines.append(f"  generated: {generated_at}")
                lines.append("---")
                if len(parts) >= 3:
                    lines.append(parts[2].strip())
        else:
            lines.append("---")
            lines.append(f"name: {skill.name}")
            lines.append(f"description: {skill.description}")
            if skill.license:
                lines.append(f"license: {skill.license}")
            lines.append("metadata:")
            lines.append("  source: riseon-agents")
            lines.append(f"  generated: {generated_at}")
            lines.append("---")
            lines.append("")
            lines.append(skill.content)

        return "\n".join(lines)

    def _copy_directory(self, src: Path, dst: Path) -> None:
        """Copy a directory recursively.

        Args:
            src: Source directory.
            dst: Destination directory.
        """
        import shutil

        if src.exists():
            shutil.copytree(src, dst, dirs_exist_ok=True)
