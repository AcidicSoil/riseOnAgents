"""Tests for generation models."""

from pathlib import Path

from riseon_agents.generation.provider_capabilities import ProviderTarget
from riseon_agents.models.generation import (
    FileStatus,
    GeneratedFile,
    GenerationLevel,
    GenerationResult,
    GenerationTarget,
)


class TestGenerationLevel:
    """Tests for the GenerationLevel enum."""

    def test_level_values(self) -> None:
        """Test that all levels have correct values."""
        assert GenerationLevel.LOCAL.value == "local"
        assert GenerationLevel.GLOBAL.value == "global"


class TestFileStatus:
    """Tests for the FileStatus enum."""

    def test_status_values(self) -> None:
        """Test that all statuses have correct values."""
        assert FileStatus.CREATED.value == "created"
        assert FileStatus.UPDATED.value == "updated"
        assert FileStatus.SKIPPED.value == "skipped"
        assert FileStatus.ERROR.value == "error"


class TestGenerationTarget:
    """Tests for the GenerationTarget dataclass."""

    def test_local_target_paths(self, temp_dir: Path) -> None:
        """Test path resolution for local target."""
        target = GenerationTarget.local(temp_dir)

        assert target.level == GenerationLevel.LOCAL
        assert target.base_path == temp_dir
        assert target.kilo_dir == temp_dir / ".kilo"
        assert target.kilocode_dir == temp_dir / ".kilocode"
        assert target.modes_file == temp_dir / ".kilo" / "custom_modes.yaml"
        assert target.agents_dir == temp_dir / ".kilo" / "agents"
        assert target.rules_dir == temp_dir / ".kilo" / "rules"
        assert target.skills_dir == temp_dir / ".kilocode" / "skills"

    def test_local_rules_mode_dir(self, temp_dir: Path) -> None:
        """Test mode-specific rules directory for local target."""
        target = GenerationTarget.local(temp_dir)
        assert target.rules_mode_dir("architect") == temp_dir / ".kilo" / "rules-architect"

    def test_global_target_paths(self) -> None:
        """Test path resolution for global target."""
        target = GenerationTarget.global_()

        assert target.level == GenerationLevel.GLOBAL
        assert target.base_path == Path.home() / ".kilocode"

    def test_ensure_directories(self, temp_dir: Path) -> None:
        """Test that ensure_directories creates required folders."""
        target = GenerationTarget.local(temp_dir)
        target.ensure_directories()

        assert target.kilo_dir.exists()
        assert target.agents_dir.exists()
        assert target.rules_dir.exists()
        assert target.skills_dir.exists()

    def test_provider_output_path_for_codex_agents(self, temp_dir: Path) -> None:
        """Provider-native paths should resolve through the capability registry."""
        target = GenerationTarget.local(temp_dir)

        assert target.provider_output_path(ProviderTarget.CODEX, "agents") == (
            temp_dir / ".codex" / "agents"
        )

    def test_provider_output_path_reuses_legacy_kilo_mapping(self, temp_dir: Path) -> None:
        """Kilo paths should keep using the existing target layout."""
        target = GenerationTarget.local(temp_dir)

        assert target.provider_output_path(ProviderTarget.KILO, "agents") == target.agents_dir
        assert target.provider_output_path(ProviderTarget.KILO, "skills") == target.skills_dir

    def test_ensure_provider_directories_creates_surface_roots(self, temp_dir: Path) -> None:
        """Provider directory creation should handle file and directory outputs."""
        target = GenerationTarget.local(temp_dir)

        target.ensure_provider_directories([ProviderTarget.CODEX, ProviderTarget.HERMES])

        assert (temp_dir / ".codex" / "agents").exists()
        assert (temp_dir / ".agents" / "skills").exists()
        assert (temp_dir / ".hermes.md").parent.exists()


class TestGeneratedFile:
    """Tests for the GeneratedFile dataclass."""

    def test_create_generated_file(self, temp_dir: Path) -> None:
        """Test creating a generated file result."""
        path = temp_dir / "test.yaml"
        file_result = GeneratedFile(path=path, status=FileStatus.CREATED)

        assert file_result.path == path
        assert file_result.status == FileStatus.CREATED
        assert file_result.error_message is None
        assert file_result.existed_before is False

    def test_is_success_property(self, temp_dir: Path) -> None:
        """Test the is_success property."""
        path = temp_dir / "test.yaml"

        created = GeneratedFile(path=path, status=FileStatus.CREATED)
        assert created.is_success is True

        updated = GeneratedFile(path=path, status=FileStatus.UPDATED)
        assert updated.is_success is True

        skipped = GeneratedFile(path=path, status=FileStatus.SKIPPED)
        assert skipped.is_success is False

        error = GeneratedFile(path=path, status=FileStatus.ERROR)
        assert error.is_success is False

    def test_is_error_property(self, temp_dir: Path) -> None:
        """Test the is_error property."""
        path = temp_dir / "test.yaml"

        error = GeneratedFile(path=path, status=FileStatus.ERROR, error_message="Failed")
        assert error.is_error is True

        created = GeneratedFile(path=path, status=FileStatus.CREATED)
        assert created.is_error is False


class TestGenerationResult:
    """Tests for the GenerationResult dataclass."""

    def test_empty_result(self) -> None:
        """Test an empty generation result."""
        result = GenerationResult()

        assert result.files == []
        assert result.target is None
        assert result.interrupted is False
        assert result.success is True

    def test_add_file(self, temp_dir: Path) -> None:
        """Test adding files to the result."""
        result = GenerationResult()
        path = temp_dir / "test.yaml"

        file_result = result.add_file(path, FileStatus.CREATED)

        assert len(result.files) == 1
        assert file_result.path == path
        assert file_result.status == FileStatus.CREATED

    def test_count_properties(self, temp_dir: Path) -> None:
        """Test the count properties."""
        result = GenerationResult()

        result.add_file(temp_dir / "created1.yaml", FileStatus.CREATED)
        result.add_file(temp_dir / "created2.yaml", FileStatus.CREATED)
        result.add_file(temp_dir / "updated.yaml", FileStatus.UPDATED)
        result.add_file(temp_dir / "skipped.yaml", FileStatus.SKIPPED)
        result.add_file(temp_dir / "error.yaml", FileStatus.ERROR, error_message="Failed")

        assert result.created_count == 2
        assert result.updated_count == 1
        assert result.skipped_count == 1
        assert result.error_count == 1
        assert result.total_count == 5
        assert result.success_count == 3

    def test_success_property(self, temp_dir: Path) -> None:
        """Test the success property."""
        result = GenerationResult()
        result.add_file(temp_dir / "created.yaml", FileStatus.CREATED)
        assert result.success is True

        result.add_file(temp_dir / "error.yaml", FileStatus.ERROR)
        assert result.success is False

    def test_interrupted_affects_success(self, temp_dir: Path) -> None:
        """Test that interrupted flag affects success."""
        result = GenerationResult(interrupted=True)
        result.add_file(temp_dir / "created.yaml", FileStatus.CREATED)
        assert result.success is False

    def test_error_files_property(self, temp_dir: Path) -> None:
        """Test getting error files."""
        result = GenerationResult()
        result.add_file(temp_dir / "good.yaml", FileStatus.CREATED)
        result.add_file(temp_dir / "bad1.yaml", FileStatus.ERROR, error_message="Error 1")
        result.add_file(temp_dir / "bad2.yaml", FileStatus.ERROR, error_message="Error 2")

        errors = result.error_files
        assert len(errors) == 2
        assert all(f.status == FileStatus.ERROR for f in errors)

    def test_get_summary(self, temp_dir: Path) -> None:
        """Test generating a summary string."""
        result = GenerationResult(target=GenerationTarget.local(temp_dir))
        result.add_file(temp_dir / "created.yaml", FileStatus.CREATED)
        result.add_file(temp_dir / "updated.yaml", FileStatus.UPDATED)

        summary = result.get_summary()
        assert "Generation Complete" in summary
        assert "Created: 1 files" in summary
        assert "Updated: 1 files" in summary
        assert "Local" in summary

    def test_get_summary_interrupted(self) -> None:
        """Test summary for interrupted generation."""
        result = GenerationResult(interrupted=True)
        summary = result.get_summary()
        assert "Generation Interrupted" in summary

    def test_get_summary_with_errors(self, temp_dir: Path) -> None:
        """Test summary includes error count."""
        result = GenerationResult()
        result.add_file(temp_dir / "error.yaml", FileStatus.ERROR)

        summary = result.get_summary()
        assert "Generation Failed" in summary
        assert "Errors: 1 files" in summary
