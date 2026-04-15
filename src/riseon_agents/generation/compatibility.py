"""Generator for provider-native compatibility surfaces."""

from pathlib import Path

from riseon_agents.generation.provider_capabilities import (
    ProviderTarget,
    get_provider_capabilities,
)
from riseon_agents.generation.provider_emitters import (
    emit_codex_agent_manifest,
    emit_gemini_agent_manifest,
    emit_hermes_identity,
    emit_project_instructions,
    emit_skill_surface,
)
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.models.generation import FileStatus, GenerationResult, GenerationTarget
from riseon_agents.models.identity_spec import IdentitySpec
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
        identity_specs: list[IdentitySpec] | None = None,
    ) -> GenerationResult:
        """Generate supported compatibility surfaces for the selected providers."""
        result = GenerationResult(target=target)
        emitted_paths: set[tuple[str, str]] = set()
        identity_specs = identity_specs or []
        target.ensure_provider_directories(providers)

        for provider in providers:
            capabilities = get_provider_capabilities(provider)

            if project_instructions and capabilities.supports_surface("project_instructions"):
                for instructions in project_instructions:
                    output_path = emit_project_instructions(target, instructions, provider)
                    self._record_emitted(result, emitted_paths, "project_instructions", output_path)

            if skills and capabilities.supports_surface("skills"):
                for skill in skills:
                    output_path = emit_skill_surface(target, skill, provider)
                    self._record_emitted(result, emitted_paths, "skills", output_path)

            if agent_profiles and capabilities.supports_surface("agents"):
                if provider is ProviderTarget.CODEX:
                    for agent_profile in agent_profiles:
                        output_path = emit_codex_agent_manifest(target, agent_profile, provider)
                        self._record_emitted(result, emitted_paths, "agents", output_path)
                elif provider is ProviderTarget.GEMINI:
                    for agent_profile in agent_profiles:
                        output_path = emit_gemini_agent_manifest(target, agent_profile, provider)
                        self._record_emitted(result, emitted_paths, "agents", output_path)
                else:
                    result.add_file(
                        path=target.base_path / provider.value,
                        status=FileStatus.ERROR,
                        error_message=(
                            f"Provider '{provider.value}' agent manifest emission is not implemented"
                        ),
                    )

            if identity_specs and capabilities.supports_surface("identity"):
                if provider is ProviderTarget.HERMES:
                    for identity in identity_specs:
                        output_path = emit_hermes_identity(target, identity, provider)
                        self._record_emitted(result, emitted_paths, "identity", output_path)
                else:
                    result.add_file(
                        path=target.base_path / provider.value,
                        status=FileStatus.ERROR,
                        error_message=(
                            f"Provider '{provider.value}' identity emission is not implemented"
                        ),
                    )

        return result

    def _record_emitted(
        self,
        result: GenerationResult,
        emitted_paths: set[tuple[str, str]],
        surface: str,
        output_path: Path,
    ) -> None:
        """Record a generated artifact once per unique surface or path."""
        output_path_str = str(output_path)
        emission_key = (surface, output_path_str)
        if emission_key in emitted_paths:
            return
        emitted_paths.add(emission_key)
        result.add_file(path=output_path, status=self._status_for(output_path))

    def _status_for(self, output_path: object) -> FileStatus:
        """Return file status for a freshly emitted compatibility artifact."""
        del output_path
        return FileStatus.CREATED
