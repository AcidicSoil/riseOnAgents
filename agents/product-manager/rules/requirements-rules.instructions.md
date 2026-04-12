---
description: Requirements analysis and management rules for eliciting, validating, and documenting functional and non-functional requirements
applyTo: '**/docs/product/**,**/docs/requirements/**,**/*.prd'
---

# Requirements Rules

Requirements analysis and management rules for eliciting, validating, documenting, and tracking functional and non-functional requirements.

## Requirements Documentation

### PRD (Product Requirements Document) Requirements
✅ **All PRDs must:**
- Have clear problem statement
- Define target users with personas
- Specify measurable success metrics
- Include functional requirements
- Include non-functional requirements
- List stakeholders and approvals
- Be version controlled
- Be stored in `/docs/product/`

### PRD Structure
```markdown
# Product Requirements: {Feature}

## Executive Summary
{Brief overview}

## Problem Statement
{What problem are we solving?}

## Target Users
{User personas}

## Business Goals
{Business objectives}

## Success Metrics
{Measurable KPIs}

## Functional Requirements
{What the system should do}

## Non-Functional Requirements
{Performance, security, usability}

## User Stories
{Link to stories document}

## Out of Scope
{What is explicitly not included}

## Open Questions
{Decisions pending}

## Timeline
{Target dates}

## Stakeholders
{Key stakeholders}

## Sign-off
{Approvals}
```

## Requirements Quality Standards

### Clarity
✅ **Requirements must be:**
- Unambiguous (single interpretation)
- Clear and concise
- Free of technical jargon
- Written in active voice
- Understandable by all stakeholders

❌ **Avoid:**
- Vague terms (user-friendly, robust)
- Ambiguous pronouns
- Undefined acronyms
- Passive voice
- Technical implementation details

### Completeness
✅ **Requirements must include:**
- All scenarios (happy path, error paths, edge cases)
- All data elements defined
- All error conditions addressed
- All external interfaces specified
- All constraints identified

### Consistency
✅ **Requirements must be:**
- Internally consistent (no conflicts)
- Terminology consistent
- Format consistent
- Aligned with business goals
- Aligned with other requirements

### Testability
✅ **Requirements must have:**
- Measurable criteria
- Observable outcomes
- Verifiable conditions
- Clear acceptance criteria
- Quantifiable targets

**Good:**
- "System shall respond within 200ms for 95% of requests"
- "System shall support 1000 concurrent users"

**Bad:**
- "System shall be fast"
- "System shall handle many users"

### Traceability
✅ **All requirements must:**
- Have unique identifier (FR-001, NFR-001)
- Be traceable to source
- Be traceable to test cases
- Track changes and versions
- Link to related requirements

## Requirements Elicitation

### Stakeholder Identification
✅ **Must identify:**
- Primary stakeholders (sponsors, users)
- Secondary stakeholders (support, operations)
- Tertiary stakeholders (compliance, legal)
- Decision makers
- Influencers

### Elicitation Techniques
✅ **Use appropriate techniques:**
- **Interviews**: For individual perspectives
- **Workshops**: For group consensus
- **Surveys**: For broad input
- **Observation**: For current process understanding
- **Document Analysis**: For existing systems

### Requirements Validation
✅ **Must validate:**
- Requirements reviewed by stakeholders
- Requirements reviewed by technical team
- Acceptance criteria defined
- Testability verified
- Feasibility confirmed

## Requirements Categorization

### Functional Requirements
**Format:**
```
FR-XXX: {Requirement Name}
The system shall {action} {object} {condition}

Example:
FR-001: User Authentication
The system shall authenticate users via SSO when accessing the application.
```

**Categories:**
- Business transactions
- Data management
- Administrative functions
- Reporting
- Integrations
- User interactions

### Non-Functional Requirements
**Format:**
```
NFR-XXX: {Requirement Name}
Category: {Performance/Security/Usability}
Target: {measurable target}
Priority: {Must/Should/Could}
```

**Categories:**
- **Performance**: Response time, throughput
- **Security**: Authentication, authorization, encryption
- **Usability**: Accessibility, learnability
- **Reliability**: Availability, fault tolerance
- **Maintainability**: Modularity, testability
- **Compliance**: Regulatory, standards

## Requirements Prioritization

### MoSCoW Method
**Must Have (60% of effort):**
- Critical for success
- Non-negotiable
- Legal/regulatory requirements
- No workaround exists

**Should Have (20% of effort):**
- Important for success
- Significant value add
- Workaround exists but inconvenient

**Could Have (20% of effort):**
- Desirable but not necessary
- Low impact if omitted
- Can be deferred

**Won't Have:**
- Explicitly excluded
- Documented for future
- Low priority

### Prioritization Criteria
✅ **Consider:**
- Business value
- User impact
- Risk reduction
- Technical dependencies
- Regulatory requirements
- Cost of delay

## Requirements Management

### Change Management
✅ **All changes must:**
- Be documented with rationale
- Be approved by stakeholders
- Assess impact on timeline/cost
- Update related requirements
- Update test cases
- Be version controlled

### Change Request Format
```markdown
## Change Request: CR-XXX

**Requirement**: {ID and name}
**Requested By**: {Stakeholder}
**Date**: {Date}

**Description**: {What is changing}

**Rationale**: {Why the change is needed}

**Impact Analysis**:
- Timeline: {Impact}
- Cost: {Impact}
- Other Requirements: {Impact}
- Tests: {Impact}

**Approval**:
- Product Manager: {Name, Date}
- Technical Lead: {Name, Date}
- Stakeholder: {Name, Date}
```

### Version Control
✅ **Must track:**
- Version number
- Change date
- Change author
- Change description
- Approval status

## Requirements Review

### Review Process
1. **Preparation**: Distribute requirements in advance
2. **Individual Review**: Stakeholders review independently
3. **Review Meeting**: Walk through requirements
4. **Issue Capture**: Document feedback and issues
5. **Resolution**: Address all issues
6. **Sign-off**: Obtain approval

### Review Checklist
- [ ] Clear and unambiguous
- [ ] Complete and consistent
- [ ] Testable and verifiable
- [ ] Feasible and realistic
- [ ] Aligned with business goals
- [ ] Properly prioritized
- [ ] Dependencies identified
- [ ] Risks documented
- [ ] Stakeholders identified

### Review Participants
✅ **Must include:**
- Product Manager (owner)
- Business stakeholders
- Technical team representatives
- QA representatives
- Operations representatives (if applicable)

## Common Requirements Issues

### Ambiguity
**Symptoms:**
- Vague terms
- Multiple interpretations
- Unclear conditions

**Fix:**
- Use precise language
- Define all terms
- Specify conditions
- Add examples

### Incompleteness
**Symptoms:**
- Missing scenarios
- Undefined data elements
- Unspecified error handling

**Fix:**
- Use checklists
- Review use cases
- Ask probing questions
- Document assumptions

### Gold Plating
**Symptoms:**
- Requirements beyond scope
- Nice-to-have treated as must-have
- Unnecessary features

**Fix:**
- Validate against business goals
- Challenge each requirement
- Apply prioritization
- Get stakeholder buy-in

### Scope Creep
**Symptoms:**
- Continuous additions
- Expanding requirements
- Timeline slippage

**Fix:**
- Enforce change management
- Revisit priorities
- Communicate impact
- Get formal approval

## References

- [Software Requirements](https://www.oreilly.com/library/view/software-requirements-3rd/9780735679665/) - Karl Wiegers
- [Writing Effective Use Cases](https://www.oreilly.com/library/view/writing-effective-use/0201702258/) - Alistair Cockburn
- [Requirements Engineering](https://www.oreilly.com/library/view/requirements-engineering/9781119954200/) - Chris Rupp
- [BABOK Guide](https://www.iiba.org/career-resources/a-business-professionals-guide-to-the-babok-guide/) - IIBA

## MCP Integrations & Tools Required

**Always use available MCPs** when implementing or verifying rules:
- 🎯 Use **GitHub MCP** to find existing codebase examples matching this rule
- 🎯 Use **Brave Search MCP** to lookup latest documentation or official best practices
- 🎯 Use **Context7 MCP** to query historical context related to codebase structure before making decisions
