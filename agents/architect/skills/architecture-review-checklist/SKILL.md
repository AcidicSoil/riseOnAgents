---
name: architecture-review-checklist
description: Comprehensive checklist for reviewing software architecture designs, identifying risks, gaps, and improvement opportunities. Use for architecture reviews, design validation, and quality gates.
---

# Architecture Review Checklist

A structured checklist for reviewing software architecture designs. Use this to identify risks, gaps, and improvement opportunities before implementation.

---

## When to Use This Skill

Use this skill when:
- Conducting architecture design reviews
- Validating system design before implementation
- Performing architecture compliance audits
- Reviewing ADRs (Architectural Decision Records)
- Pre-implementation quality gates
- Technical due diligence

---

## Review Categories

This checklist covers 10 review categories:

1. **Business Alignment** - Does it solve the right problem?
2. **Functional Completeness** - Does it meet all requirements?
3. **Scalability** - Can it handle growth?
4. **Performance** - Is it fast enough?
5. **Security** - Is it secure?
6. **Reliability** - Will it stay up?
7. **Maintainability** - Can we change it easily?
8. **Observability** - Can we understand its behavior?
9. **Cost** - Is it affordable?
10. **Implementation Feasibility** - Can we build it?

---

## 1. Business Alignment Review

### Problem-Solution Fit
- [ ] Problem statement is clear and documented
- [ ] Solution directly addresses the problem
- [ ] Business value is quantified
- [ ] Success criteria are defined and measurable

### Stakeholder Alignment
- [ ] All stakeholders identified
- [ ] Stakeholder requirements captured
- [ ] Conflicting requirements resolved
- [ ] Business sponsors committed

### Strategic Fit
- [ ] Aligned with company strategy
- [ ] Consistent with existing systems
- [ ] Supports future business initiatives
- [ ] Time-to-market is acceptable

### Review Questions
- What business problem does this solve?
- How do we measure success?
- What happens if we don't build this?
- Is this the right time to build this?

---

## 2. Functional Completeness Review

### Requirements Coverage
- [ ] All functional requirements addressed
- [ ] All user stories mapped to components
- [ ] Edge cases considered
- [ ] Error scenarios handled

### Integration Points
- [ ] All external integrations identified
- [ ] API contracts defined
- [ ] Data exchange formats specified
- [ ] Integration patterns chosen appropriately

### Data Requirements
- [ ] Data model complete
- [ ] Data sources identified
- [ ] Data retention requirements defined
- [ ] Data migration strategy (if applicable)

### Review Questions
- Are there any unaddressed requirements?
- What edge cases might break the system?
- How do we handle integration failures?
- Is the data model sufficient?

---

## 3. Scalability Review

### Capacity Planning
- [ ] Current load documented
- [ ] Growth projections documented
- [ ] Peak load scenarios identified
- [ ] Capacity headroom planned (e.g., 3x current load)

### Scaling Strategy
- [ ] Horizontal scaling supported
- [ ] Vertical scaling limits understood
- [ ] Auto-scaling configured
- [ ] Database scaling strategy defined

### Bottleneck Analysis
- [ ] Single points of failure identified
- [ ] Bottlenecks under load simulated
- [ ] Third-party service limits understood
- [ ] Backpressure mechanisms in place

### Review Questions
- What happens at 10x current load?
- Which component fails first?
- How quickly can we scale?
- What's the maximum capacity?

---

## 4. Performance Review

### Latency Targets
- [ ] Response time targets defined (p50, p95, p99)
- [ ] End-to-end latency budget allocated
- [ ] Network latency considered
- [ ] Database performance targets set

### Throughput Targets
- [ ] RPS (requests per second) target defined
- [ ] Data throughput target defined
- [ ] Concurrent user capacity defined

### Optimization Strategies
- [ ] Caching strategy defined
- [ ] Query optimization planned
- [ ] Async processing used where appropriate
- [ ] CDN usage planned (if applicable)

### Review Questions
- What's the acceptable response time?
- Which operations are performance-critical?
- How do we handle performance degradation?
- What's the performance testing strategy?

---

## 5. Security Review

### Authentication & Authorization
- [ ] Authentication mechanism appropriate
- [ ] MFA considered for sensitive operations
- [ ] Authorization model defined (RBAC, ABAC)
- [ ] Least privilege principle applied

### Data Protection
- [ ] Encryption in transit (TLS)
- [ ] Encryption at rest
- [ ] Key management strategy
- [ ] PII data identified and protected

### Threat Mitigation
- [ ] OWASP Top 10 addressed
- [ ] DDoS protection planned
- [ ] Rate limiting defined
- [ ] Input validation strategy

### Compliance
- [ ] Applicable regulations identified
- [ ] Compliance requirements documented
- [ ] Audit trail capability exists
- [ ] Data residency requirements met

### Review Questions
- What sensitive data is handled?
- What are the attack vectors?
- How do we detect security breaches?
- What compliance requirements apply?

---

## 6. Reliability Review

### Availability
- [ ] Availability target defined (e.g., 99.9%)
- [ ] Maintenance windows planned
- [ ] Deployment strategy defined
- [ ] Zero-downtime deployment capability

### Fault Tolerance
- [ ] Single points of failure eliminated
- [ ] Circuit breakers implemented
- [ ] Retry policies with backoff
- [ ] Graceful degradation strategy

### Disaster Recovery
- [ ] RTO (Recovery Time Objective) defined
- [ ] RPO (Recovery Point Objective) defined
- [ ] Backup strategy defined
- [ ] DR tested within last 6 months

### Review Questions
- What's the cost of downtime?
- How quickly can we recover?
- What data can't be lost?
- What happens if dependencies fail?

---

## 7. Maintainability Review

### Code Quality
- [ ] Modular design with clear boundaries
- [ ] Separation of concerns
- [ ] Code style guidelines defined
- [ ] Code review process defined

### Documentation
- [ ] Architecture documentation complete
- [ ] API documentation generated
- [ ] Runbooks for operations
- [ ] Onboarding documentation exists

### Testing
- [ ] Test coverage target defined (>80%)
- [ ] Test automation in CI/CD
- [ ] E2E tests for critical paths

### Technical Debt
- [ ] Technical debt tracked
- [ ] Refactoring planned
- [ ] Dependency updates automated

### Review Questions
- How easy is it to add features?
- How long to onboard a new developer?
- What's the technical debt level?
- How do we prevent debt accumulation?

---

## 8. Observability Review

### Logging
- [ ] Structured logging implemented
- [ ] Log levels defined appropriately
- [ ] Correlation IDs for tracing
- [ ] Sensitive data excluded from logs

### Metrics
- [ ] Business metrics defined
- [ ] Technical metrics defined
- [ ] Dashboards created
- [ ] Alerting thresholds defined

### Tracing
- [ ] Distributed tracing implemented
- [ ] Trace context propagation
- [ ] Sampling strategy (if high volume)

### Alerting
- [ ] Alert strategy defined
- [ ] On-call rotation defined
- [ ] Runbooks for common alerts
- [ ] Alert fatigue prevention

### Review Questions
- How do we know if the system is healthy?
- How do we debug production issues?
- What metrics matter to the business?
- How quickly can we detect issues?

---

## 9. Cost Review

### Infrastructure Costs
- [ ] Compute costs estimated
- [ ] Storage costs estimated
- [ ] Network costs estimated
- [ ] Third-party service costs estimated

### Operational Costs
- [ ] Team size estimated
- [ ] Maintenance effort estimated
- [ ] Support costs estimated

### Cost Optimization
- [ ] Right-sizing applied
- [ ] Auto-scaling for cost optimization
- [ ] Cost monitoring implemented
- [ ] Budget alerts configured

### ROI Analysis
- [ ] Business value quantified
- [ ] Cost-benefit analysis completed
- [ ] Alternative approaches compared

### Review Questions
- What's the total cost of ownership?
- What are the biggest cost drivers?
- How do costs scale with usage?
- Is this the most cost-effective solution?

---

## 10. Implementation Feasibility Review

### Team Capability
- [ ] Team has required skills
- [ ] Training needs identified
- [ ] Knowledge gaps addressed
- [ ] Team bandwidth sufficient

### Technology Risks
- [ ] Technology maturity assessed
- [ ] Proof-of-concept completed (if new tech)
- [ ] Vendor lock-in considered
- [ ] Exit strategy defined

### Timeline
- [ ] Implementation timeline realistic
- [ ] Dependencies identified
- [ ] Critical path understood
- [ ] Buffer for unknowns included

### Review Questions
- Does the team have the right skills?
- What are the technology risks?
- Is the timeline realistic?
- What could delay implementation?

---

## Risk Assessment Matrix

For each identified risk, document:

| Risk | Likelihood | Impact | Mitigation | Owner |
|------|------------|--------|------------|-------|
| {Risk description} | High/Med/Low | High/Med/Low | {How to mitigate} | {Who} |

### Risk Scoring
- **Critical**: High likelihood × High impact → Must address before implementation
- **High**: High likelihood × Medium impact OR Medium × High → Address in sprint 1
- **Medium**: Medium × Medium → Track and address
- **Low**: Any Low × any → Monitor

---

## Review Output Template

```markdown
# Architecture Review: {System Name}

## Summary
**Date:** {Review date}
**Reviewers:** {Names}
**Status:** ✅ Approved / ⚠️ Approved with conditions / ❌ Needs revision

## Overall Assessment
{2-3 paragraph summary}

## Category Scores
| Category | Score | Notes |
|----------|-------|-------|
| Business Alignment | ✅/⚠️/❌ | {Brief note} |
| Functional Completeness | ✅/⚠️/❌ | |
| Scalability | ✅/⚠️/❌ | |
| Performance | ✅/⚠️/❌ | |
| Security | ✅/⚠️/❌ | |
| Reliability | ✅/⚠️/❌ | |
| Maintainability | ✅/⚠️/❌ | |
| Observability | ✅/⚠️/❌ | |
| Cost | ✅/⚠️/❌ | |
| Feasibility | ✅/⚠️/❌ | |

## Critical Issues
{List any ❌ items with required actions}

## Recommendations
{List improvements and suggestions}

## Follow-up Actions
| Action | Owner | Due Date |
|--------|-------|----------|
| {Action} | {Who} | {When} |
```

---

## Related Skills

- **nfr-analysis-checklist** - Deep NFR analysis
- **security-architecture** - Security-specific review
- **performance-modeling** - Performance-specific review
- **cost-estimation** - Cost-specific analysis

---

## Usage Guidelines

### Before the Review
1. Distribute architecture documentation 48 hours in advance
2. Ensure all reviewers have read the documentation
3. Prepare specific questions for each category
4. Set up review meeting with right stakeholders

### During the Review
1. Walk through each category systematically
2. Document all questions and concerns
3. Score each category (✅/⚠️/❌)
4. Identify critical issues (must-fix before implementation)

### After the Review
1. Send review summary within 24 hours
2. Track action items to closure
3. Schedule follow-up if needed
4. Archive review for future reference

---

## Output Format

When using this skill, provide:
1. **Completed checklist** (all 10 categories)
2. **Risk assessment matrix**
3. **Category scores** (✅/⚠️/❌)
4. **Critical issues** (must-fix items)
5. **Recommendations** (improvements)
6. **Follow-up actions** (with owners and dates)
