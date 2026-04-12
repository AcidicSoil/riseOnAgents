---
description: Domain-Driven Design rules and guidelines for aggregate design, entities, value objects, domain events, and ubiquitous language
applyTo: '**/*.cs,**/*.java,**/*.ts,**/domain/**,**/docs/domain/**'
---

# DDD Rules

Domain-Driven Design rules and guidelines for modeling complex business domains.

## Aggregate Design Rules

### Aggregate Boundaries
✅ **DO:**
- Design aggregates around business invariants
- Keep aggregates small (transactional consistency boundary)
- Ensure each aggregate has exactly one root entity
- Reference other aggregates by ID only (never by object reference)
- Make aggregate roots responsible for consistency

❌ **DON'T:**
- Create large aggregates with many entity types
- Allow bidirectional relationships between aggregates
- Reference other aggregates directly (use IDs)
- Put business logic outside aggregates (anemic domain model)
- Design aggregates based on data model instead of business rules

### Aggregate Root Responsibilities
✅ **MUST:**
- Enforce all invariants within the aggregate
- Be the only entry point for modifications
- Contain all business logic related to invariants
- Raise domain events for state changes
- Validate all commands before applying

❌ **MUST NOT:**
- Allow direct modification of internal entities
- Expose internal state publicly
- Have no-argument constructors (require valid state)
- Contain logic that belongs to other aggregates

### Aggregate Size Guidelines
| Metric | Guideline | Rationale |
|--------|-----------|-----------|
| **Entities per Aggregate** | 2-5 | Keep focused, maintainable |
| **Value Objects per Entity** | 3-7 | Encapsulate concepts |
| **Methods per Aggregate Root** | 5-15 | Business capabilities |
| **Lines of Code** | < 500 | Maintainability |

## Entity Design Rules

### Identity
✅ **Entities MUST:**
- Have a unique identity that persists through state changes
- Define identity explicitly (ID field, not just database primary key)
- Maintain identity throughout lifecycle
- Implement equality based on identity, not attributes

❌ **Entities MUST NOT:**
- Be defined solely by attributes (use Value Objects instead)
- Change identity during lifecycle
- Have mutable identity fields
- Use database-generated IDs for domain equality

### Entity Lifecycle
✅ **DO:**
- Define clear creation rules (factories)
- Manage entity state transitions explicitly
- Validate state before transitions
- Raise domain events for significant state changes

❌ **DON'T:**
- Allow invalid state transitions
- Expose state setters without validation
- Create entities with invalid initial state
- Hide state transitions from domain layer

### Entity Encapsulation
✅ **DO:**
- Encapsulate state (private fields)
- Expose behavior, not data
- Validate invariants in methods
- Use Value Objects for complex attributes

❌ **DON'T:**
- Create anemic entities (getters/setters only)
- Expose internal collections directly
- Allow external state modification
- Put business logic outside entities

## Value Object Rules

### Immutability
✅ **Value Objects MUST:**
- Be immutable (all fields final/readonly)
- Have no setters
- Return new instances for modifications
- Be freely shareable without side effects

❌ **Value Objects MUST NOT:**
- Have mutable state
- Expose setters or mutators
- Change after creation
- Maintain references to mutable objects

### Identity
✅ **Value Objects:**
- Have NO identity (equality by attributes)
- Implement equality based on all attributes
- Can be compared for equality
- Are interchangeable if attributes match

❌ **Value Objects:**
- Should not have ID fields
- Should not be tracked for identity
- Should not have lifecycle management

### Self-Validation
✅ **Value Objects MUST:**
- Validate themselves on creation
- Throw exception if invalid
- Encapsulate validation logic
- Ensure only valid instances exist

❌ **Value Objects MUST NOT:**
- Allow invalid state
- Require external validation
- Have "isValid" methods (should be impossible to be invalid)
- Accept invalid constructor arguments

### Common Value Objects
**Implement as Value Objects:**
- Money (amount, currency)
- Date ranges (start, end)
- Addresses (street, city, state, postalCode, country)
- Email addresses (address)
- Phone numbers (number, country code)
- Names (first, last)
- Coordinates (latitude, longitude)
- Color (RGB, hex)
- Measurements (value, unit)

## Domain Event Rules

### Event Naming
✅ **DO:**
- Use past tense (OrderCreated, PaymentProcessed)
- Name from domain perspective (not technical)
- Be specific and descriptive
- Use ubiquitous language terms

❌ **DON'T:**
- Use present tense (OrderCreating)
- Use technical names (EntityChanged, DataUpdated)
- Use vague names (SomethingHappened)
- Use imperative mood (CreateOrder - this is a command)

### Event Content
✅ **Domain Events MUST:**
- Represent completed business actions
- Contain all relevant data for handlers
- Be self-contained (no external lookups needed)
- Use primitive types or Value Objects
- Include timestamps

❌ **Domain Events MUST NOT:**
- Represent ongoing processes
- Reference entities directly (use IDs)
- Require database queries to understand
- Contain sensitive data unnecessarily
- Be mutable after creation

### Event Usage
✅ **DO:**
- Raise events for significant state changes
- Use events for cross-aggregate communication
- Implement event handlers for side effects
- Store events for audit/audit trail

❌ **DON'T:**
- Raise events for technical changes
- Use events for synchronous flow control
- Allow handlers to modify raising aggregate
- Ignore events in same transaction

## Ubiquitous Language Rules

### Language Development
✅ **DO:**
- Use domain terms consistently in code
- Involve domain experts in language definition
- Document terms in glossary
- Refactor language as understanding evolves
- Use same terms in code, docs, and conversation

❌ **DON'T:**
- Use technical jargon in domain layer
- Have different terms for same concept
- Allow ambiguous terms
- Ignore domain expert input

### Glossary Requirements
✅ **Every project MUST maintain:**
- Glossary of domain terms (`/docs/domain/glossary.md`)
- Definitions with examples
- Context boundaries for terms
- Evolution history (as terms change)

### Language in Code
✅ **DO:**
- Name classes after domain concepts
- Use domain verbs for methods
- Reflect domain processes in workflows
- Avoid technical abstractions in domain layer

❌ **DON'T:**
- Use generic names (Manager, Processor, Handler)
- Mix domain and technical language
- Leak technical concerns to domain layer
- Use database terminology in domain

## Repository Rules

### Repository Design
✅ **DO:**
- Create one repository per aggregate root
- Define repository interfaces in domain layer
- Implement repositories in infrastructure layer
- Return domain entities, not DTOs or DataSets
- Use specification pattern for complex queries

❌ **DON'T:**
- Create repositories for entities inside aggregates
- Expose database-specific operations
- Return data structures instead of entities
- Put business logic in repositories
- Allow repositories to modify entities

### Repository Methods
✅ **Standard Methods:**
- `GetById(id)`: Retrieve by identity
- `Find(specification)`: Find by criteria
- `Add(entity)`: Persist new entity
- `Remove(entity)`: Delete entity
- `Unit of Work`: Transaction management

❌ **Avoid:**
- `GetAll()` without pagination
- Methods that return partial entities
- Methods that bypass aggregate invariants
- Direct SQL in domain layer

## Bounded Context Rules

### Context Identification
✅ **Look for:**
- Different meanings of same terms
- Separate business processes
- Organizational boundaries (teams)
- Data ownership boundaries
- Different consistency requirements

### Context Mapping
✅ **Document relationships:**
- Upstream/downstream dependencies
- Integration patterns (ACL, OHS, CF, etc.)
- Shared kernels (minimize these)
- Partnership relationships
- Customer-supplier relationships

### Context Boundaries
✅ **DO:**
- Keep contexts small and focused
- Minimize coupling between contexts
- Use explicit translation layers
- Define context maps

❌ **DON'T:**
- Share entities between contexts
- Allow direct database access across contexts
- Have implicit dependencies
- Create distributed monoliths

## Event Storming Guidelines

### Event Types
**Orange (Domain Events):**
- Facts that happened in the domain
- Named in past tense
- Business-significant

**Blue (Commands):**
- Intent to perform action
- Named in imperative
- Trigger state changes

**Yellow (Actors/Aggregates):**
- Users or systems initiating actions
- Aggregate roots managing state

**Purple (Policies):**
- Business rules triggered by events
- "When X, then Y" logic

**Green (Read Models):**
- Queryable projections
- Optimized for specific views

**Pink (External Systems):**
- Third-party integrations
- Legacy systems

### Event Storming Output
✅ **Must produce:**
- Domain event stream (timeline)
- Aggregate identification
- Bounded context boundaries
- Process flows
- Pain points and opportunities

## Quality Checklist

### Aggregate Design
- [ ] Clear aggregate root identified
- [ ] All invariants documented
- [ ] Proper encapsulation
- [ ] References other aggregates by ID only
- [ ] Small enough for single transaction
- [ ] Business logic inside aggregate

### Entity Design
- [ ] Identity clearly defined
- [ ] State encapsulated
- [ ] Contains behavior (not anemic)
- [ ] Manages lifecycle
- [ ] Equality based on identity

### Value Object Design
- [ ] Immutable (all fields final)
- [ ] Self-validating
- [ ] No identity
- [ ] Equality by attributes
- [ ] Shareable without side effects

### Domain Events
- [ ] Named in past tense
- [ ] Represents completed action
- [ ] Contains necessary payload
- [ ] Business-significant (not technical)
- [ ] No entity references (use IDs)

### Ubiquitous Language
- [ ] Glossary exists and is up-to-date
- [ ] Terms used consistently in code
- [ ] Domain experts validate language
- [ ] No ambiguous terms
- [ ] Technical jargon avoided in domain

## References

- [Domain-Driven Design Reference](https://domainlanguage.com/ddd/)
- [DDD by Evans](https://www.domainlanguage.com/ddd/reference/)
- [Implementing Domain-Driven Design](https://www.oreilly.com/library/view/implementing-domain-driven-design/9780321834577/)
- [Event Storming](https://eventstorming.com/)
- [DDD Quickly](https://www.infoq.com/minibooks/domain-driven-design-quickly)

## MCP Integrations & Tools Required

**Always use available MCPs** when implementing or verifying rules:
- 🎯 Use **GitHub MCP** to find existing codebase examples matching this rule
- 🎯 Use **Brave Search MCP** to lookup latest documentation or official best practices
- 🎯 Use **Context7 MCP** to query historical context related to codebase structure before making decisions
