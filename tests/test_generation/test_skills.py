"""Tests for skills generation.

Covers T048: User Story 5 - Generate skill files.
"""



from riseon_agents.generation.skills import SkillsGenerator
from riseon_agents.models.skill import Skill


class TestSkillsGenerator:
    """T048: Tests for skills generation."""

    def test_generator_exists(self):
        """SkillsGenerator can be instantiated."""
        generator = SkillsGenerator()
        assert generator is not None

    def test_generate_single_skill(self, tmp_path):
        """Generate directory and SKILL.md for single skill."""
        skill = Skill(
            name="speckit-specify",
            description="Speckit specify skill",
            content="---\nname: speckit-specify\n---\n\n# Skill",
            source_path=tmp_path / "speckit-specify" / "SKILL.md",
        )

        generator = SkillsGenerator()
        result = generator.generate([skill], tmp_path)

        assert result.error_count == 0
        assert len(result.files) >= 1
        # Should create a directory
        assert any("speckit-specify" in str(f.path) for f in result.files)

    def test_skill_content_includes_metadata(self, tmp_path):
        """Generated SKILL.md includes metadata."""
        skill = Skill(
            name="my-skill",
            description="My skill description",
            content="---\nname: my-skill\n---\n\n# Instructions",
            source_path=tmp_path / "my-skill" / "SKILL.md",
        )

        generator = SkillsGenerator()
        result = generator.generate([skill], tmp_path)

        # Find SKILL.md file
        skill_files = [f for f in result.files if f.path.name == "SKILL.md"]
        assert len(skill_files) == 1

        # Read content from file
        content = skill_files[0].path.read_text()
        assert "metadata:" in content
        assert "source: riseon-agents" in content
        assert "generated:" in content

    def test_generate_multiple_skills(self, tmp_path):
        """Generate multiple skill directories."""
        skills = [
            Skill(
                name="skill1",
                description="Skill 1",
                content="# Skill 1",
                source_path=tmp_path / "skill1" / "SKILL.md",
            ),
            Skill(
                name="skill2",
                description="Skill 2",
                content="# Skill 2",
                source_path=tmp_path / "skill2" / "SKILL.md",
            ),
        ]

        generator = SkillsGenerator()
        result = generator.generate(skills, tmp_path)

        assert result.error_count == 0
        # Should have files for both skills
        paths = [str(f.path) for f in result.files]
        assert any("skill1" in p for p in paths)
        assert any("skill2" in p for p in paths)

    def test_empty_skills_list(self, tmp_path):
        """Handle empty skills list gracefully."""
        generator = SkillsGenerator()
        result = generator.generate([], tmp_path)

        assert result.error_count > 0
        assert len(result.files) > 0

    def test_skills_written_to_skills_subdir(self, tmp_path):
        """Skills written to .kilocode/skills/ subdirectory."""
        skill = Skill(
            name="test-skill",
            description="Test skill",
            content="# Test",
            source_path=tmp_path / "test-skill" / "SKILL.md",
        )

        generator = SkillsGenerator()
        result = generator.generate([skill], tmp_path)

        # Check path includes skills/ subdirectory
        assert any("skills" in str(f.path) for f in result.files)

    def test_preserves_original_content(self, tmp_path):
        """Preserves original skill content."""
        original_content = "---\nname: my-skill\n---\n\n# My Skill\n\nInstructions here."
        skill = Skill(
            name="my-skill",
            description="My skill",
            content=original_content,
            source_path=tmp_path / "my-skill" / "SKILL.md",
        )

        generator = SkillsGenerator()
        result = generator.generate([skill], tmp_path)

        # Find SKILL.md and verify content includes original
        skill_files = [f for f in result.files if f.path.name == "SKILL.md"]
        assert len(skill_files) == 1
        assert "Instructions here" in skill_files[0].path.read_text()

    def test_creates_directory_structure(self, tmp_path):
        """Creates proper directory structure for skill."""
        skill = Skill(
            name="my-skill",
            description="My skill",
            content="# Skill",
            source_path=tmp_path / "my-skill" / "SKILL.md",
        )

        generator = SkillsGenerator()
        result = generator.generate([skill], tmp_path)

        # Find any file path that contains the skill name
        skill_paths = [f.path for f in result.files if "my-skill" in str(f.path)]
        assert len(skill_paths) > 0

        # Verify parent directories are created
        for path in skill_paths:
            assert path.parent.exists()
