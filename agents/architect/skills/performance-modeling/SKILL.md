---
name: performance-modeling
description: Performance modeling and capacity planning. Use when analyzing performance requirements, capacity planning, load testing strategies, bottleneck analysis, or performance optimization planning.
license: Apache 2.0
---

# Performance Modeling

Performance modeling, capacity planning, and optimization strategies for building scalable, high-performance systems.

## When to Use This Skill

Use this skill when:
- Analyzing performance requirements (RPS, latency, throughput)
- Capacity planning and scalability analysis
- Load testing strategy design
- Bottleneck identification and analysis
- Performance optimization planning
- Defining SLIs, SLOs, and SLAs
- Performance budget definition
- Scaling strategy (horizontal vs vertical)

## Core Performance Concepts

### Performance Metrics
| Metric | Description | Target |
|--------|-------------|--------|
| **Latency** | Time to complete a request | p50 < 100ms, p95 < 200ms, p99 < 500ms |
| **Throughput** | Requests per second (RPS) | Based on business requirements |
| **Concurrency** | Simultaneous users/requests | Peak concurrent users |
| **Error Rate** | Percentage of failed requests | < 0.1% |
| **Utilization** | Resource usage (CPU, memory) | < 70% average, < 85% peak |

### Little's Law
```
N = λ × W
Where:
  N = Number of requests in system
  λ = Arrival rate (requests/second)
  W = Average response time (seconds)
```

**Use case:** Estimate concurrent connections needed

### USE Method (Utilization, Saturation, Errors)
For every resource, analyze:
- **Utilization**: Percentage of time busy
- **Saturation**: Queue length when busy
- **Errors**: Error rate

## Capacity Planning Framework

### Step 1: Define Requirements
**Business Metrics:**
- Peak concurrent users
- Transactions per second
- Data volume (read/write)
- Growth projections (monthly/yearly)

**Technical Metrics:**
- Response time targets (p50, p95, p99)
- Availability target (99.9%, 99.99%, 99.999%)
- Recovery time objective (RTO)
- Recovery point objective (RPO)

### Step 2: Workload Characterization
**Request Types:**
- Read-heavy vs write-heavy
- Synchronous vs asynchronous
- CPU-bound vs I/O-bound
- Session-based vs stateless

**Traffic Patterns:**
- Peak hours/days
- Seasonal variations
- Growth trends
- Burst patterns

### Step 3: Resource Estimation
**Formula:**
```
Servers = (Total RPS × Avg Response Time) / (Target Utilization × Server Capacity)
```

**Example Calculation:**
```
Requirements:
  - Peak RPS: 10,000
  - Avg Response Time: 50ms (0.05s)
  - Target Utilization: 70%
  - Server Capacity: 1,000 RPS per server

Calculation:
  Servers = (10,000 × 0.05) / (0.70 × 1,000)
  Servers = 500 / 700
  Servers = 0.714 → Round up to 1 server minimum
  
With redundancy (3 replicas):
  Total servers = 1 × 3 = 3 servers
```

### Step 4: Scaling Strategy
**Horizontal Scaling:**
- Add more servers
- Better fault tolerance
- Requires stateless design
- Load balancing needed

**Vertical Scaling:**
- Add more resources (CPU, RAM)
- Simpler architecture
- Limited by hardware
- Single point of failure

## Bottleneck Analysis

### Types of Bottlenecks
| Type | Symptoms | Analysis Tools |
|------|----------|----------------|
| **CPU-bound** | High CPU utilization, slow processing | Profiler, top, perf |
| **Memory-bound** | High memory usage, GC pressure | Heap dumps, memory profiler |
| **I/O-bound** | High disk/network wait time | iostat, netstat, Wireshark |
| **Database** | Slow queries, lock contention | Query plans, slow query log |
| **Network** | High latency, packet loss | ping, traceroute, tcpdump |

### Amdahl's Law
```
Speedup = 1 / ((1 - P) + (P / S))
Where:
  P = Parallelizable portion
  S = Speedup of parallel portion
```

**Implication:** Optimize the slowest sequential parts first

### Queueing Theory Basics
```
Response Time = Service Time + Wait Time
Wait Time increases exponentially as utilization approaches 100%
```

**Rule of thumb:** Keep utilization below 70% for acceptable latency

## Load Testing Strategy

### Test Types
| Type | Purpose | Duration |
|------|---------|----------|
| **Load Test** | Verify performance under expected load | 1-4 hours |
| **Stress Test** | Find breaking point | 30 min - 2 hours |
| **Soak Test** | Identify memory leaks, degradation | 24-72 hours |
| **Spike Test** | Test sudden traffic bursts | 15-30 min |
| **Chaos Test** | Verify resilience under failures | Ongoing |

### Load Test Plan
**1. Define Objectives**
- Peak RPS to test
- Response time targets
- Error rate threshold
- Resource utilization limits

**2. Design Test Scenarios**
- Typical user journeys
- Critical workflows
- Edge cases

**3. Configure Test Environment**
- Production-like infrastructure
- Realistic data volume
- Network conditions

**4. Execute Tests**
- Ramp-up gradually
- Monitor all metrics
- Capture bottlenecks

**5. Analyze Results**
- Compare against targets
- Identify bottlenecks
- Document findings

### Load Testing Tools
- **k6**: Developer-friendly, scriptable
- **Gatling**: High performance, detailed reports
- **JMeter**: Mature, extensible
- **Locust**: Python-based, distributed
- **Artillery**: Modern, API-focused

## Performance Optimization Strategies

### Database Optimization
**Indexing:**
- Covering indexes
- Composite indexes
- Partial indexes

**Query Optimization:**
- Avoid N+1 queries
- Use appropriate joins
- Limit result sets
- Cache frequently accessed data

**Schema Optimization:**
- Normalize for writes
- Denormalize for reads
- Partitioning strategies
- Archiving old data

### Caching Strategies
**Cache Levels:**
1. **Browser Cache**: Static assets
2. **CDN Cache**: Global content delivery
3. **Application Cache**: In-memory (Redis, Memcached)
4. **Database Cache**: Query cache, buffer pool

**Cache Patterns:**
- Cache-aside (lazy loading)
- Write-through
- Write-behind
- Refresh-ahead

**Cache Invalidation:**
- TTL-based
- Event-based
- Manual invalidation

### Asynchronous Processing
**When to Use:**
- Non-critical path operations
- Batch processing
- External integrations
- Reporting/analytics

**Patterns:**
- Message queues (RabbitMQ, SQS)
- Event streaming (Kafka, Kinesis)
- Background jobs (Celery, Bull)

## SLI/SLO/SLA Framework

### Definitions
- **SLI (Service Level Indicator)**: What you measure (e.g., latency, error rate)
- **SLO (Service Level Objective)**: Target value (e.g., 99.9% availability)
- **SLA (Service Level Agreement)**: Contract with consequences

### Example SLIs
| Service Type | SLI | Target |
|--------------|-----|--------|
| **Web Service** | Request latency (p99) | < 500ms |
| **API** | Success rate | > 99.9% |
| **Database** | Query latency (p95) | < 100ms |
| **Batch Job** | Completion time | < 4 hours |

### Error Budget
```
Error Budget = 1 - SLO
Example: 99.9% availability = 0.1% error budget
  = 43 minutes of downtime per month
  = 8.76 hours per year
```

**Use:** Balance innovation vs reliability

## Capacity Planning Template

```markdown
# Capacity Plan for {System}

## Business Requirements
- Peak concurrent users: {number}
- Peak RPS: {number}
- Data growth: {percentage}/month
- Availability target: {percentage}

## Current Baseline
- Current RPS: {number}
- Current latency (p50/p95/p99): {values}
- Current error rate: {percentage}
- Current resource utilization: {percentages}

## Projections
- 6 months: {growth percentage}
- 12 months: {growth percentage}
- 24 months: {growth percentage}

## Resource Requirements
- Application servers: {count} ({instance type})
- Database: {instance type}, {read replicas}
- Cache: {instance type}, {cluster size}
- Load balancers: {count}

## Scaling Strategy
- Horizontal scaling trigger: {utilization percentage}
- Scale-up increment: {count} servers
- Scale-down threshold: {utilization percentage}
- Cooldown period: {minutes}

## Budget
- Monthly infrastructure cost: ${amount}
- Growth projection: ${amount}/month
```

## Performance Budget

Define budgets for:
- **Bundle Size**: Max JavaScript/CSS size
- **Load Time**: Max page load time
- **Time to Interactive**: Max TTI
- **API Latency**: Max response time
- **Error Rate**: Max acceptable errors

## Monitoring and Alerting

### Key Dashboards
- **Business Metrics**: RPS, conversions, revenue
- **Performance Metrics**: Latency, throughput, errors
- **Resource Metrics**: CPU, memory, disk, network
- **Dependency Metrics**: Database, cache, external APIs

### Alerting Rules
- **Critical**: Service down, high error rate
- **Warning**: High latency, resource saturation
- **Info**: Anomalies, trend changes

## Output Format

When using this skill, create:

1. **Performance Requirements Document** (`/docs/performance/{system}_Requirements.md`)
   - SLIs and SLOs
   - Performance budgets
   - Capacity targets

2. **Capacity Plan** (`/docs/performance/{system}_Capacity.md`)
   - Resource requirements
   - Scaling strategy
   - Cost estimates

3. **Load Test Report** (`/docs/performance/{system}_LoadTest.md`)
   - Test scenarios
   - Results analysis
   - Bottleneck identification

4. **Performance Optimization Plan** (`/docs/performance/{system}_Optimization.md`)
   - Identified bottlenecks
   - Optimization recommendations
   - Expected improvements

## Best Practices

1. **Measure First**: Don't optimize without data
2. **Set Realistic Targets**: Balance performance and cost
3. **Test in Production-like Environment**: staging ≠ production
4. **Monitor Continuously**: Performance degrades over time
5. **Plan for Growth**: Account for 12-24 month growth
6. **Automate Scaling**: Use auto-scaling groups
7. **Document Assumptions**: Future teams need context
8. **Review Regularly**: Update capacity plans quarterly

## References

- [Google SRE Book](https://sre.google/books/) - Performance and capacity planning
- [USE Method](http://www.brendangregg.com/usemethod.html) - Resource analysis
- [Little's Law](https://en.wikipedia.org/wiki/Little%27s_law) - Queueing theory
- [k6 Documentation](https://k6.io/docs/) - Load testing
- [Performance Calendar](https://calendar.perfplanet.com/) - Performance articles

### MCP Interactions
- **GitHub MCP**: Search repository for previous similar actions or related PRs before executing this skill.
- **Brave Search MCP**: Validate current patterns against the live internet if the context is sparse.
- **Context7 MCP**: Extract deep architectural/domain context relevant to the skill's execution.
