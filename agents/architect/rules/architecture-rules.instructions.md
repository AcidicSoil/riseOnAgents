---
description: Architecture rules and guidelines for documentation, ADRs, diagrams, and review processes
applyTo: '**/*.md,**/*.adr,**/docs/architecture/**,**/docs/diagrams/**'
---

# Architecture Rules

Rules and guidelines for architectural documentation, decision records, diagrams, and review processes.

## ADR (Architectural Decision Records) Requirements

### Format Requirements
✅ **All ADRs must:**
- Use standard ADR format with front matter
- Be saved in `/docs/adr/` directory
- Follow naming convention: `adr-NNNN-[title-slug].md`
- Include sequential 4-digit numbering (0001, 0002, ...)
- Have clear status (Proposed, Accepted, Rejected, Superseded, Deprecated)
- Document context, decision, and consequences
- List alternatives considered with rejection rationale
- Include implementation notes when applicable
- Reference related ADRs

### ADR Review Process
1. **Author creates ADR** with proposed status
2. **Team review** within 5 business days
3. **Architecture Review Board** approval (if required)
4. **Status updated** to Accepted/Rejected
5. **Implementation** begins after acceptance
6. **Review after implementation** (post-mortem if needed)

## Diagram Standards

### Required Diagrams
All architecture documentation **must** include:

1. **System Context Diagram** (C4 Level 1)
   - Shows system boundary
   - External actors and systems
   - High-level interactions

2. **Container Diagram** (C4 Level 2)
   - Major technical containers
   - Technology choices
   - Communication protocols

3. **Deployment Diagram**
   - Physical/logical deployment
   - Infrastructure components
   - Environment separation

### Diagram Requirements
✅ **All diagrams must:**
- Use Mermaid syntax (renders in Markdown)
- Have clear, descriptive titles
- Include legend/key for complex diagrams
- Use consistent styling across all diagrams
- Have accompanying explanations
- Be saved in `/docs/diagrams/` as `.mmd` files (standalone)
- Be embedded in architecture documentation

### Prohibited Practices
❌ **Do NOT:**
- Mix C4 levels in same diagram
- Use proprietary diagram formats only (Visio, draw.io without export)
- Create diagrams without explanations
- Use unclear abbreviations without legend
- Create outdated diagrams (keep synchronized with implementation)

## Documentation Requirements

### Architecture Documentation Location
All architecture documentation **must** be saved in:
- `/docs/architecture/` - Main architecture documents
- `/docs/adr/` - Architectural Decision Records
- `/docs/diagrams/` - Standalone diagram files
- `/docs/domain/` - Domain model documentation
- `/docs/microservices/` - Microservices documentation
- `/docs/security/` - Security architecture

### Documentation Structure
Main architecture document **must** include:
1. Executive Summary
2. Business Context
3. System Context Diagram
4. Architecture Overview
5. Container Architecture
6. Component Architecture (for critical containers)
7. Deployment Architecture
8. Key Workflows (sequence diagrams)
9. Data Architecture
10. NFR Analysis (Scalability, Performance, Security, Reliability, Maintainability, Observability)
11. Architectural Decisions (links to ADRs)
12. Risks and Mitigations
13. Trade-offs
14. Technology Stack
15. Next Steps

### Documentation Quality
✅ **All documentation must:**
- Use clear, professional language
- Define technical terms (include glossary if needed)
- Include visual aids (diagrams over text)
- Provide examples for complex concepts
- Be version controlled (Git)
- Include table of contents for documents >10 pages
- Link related documents (ADRs, diagrams, specs)
- Be kept up-to-date with implementation

## Review Process

### Architecture Review Triggers
**Required reviews for:**
- New system architecture
- Major architectural changes
- Technology stack changes
- NFR target changes
- Security architecture changes
- Integration with external systems

### Review Checklist
Reviewers **must** verify:
- [ ] ADRs created for significant decisions
- [ ] All required diagrams present and accurate
- [ ] NFR analysis complete
- [ ] Security considerations addressed
- [ ] Risks identified with mitigations
- [ ] Trade-offs documented
- [ ] Documentation follows standards
- [ ] Implementation plan exists
- [ ] Team alignment achieved

### Review Approval
- **Minor changes**: Team lead approval
- **Major changes**: Architecture Review Board
- **Security changes**: Security team + ARB
- **NFR changes**: Stakeholder approval

## NFR Documentation Requirements

@reference Rules/_shared/nfr-framework.md

### NFR Targets
All NFR targets **must** be:
- **Specific**: Clear, unambiguous
- **Measurable**: Quantifiable metrics
- **Achievable**: Realistic given constraints
- **Relevant**: Aligned with business goals
- **Time-bound**: With timeline if applicable

## Technology Stack Documentation

### Required Information
For each technology in the stack:
- **Name and version** (exact version, not "latest")
- **Purpose**: Why this technology was chosen
- **Alternatives considered**: Other options evaluated
- **License**: Open-source or commercial
- **Support**: Vendor/community support status
- **End of life**: Known EOL dates
- **Upgrade path**: Version upgrade strategy

### Technology Standards
✅ **Approved technologies**: Use standard list (maintained separately)
⚠️ **New technologies**: Require ADR and ARB approval
❌ **Prohibited technologies**: Security/compliance restrictions

## Compliance and Audit

### Audit Trail
All architectural decisions **must** have:
- ADR with decision date and authors
- Review meeting notes (if applicable)
- Approval records
- Implementation status

### Documentation Retention
- Keep all ADRs indefinitely (even superseded)
- Maintain architecture history
- Document migrations and transitions
- Archive old versions properly

## Tools and Templates

### Recommended Tools
- **Diagrams**: Mermaid (preferred), PlantUML, Structurizr
- **Documentation**: Markdown, AsciiDoc
- **Version Control**: Git
- **Review**: GitHub/GitLab pull requests
- **Storage**: Repository `/docs` directory

### Templates Available
- ADR template: `/templates/adr-template.md`
- Architecture document template: `/templates/architecture-template.md`
- Diagram templates: `/templates/diagrams/`
- Review checklist: `/templates/review-checklist.md`

## Enforcement

### Compliance Checks
- **Automated**: CI/CD checks for documentation presence
- **Manual**: Architecture Review Board audits
- **Periodic**: Quarterly documentation reviews

### Non-Compliance Handling
1. **First occurrence**: Warning and guidance
2. **Repeated**: Required remediation plan
3. **Persistent**: Escalation to management

## References

- [ADR GitHub](https://adr.github.io/) - ADR format reference
- [C4 Model](https://c4model.com/) - Architecture diagrams
- [Mermaid Documentation](https://mermaid.js.org/) - Diagram syntax
- [ISO 25010](https://iso25000.com/) - Quality model
- [Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/) - Architecture best practices

## MCP Integrations & Tools Required

**Always use available MCPs** when implementing or verifying rules:
- 🎯 Use **GitHub MCP** to find existing codebase examples matching this rule
- 🎯 Use **Brave Search MCP** to lookup latest documentation or official best practices
- 🎯 Use **Context7 MCP** to query historical context related to codebase structure before making decisions
