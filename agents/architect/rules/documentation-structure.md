## Documentation Structure

Structure the `{app}_Architecture.md` file as follows:

```markdown
# {Application Name} - Architecture Plan

## Executive Summary
Brief overview of the system, business goals, and architectural approach

## Business Context
- Problem statement
- Business objectives
- Key stakeholders
- Success criteria

## System Context
[Mermaid C4Context diagram]
[Explanation of system boundary and external actors]

## Architecture Overview
- Architectural patterns used
- Key design decisions
- Technology stack summary

## Container Architecture
[Mermaid C4Container diagram]
[Detailed explanation of each container]

## Component Architecture
[Mermaid C4Component diagrams for critical containers]
[Component responsibilities and relationships]

## Deployment Architecture
[Mermaid C4Deployment diagram]
[Infrastructure components and environments]

## Key Workflows
[Mermaid sequence diagrams for critical use cases]
[Step-by-step workflow explanations]

## Data Architecture
- Data model overview
- Database selection rationale
- Data flow diagrams
- Data retention policies

## Non-Functional Requirements Analysis

### Scalability
[How the architecture supports scaling]

### Performance
[Performance characteristics and optimizations]

### Security
[Security architecture and controls]

### Reliability
[HA, DR, fault tolerance measures]

### Maintainability
[Design for maintainability]

### Observability
[Logging, monitoring, tracing strategy]

## Architectural Decisions
- [ADR-0001: Key Decision 1](/docs/adr/adr-0001-decision-1.md)
- [ADR-0002: Key Decision 2](/docs/adr/adr-0002-decision-2.md)

## Risks and Mitigations
[Identified risks with mitigation strategies]

## Trade-offs
[Architectural trade-offs and rationale]

## Technology Stack
[Detailed technology choices with versions and rationale]

## Migration Strategy (if applicable)
[Phased approach from current to target architecture]

## Next Steps
[Recommended actions for implementation teams]

## References
[Links to related documentation, standards, frameworks]
```
