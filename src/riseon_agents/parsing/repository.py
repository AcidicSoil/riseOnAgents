"""Agent repository for discovering and loading agent definitions.

Scans the agents/ folder structure and loads all agent, subagent, rule,
and skill definitions into the data model.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from riseon_agents.models.agent import PermissionLevel, PrimaryAgent, Subagent
from riseon_agents.models.agent_profile import AgentProfile
from riseon_agents.models.identity_spec import IdentitySpec
from riseon_agents.models.project_instructions import ProjectInstructions
from riseon_agents.models.rule import Rule
from riseon_agents.models.rule_spec import RuleSpec
from riseon_agents.models.skill import Skill
from riseon_agents.models.skill_spec import SkillSpec
from riseon_agents.parsing.frontmatter import FrontmatterParser, ParsedDocument

logger = logging.getLogger(__name__)


@dataclass
class LoadWarning:
    """Warning generated during agent loading."""

    path: Path
    message: str
    exception: Exception | None = None


@dataclass
class LoadResult:
    """Result of loading agents from a directory."""

    agents: list[PrimaryAgent] = field(default_factory=list)
    warnings: list[LoadWarning] = field(default_factory=list)

    @property
    def success(self) -> bool:
        """Check if loading completed without fatal errors."""
        return len(self.agents) > 0 or len(self.warnings) == 0


class AgentRepository:
    """Repository for discovering and loading agent definitions.

    Scans the agents/ folder and loads all primary agents with their
    subagents, rules, and skills.
    """

    def __init__(self, agents_path: Path) -> None:
        """Initialize the repository.

        Args:
            agents_path: Path to the agents/ folder
        """
        self.agents_path = agents_path.resolve()
        self.parser = FrontmatterParser()
        self._agents: list[PrimaryAgent] = []
        self._warnings: list[LoadWarning] = []

    def discover(self) -> LoadResult:
        """Discover and load all agents from the agents/ folder.

        Returns:
            LoadResult with loaded agents and any warnings
        """
        self._agents = []
        self._warnings = []

        if not self.agents_path.exists():
            self._warnings.append(
                LoadWarning(
                    path=self.agents_path,
                    message=f"Agents folder not found: {self.agents_path}",
                )
            )
            return LoadResult(agents=[], warnings=self._warnings)

        if not self.agents_path.is_dir():
            self._warnings.append(
                LoadWarning(
                    path=self.agents_path,
                    message=f"Agents path is not a directory: {self.agents_path}",
                )
            )
            return LoadResult(agents=[], warnings=self._warnings)

        # Discover primary agent directories
        for agent_dir in sorted(self.agents_path.iterdir()):
            if not agent_dir.is_dir():
                continue
            if agent_dir.name.startswith("."):
                continue

            primary = self._load_primary_agent(agent_dir)
            if primary:
                self._agents.append(primary)

        return LoadResult(agents=self._agents, warnings=self._warnings)

    def _load_primary_agent(self, agent_dir: Path) -> PrimaryAgent | None:
        """Load a primary agent from its directory.

        Args:
            agent_dir: Path to the agent's directory

        Returns:
            PrimaryAgent or None if loading failed
        """
        # Find the primary agent definition file
        # Convention: {agent-name}/{agent-name}.agent.md
        agent_name = agent_dir.name
        agent_file = agent_dir / f"{agent_name}.agent.md"

        if not agent_file.exists():
            # Also try without .agent suffix
            agent_file = agent_dir / f"{agent_name}.md"
            if not agent_file.exists():
                self._warnings.append(
                    LoadWarning(
                        path=agent_dir,
                        message=f"No agent definition file found in {agent_dir}",
                    )
                )
                return None

        try:
            doc = self.parser.parse_file(agent_file)
            primary = self._parse_primary_agent(doc, agent_dir)

            # Load subagents
            subagents_dir = agent_dir / "subagents"
            if subagents_dir.exists() and subagents_dir.is_dir():
                primary.subagents = self._load_subagents(subagents_dir, primary.name)

            # Load rules
            rules_dir = agent_dir / "rules"
            if rules_dir.exists() and rules_dir.is_dir():
                primary.rules = self._load_rules(rules_dir, primary.slug)

            # Load skills
            skills_dir = agent_dir / "skills"
            if skills_dir.exists() and skills_dir.is_dir():
                primary.skills = self._load_skills(skills_dir)

            return primary

        except Exception as e:
            self._warnings.append(
                LoadWarning(
                    path=agent_file,
                    message=f"Failed to load agent: {e}",
                    exception=e,
                )
            )
            return None

    def _parse_primary_agent(self, doc: ParsedDocument, _agent_dir: Path) -> PrimaryAgent:
        """Parse a primary agent from a document.

        Args:
            doc: Parsed document with frontmatter and body
            agent_dir: Path to the agent's directory

        Returns:
            PrimaryAgent instance
        """
        # Parse permissions
        permissions_raw = self.parser.get_dict(doc, "permissions")
        permissions = self._parse_permissions(permissions_raw)

        # Parse handoffs
        handoffs_raw = self.parser.get_list(doc, "handoffs")
        handoffs = self._parse_handoffs(handoffs_raw)

        return PrimaryAgent(
            name=self.parser.get_required_string(doc, "name"),
            description=self.parser.get_required_string(doc, "description"),
            markdown_body=doc.body.strip(),
            tools=self.parser.get_list(doc, "tools"),
            temperature=self.parser.get_float(doc, "temperature", 0.1),
            steps=self.parser.get_int(doc, "steps", 40),
            permissions=permissions,
            handoffs=handoffs,
            source_path=doc.source_path,
        )

    def _parse_permissions(self, permissions_raw: dict[str, Any]) -> dict[str, PermissionLevel]:
        """Parse permissions dict to PermissionLevel enums."""
        result: dict[str, PermissionLevel] = {}
        for key, value in permissions_raw.items():
            try:
                result[key] = PermissionLevel(str(value).lower())
            except ValueError:
                logger.warning(f"Unknown permission level '{value}' for '{key}'")
        return result

    def _parse_handoffs(self, handoffs_raw: list[Any]) -> list[str]:
        """Parse handoffs list to agent names."""
        result: list[str] = []
        for item in handoffs_raw:
            if isinstance(item, dict) and "agent" in item:
                result.append(str(item["agent"]))
            elif isinstance(item, str):
                result.append(item)
        return result

    def _load_subagents(self, subagents_dir: Path, parent_name: str) -> list[Subagent]:
        """Load all subagents from a directory.

        Args:
            subagents_dir: Path to the subagents/ directory
            parent_name: Name of the parent primary agent

        Returns:
            List of Subagent instances
        """
        subagents: list[Subagent] = []

        for subagent_file in sorted(subagents_dir.glob("*.agent.md")):
            try:
                doc = self.parser.parse_file(subagent_file)
                subagent = self._parse_subagent(doc, parent_name)
                subagents.append(subagent)
            except Exception as e:
                self._warnings.append(
                    LoadWarning(
                        path=subagent_file,
                        message=f"Failed to load subagent: {e}",
                        exception=e,
                    )
                )

        # Also try .md files without .agent suffix
        for subagent_file in sorted(subagents_dir.glob("*.md")):
            if subagent_file.name.endswith(".agent.md"):
                continue  # Already processed
            try:
                doc = self.parser.parse_file(subagent_file)
                # Only process if it looks like a subagent (has mode: subagent)
                if doc.frontmatter.get("mode") == "subagent":
                    subagent = self._parse_subagent(doc, parent_name)
                    subagents.append(subagent)
            except Exception as e:
                self._warnings.append(
                    LoadWarning(
                        path=subagent_file,
                        message=f"Failed to load subagent: {e}",
                        exception=e,
                    )
                )

        return subagents

    def _parse_subagent(self, doc: ParsedDocument, parent_name: str) -> Subagent:
        """Parse a subagent from a document.

        Args:
            doc: Parsed document with frontmatter and body
            parent_name: Name of the parent primary agent

        Returns:
            Subagent instance
        """
        permissions_raw = self.parser.get_dict(doc, "permissions")
        permissions = self._parse_permissions(permissions_raw)

        return Subagent(
            name=self.parser.get_required_string(doc, "name"),
            description=self.parser.get_required_string(doc, "description"),
            markdown_body=doc.body.strip(),
            tools=self.parser.get_list(doc, "tools"),
            temperature=self.parser.get_float(doc, "temperature", 0.1),
            steps=self.parser.get_int(doc, "steps", 15),
            permissions=permissions,
            model_variant=self.parser.get_optional_string(doc, "modelVariant"),
            target=self.parser.get_optional_string(doc, "target") or "opencode",
            source_path=doc.source_path,
            parent_agent=parent_name,
        )

    def _load_rules(self, rules_dir: Path, mode_slug: str) -> list[Rule]:
        """Load all rules from a directory.

        Args:
            rules_dir: Path to the rules/ directory
            mode_slug: Slug of the parent mode (for mode-specific rules)

        Returns:
            List of Rule instances
        """
        rules: list[Rule] = []

        # Load shared rules from _shared/ subdirectory
        shared_dir = rules_dir / "_shared"
        if shared_dir.exists() and shared_dir.is_dir():
            for rule_file in sorted(shared_dir.glob("*.md")):
                try:
                    rule = self._load_rule_file(rule_file, is_shared=True)
                    rules.append(rule)
                except Exception as e:
                    self._warnings.append(
                        LoadWarning(
                            path=rule_file,
                            message=f"Failed to load rule: {e}",
                            exception=e,
                        )
                    )

        # Load mode-specific rules from root of rules/ directory
        for rule_file in sorted(rules_dir.glob("*.md")):
            try:
                rule = self._load_rule_file(rule_file, is_shared=False, mode_slug=mode_slug)
                rules.append(rule)
            except Exception as e:
                self._warnings.append(
                    LoadWarning(
                        path=rule_file,
                        message=f"Failed to load rule: {e}",
                        exception=e,
                    )
                )

        return rules

    def _load_rule_file(
        self, rule_file: Path, is_shared: bool, mode_slug: str | None = None
    ) -> Rule:
        """Load a single rule file.

        Args:
            rule_file: Path to the rule .md file
            is_shared: Whether this is a shared rule
            mode_slug: Mode slug for mode-specific rules

        Returns:
            Rule instance
        """
        content = rule_file.read_text(encoding="utf-8")
        name = rule_file.stem  # Filename without extension

        return Rule(
            name=name,
            content=content,
            is_shared=is_shared,
            mode_slug=mode_slug if not is_shared else None,
            source_path=rule_file,
        )

    def _load_skills(self, skills_dir: Path) -> list[Skill]:
        """Load all skills from a directory.

        Args:
            skills_dir: Path to the skills/ directory

        Returns:
            List of Skill instances
        """
        skills: list[Skill] = []

        for skill_subdir in sorted(skills_dir.iterdir()):
            if not skill_subdir.is_dir():
                continue
            if skill_subdir.name.startswith("."):
                continue

            skill_file = skill_subdir / "SKILL.md"
            if not skill_file.exists():
                self._warnings.append(
                    LoadWarning(
                        path=skill_subdir,
                        message=f"No SKILL.md found in {skill_subdir}",
                    )
                )
                continue

            try:
                skill = self._load_skill(skill_file, skill_subdir)
                skills.append(skill)
            except Exception as e:
                self._warnings.append(
                    LoadWarning(
                        path=skill_file,
                        message=f"Failed to load skill: {e}",
                        exception=e,
                    )
                )

        return skills

    def _load_skill(self, skill_file: Path, skill_dir: Path) -> Skill:
        """Load a single skill.

        Args:
            skill_file: Path to SKILL.md
            skill_dir: Path to the skill directory

        Returns:
            Skill instance
        """
        doc = self.parser.parse_file(skill_file)
        content = skill_file.read_text(encoding="utf-8")

        # Check for resource directories
        has_scripts = (skill_dir / "scripts").is_dir()
        has_references = (skill_dir / "references").is_dir()
        has_assets = (skill_dir / "assets").is_dir()

        # Get metadata
        metadata_raw = self.parser.get_dict(doc, "metadata")
        metadata = {str(k): str(v) for k, v in metadata_raw.items()}

        return Skill(
            name=self.parser.get_required_string(doc, "name"),
            description=self.parser.get_required_string(doc, "description"),
            content=content,
            license=self.parser.get_optional_string(doc, "license"),
            metadata=metadata,
            has_scripts=has_scripts,
            has_references=has_references,
            has_assets=has_assets,
            source_path=skill_file,
            source_dir=skill_dir,
        )

    @property
    def agents(self) -> list[PrimaryAgent]:
        """Get all loaded agents."""
        return self._agents

    @property
    def warnings(self) -> list[LoadWarning]:
        """Get all warnings from the last load operation."""
        return self._warnings

    def discover_agents(self) -> list[PrimaryAgent]:
        """Discover and return all agents from the agents/ folder.

        This is a convenience method that calls discover() and returns
        just the agents list.

        Returns:
            List of PrimaryAgent instances.
        """
        result = self.discover()
        return result.agents

    def get_agent_by_name(self, name: str) -> PrimaryAgent | None:
        """Find an agent by name.

        Args:
            name: The agent name to find

        Returns:
            PrimaryAgent or None if not found
        """
        for agent in self._agents:
            if agent.name == name:
                return agent
        return None

    def get_all_subagents(self) -> list[Subagent]:
        """Get all subagents across all primary agents."""
        result: list[Subagent] = []
        for agent in self._agents:
            result.extend(agent.subagents)
        return result

    def get_all_rules(self) -> list[Rule]:
        """Get all rules across all primary agents."""
        result: list[Rule] = []
        for agent in self._agents:
            result.extend(agent.rules)
        return result

    def get_all_skills(self) -> list[Skill]:
        """Get all skills across all primary agents."""
        result: list[Skill] = []
        for agent in self._agents:
            result.extend(agent.skills)
        return result

    def get_project_instructions(self) -> list[ProjectInstructions]:
        """Return project instruction surfaces for all loaded primary agents."""
        return [ProjectInstructions.from_primary_agent(agent) for agent in self._agents]

    def get_agent_profiles(self) -> list[AgentProfile]:
        """Return canonical agent profiles for all loaded subagents."""
        profiles: list[AgentProfile] = []
        for agent in self._agents:
            profiles.extend(AgentProfile.from_subagent(subagent) for subagent in agent.subagents)
        return profiles

    def get_rule_specs(self) -> list[RuleSpec]:
        """Return canonical rule specs for all loaded rules."""
        specs: list[RuleSpec] = []
        for agent in self._agents:
            specs.extend(RuleSpec.from_rule(rule) for rule in agent.rules)
        return specs

    def get_skill_specs(self) -> list[SkillSpec]:
        """Return canonical skill specs for all loaded skills."""
        specs: list[SkillSpec] = []
        for agent in self._agents:
            specs.extend(SkillSpec.from_skill(skill) for skill in agent.skills)
        return specs

    def get_identity_specs(self) -> list[IdentitySpec]:
        """Return provider identity specs discovered from the repository.

        The current canonical repository layout does not define a dedicated
        identity source, so this remains empty until a first-class identity
        surface is added.
        """
        return []
