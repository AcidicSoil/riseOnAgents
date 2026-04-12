---
name: nfr-analysis-checklist
description: Comprehensive checklist for analyzing Non-Functional Requirements (NFRs) including scalability, performance, security, reliability, maintainability, observability, and cost.
---

# NFR Analysis Checklist

A structured checklist for analyzing and documenting Non-Functional Requirements (NFRs) in software architecture. Use this to ensure all quality attributes are considered.

---

## When to Use This Skill

Use this skill when:
- Creating architecture documentation
- Reviewing system design
- Creating ADRs for technology choices
- Planning system evolution
- Conducting architecture reviews
- Estimating project effort

---

## NFR Categories

This checklist covers 7 NFR categories:

1. **Scalability** - Ability to handle growth
2. **Performance** - Speed and responsiveness
3. **Security** - Protection against threats
4. **Reliability** - Uptime and fault tolerance
5. **Maintainability** - Ease of changes and updates
6. **Observability** - Monitoring and debugging capability
7. **Cost Efficiency** - Financial sustainability

---

## 1. Scalability Checklist

### Capacity Planning
- [ ] Current load estimated (requests/second, data volume, users)
- [ ] Expected growth rate (monthly/yearly)
- [ ] Peak vs. average load ratio understood
- [ ] Seasonal patterns identified

### Scaling Strategy
- [ ] Horizontal vs. vertical scaling decision made
- [ ] Load balancing approach defined
- [ ] Auto-scaling triggers and policies defined
- [ ] Database scaling strategy (sharding, replication, partitioning)
- [ ] Caching layers and strategies planned

### Bottlenecks
- [ ] Single points of failure identified
- [ ] Database bottlenecks analyzed
- [ ] Network bandwidth considered
- [ ] Third-party service limits understood

### Questions to Ask
- What happens if traffic increases 10x tomorrow?
- Which components will fail first under load?
- How long does it take to scale up?
- What's the maximum theoretical capacity?

---

## 2. Performance Checklist

### Latency Requirements
- [ ] Response time targets defined (p50, p95, p99)
- [ ] End-to-end latency budget allocated per component
- [ ] Network latency considered (cross-region, CDN)
- [ ] Database query performance targets set

### Throughput Requirements
- [ ] Requests per second (RPS) target defined
- [ ] Data processing rate defined (records/second)
- [ ] Concurrent user capacity defined
- [ ] Batch processing throughput defined (if applicable)

### Optimization Strategies
- [ ] Caching strategy defined (what, where, how long)
- [ ] Database query optimization planned
- [ ] Async processing opportunities identified
- [ ] CDN usage planned (if applicable)
- [ ] Connection pooling configured

### Monitoring
- [ ] Performance metrics identified
- [ ] Baseline measurements planned
- [ ] Alerting thresholds defined
- [ ] Performance testing strategy defined

### Questions to Ask
- What's the acceptable response time for users?
- Which operations are performance-critical?
- What's the performance budget per API call?
- How will performance degrade under load?

---

## 3. Security Checklist

### Authentication
- [ ] Authentication mechanism defined (OAuth, JWT, SAML, etc.)
- [ ] Multi-factor authentication (MFA) requirements defined
- [ ] Session management strategy defined
- [ ] Password policies defined
- [ ] API authentication strategy defined

### Authorization
- [ ] Authorization model defined (RBAC, ABAC, etc.)
- [ ] Role hierarchy defined
- [ ] Permission granularity defined
- [ ] Cross-tenant isolation verified (if multi-tenant)

### Data Protection
- [ ] Encryption in transit (TLS version defined)
- [ ] Encryption at rest (algorithm defined)
- [ ] Key management strategy defined
- [ ] PII data identified and protected
- [ ] Secrets management approach defined

### Threat Mitigation
- [ ] OWASP Top 10 addressed
- [ ] DDoS protection planned
- [ ] Rate limiting defined
- [ ] Input validation strategy defined
- [ ] SQL injection prevention verified
- [ ] XSS prevention verified
- [ ] CSRF protection implemented

### Compliance
- [ ] GDPR requirements considered (if applicable)
- [ ] LGPD requirements considered (if applicable)
- [ ] HIPAA requirements considered (if applicable)
- [ ] PCI-DSS requirements considered (if applicable)
- [ ] SOC 2 requirements considered (if applicable)
- [ ] Industry-specific regulations identified

### Questions to Ask
- What sensitive data does the system handle?
- What are the consequences of a data breach?
- What compliance requirements apply?
- How are secrets managed in development vs. production?

---

## 4. Reliability Checklist

### Availability
- [ ] Availability target defined (e.g., 99.9%, 99.99%)
- [ ] Maintenance windows planned
- [ ] Deployment strategy defined (blue-green, canary, rolling)
- [ ] Zero-downtime deployment capability verified

### Fault Tolerance
- [ ] Single points of failure eliminated
- [ ] Circuit breakers implemented
- [ ] Retry policies defined (with backoff)
- [ ] Bulkhead isolation implemented
- [ ] Graceful degradation strategy defined

### Disaster Recovery
- [ ] RTO (Recovery Time Objective) defined
- [ ] RPO (Recovery Point Objective) defined
- [ ] Backup strategy defined (frequency, retention)
- [ ] Restore procedure tested
- [ ] Failover mechanism tested
- [ ] DR site/region identified

### Data Integrity
- [ ] Transaction management strategy defined
- [ ] Data validation on input
- [ ] Idempotency guarantees defined
- [ ] Data consistency model defined (strong, eventual)

### Questions to Ask
- What's the cost of downtime per hour?
- How quickly must the system recover?
- What data can't be lost?
- What happens if a dependency fails?

---

## 5. Maintainability Checklist

### Code Organization
- [ ] Modular design with clear boundaries
- [ ] Separation of concerns enforced
- [ ] Code style guidelines defined
- [ ] Code review process defined

### Documentation
- [ ] Architecture documentation up-to-date
- [ ] API documentation generated
- [ ] Runbooks for common operations
- [ ] Onboarding documentation exists

### Testing
- [ ] Unit test coverage target defined (>80%)
- [ ] Integration test coverage defined
- [ ] E2E tests for critical paths
- [ ] Test automation in CI/CD

### Technical Debt
- [ ] Technical debt tracking mechanism
- [ ] Debt repayment strategy
- [ ] Regular refactoring planned
- [ ] Dependency update process defined

### Developer Experience
- [ ] Local development environment documented
- [ ] Fast build times (<5 min)
- [ ] Clear error messages
- [ ] Good IDE support (types, autocomplete)

### Questions to Ask
- How long does it take to onboard a new developer?
- How easy is it to add a new feature?
- What's the current technical debt level?
- How often do we refactor?

---

## 6. Observability Checklist

### Logging
- [ ] Structured logging implemented
- [ ] Log levels defined (DEBUG, INFO, WARN, ERROR)
- [ ] Correlation IDs for request tracing
- [ ] Log aggregation system selected
- [ ] Sensitive data excluded from logs
- [ ] Log retention policy defined

### Metrics
- [ ] Business metrics defined (orders, conversions, etc.)
- [ ] Technical metrics defined (latency, errors, throughput)
- [ ] Metrics collection system selected
- [ ] Dashboard strategy defined
- [ ] Metric retention policy defined

### Tracing
- [ ] Distributed tracing implemented
- [ ] Trace context propagation verified
- [ ] Sampling strategy defined (if high volume)
- [ ] Tracing system selected

### Alerting
- [ ] Alert strategy defined (what to alert on)
- [ ] Alert routing defined (who gets notified)
- [ ] On-call rotation defined
- [ ] Alert fatigue prevention measures
- [ ] Runbooks for common alerts

### Debugging
- [ ] Debugging tools available
- [ ] Production debugging approach defined
- [ ] Profiling capability exists
- [ ] Health check endpoints implemented

### Questions to Ask
- How do we know if the system is healthy?
- How do we debug production issues?
- What metrics matter to the business?
- How quickly can we detect and respond to issues?

---

## 7. Cost Efficiency Checklist

### Infrastructure Costs
- [ ] Compute costs estimated (servers, containers, functions)
- [ ] Storage costs estimated (database, object storage)
- [ ] Network costs estimated (egress, CDN)
- [ ] Third-party service costs estimated

### Licensing Costs
- [ ] Software licenses identified
- [ ] Open-source compliance verified
- [ ] Subscription costs estimated
- [ ] Enterprise support costs considered

### Operational Costs
- [ ] Team size and skills required
- [ ] Training costs estimated
- [ ] Maintenance effort estimated
- [ ] Support costs estimated

### Cost Optimization
- [ ] Right-sizing strategy defined
- [ ] Reserved capacity vs. on-demand decision
- [ ] Auto-scaling for cost optimization
- [ ] Spot/preemptible instances considered
- [ ] Cost monitoring and alerting implemented

### ROI Analysis
- [ ] Business value quantified
- [ ] Cost-benefit analysis completed
- [ ] Payback period calculated
- [ ] Alternative approaches compared

### Questions to Ask
- What's the total cost of ownership (TCO)?
- What are the biggest cost drivers?
- How do costs scale with usage?
- What's the break-even point?

---

## NFR Documentation Template

For each NFR category, document:

```markdown
## {NFR Category}

### Requirements
- **Target:** {Specific, measurable target}
- **Priority:** {High/Medium/Low}

### Current State
{Description of current implementation or gaps}

### Strategy
{Approach to meeting the requirement}

### Trade-offs
{What was sacrificed to achieve this}

### Monitoring
{How we measure success}

### Open Issues
{Known gaps or future work}
```

---

## NFR Priority Matrix

Use this matrix to prioritize NFRs:

| Priority | Criteria | Example |
|----------|----------|---------|
| **P0** | Legal/compliance requirement, business-critical | Security, data protection |
| **P1** | Essential for system to function | Reliability, basic performance |
| **P2** | Important for user experience | Advanced performance, observability |
| **P3** | Nice to have, can be deferred | Advanced cost optimization |

---

## Related Skills

- **performance-modeling** - Deep dive into performance analysis
- **security-architecture** - Deep dive into security patterns
- **cost-estimation** - Detailed cost analysis
- **architecture-blueprint-generator** - Complete architecture docs

---

## Usage Example

When analyzing an architecture decision:

1. **Review all 7 NFR categories**
2. **Mark checklist items** (✅ met, ❌ gap, ⚠️ partial)
3. **Document gaps** with mitigation plans
4. **Prioritize gaps** by impact
5. **Create action items** for addressing gaps

---

## Output Format

When using this skill, provide:
1. **Completed checklist** (all 7 categories)
2. **Gap analysis** (what's missing)
3. **Priority matrix** (what to address first)
4. **Recommendations** (specific actions)
5. **Trade-offs** (what was sacrificed)
