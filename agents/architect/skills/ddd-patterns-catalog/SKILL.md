---
name: ddd-patterns-catalog
description: Catalog of Domain-Driven Design (DDD) patterns including strategic patterns (bounded contexts, subdomains, context maps) and tactical patterns (aggregates, entities, value objects, domain events). Use when modeling complex business domains.
---

# DDD Patterns Catalog

A comprehensive catalog of Domain-Driven Design (DDD) patterns for modeling complex business domains. Organized into Strategic and Tactical patterns.

---

## When to Use This Skill

Use this skill when:
- Designing domain models for complex business logic
- Decomposing systems by business domain
- Creating bounded contexts
- Modeling aggregates and entities
- Implementing domain events
- Training team on DDD concepts
- Refactoring anemic domain models

---

## DDD Overview

```
                    Domain-Driven Design
                           │
        ┌──────────────────┴──────────────────┐
        │                                     │
    STRATEGIC                             TACTICAL
    (Big Picture)                      (Implementation)
        │                                     │
        ├─ Subdomains                         ├─ Aggregates
        ├─ Bounded Contexts                   ├─ Entities
        ├─ Context Maps                       ├─ Value Objects
        └─ Ubiquitous Language                ├─ Domain Events
                                              ├─ Domain Services
                                              └─ Repositories
```

---

## Strategic Patterns

Strategic patterns help you understand and organize the big picture of your domain.

### Pattern: Ubiquitous Language
**Problem**: Communication gaps between technical and business teams.

**Solution**: Develop a shared language used by everyone (developers, business, documentation, code).

**Example**:
```
Business term: "Place Order"
Code: orderService.placeOrder(customer, items)
Database: orders table
Events: OrderPlaced
```

**When to Use**:
- Complex business domains
- Multiple stakeholders
- Knowledge-intensive projects

**Benefits**:
- ✅ Reduces translation errors
- ✅ Improves collaboration
- ✅ Code reflects business

---

### Pattern: Subdomains
**Problem**: How to organize a large domain?

**Solution**: Divide domain into subdomains based on business capabilities.

**Types**:
```
CORE DOMAIN         → Business differentiator (invest heavily)
SUPPORTING DOMAIN   → Needed but not differentiating (build internally)
GENERIC DOMAIN      → Commodity (buy or outsource)
```

**Example (E-commerce)**:
```
Core:
  - Catalog Management
  - Order Processing
  - Pricing Engine

Supporting:
  - Inventory Management
  - Shipping Calculator
  - Recommendation Engine

Generic:
  - Authentication
  - Payment Processing (use Stripe)
  - Email Notifications (use SendGrid)
```

**When to Use**:
- Large, complex domains
- Multiple business capabilities
- Need to prioritize investment

---

### Pattern: Bounded Context
**Problem**: How to manage different meanings of the same concept?

**Solution**: Define explicit boundaries where a model has specific meaning.

**Example**:
```
┌─────────────────┐     ┌─────────────────┐
│  Sales Context  │     │ Shipping Context│
│                 │     │                 │
│  "Order"        │     │  "Order"        │
│  - Customer     │     │  - Items        │
│  - Items        │     │  - Address      │
│  - Payment      │     │  - Carrier      │
└─────────────────┘     └─────────────────┘

Same word, different models
```

**When to Use**:
- Same concept has different meanings
- Large teams working on different parts
- Need clear model boundaries

**Benefits**:
- ✅ Clear model ownership
- ✅ Reduced complexity per context
- ✅ Independent evolution

---

### Pattern: Context Map
**Problem**: How do bounded contexts relate?

**Solution**: Document relationships and integration patterns between contexts.

**Relationship Patterns**:

**1. Partnership**
```
Context A ←───→ Context B
    (Both depend on each other)
```

**2. Shared Kernel**
```
Context A ──┬── Context B
            │
        [Shared Code]
```

**3. Customer-Supplier**
```
Context A (Customer) ←── Context B (Supplier)
    (A uses B's model)
```

**4. Conformist**
```
Context A → Follows → Context B
    (A adapts to B's model)
```

**5. Anti-Corruption Layer (ACL)**
```
Context A ← [ACL] ← Context B
    (ACL translates between models)
```

**6. Open Host Service**
```
Context A → [Public API] → Anyone
    (A provides public API)
```

**7. Published Language**
```
Context A → [Common Language] → Context B
    (Both use common protocol)
```

**When to Use**:
- Multiple bounded contexts
- Integration needed
- Model translation required

---

## Tactical Patterns

Tactical patterns help you implement the domain model in code.

### Pattern: Entity
**Problem**: How to model objects with identity and lifecycle?

**Solution**: Create objects defined by their identity, not attributes.

**Characteristics**:
- Has unique identity (ID)
- Mutable state
- Has lifecycle (created, modified, deleted)
- Encapsulates business logic

**Example**:
```typescript
class Order {
  constructor(
    public id: OrderId,        // Identity
    public customerId: CustomerId,
    private items: OrderItem[],
    public status: OrderStatus // Mutable
  ) {}

  // Business logic
  addItem(product: Product, quantity: number) {
    if (this.status !== 'DRAFT') {
      throw new Error('Cannot modify placed order');
    }
    this.items.push(new OrderItem(product, quantity));
  }

  place() {
    if (this.items.length === 0) {
      throw new Error('Cannot place empty order');
    }
    this.status = 'PLACED';
    // Raise domain event
    DomainEvents.raise(new OrderPlaced(this.id));
  }
}
```

**When to Use**:
- Object has lifecycle
- Identity matters more than attributes
- Business logic needed

---

### Pattern: Value Object
**Problem**: How to model objects defined by their attributes?

**Solution**: Create immutable objects defined by their value, not identity.

**Characteristics**:
- No identity (compared by value)
- Immutable
- Self-validating
- Can replace Entity attributes

**Example**:
```typescript
// Immutable value object
class Money {
  constructor(
    public readonly amount: number,
    public readonly currency: string
  ) {
    if (amount < 0) {
      throw new Error('Amount cannot be negative');
    }
  }

  // Operations return new instances
  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error('Cannot add different currencies');
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && 
           this.currency === other.currency;
  }
}

// Usage
const price = new Money(100, 'USD');
const tax = new Money(10, 'USD');
const total = price.add(tax); // New instance
```

**Common Value Objects**:
- Money, Address, DateRange, Email, PhoneNumber, Color, Coordinate

**When to Use**:
- Describe characteristics
- No lifecycle needed
- Can be immutable

**Benefits**:
- ✅ Thread-safe (immutable)
- ✅ Easy to test
- ✅ Self-validating

---

### Pattern: Aggregate
**Problem**: How to maintain consistency boundaries?

**Solution**: Group related entities under a single root entity.

**Characteristics**:
- Aggregate Root (AR) controls access
- Child entities only accessible via AR
- Invariants enforced within boundary
- Single transaction per aggregate

**Example**:
```typescript
// Aggregate Root
class Order {
  constructor(
    public id: OrderId,
    private items: OrderItem[],  // Child entities
    private shippingAddress: Address,
    public status: OrderStatus
  ) {}

  // All modifications go through root
  addItem(product: Product, quantity: number) {
    // Enforce invariant
    if (this.items.length >= 100) {
      throw new Error('Maximum 100 items per order');
    }
    this.items.push(new OrderItem(product, quantity));
  }

  // Business operation
  cancel() {
    if (this.status === 'SHIPPED') {
      throw new Error('Cannot cancel shipped order');
    }
    this.status = 'CANCELLED';
    DomainEvents.raise(new OrderCancelled(this.id));
  }
}

// Repository works with aggregates only
interface OrderRepository {
  findById(id: OrderId): Promise<Order>;
  save(order: Order): Promise<void>;  // Save entire aggregate
}
```

**Aggregate Design Guidelines**:
- Keep aggregates small (1 root + few children)
- Reference other aggregates by ID only
- One aggregate = one transaction
- Design around invariants

**When to Use**:
- Need consistency boundary
- Transaction boundary needed
- Invariants must be enforced

---

### Pattern: Domain Event
**Problem**: How to capture domain occurrences and decouple side effects?

**Solution**: Record significant domain events as immutable facts.

**Characteristics**:
- Past tense (OrderPlaced, PaymentReceived)
- Immutable (fact that happened)
- Contains all relevant data
- Triggers side effects

**Example**:
```typescript
// Event definition
class OrderPlaced implements DomainEvent {
  constructor(
    public readonly orderId: OrderId,
    public readonly customerId: CustomerId,
    public readonly total: Money,
    public readonly occurredOn: Date = new Date()
  ) {}
}

// Raise event in entity
class Order {
  place() {
    // ... business logic
    this.status = 'PLACED';
    
    // Raise event
    DomainEvents.raise(new OrderPlaced(
      this.id,
      this.customerId,
      this.calculateTotal()
    ));
  }
}

// Handle event
class OrderPlacedHandler implements EventHandler<OrderPlaced> {
  async handle(event: OrderPlaced) {
    // Side effects
    await emailService.sendConfirmation(event.customerId);
    await inventoryService.reserveItems(event.orderId);
    await analyticsService.trackOrder(event);
  }
}
```

**When to Use**:
- Need to track what happened
- Decouple side effects
- Eventual consistency acceptable
- Audit trail needed

**Benefits**:
- ✅ Loose coupling
- ✅ Audit trail
- ✅ Multiple side effects

---

### Pattern: Domain Service
**Problem**: Where to put logic that doesn't fit in entities/value objects?

**Solution**: Create stateless services for domain operations.

**When to Use**:
- Operation involves multiple aggregates
- No natural entity to own the logic
- External system interaction

**Example**:
```typescript
// Domain Service (not application service!)
class OrderFulfillmentService {
  constructor(
    private orderRepo: OrderRepository,
    private inventoryService: InventoryService,
    private shippingCalculator: ShippingCalculator
  ) {}

  // Business logic spanning aggregates
  async fulfillOrder(orderId: OrderId): Promise<void> {
    const order = await this.orderRepo.findById(orderId);
    
    if (!order.canBeFulfilled()) {
      throw new Error('Order cannot be fulfilled');
    }

    // Check inventory across warehouses
    for (const item of order.items) {
      const availability = await this.inventoryService.checkAvailability(
        item.productId
      );
      if (!availability.hasStock(item.quantity)) {
        throw new Error(`Insufficient stock for ${item.productId}`);
      }
    }

    // Calculate optimal shipping
    const shippingOption = await this.shippingCalculator.calculateBest(
      order.shippingAddress,
      order.items
    );

    order.assignShipping(shippingOption);
    await this.orderRepo.save(order);
  }
}
```

**Difference from Application Service**:
- **Domain Service**: Contains business logic
- **Application Service**: Orchestrates use cases, no business logic

---

### Pattern: Repository
**Problem**: How to abstract data access for aggregates?

**Solution**: Create collection-like interface for aggregates.

**Characteristics**:
- Works with aggregates only (not entities inside)
- Collection-like interface (add, remove, find)
- Abstracts persistence mechanism

**Example**:
```typescript
// Repository interface (in domain layer)
interface OrderRepository {
  findById(id: OrderId): Promise<Order | null>;
  findByCustomer(customerId: CustomerId): Promise<Order[]>;
  findByStatus(status: OrderStatus): Promise<Order[]>;
  save(order: Order): Promise<void>;
  remove(order: Order): Promise<void>;
}

// Implementation (in infrastructure layer)
class PostgresOrderRepository implements OrderRepository {
  constructor(private db: Database) {}

  async findById(id: OrderId): Promise<Order | null> {
    const row = await this.db.query(
      'SELECT * FROM orders WHERE id = $1',
      [id]
    );
    return row ? this.mapToDomain(row) : null;
  }

  async save(order: Order): Promise<void> {
    // Save entire aggregate in one transaction
    await this.db.transaction(async (tx) => {
      await tx.query('UPDATE orders SET ... WHERE id = $1', [order.id]);
      await tx.query('DELETE FROM order_items WHERE order_id = $1', [order.id]);
      for (const item of order.items) {
        await tx.query('INSERT INTO order_items ...', [/* item data */]);
      }
    });
  }
}
```

**When to Use**:
- Need to persist aggregates
- Want to abstract persistence
- Need testable domain layer

---

## DDD Layered Architecture

```
┌─────────────────────────────────────────┐
│           PRESENTATION LAYER            │
│         (Controllers, GraphQL)          │
├─────────────────────────────────────────┤
│          APPLICATION LAYER              │
│    (Use Cases, Application Services)    │
├─────────────────────────────────────────┤
│            DOMAIN LAYER                 │
│  (Entities, Value Objects, Aggregates,  │
│   Domain Events, Domain Services)       │
├─────────────────────────────────────────┤
│        INFRASTRUCTURE LAYER             │
│   (Repositories, External Services)     │
└─────────────────────────────────────────┘
```

**Dependency Rule**: Dependencies point inward (Infrastructure → Domain)

---

## Pattern Selection Guide

| Problem | Recommended Pattern |
|---------|-------------------|
| Complex business logic | Aggregate + Domain Service |
| Need identity | Entity |
| Describe characteristics | Value Object |
| Track what happened | Domain Event |
| Multiple aggregates involved | Domain Service |
| Different model meanings | Bounded Context |
| Context integration | Context Map patterns |
| Persistence abstraction | Repository |

---

## Related Skills

- **microservices-patterns** - Microservices architecture patterns
- **architecture-review-checklist** - Review DDD architecture
- **context-map** - Map bounded contexts

---

## Output Format

When using this skill, provide:
1. **Pattern name** and category (Strategic/Tactical)
2. **Problem** it solves
3. **Solution** with code example
4. **When to use**
5. **Trade-offs** (pros/cons)
6. **Related patterns**
7. **Code example** in user's language (TypeScript, C#, Java, Python, etc.)
