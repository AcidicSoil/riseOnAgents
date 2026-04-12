"""Generator for provider-native compatibility surfaces."""

from riseon_agents.generation.provider_capabilities import (
    ProviderTarget,
    get_provider_capabilities,
)
from riseon_agents.generation.provider_emitters import (
    emit_codex_agent_manifest,
    emit_gemini_agent_manifest,
    emit_project_instructions,
    emit_skill_surface,
)
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.models.generation import FileStatus, GenerationResult, GenerationTarget
from riseon_agents.models.project_instructions import ProjectInstructions
from riseon_agents.models.skill_spec import SkillSpec


class CompatibilityGenerator:
    """Generate provider-native project instruction, skill, and agent surfaces."""

    def generate(
        self,
        target: GenerationTarget,
        providers: list[ProviderTarget],
        project_instructions: list[ProjectInstructions],
        skills: list[SkillSpec],
        agent_profiles: list[AgentProfile],
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

            if agent_profiles:
                if provider is ProviderTarget.CODEX and capabilities.supports_surface("agents"):
                    for agent_profile in agent_profiles:
                        output_path = emit_codex_agent_manifest(target, agent_profile, provider)
                        result.add_file(path=output_path, status=self._status_for(output_path))
                elif provider is ProviderTarget.GEMINI and capabilities.supports_surface("agents"):
                    for agent_profile in agent_profiles:
                        output_path = emit_gemini_agent_manifest(target, agent_profile, provider)
                        result.add_file(path=output_path, status=self._status_for(output_path))
                elif capabilities.supports_surface("agents"):
                    result.add_file(
                        path=target.base_path / provider.value,
                        status=FileStatus.ERROR,
                        error_message=(
                            f"Provider '{provider.value}' agent manifest emission is not implemented"
                        ),
                    )
                else:
                    result.add_file(
                        path=target.base_path / provider.value,
                        status=FileStatus.ERROR,
                        error_message=f"Provider '{provider.value}' does not support agents",
                    )

        return result

    def _status_for(self, output_path: object) -> FileStatus:
        """Return file status for a freshly emitted compatibility artifact."""
        del output_path
        return FileStatus.CREATED
