<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version Change: 1.0.0 → 1.1.0 (Technology stack update)
Modified Principles: None
Modified Sections:
  - Technology Standards: Updated to Python/Textual stack
  - Supported Platforms: Added Kilo Code, Windsurf
  - Code Quality: Changed from TypeScript to Python tooling
Added Sections: None
Removed Sections: None
Templates Requiring Updates: None
Follow-up TODOs: None
================================================================================
-->

# RiseOn.Agents Constitution

## Core Principles

### I. Documentation-First Development

All agent configurations, skills, and integrations MUST be based on **official documentation** from AI coding platforms (GitHub Copilot, OpenCode, Cursor, Windsurf, etc.).

- Agent definitions MUST reference official platform specifications
- Skills MUST implement patterns documented by platform vendors
- Configuration schemas MUST follow platform-defined standards
- Breaking changes in platform documentation MUST trigger agent review
- Unofficial or undocumented patterns are PROHIBITED in production agents

**Rationale**: Official documentation ensures stability, maintainability, and compatibility with platform updates. Undocumented features may break without warning.

### II. Modern TUI Design (NON-NEGOTIABLE)

All Text User Interface (TUI) components MUST be modern, intuitive, and visually appealing.

- Use Textual/Rich framework (Python) for all TUI components
- Implement responsive layouts that adapt to terminal dimensions
- Provide clear visual feedback for all user actions
- Use consistent color schemes and styling across all interfaces
- Include keyboard navigation with discoverable shortcuts
- Display progress indicators for long-running operations
- Error states MUST be clearly distinguishable with actionable guidance

**Rationale**: Modern TUI design improves developer experience, reduces cognitive load, and increases adoption rates for AI coding tools.

### III. Phase-Based Validation (NON-NEGOTIABLE)

Every development phase MUST include explicit user validation and practical testing.

- Phase completion REQUIRES user sign-off before proceeding
- Each phase MUST produce testable, demonstrable artifacts
- Validation criteria MUST be defined BEFORE implementation begins
- Practical tests MUST exercise real user workflows, not just unit tests
- Validation results MUST be documented with evidence (screenshots, logs, demos)
- Rollback procedures MUST be defined for failed validations

**Rationale**: Early validation prevents accumulated technical debt and ensures features meet actual user needs before significant investment.

### IV. Test-First Development

TDD (Test-Driven Development) is mandatory for all agent features and skills.

- Tests MUST be written and approved BEFORE implementation
- Tests MUST fail initially (Red-Green-Refactor cycle)
- Contract tests MUST verify agent-to-agent communication
- Integration tests MUST validate complete user journeys
- Acceptance tests MUST map to specification acceptance criteria

**Rationale**: Test-first ensures requirements are understood before coding and creates a safety net for refactoring.

### V. Agent Modularity

Agents, skills, and subagents MUST be self-contained and independently deployable.

- Each agent MUST have a clear, single responsibility
- Skills MUST be reusable across multiple agents
- Subagents MUST be invokable without parent agent context
- Dependencies between agents MUST be explicit and versioned
- Circular dependencies between agents are PROHIBITED

**Rationale**: Modularity enables independent testing, deployment, and maintenance of individual components.

### VI. Observability and Traceability

All agent operations MUST be observable and traceable.

- Structured logging MUST be implemented for all agent actions
- Handoffs between agents MUST include context preservation
- Decision paths MUST be auditable (why did the agent choose X?)
- Performance metrics MUST be collected for optimization
- Error traces MUST include sufficient context for debugging

**Rationale**: AI agents require explainability for trust and debugging. Users must understand why recommendations were made.

### VII. Simplicity Over Complexity

Start simple and add complexity only when justified.

- YAGNI (You Aren't Gonna Need It) principle applies
- Complexity MUST be justified with documented rationale
- Abstractions MUST solve proven problems, not anticipated ones
- Configuration options MUST have sensible defaults
- Agent capabilities MUST be incrementally enabled

**Rationale**: Simple solutions are easier to maintain, debug, and extend. Premature complexity is a common cause of project failure.

## Technology Standards

### Agent Definition Format

- YAML frontmatter for metadata (name, description, tools, permissions)
- Markdown body for instructions and context
- Skills referenced via `@reference` or file paths
- Handoffs explicitly declared in frontmatter

### Supported Platforms

All agents MUST be compatible with:

- **Kilo Code**: JetBrains IDEs
- **OpenCode**: Terminal/CLI
- **GitHub Copilot**: VS Code, JetBrains
- **Windsurf**: Windsurf Editor

Platform-specific features MUST be gracefully degraded when unavailable.

### Code Quality

- Python 3.11+ for TUI application
- Textual/Rich for terminal user interface
- Markdown for documentation and agent definitions
- YAML for configuration and metadata
- Linting MUST pass before commits (Ruff, Black)
- Type hints MUST be used and validated with mypy

## Development Workflow

### Feature Development Lifecycle

1. **Specification**: Define user stories and acceptance criteria
2. **Planning**: Create technical design with architecture decisions
3. **Task Breakdown**: Decompose into independently testable tasks
4. **Implementation**: TDD with phase-based validation gates
5. **Review**: Code review with constitution compliance check
6. **Validation**: User acceptance testing with practical exercises
7. **Documentation**: Update agent files and guidelines

### Phase Gates

Each phase MUST pass these gates before proceeding:

| Phase | Gate Criteria |
|-------|---------------|
| Specification | User stories approved, acceptance criteria defined |
| Planning | Architecture review passed, complexity justified |
| Tasks | Dependencies mapped, parallel opportunities identified |
| Implementation | Tests passing, TUI rendering correctly |
| Review | PR approved, no constitution violations |
| Validation | User sign-off obtained, demo completed |

### Commit Standards

- Conventional commits format: `type(scope): description`
- Types: feat, fix, docs, style, refactor, test, chore
- Scope: agent name, skill name, or component
- Description: imperative mood, lowercase, no period

## Governance

### Constitution Authority

This constitution supersedes all other development practices. When conflicts arise:

1. Constitution principles take precedence
2. Amendments require documented rationale
3. Temporary exceptions require explicit approval and expiration date

### Amendment Process

1. Propose change with rationale in PR
2. Review impact on existing agents and workflows
3. Update all affected templates and documentation
4. Increment constitution version appropriately
5. Communicate changes to all contributors

### Versioning Policy

- **MAJOR**: Backward-incompatible principle changes
- **MINOR**: New principles or expanded guidance
- **PATCH**: Clarifications and typo fixes

### Compliance Review

- All PRs MUST include constitution compliance checklist
- Violations MUST be resolved or explicitly justified
- Regular audits of existing agents for compliance drift

**Version**: 1.1.0 | **Ratified**: 2026-03-29 | **Last Amended**: 2026-03-29
