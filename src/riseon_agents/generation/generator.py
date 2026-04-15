"""Main generator orchestrator.

Implements T054: User Story 5 - Create KiloCodeGenerator orchestrator.
Implements T073: User Story 4 - Use GenerationTarget for path resolution.
Implements T076, T077: User Story 6 - Validate YAML and Markdown files.
Implements T081, T082: User Story 9 - Permission errors and interruption handling.
"""

import os
from pathlib import Path

import yaml

from riseon_agents.generation.modes import ModesGenerator
from riseon_agents.generation.rules import RulesGenerator
from riseon_agents.generation.skills import SkillsGenerator
from riseon_agents.generation.subagents import SubagentsGenerator
from riseon_agents.models.agent import PrimaryAgent
from riseon_agents.models.generation import (
    FileStatus,
    GenerationLevel,
    GenerationResult,
    GenerationTarget,
    ValidationResult,
    ValidationStatus,
)


class KiloCodeGenerator:
    """Main orchestrator for generating Kilo Code configuration files.

    Coordinates the generation of all configuration files:
    - custom_modes.yaml (Primary Agents)
    - .kilo/agents/*.md (Subagents)
    - .kilo/rules/*.md (Shared rules)
    - .kilo/rules-{mode}/*.md (Mode-specific rules)
    - .kilocode/skills/{skill}/SKILL.md (Skills)
    """

    def __init__(self) -> None:
        """Initialize the generator with sub-generators."""
        self.modes_gen = ModesGenerator()
        self.subagents_gen = SubagentsGenerator()
        self.rules_gen = RulesGenerator()
        self.skills_gen = SkillsGenerator()

    def generate(
        self,
        agents: list[PrimaryAgent],
        level: GenerationLevel,
        base_dir: Path,
        overwrite: bool = False,
    ) -> GenerationResult:
        """Generate all configuration files for the selected agents.

        Args:
            agents: List of selected PrimaryAgent objects.
            level: Generation level (LOCAL or GLOBAL).
            base_dir: Base directory for generation (project root for LOCAL).
            overwrite: Whether to overwrite existing files.

        Returns:
            GenerationResult with all generated files and status.
        """
        result = GenerationResult()
        _ = overwrite  # Reserved for overwrite policy compatibility while generators overwrite in place.
        generated_files: list[Path] = []  # T082: Track for cleanup

        if not agents:
            result.add_file(
                path=base_dir / "custom_modes.yaml",
                status=FileStatus.ERROR,
                error_message="No agents selected for generation. Please select at least one agent.",
            )
            return result

        try:
            # T073: Use GenerationTarget for path resolution
            if level == GenerationLevel.LOCAL:
                target = GenerationTarget.local(base_dir)
            else:
                target = GenerationTarget.global_()

            # T081, T083: Create directories with permission checking
            try:
                target.ensure_directories()
            except PermissionError as e:
                result.add_file(
                    path=target.kilo_dir,
                    status=FileStatus.ERROR,
                    error_message=self._format_permission_error(e, target.kilo_dir),
                )
                return result
            except OSError as e:
                result.add_file(
                    path=target.kilo_dir,
                    status=FileStatus.ERROR,
                    error_message=f"Failed to create directories: {e}",
                )
                return result

            # Generate custom_modes.yaml
            try:
                modes_result = self.modes_gen.generate(agents, target.kilo_dir)
                result.files.extend(modes_result.files)
                # T082: Track successfully generated files for cleanup
                for file_info in modes_result.files:
                    if file_info.status in (FileStatus.CREATED, FileStatus.UPDATED):
                        generated_files.append(file_info.path)
            except PermissionError as e:
                result.add_file(
                    path=target.modes_file,
                    status=FileStatus.ERROR,
                    error_message=self._format_permission_error(e, target.modes_file),
                )
                return result
            except Exception as e:
                result.add_file(
                    path=target.modes_file,
                    status=FileStatus.ERROR,
                    error_message=f"Modes generation failed: {e}",
                )

            # Collect all subagents, rules, and skills from selected agents
            all_subagents = []
            all_rules = []
            all_skills = []

            for agent in agents:
                all_subagents.extend(agent.subagents)
                all_rules.extend(agent.rules)
                all_skills.extend(agent.skills)

            # Generate subagent files
            if all_subagents:
                try:
                    subagents_result = self.subagents_gen.generate(all_subagents, target.kilo_dir)
                    result.files.extend(subagents_result.files)
                    for file_info in subagents_result.files:
                        if file_info.status in (FileStatus.CREATED, FileStatus.UPDATED):
                            generated_files.append(file_info.path)
                except PermissionError as e:
                    result.add_file(
                        path=target.agents_dir,
                        status=FileStatus.ERROR,
                        error_message=self._format_permission_error(e, target.agents_dir),
                    )
                except Exception as e:
                    result.add_file(
                        path=target.agents_dir,
                        status=FileStatus.ERROR,
                        error_message=f"Subagents generation failed: {e}",
                    )

            # Generate rule files
            if all_rules:
                try:
                    rules_result = self.rules_gen.generate(all_rules, target.kilo_dir)
                    result.files.extend(rules_result.files)
                    for file_info in rules_result.files:
                        if file_info.status in (FileStatus.CREATED, FileStatus.UPDATED):
                            generated_files.append(file_info.path)
                except PermissionError as e:
                    result.add_file(
                        path=target.rules_dir,
                        status=FileStatus.ERROR,
                        error_message=self._format_permission_error(e, target.rules_dir),
                    )
                except Exception as e:
                    result.add_file(
                        path=target.rules_dir,
                        status=FileStatus.ERROR,
                        error_message=f"Rules generation failed: {e}",
                    )

            # Generate skill files
            if all_skills:
                try:
                    skills_result = self.skills_gen.generate(all_skills, target.kilocode_dir)
                    result.files.extend(skills_result.files)
                    for file_info in skills_result.files:
                        if file_info.status in (FileStatus.CREATED, FileStatus.UPDATED):
                            generated_files.append(file_info.path)
                except PermissionError as e:
                    result.add_file(
                        path=target.skills_dir,
                        status=FileStatus.ERROR,
                        error_message=self._format_permission_error(e, target.skills_dir),
                    )
                except Exception as e:
                    result.add_file(
                        path=target.skills_dir,
                        status=FileStatus.ERROR,
                        error_message=f"Skills generation failed: {e}",
                    )

            # Store target in result
            result.target = target

            # T076, T077: Validate generated files
            if result.success:
                self.validate_generation_result(result)

            return result

        except KeyboardInterrupt:
            # T082: Handle generation interruption - cleanup partial files
            self._cleanup_partial_files(generated_files)
            result.add_file(
                path=base_dir / "generation",
                status=FileStatus.ERROR,
                error_message="Generation interrupted. Partial files have been cleaned up.",
            )
            return result
        except Exception as e:
            result.add_file(
                path=base_dir / "generation",
                status=FileStatus.ERROR,
                error_message=f"Generation failed: {e}",
            )
            return result

    def check_existing_files(
        self,
        agents: list[PrimaryAgent],
        level: GenerationLevel,
        base_dir: Path,
    ) -> list[Path]:
        """Check for existing files that would be overwritten.

        Args:
            agents: List of selected PrimaryAgent objects.
            level: Generation level.
            base_dir: Base directory.

        Returns:
            List of existing file paths.
        """
        existing = []

        # T073: Use GenerationTarget for path resolution
        if level == GenerationLevel.LOCAL:
            target = GenerationTarget.local(base_dir)
        else:
            target = GenerationTarget.global_()

        # Check custom_modes.yaml
        if target.modes_file.exists():
            existing.append(target.modes_file)

        # Check agent files
        for agent in agents:
            # Subagent files
            for subagent in agent.subagents:
                subagent_file = target.agents_dir / f"{subagent.slug}.md"
                if subagent_file.exists():
                    existing.append(subagent_file)

            # Rule files
            for rule in agent.rules:
                if rule.is_shared:
                    rule_file = target.rules_dir / f"{rule.filename}"
                else:
                    mode_slug = rule.mode_slug or "default"
                    rule_file = target.rules_mode_dir(mode_slug) / f"{rule.filename}"
                if rule_file.exists():
                    existing.append(rule_file)

            # Skill files
            for skill in agent.skills:
                skill_file = target.skills_dir / skill.name / "SKILL.md"
                if skill_file.exists():
                    existing.append(skill_file)

        return existing

    def validate_yaml(self, file_path: Path) -> ValidationResult:
        """Validate a YAML file for syntax errors.

        Implements T076: User Story 6 - YAML validation.

        Args:
            file_path: Path to the YAML file to validate.

        Returns:
            ValidationResult with status and any errors found.
        """
        result = ValidationResult(file_path=file_path)

        if not file_path.exists():
            result.add_error(
                message=f"File does not exist: {file_path}",
                error_type="file_not_found",
            )
            return result

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(
                message=f"Cannot read file: {e}",
                error_type="read_error",
            )
            return result

        # Try to parse YAML
        try:
            yaml.safe_load(content)
            # If we get here, YAML is valid
            result.status = ValidationStatus.PASS
        except yaml.YAMLError as e:
            # Extract line number if available
            line_num = None
            column = None
            if hasattr(e, "problem_mark") and e.problem_mark:
                line_num = e.problem_mark.line + 1  # Convert to 1-indexed
                column = e.problem_mark.column

            result.add_error(
                message=str(e),
                line_number=line_num,
                column=column,
                error_type="yaml_syntax",
            )

        return result

    def validate_markdown(self, file_path: Path) -> ValidationResult:
        """Validate a Markdown file for structure errors.

        Implements T077: User Story 6 - Markdown structure validation.

        Checks:
        - File exists and is readable
        - Has valid YAML frontmatter (if present)
        - Has content after frontmatter

        Args:
            file_path: Path to the Markdown file to validate.

        Returns:
            ValidationResult with status and any errors found.
        """
        result = ValidationResult(file_path=file_path)

        if not file_path.exists():
            result.add_error(
                message=f"File does not exist: {file_path}",
                error_type="file_not_found",
            )
            return result

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(
                message=f"Cannot read file: {e}",
                error_type="read_error",
            )
            return result

        # Check for empty file
        if not content.strip():
            result.add_error(
                message="File is empty",
                error_type="empty_file",
            )
            return result

        # Check for frontmatter
        if content.startswith("---"):
            # Extract frontmatter
            lines = content.split("\n")
            frontmatter_lines = []
            in_frontmatter = False
            frontmatter_end_line = None

            for i, line in enumerate(lines):
                if line.strip() == "---":
                    if not in_frontmatter:
                        in_frontmatter = True
                    else:
                        frontmatter_end_line = i
                        break
                elif in_frontmatter:
                    frontmatter_lines.append(line)

            if frontmatter_end_line is None:
                result.add_error(
                    message="Unclosed frontmatter block (missing closing '---')",
                    line_number=1,
                    error_type="frontmatter_unclosed",
                )
                return result

            # Validate frontmatter YAML
            if frontmatter_lines:
                try:
                    yaml_content = "\n".join(frontmatter_lines)
                    yaml.safe_load(yaml_content)
                except yaml.YAMLError as e:
                    line_num = None
                    if hasattr(e, "problem_mark") and e.problem_mark:
                        line_num = e.problem_mark.line + 1  # Convert to 1-indexed

                    result.add_error(
                        message=f"Invalid frontmatter YAML: {e}",
                        line_number=line_num,
                        error_type="frontmatter_yaml",
                    )
                    return result

            # Check for content after frontmatter
            content_after = "\n".join(lines[frontmatter_end_line + 1 :])
            if not content_after.strip():
                result.add_error(
                    message="No content after frontmatter",
                    line_number=frontmatter_end_line + 1,
                    error_type="no_content",
                )
                return result

        # If we got here without errors, validation passed
        result.status = ValidationStatus.PASS
        return result

    def validate_generation_result(self, result: GenerationResult) -> None:
        """Validate all generated files in a generation result.

        Runs validation on all successfully generated files and adds
        validation results to the generation result.

        Args:
            result: The GenerationResult to validate.
        """
        for file_info in result.files:
            if file_info.status not in (FileStatus.CREATED, FileStatus.UPDATED):
                # Skip files that weren't successfully generated
                continue

            file_path = file_info.path

            # Determine validation type based on file extension
            if file_path.suffix == ".yaml" or file_path.suffix == ".yml":
                validation_result = self.validate_yaml(file_path)
            elif file_path.suffix == ".md":
                validation_result = self.validate_markdown(file_path)
            else:
                # Skip unknown file types
                continue

            result.add_validation_result(validation_result)

    def _format_permission_error(self, _error: PermissionError, path: Path) -> str:
        """T081: Format permission error with suggested resolution.

        Args:
            error: The PermissionError that occurred.
            path: The path that caused the error.

        Returns:
            Formatted error message with resolution suggestion.
        """
        msg = f"Permission denied: {path}\n\n"
        msg += "Suggested resolution:\n"

        # Check if it's a directory permission issue
        parent = path.parent
        if not parent.exists():
            msg += f"- Parent directory does not exist: {parent}\n"
            msg += "- Create the directory structure first\n"
        elif not os.access(parent, os.W_OK):
            msg += f"- No write permission to: {parent}\n"
            if "home" in str(parent).lower() or str(parent).startswith("/home"):
                msg += "- Try running without elevated permissions\n"
            else:
                msg += "- Try running with elevated permissions (e.g., sudo)\n"
            msg += "- Or choose a different target directory\n"
        else:
            msg += "- Check file permissions and try again\n"
            msg += "- Ensure you have write access to the target location\n"

        return msg

    def _cleanup_partial_files(self, files: list[Path]) -> None:
        """T082: Clean up partial files after generation interruption.

        Deletes files that were created during interrupted generation
        to prevent partial/corrupt configuration files.

        Args:
            files: List of file paths to clean up.
        """
        for file_path in files:
            try:
                if file_path.exists():
                    file_path.unlink()
            except (OSError, PermissionError):
                # If we can't delete, just continue
                pass

    def _cleanup_incomplete_generation(self, target: GenerationTarget) -> None:
        """T082: Clean up incomplete generation on interruption.

        Attempts to remove any directories or files created during
        an interrupted generation process.

        Args:
            target: The GenerationTarget to clean up.
        """
        # Try to clean up directories if empty
        for dir_path in [target.skills_dir, target.agents_dir, target.rules_dir, target.kilo_dir]:
            try:
                if dir_path.exists() and dir_path.is_dir() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
            except (OSError, PermissionError):
                pass
