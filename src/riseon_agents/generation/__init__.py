"""Generation module for RiseOn.Agents.

This package contains generators for creating Kilo Code configuration files.
"""

from riseon_agents.generation.compatibility import CompatibilityGenerator
from riseon_agents.generation.generator import KiloCodeGenerator
from riseon_agents.generation.modes import ModesGenerator
from riseon_agents.generation.provider_capabilities import (
    ArtifactFormat,
    ProviderCapabilities,
    ProviderTarget,
    get_provider_capabilities,
)
from riseon_agents.generation.provider_emitters import (
    emit_project_instructions,
    emit_skill_surface,
)
from riseon_agents.generation.rules import RulesGenerator
from riseon_agents.generation.skills import SkillsGenerator
from riseon_agents.generation.subagents import SubagentsGenerator

__all__ = [
    "CompatibilityGenerator",
    "KiloCodeGenerator",
    "ModesGenerator",
    "SubagentsGenerator",
    "RulesGenerator",
    "SkillsGenerator",
    "emit_skill_surface",
    "emit_project_instructions",
    "ProviderTarget",
    "ArtifactFormat",
    "ProviderCapabilities",
    "get_provider_capabilities",
]
