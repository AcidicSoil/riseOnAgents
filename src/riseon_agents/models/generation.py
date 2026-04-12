"""Generation models for RiseOn.Agents.

Defines the data structures for configuration file generation including
target paths, file status tracking, and generation results.
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from riseon_agents.generation.provider_capabilities import ProviderTarget


class ValidationStatus(Enum):
    """Status of a validation check."""

    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"


@dataclass
class ValidationError:
    """A single validation error with location information.

    Attributes:
        file_path: Path to the file that failed validation
        line_number: Line number where the error occurred (1-indexed, None if not applicable)
        column: Column number where the error occurred (None if not applicable)
        message: Human-readable error message
        error_type: Type of error (e.g., "yaml_syntax", "markdown_structure")
    """

    file_path: Path
    message: str
    line_number: int | None = None
    column: int | None = None
    error_type: str = ""

    def __str__(self) -> str:
        """String representation with location info."""
        location = str(self.file_path)
        if self.line_number is not None:
            location += f":{self.line_number}"
            if self.column is not None:
                location += f":{self.column}"
        return f"{location}: {self.message}"


@dataclass
class ValidationResult:
    """Complete result of validation for a single file.

    Attributes:
        file_path: Path to the validated file
        status: PASS, FAIL, or WARNING
        errors: List of validation errors found
    """

    file_path: Path
    status: ValidationStatus = ValidationStatus.PASS
    errors: list[ValidationError] = field(default_factory=list)

    def add_error(
        self,
        message: str,
        line_number: int | None = None,
        column: int | None = None,
        error_type: str = "",
    ) -> None:
        """Add a validation error to this result."""
        error = ValidationError(
            file_path=self.file_path,
            message=message,
            line_number=line_number,
            column=column,
            error_type=error_type,
        )
        self.errors.append(error)
        # Update status to FAIL if we have any errors
        self.status = ValidationStatus.FAIL

    @property
    def is_valid(self) -> bool:
        """Check if the file passed validation."""
        return self.status == ValidationStatus.PASS and len(self.errors) == 0


class GenerationLevel(Enum):
    """Where to generate configuration files."""

    LOCAL = "local"  # Project: ./.kilo/
    GLOBAL = "global"  # User: ~/.kilocode/


class FileStatus(Enum):
    """Status of a generated file."""

    CREATED = "created"
    UPDATED = "updated"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class GenerationTarget:
    """Target configuration for generation.

    Resolves paths based on generation level (Local vs Global) while also
    exposing provider-native output locations through the capability registry.
    """

    level: GenerationLevel
    base_path: Path  # Resolved absolute path (project root or home)

    @property
    def kilo_dir(self) -> Path:
        """Path to .kilo directory."""
        if self.level == GenerationLevel.LOCAL:
            return self.base_path / ".kilo"
        return self.base_path  # Global uses ~/.kilocode directly

    @property
    def kilocode_dir(self) -> Path:
        """Path to .kilocode directory (for skills)."""
        if self.level == GenerationLevel.LOCAL:
            return self.base_path / ".kilocode"
        return self.base_path  # Global uses ~/.kilocode directly

    @property
    def modes_file(self) -> Path:
        """Path to custom_modes.yaml."""
        return self.kilo_dir / "custom_modes.yaml"

    @property
    def agents_dir(self) -> Path:
        """Path to agents directory."""
        return self.kilo_dir / "agents"

    @property
    def rules_dir(self) -> Path:
        """Path to shared rules directory."""
        return self.kilo_dir / "rules"

    def rules_mode_dir(self, mode_slug: str) -> Path:
        """Path to mode-specific rules directory."""
        return self.kilo_dir / f"rules-{mode_slug}"

    @property
    def skills_dir(self) -> Path:
        """Path to skills directory."""
        return self.kilocode_dir / "skills"

    @classmethod
    def local(cls, project_root: Path) -> "GenerationTarget":
        """Create a local generation target."""
        return cls(level=GenerationLevel.LOCAL, base_path=project_root.resolve())

    @classmethod
    def global_(cls) -> "GenerationTarget":
        """Create a global generation target."""
        return cls(level=GenerationLevel.GLOBAL, base_path=Path.home() / ".kilocode")

    def provider_output_path(self, provider: "ProviderTarget | str", surface: str) -> Path:
        """Resolve a provider-native path for the requested compatibility surface."""
        from riseon_agents.generation.provider_capabilities import get_provider_capabilities

        capabilities = get_provider_capabilities(provider)
        relative_output = capabilities.output_locations.get(surface)
        if relative_output is None:
            raise ValueError(
                f"Provider '{capabilities.provider.value}' does not support surface '{surface}'"
            )

        if capabilities.provider.value == "kilo":
            return self._resolve_kilo_surface(surface)

        if self.level == GenerationLevel.GLOBAL:
            provider_root = self.base_path / capabilities.provider.value
        else:
            provider_root = self.base_path

        return provider_root / relative_output

    def ensure_directories(self) -> None:
        """Create all necessary directories for the current Kilo generation path."""
        self.kilo_dir.mkdir(parents=True, exist_ok=True)
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        self.rules_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)

    def ensure_provider_directories(self, providers: list["ProviderTarget | str"]) -> None:
        """Create directories for the requested provider targets.

        File-like outputs create only their parent directories; directory-like
        outputs are created directly.
        """
        from riseon_agents.generation.provider_capabilities import get_provider_capabilities

        for provider in providers:
            capabilities = get_provider_capabilities(provider)
            for surface, relative_output in capabilities.output_locations.items():
                output_path = self.provider_output_path(capabilities.provider, surface)
                if Path(relative_output).suffix:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                else:
                    output_path.mkdir(parents=True, exist_ok=True)

    def _resolve_kilo_surface(self, surface: str) -> Path:
        """Resolve legacy Kilo output paths."""
        if surface == "modes":
            return self.modes_file
        if surface == "skills":
            return self.skills_dir
        if surface == "agents":
            return self.agents_dir
        if surface == "rules":
            return self.rules_dir
        raise ValueError(f"Unsupported Kilo surface '{surface}'")


@dataclass
class GeneratedFile:
    """Result of generating a single file."""

    path: Path
    status: FileStatus
    error_message: str | None = None
    existed_before: bool = False

    @property
    def is_success(self) -> bool:
        """Check if the file was generated successfully."""
        return self.status in (FileStatus.CREATED, FileStatus.UPDATED)

    @property
    def is_error(self) -> bool:
        """Check if there was an error generating this file."""
        return self.status == FileStatus.ERROR


@dataclass
class GenerationResult:
    """Complete result of a generation operation."""

    files: list[GeneratedFile] = field(default_factory=list)
    target: GenerationTarget | None = None
    interrupted: bool = False
    validation_results: list[ValidationResult] = field(default_factory=list)

    def add_file(
        self,
        path: Path,
        status: FileStatus,
        error_message: str | None = None,
        existed_before: bool = False,
    ) -> GeneratedFile:
        """Add a file result to the generation."""
        file_result = GeneratedFile(
            path=path,
            status=status,
            error_message=error_message,
            existed_before=existed_before,
        )
        self.files.append(file_result)
        return file_result

    def add_validation_result(self, result: ValidationResult) -> None:
        """Add a validation result to the generation."""
        self.validation_results.append(result)

    @property
    def validation_passed(self) -> bool:
        """Check if all validations passed."""
        if not self.validation_results:
            return True  # No validation run = pass by default
        return all(r.is_valid for r in self.validation_results)

    @property
    def validation_errors(self) -> list[ValidationError]:
        """Get all validation errors from all results."""
        errors = []
        for result in self.validation_results:
            errors.extend(result.errors)
        return errors

    @property
    def created_count(self) -> int:
        """Count of newly created files."""
        return sum(1 for f in self.files if f.status == FileStatus.CREATED)

    @property
    def updated_count(self) -> int:
        """Count of updated files."""
        return sum(1 for f in self.files if f.status == FileStatus.UPDATED)

    @property
    def skipped_count(self) -> int:
        """Count of skipped files."""
        return sum(1 for f in self.files if f.status == FileStatus.SKIPPED)

    @property
    def error_count(self) -> int:
        """Count of files with errors."""
        return sum(1 for f in self.files if f.status == FileStatus.ERROR)

    @property
    def total_count(self) -> int:
        """Total count of files processed."""
        return len(self.files)

    @property
    def success_count(self) -> int:
        """Count of successfully generated files."""
        return self.created_count + self.updated_count

    @property
    def success(self) -> bool:
        """Check if generation completed without errors."""
        return self.error_count == 0 and not self.interrupted

    @property
    def error_files(self) -> list[GeneratedFile]:
        """Get list of files that had errors."""
        return [f for f in self.files if f.status == FileStatus.ERROR]

    def get_summary(self) -> str:
        """Get a human-readable summary of the generation result."""
        lines = []
        if self.interrupted:
            lines.append("Generation Interrupted")
        else:
            lines.append("Generation Complete" if self.success else "Generation Failed")

        lines.append("")
        lines.append(f"Created: {self.created_count} files")
        lines.append(f"Updated: {self.updated_count} files")
        lines.append(f"Skipped: {self.skipped_count} files")

        if self.error_count > 0:
            lines.append(f"Errors: {self.error_count} files")

        if self.target:
            level_str = "Local" if self.target.level == GenerationLevel.LOCAL else "Global"
            lines.append("")
            lines.append(f"Target: {level_str} ({self.target.base_path})")

        # Add validation section if validation was run
        if self.validation_results:
            lines.append("")
            if self.validation_passed:
                lines.append("Validation: All files passed validation ✓")
            else:
                lines.append("Validation: Some files failed validation ✗")
                lines.append(f"  {len(self.validation_errors)} error(s) found")

        return "\n".join(lines)
