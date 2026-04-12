"""Generator for custom_modes.yaml.

Implements T050: User Story 5 - Generate custom_modes.yaml.
"""

from datetime import datetime
from pathlib import Path

from riseon_agents.models.agent import PermissionLevel, PrimaryAgent
from riseon_agents.models.generation import FileStatus, GenerationResult


class ModesGenerator:
    """Generator for custom_modes.yaml file.

    Creates the custom_modes.yaml file containing all Primary Agent
    definitions mapped to Kilo Code custom mode format.
    """

    def generate(self, agents: list[PrimaryAgent], target_dir: Path) -> GenerationResult:
        """Generate custom_modes.yaml for the given agents.

        Args:
            agents: List of PrimaryAgent objects to generate modes for.
            target_dir: Target directory for output.

        Returns:
            GenerationResult with the generated file.
        """
        result = GenerationResult()

        if not agents:
            result.add_file(
                path=target_dir / "custom_modes.yaml",
                status=FileStatus.ERROR,
                error_message="No agents selected for generation",
            )
            return result

        try:
            # Generate the YAML content
            content = self._generate_content(agents)

            # Create the output file
            output_path = target_dir / "custom_modes.yaml"

            # Check if file exists
            existed = output_path.exists()

            # Write to file
            output_path.write_text(content, encoding="utf-8")

            # Add to result
            result.add_file(
                path=output_path,
                status=FileStatus.UPDATED if existed else FileStatus.CREATED,
                existed_before=existed,
            )

        except Exception as e:
            result.add_file(
                path=target_dir / "custom_modes.yaml",
                status=FileStatus.ERROR,
                error_message=f"Failed to generate custom_modes.yaml: {e}",
            )

        return result

    def _generate_content(self, agents: list[PrimaryAgent]) -> str:
        """Generate the YAML content for custom_modes.yaml.

        Args:
            agents: List of PrimaryAgent objects.

        Returns:
            YAML content as string.
        """
        lines = [
            "# RiseOn.Agents Generated Configuration",
            f"# Generated: {datetime.utcnow().isoformat()}Z",
            "",
            "customModes:",
        ]

        for agent in agents:
            mode_entry = self._generate_mode_entry(agent)
            lines.extend(mode_entry)

        return "\n".join(lines)

    def _generate_mode_entry(self, agent: PrimaryAgent) -> list[str]:
        """Generate a single mode entry for an agent.

        Args:
            agent: PrimaryAgent to generate entry for.

        Returns:
            List of lines for the mode entry.
        """
        lines = [
            f"  - slug: {agent.slug}",
            f"    name: {agent.display_name}",
            f"    description: {agent.description}",
            "    roleDefinition: |",
        ]

        # Add markdown body as literal block
        for line in agent.markdown_body.split("\n"):
            lines.append(f"      {line}")

        # Add groups based on permissions
        groups = self._map_permissions_to_groups(agent.permissions)
        if groups:
            lines.append("    groups:")
            for group in groups:
                lines.append(f"      - {group}")

        return lines

    def _map_permissions_to_groups(self, permissions: dict[str, PermissionLevel]) -> list[str]:
        """Map agent permissions to Kilo Code groups.

        Args:
            permissions: Dictionary of permission names to levels.

        Returns:
            List of group names for Kilo Code.
        """
        groups = []

        # Always include read
        groups.append("read")

        # Edit permission
        if permissions.get("edit") == PermissionLevel.ALLOW:
            groups.append("edit")

        # Bash/command permission
        if permissions.get("bash") == PermissionLevel.ALLOW:
            groups.append("command")

        # Webfetch/browser permission
        if permissions.get("webfetch") == PermissionLevel.ALLOW:
            groups.append("browser")

        # MCP tools
        if permissions.get("mcp") == PermissionLevel.ALLOW:
            groups.append("mcp")

        return groups
