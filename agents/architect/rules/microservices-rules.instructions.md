---
description: Microservices architecture rules and guidelines for service boundaries, API design, communication patterns, data management, and resilience
applyTo: '**/*.cs,**/*.java,**/*.ts,**/services/**,**/docs/microservices/**'
---

# Microservices Rules

Microservices architecture rules and guidelines for designing, building, and operating distributed systems.

## Service Boundary Rules

### Decomposition Principles
✅ **DO:**
- Align services with business capabilities
- Follow domain-driven decomposition (bounded contexts)
- Ensure single responsibility per service
- Design for independent deployment
- Own data exclusively per service

❌ **DON'T:**
- Create services based on technical layers
- Share databases between services
- Create distributed monoliths (tight coupling)
- Make services too small (nano-services)
- Make services too large (mini-monoliths)

### Service Size Guidelines
| Metric | Guideline | Rationale |
|--------|-----------|-----------|
| **Team Size** | 2-pizza team (6-10 people) | Ownership and autonomy |
| **Code Base** | Understandable by single team | Maintainability |
| **Deployment** | Independent, < 10 minutes | Fast iteration |
| **Startup Time** | < 30 seconds | Fast scaling |
| **Database** | Owned by single service | Data sovereignty |

### Service Identification
✅ **Services SHOULD have:**
- Clear business capability
- Well-defined API
- Owned data store
- Independent deployment pipeline
- Dedicated team (or clear ownership)

## API Design Rules

### REST API Standards
✅ **DO:**
- Use resource-based URLs (`/api/users/{id}`)
- Use proper HTTP verbs (GET, POST, PUT, DELETE, PATCH)
- Return appropriate status codes
- Version APIs from day one (`/api/v1/`)
- Support pagination (`?page=1&size=20`)
- Implement filtering and sorting
- Use consistent error response format

❌ **DON'T:**
- Use verbs in URLs (`/api/createUser`)
- Use GET for state-changing operations
- Return 200 for errors
- Version in query params (`?version=1`)
- Return all data without pagination
- Mix success and error formats

### Status Code Usage
| Code | When to Use |
|------|-------------|
| **200 OK** | Successful GET, PUT, PATCH |
| **201 Created** | Successful POST, resource created |
| **204 No Content** | Successful DELETE |
| **400 Bad Request** | Invalid input, validation errors |
| **401 Unauthorized** | Missing authentication |
| **403 Forbidden** | Insufficient permissions |
| **404 Not Found** | Resource doesn't exist |
| **409 Conflict** | Business rule violation |
| **422 Unprocessable Entity** | Validation errors (semantic) |
| **429 Too Many Requests** | Rate limit exceeded |
| **500 Internal Server Error** | Server-side failure |
| **503 Service Unavailable** | Service down for maintenance |

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input provided",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ],
    "timestamp": "2024-01-01T12:00:00Z",
    "path": "/api/users",
    "traceId": "abc123"
  }
}
```

### API Versioning
✅ **DO:**
- Use URL versioning (`/api/v1/`, `/api/v2/`)
- Support at least 2 versions simultaneously
- Deprecate old versions with timeline
- Document breaking changes clearly
- Provide migration guides

❌ **DON'T:**
- Change API behavior without version bump
- Remove old versions without notice
- Use breaking changes in same version
- Version based on implementation details

## Communication Rules

### Synchronous vs Asynchronous
**Use Synchronous (REST, gRPC) when:**
- Immediate response required
- Simple request/response
- Real-time decision needed
- Few services involved (chain < 3)

**Use Asynchronous (Events, Messages) when:**
- Eventual consistency acceptable
- Decoupling required
- High throughput needed
- Background processing
- Multiple subscribers

### Communication Patterns
✅ **DO:**
- Use API Gateway for external clients
- Implement circuit breakers for all external calls
- Set timeouts on all calls
- Use retry with exponential backoff
- Implement idempotency for operations
- Use correlation IDs for tracing

❌ **DON'T:**
- Create long chains of synchronous calls
- Call services directly from frontend
- Retry without limits
- Make calls without timeouts
- Ignore network failures
- Assume services are always available

### Timeout Configuration
```yaml
# Standard timeout configuration
timeouts:
  connection: 5s      # Time to establish connection
  read: 30s          # Time to wait for response
  write: 30s         # Time to send request
  
# Service-specific
services:
  database:
    timeout: 5s
    retries: 3
  external-api:
    timeout: 10s
    retries: 2
  internal-service:
    timeout: 3s
    retries: 3
```

### Circuit Breaker Pattern
```yaml
circuit-breaker:
  failure-threshold: 5        # Failures before opening
  reset-timeout: 30s          # Time before half-open
  half-open-requests: 3       # Requests to test
  success-threshold: 2        # Successes to close
  
states:
  CLOSED: Normal operation
  OPEN: Failing fast, no requests
  HALF_OPEN: Testing recovery
```

## Data Management Rules

### Database per Service
✅ **DO:**
- Give each service its own database
- Own schema exclusively
- Choose appropriate database technology
- Manage migrations independently
- Handle data synchronization via events

❌ **DON'T:**
- Share databases between services
- Access another service's database directly
- Use distributed transactions (2PC)
- Create foreign keys across services
- Perform joins across service boundaries

### Data Consistency Patterns
**Saga Pattern (Distributed Transactions):**

**Choreography-based:**
```
Service A → Event → Service B → Event → Service C
                    ↓                     ↓
              Compensating          Compensating
              if needed             if needed
```
✅ Use when: Few participants, simple workflows

**Orchestration-based:**
```
Orchestrator → Service A → Service B → Service C
                  ↓            ↓            ↓
            Compensating  Compensating  Compensating
```
✅ Use when: Many participants, complex workflows

### CQRS (Command Query Responsibility Segregation)
✅ **Use CQRS when:**
- Read and write workloads differ significantly
- Complex queries needed
- Performance is critical
- Event sourcing is used

❌ **Avoid CQRS when:**
- Simple CRUD operations
- Team is small
- Added complexity not justified

### Event Sourcing
✅ **Use Event Sourcing when:**
- Audit trail is required
- Temporal queries needed (state at time X)
- Event-driven architecture
- Business process tracking

❌ **Avoid Event Sourcing when:**
- Simple CRUD is sufficient
- Team lacks experience
- Performance is critical for reads
- Storage cost is concern

## Resilience Rules

### Retry Policy
```yaml
retry:
  max-retries: 3
  initial-delay: 1s
  max-delay: 10s
  multiplier: 2        # Exponential backoff
  jitter: true         # Add randomness
  retry-on:            # When to retry
    - 5xx errors
    - Connection errors
    - Timeouts
  never-retry:         # When NOT to retry
    - 4xx errors (client errors)
    - Validation errors
    - Idempotency concerns
```

### Bulkhead Pattern
```yaml
bulkhead:
  max-concurrent-calls: 10
  max-wait-duration: 100ms
  
# Isolate resources
isolates:
  - Database connections per service
  - Thread pools per dependency
  - Memory limits per component
```

### Fallback Strategies
✅ **Implement fallbacks for:**
- External service failures
- Cache misses with stale data option
- Non-critical features
- Degraded mode operation

**Examples:**
- Return cached data if service unavailable
- Show default recommendations
- Disable non-essential features
- Queue requests for later processing

## Observability Rules

### Logging
✅ **DO:**
- Use structured logging (JSON format)
- Include correlation IDs in all logs
- Log at appropriate levels (DEBUG, INFO, WARN, ERROR)
- Include context (user ID, request ID, service name)
- Centralize logs (ELK, Splunk, CloudWatch)

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "service": "order-service",
  "traceId": "abc123",
  "spanId": "span456",
  "userId": "user789",
  "message": "Order created",
  "orderId": "order-001",
  "amount": 99.99
}
```

❌ **DON'T:**
- Log sensitive data (PII, passwords, tokens)
- Use unstructured logging
- Log excessively at INFO level
- Ignore log rotation
- Store logs only locally

### Metrics
✅ **Collect RED metrics:**
- **Rate**: Requests per second
- **Errors**: Error rate (percentage)
- **Duration**: Response time (p50, p95, p99)

✅ **Collect USE metrics:**
- **Utilization**: Resource usage percentage
- **Saturation**: Queue lengths
- **Errors**: Hardware-level errors

**Standard Metrics:**
- Request count (total, by endpoint, by status)
- Response time (histogram with percentiles)
- Error count (by type)
- Dependencies (database, cache, external APIs)
- Business metrics (orders, revenue, users)

### Distributed Tracing
✅ **DO:**
- Implement tracing in all services
- Propagate trace context
- Sample appropriately (1-10% in production)
- Include business context in spans
- Use standard format (W3C Trace Context)

❌ **DON'T:**
- Trace only some services
- Drop trace context between services
- Sample 100% in production (too much data)
- Ignore async boundaries

## Deployment Rules

### Container Standards
✅ **DO:**
- Use official base images
- Run as non-root user
- Minimize image layers
- Use multi-stage builds
- Scan images for vulnerabilities
- Tag with semantic versions

❌ **DON'T:**
- Use `latest` tag in production
- Run as root
- Include unnecessary packages
- Store secrets in images
- Skip vulnerability scanning

### Health Checks
```yaml
health:
  liveness:
    path: /health/live
    interval: 10s
    timeout: 5s
    failure-threshold: 3
    
  readiness:
    path: /health/ready
    interval: 10s
    timeout: 5s
    failure-threshold: 3
    
  startup:
    path: /health/started
    interval: 5s
    timeout: 5s
    failure-threshold: 30
```

### CI/CD Requirements
✅ **Pipeline must include:**
- Automated tests (unit, integration, contract)
- Security scanning (SAST, DAST, SCA)
- Container image build and scan
- Deployment to staging
- Smoke tests
- Production deployment (blue-green or canary)
- Rollback capability

## Quality Checklist

### Service Design
- [ ] Single, clear responsibility
- [ ] Independent deployment
- [ ] Owns its data
- [ ] Well-defined API
- [ ] Appropriate size

### API Design
- [ ] RESTful conventions followed
- [ ] Proper status codes
- [ ] Consistent error format
- [ ] Versioned
- [ ] Documented (OpenAPI/Swagger)

### Communication
- [ ] Circuit breakers configured
- [ ] Timeouts set
- [ ] Retry with backoff
- [ ] Correlation IDs
- [ ] Async where appropriate

### Data Management
- [ ] Database per service
- [ ] No distributed transactions
- [ ] Eventual consistency strategy
- [ ] Data synchronization plan

### Resilience
- [ ] Circuit breakers
- [ ] Retry policies
- [ ] Timeouts
- [ ] Fallbacks
- [ ] Bulkheads

### Observability
- [ ] Structured logging
- [ ] Correlation IDs
- [ ] RED metrics
- [ ] Distributed tracing
- [ ] Alerting configured

## References

- [Microservices.io](https://microservices.io/) - Patterns reference
- [Building Microservices](https://www.oreilly.com/library/view/building-microservices/9781491950340/) - Sam Newman
- [Microservices Patterns](https://www.manning.com/books/microservices-patterns) - Chris Richardson
- [12 Factor App](https://12factor.net/) - Cloud-native principles
- [Resilience Patterns](https://github.com/App-vNext/Polly) - Polly documentation

## MCP Integrations & Tools Required

**Always use available MCPs** when implementing or verifying rules:
- 🎯 Use **GitHub MCP** to find existing codebase examples matching this rule
- 🎯 Use **Brave Search MCP** to lookup latest documentation or official best practices
- 🎯 Use **Context7 MCP** to query historical context related to codebase structure before making decisions
