---
name: microservices-patterns
description: Catalog of microservices architecture patterns including decomposition strategies, communication patterns, data management, and operational patterns. Use when designing or evolving microservices architectures.
---

# Microservices Patterns Catalog

A comprehensive catalog of patterns for designing, building, and operating microservices architectures. Organized by category for easy reference.

---

## When to Use This Skill

Use this skill when:
- Decomposing a monolith into microservices
- Designing new microservices architecture
- Solving specific microservices challenges
- Creating architecture documentation
- Making technology decisions
- Training team on microservices patterns

---

## Pattern Categories

1. **Decomposition Patterns** - How to split services
2. **Communication Patterns** - How services talk
3. **Data Management Patterns** - How to handle data
4. **Operational Patterns** - How to run services
5. **Security Patterns** - How to secure services
6. **Testing Patterns** - How to test services

---

## 1. Decomposition Patterns

### Pattern: Decompose by Business Capability
**Problem**: How to define service boundaries?

**Solution**: Organize services around business capabilities (what the business does).

**Example**:
```
- Marketing Service
- Sales Service
- Inventory Service
- Shipping Service
- Customer Service
```

**When to Use**:
- Clear business domains exist
- Teams organized by business function
- Need clear ownership

**Trade-offs**:
- ✅ Aligns with business organization
- ✅ Clear ownership
- ❌ May not match technical boundaries

---

### Pattern: Decompose by Subdomain (DDD)
**Problem**: How to define service boundaries using domain knowledge?

**Solution**: Use Domain-Driven Design subdomains (Core, Supporting, Generic).

**Example**:
```
Core Domain:
  - Order Processing Service
  - Payment Service

Supporting Domain:
  - Inventory Service
  - Notification Service

Generic Domain:
  - Authentication Service
  - Reporting Service
```

**When to Use**:
- Complex business logic
- Domain experts available
- Long-term maintainability important

**Trade-offs**:
- ✅ Matches business complexity
- ✅ Clear bounded contexts
- ❌ Requires DDD expertise

---

### Pattern: Strangler Fig
**Problem**: How to migrate from monolith to microservices?

**Solution**: Gradually replace monolith features with services, routing traffic progressively.

**Example**:
```
         ┌─────────────────┐
         │     Router      │
         └────┬────────┬───┘
              │        │
         ┌────┴────┐  ┌┴──────────┐
         │Monolith │  │New Service│
         └─────────┘  └───────────┘
```

**When to Use**:
- Migrating legacy monolith
- Minimize risk
- Incremental migration needed

**Trade-offs**:
- ✅ Low risk
- ✅ Incremental
- ❌ Temporary complexity

---

### Pattern: Service per Team
**Problem**: How to align services with team structure?

**Solution**: Design services to match team boundaries (Conway's Law).

**Example**:
```
Team A (5 people) → Service A
Team B (5 people) → Service B
Team C (5 people) → Service C
```

**When to Use**:
- Multiple teams
- Need clear ownership
- Fast iteration required

**Trade-offs**:
- ✅ Clear ownership
- ✅ Team autonomy
- ❌ May create suboptimal boundaries

---

## 2. Communication Patterns

### Pattern: Synchronous Request/Response
**Problem**: How to handle immediate responses?

**Solution**: Use HTTP/REST, gRPC, or GraphQL for synchronous calls.

**Example**:
```
Client → API Gateway → Service A → Service B → Response
```

**When to Use**:
- Immediate response needed
- Simple request/response flows
- Real-time user interactions

**Trade-offs**:
- ✅ Simple to implement
- ✅ Immediate feedback
- ❌ Tight coupling
- ❌ Cascading failures

---

### Pattern: Async Message-Based
**Problem**: How to decouple services?

**Solution**: Use message queues (RabbitMQ, Kafka, SQS) for async communication.

**Example**:
```
Service A → [Message Queue] → Service B
                     └─────→ Service C
```

**When to Use**:
- Loose coupling needed
- Eventual consistency acceptable
- Load leveling required

**Trade-offs**:
- ✅ Loose coupling
- ✅ Better resilience
- ❌ More complex
- ❌ Eventual consistency

---

### Pattern: Event Sourcing
**Problem**: How to maintain audit trail and support temporal queries?

**Solution**: Store state changes as events, reconstruct state by replaying events.

**Example**:
```
Events:
  - OrderCreated
  - PaymentReceived
  - OrderShipped
  
State = ApplyAll(events)
```

**When to Use**:
- Audit trail required
- Temporal queries needed
- Complex business processes

**Trade-offs**:
- ✅ Full audit trail
- ✅ Temporal queries
- ❌ Complex implementation
- ❌ Event schema evolution

---

### Pattern: CQRS (Command Query Responsibility Segregation)
**Problem**: How to optimize read and write performance independently?

**Solution**: Separate read and write models, potentially with different databases.

**Example**:
```
        Write Model              Read Model
        (Commands)               (Queries)
            ↓                        ↑
    ┌───────────────┐        ┌──────────────┐
    │ Write DB      │ ─────→ │ Read DB      │
    │ (Normalized)  │  Sync  │ (Denormalized)│
    └───────────────┘        └──────────────┘
```

**When to Use**:
- Different read/write loads
- Complex queries on read side
- Performance optimization needed

**Trade-offs**:
- ✅ Independent scaling
- ✅ Optimized queries
- ❌ Eventual consistency
- ❌ More infrastructure

---

### Pattern: Saga
**Problem**: How to manage distributed transactions?

**Solution**: Break transaction into sequence of local transactions with compensating actions.

**Example**:
```
1. Create Order (Order Service)
2. Reserve Inventory (Inventory Service)
3. Process Payment (Payment Service)

If step 3 fails:
  → Cancel Order (compensate step 1)
  → Release Inventory (compensate step 2)
```

**When to Use**:
- Distributed transactions needed
- ACID not possible across services
- Business process spans services

**Trade-offs**:
- ✅ Eventually consistent
- ✅ Works across services
- ❌ Complex to implement
- ❌ Compensating transactions needed

---

## 3. Data Management Patterns

### Pattern: Database per Service
**Problem**: How to avoid database coupling?

**Solution**: Each service owns its database, no direct access from other services.

**Example**:
```
Service A → DB A (PostgreSQL)
Service B → DB B (MongoDB)
Service C → DB C (Redis)
```

**When to Use**:
- Microservices architecture
- Need loose coupling
- Different data models needed

**Trade-offs**:
- ✅ Loose coupling
- ✅ Technology diversity
- ❌ Data consistency challenges
- ❌ More databases to manage

---

### Pattern: Shared Database (Anti-Pattern)
**Problem**: ⚠️ **Warning**: Multiple services sharing a database.

**Why It's Bad**:
- Tight coupling
- Schema changes break services
- Can't scale independently
- Unclear ownership

**Solution**: Refactor to Database per Service.

---

### Pattern: API Composition
**Problem**: How to query data across services?

**Solution**: Use a composer/aggregator service to query multiple services and combine results.

**Example**:
```
              API Composer
              /    |    \
             ↓     ↓     ↓
        Service A  B     C
             \     |    /
              Combine Results
```

**When to Use**:
- Need data from multiple services
- Query is read-only
- Simple aggregation

**Trade-offs**:
- ✅ Simple to implement
- ✅ No data duplication
- ❌ Performance (multiple calls)
- ❌ Point of failure

---

### Pattern: CQRS with Event Sourcing
**Problem**: How to combine read optimization with audit trail?

**Solution**: Use CQRS for read/write separation + Event Sourcing for audit.

**When to Use**:
- Both requirements exist
- Complex business processes
- High performance needed

---

## 4. Operational Patterns

### Pattern: Service Discovery
**Problem**: How do services find each other?

**Solution**: Use service registry (Consul, Eureka, Kubernetes DNS).

**Example**:
```
Service A registers → [Service Registry] ← Service B queries
```

**When to Use**:
- Dynamic scaling
- Container orchestration
- Cloud-native deployment

---

### Pattern: API Gateway
**Problem**: How to provide unified entry point?

**Solution**: Use API Gateway for routing, authentication, rate limiting.

**Example**:
```
Client → API Gateway → [Service A, Service B, Service C]
```

**When to Use**:
- Multiple services
- Cross-cutting concerns
- Client simplification needed

---

### Pattern: Circuit Breaker
**Problem**: How to handle cascading failures?

**Solution**: Stop calling failing service temporarily, fail fast.

**States**:
- **Closed**: Normal operation
- **Open**: Failing, reject calls
- **Half-Open**: Testing if service recovered

**When to Use**:
- External dependencies
- Prevent cascading failures
- Improve resilience

---

### Pattern: Bulkhead
**Problem**: How to isolate failures?

**Solution**: Partition resources so failure in one area doesn't affect others.

**Example**:
```
Thread Pool A → Service A (isolated)
Thread Pool B → Service B (isolated)
Thread Pool C → Service C (isolated)
```

**When to Use**:
- Critical and non-critical calls
- Resource isolation needed
- Prevent resource exhaustion

---

### Pattern: Retry with Backoff
**Problem**: How to handle transient failures?

**Solution**: Retry failed calls with exponential backoff.

**Example**:
```
Attempt 1: Fail → Wait 1s
Attempt 2: Fail → Wait 2s
Attempt 3: Fail → Wait 4s
Attempt 4: Success
```

**When to Use**:
- Transient failures expected
- Idempotent operations
- External services

---

## 5. Security Patterns

### Pattern: Token-Based Authentication
**Problem**: How to authenticate across services?

**Solution**: Use JWT or OAuth tokens, validate at gateway or each service.

**When to Use**:
- Stateless authentication
- Multiple services
- Mobile/web clients

---

### Pattern: Zero Trust Network
**Problem**: How to secure service-to-service communication?

**Solution**: Authenticate and authorize every request, even internal.

**Practices**:
- mTLS for all service communication
- Service identity verification
- Least privilege access

**When to Use**:
- High security requirements
- Multi-tenant systems
- Regulated industries

---

### Pattern: Secrets Management
**Problem**: How to manage credentials securely?

**Solution**: Use secrets management service (Vault, AWS Secrets Manager).

**When to Use**:
- Multiple services need secrets
- Secret rotation required
- Compliance requirements

---

## 6. Testing Patterns

### Pattern: Consumer-Driven Contracts
**Problem**: How to test service integration without full environment?

**Solution**: Define contracts from consumer perspective, verify providers.

**When to Use**:
- Multiple consuming services
- Independent deployment
- Fast feedback needed

---

### Pattern: Test Pyramid for Microservices
**Problem**: How to test microservices effectively?

**Solution**:
```
        /‾‾‾‾‾\
       /  E2E   \  (Few)
      /──────────\
     /Integration/  (Some)
    /──────────────\
   /     Unit       \  (Many)
  /__________________\
```

**When to Use**:
- All microservices projects
- Balance coverage and speed

---

### Pattern: Contract Testing
**Problem**: How to ensure service compatibility?

**Solution**: Test API contracts independently of implementation.

**Tools**: Pact, Spring Cloud Contract

**When to Use**:
- Multiple teams
- Independent deployment
- API stability important

---

## Pattern Selection Guide

| Problem | Recommended Patterns |
|---------|---------------------|
| Decomposing monolith | Strangler Fig, Decompose by Subdomain |
| Service communication | Async Message-Based, Saga |
| Data consistency | Saga, CQRS, Event Sourcing |
| Resilience | Circuit Breaker, Bulkhead, Retry |
| Security | Token-Based Auth, Zero Trust |
| Testing | Consumer-Driven Contracts, Test Pyramid |

---

## Related Skills

- **ddd-patterns-catalog** - DDD-specific patterns
- **architecture-review-checklist** - Review microservices architecture
- **c4-diagram-patterns** - Diagram microservices

---

## Output Format

When using this skill, provide:
1. **Pattern name** and category
2. **Problem** it solves
3. **Solution** with diagram
4. **When to use**
5. **Trade-offs** (pros/cons)
6. **Example** code or architecture
7. **Related patterns**
