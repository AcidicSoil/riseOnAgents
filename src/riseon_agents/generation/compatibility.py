"""Generator for provider-native compatibility surfaces."""

from riseon_agents.generation.provider_capabilities import ProviderTarget, get_provider_capabilities
from riseon_agents.generation.provider_emitters import (
    emit_project_instructions,
    emit_skill_surface,
)
from riseon_agents.models.generation import FileStatus, GenerationResult, GenerationTarget
from riseon_agents.models.project_instructions import ProjectInstructions
from riseon_agents.models.skill_spec import SkillSpec


class CompatibilityGenerator:
    """Generate provider-native project instruction and skill surfaces."""

    def generate(
        self,
        target: GenerationTarget,
        providers: list[ProviderTarget],
        project_instructions: list[ProjectInstructions],
        skills: list[SkillSpec],
    ) -> GenerationResult:
        """Generate supported compatibility surfaces for the selected providers."""
        result = GenerationResult(target=target)
        target.ensure_provider_directories(providers)

        for provider in providers:
            capabilities = get_provider_capabilities(provider)

            if project_instructions:
                if capabilities.supports_surface("project_instructions"):
                    for instructions in project_instructions:
                        output_path = emit_project_instructions(target, instructions, provider)
                        result.add_file(path=output_path, status=self._status_for(output_path))
                else:
                    result.add_file(
                        path=target.base_path / provider.value,
                        status=FileStatus.ERROR,
                        error_message=(
                            f"Provider '{provider.value}' does not support project instructions"
                        ),
                    )

            if skills:
                if capabilities.supports_surface("skills"):
                    for skill in skills:
                        output_path = emit_skill_surface(target, skill, provider)
                        result.add_file(path=output_path, status=self._status_for(output_path))
                else:
                    result.add_file(
                        path=target.base_path / provider.value,
                        status=FileStatus.ERROR,
                        error_message=f"Provider '{provider.value}' does not support skills",
                    )

        return result

    def _status_for(self, output_path: object) -> FileStatus:
        """Return file status for a freshly emitted compatibility artifact."""
        del output_path
        return FileStatus.CREATED
