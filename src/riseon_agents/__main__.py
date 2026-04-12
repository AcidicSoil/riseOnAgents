"""Entry point for running riseon-agents as a module.

Usage:
    python -m riseon_agents
    riseon-agents  (via script entry point)
"""

import sys


def main() -> int:
    """Main entry point for the CLI application."""
    from riseon_agents.app import KiloGeneratorApp

    app = KiloGeneratorApp()
    app.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
