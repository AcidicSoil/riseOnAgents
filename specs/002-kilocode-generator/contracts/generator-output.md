# Generator Output Contracts

**Feature Branch**: `002-kilocode-generator`  
**Date**: 2026-03-30

This document defines the output format contracts for generated Kilo Code configuration files.

## 1. Custom Modes File

### File: `custom_modes.yaml`

**Location**:
- Local: `./.kilo/custom_modes.yaml` (project root)
- Global: `~/.kilocode/custom_modes.yaml`

**Schema**:
```yaml
# RiseOn.Agents Generated Configuration
# Generated: {ISO_TIMESTAMP}
# Source: {AGENTS_FOLDER_PATH}

customModes:
  - slug: {agent_name}
    name: {Agent Display Name}
    description: {agent_description}
    roleDefinition: |
      {markdown_body}
    whenToUse: {optional_when_to_use}
    customInstructions: |
      {optional_custom_instructions}
    groups:
      - read
      - edit  # or with restrictions
      - command  # if bash allowed
      - browser  # if webfetch allowed
      - mcp  # if mcp tools used
```

**Example Output**:
```yaml
# RiseOn.Agents Generated Configuration
# Generated: 2026-03-30T14:30:00Z
# Source: /home/user/projects/riseon/agents

customModes:
  - slug: architect
    name: Architect
    description: Senior software architect specialist in DDD, microservices, governance, ADR, and Mermaid diagrams
    roleDefinition: |
      # Senior Software Architect Agent
      
      You are a Senior Software Architect with deep expertise in:
      
      ## Core Expertise
      
      - **Domain-Driven Design (DDD)**: Strategic design...
    groups:
      - read
      - - edit
        - fileRegex: .*
          description: All files
      - browser
      - mcp
```

**Mapping Rules**:

| RiseOn.Agents Field | Kilo Code Field | Transformation |
|---------------------|-----------------|----------------|
| `name` | `slug` | lowercase, hyphens |
| `name` | `name` | title case, spaces |
| `description` | `description` | as-is |
| markdown body | `roleDefinition` | as-is, literal block |
| `tools` + `permissions` | `groups` | see Tool Mapping |

**Tool Mapping**:

| RiseOn tools | Kilo groups | Condition |
|--------------|-------------|-----------|
| `read`, `search` | `read` | always |
| `edit` | `edit` | if `permissions.edit != deny` |
| `bash` | `command` | if `permissions.bash != deny` |
| `webfetch` | `browser` | if `permissions.webfetch != deny` |
| `mcp` | `mcp` | if in tools list |

## 2. Subagent Files

### File: `.kilo/agents/{agent-name}.md`

**Location**:
- Local: `./.kilo/agents/{agent-name}.md`
- Global: `~/.kilocode/agents/{agent-name}.md`

**Schema**:
```yaml
---
# RiseOn.Agents Generated Subagent
# Source: {SOURCE_FILE_PATH}
description: {agent_description}
mode: subagent
temperature: {temperature}
permission:
  edit: {allow|ask|deny}
  bash: {allow|ask|deny}
---

{markdown_body}
```

**Example Output**:
```yaml
---
# RiseOn.Agents Generated Subagent
# Source: agents/architect/subagents/adr-generator.agent.md
description: Expert agent for creating comprehensive Architectural Decision Records (ADRs) with structured formatting optimized for AI consumption and human readability.
mode: subagent
temperature: 0.1
permission:
  edit: allow
  bash: deny
---

# ADR Generator Agent

You are an expert in architectural documentation, this agent creates well-structured, comprehensive Architectural Decision Records...
```

**Mapping Rules**:

| RiseOn.Agents Field | Kilo Code Field | Transformation |
|---------------------|-----------------|----------------|
| `name` | filename | `{name}.md` |
| `description` | `description` | as-is |
| `mode` | `mode` | always "subagent" |
| `temperature` | `temperature` | as-is (default 0.1) |
| `permissions` | `permission` | key mapping |
| markdown body | document body | as-is |

**Permission Mapping**:

| RiseOn Permission | Kilo Permission |
|-------------------|-----------------|
| `permissions.edit: allow` | `permission.edit: allow` |
| `permissions.edit: deny` | `permission.edit: deny` |
| `permissions.bash: allow` | `permission.bash: allow` |
| `permissions.bash: deny` | `permission.bash: deny` |

## 3. Rule Files

### Shared Rules: `.kilo/rules/{rule-name}.md`

**Location**:
- Local: `./.kilo/rules/{rule-name}.md`
- Global: `~/.kilocode/rules/{rule-name}.md`

**Schema**:
```markdown
# {Rule Name}

{rule_content}
```

**Transformation**: Copy as-is, preserving markdown formatting.

### Mode-Specific Rules: `.kilo/rules-{mode}/{rule-name}.md`

**Location**:
- Local: `./.kilo/rules-{mode-slug}/{rule-name}.md`
- Global: `~/.kilocode/rules-{mode-slug}/{rule-name}.md`

**Schema**: Same as shared rules.

**Transformation**: Copy as-is, placing in mode-specific directory.

## 4. Skill Files

### Skill Directory: `.kilocode/skills/{skill-name}/`

**Location**:
- Local: `./.kilocode/skills/{skill-name}/SKILL.md`
- Global: `~/.kilocode/skills/{skill-name}/SKILL.md`

**Schema**:
```yaml
---
name: {skill-name}
description: {skill_description}
license: {optional_license}
metadata:
  source: riseon-agents
  generated: {ISO_TIMESTAMP}
---

{skill_content}
```

**Directory Structure**:
```
skills/{skill-name}/
├── SKILL.md           # Required
├── scripts/           # Copied if exists
├── references/        # Copied if exists
└── assets/            # Copied if exists
```

**Transformation**:
1. Copy SKILL.md with added `metadata.source` and `metadata.generated`
2. Copy subdirectories (scripts/, references/, assets/) if present
3. Preserve all file permissions

## 5. Validation Contracts

### YAML Validation

All generated YAML files MUST:
- Pass PyYAML safe_load without errors
- Use consistent 2-space indentation
- Use literal block scalars (`|`) for multi-line strings
- Not exceed 80 characters per line (soft limit)

### Markdown Validation

All generated Markdown files MUST:
- Have valid YAML frontmatter (if present)
- Use proper heading hierarchy (no skipped levels)
- Have no broken internal links

### File System Validation

All generated files MUST:
- Use UTF-8 encoding
- Use Unix line endings (LF)
- Have mode 0644 (readable by all, writable by owner)
- Directories have mode 0755

## 6. Idempotency Contract

Running generation multiple times with the same input MUST produce identical output (excluding timestamps in comments).

**Idempotent Elements**:
- File structure
- File content (except generation timestamp)
- File ordering in custom_modes.yaml

**Non-Idempotent Elements**:
- Generation timestamp in comments
- File modification timestamps

## 7. Error Contracts

### Invalid Agent Definition

**Input**: Agent file with malformed YAML frontmatter

**Behavior**:
- Skip the invalid agent
- Log warning with file path and error
- Continue processing other agents
- Include warning in generation summary

**Output**: No file generated for invalid agent

### Missing Required Field

**Input**: Agent file missing `name` or `description`

**Behavior**:
- Skip the invalid agent
- Log specific missing field
- Continue processing other agents

### File Write Failure

**Input**: Cannot write to target path

**Behavior**:
- Stop generation
- Report which file failed
- List files already written
- Do not rollback already-written files (atomic per-file writes)
