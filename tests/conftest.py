"""Shared pytest fixtures for RiseOn.Agents tests."""

import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def agents_fixtures_dir(fixtures_dir: Path) -> Path:
    """Return the path to the test agent fixtures directory."""
    return fixtures_dir / "agents"


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests that need file system operations."""
    temp_path = Path(tempfile.mkdtemp())
    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def temp_agents_dir(temp_dir: Path, agents_fixtures_dir: Path) -> Path:
    """Copy agent fixtures to a temporary directory for modification tests."""
    agents_temp = temp_dir / "agents"
    if agents_fixtures_dir.exists():
        shutil.copytree(agents_fixtures_dir, agents_temp)
    else:
        agents_temp.mkdir(parents=True)
    return agents_temp


@pytest.fixture
def sample_primary_agent_yaml() -> str:
    """Sample YAML frontmatter for a primary agent."""
    return """---
name: test-agent
description: A test primary agent
tools:
  - read
  - edit
  - search
temperature: 0.1
steps: 40
permissions:
  edit: allow
  bash: deny
  webfetch: allow
handoffs:
  - agent: sub-agent-1
  - agent: sub-agent-2
---

# Test Agent

You are a test agent with the following capabilities:

## Core Expertise

- Testing
- Validation
"""


@pytest.fixture
def sample_subagent_yaml() -> str:
    """Sample YAML frontmatter for a subagent."""
    return """---
name: test-subagent
description: A test subagent
tools:
  - read
  - edit
temperature: 0.1
steps: 15
permissions:
  edit: allow
  bash: deny
mode: subagent
modelVariant: high
target: opencode
---

# Test Subagent

You are a specialized subagent for testing purposes.
"""


@pytest.fixture
def sample_skill_yaml() -> str:
    """Sample YAML frontmatter for a skill."""
    return """---
name: test-skill
description: A test skill for validation
license: MIT
---

# Test Skill

This skill provides testing capabilities.

## Usage

Use this skill when you need to test something.
"""


@pytest.fixture
def sample_rule_content() -> str:
    """Sample content for a rule file."""
    return """# Test Rule

This is a test rule that provides guidance for testing.

## Guidelines

1. Always write tests first
2. Keep tests focused and small
3. Use descriptive test names
"""
