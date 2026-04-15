---
name: story-slicing
description: User story slicing techniques for breaking large stories into smaller, implementable pieces. Use when refining backlog or splitting epics.
license: Apache 2.0
---

# Story Slicing Techniques

## When to Use This Skill

- Refining backlog
- Splitting epics
- Making stories implementable

## Core Concepts

### By Workflow Step

```
Epic: User Registration
├── Story: User can enter registration details
├── Story: User can verify email address
├── Story: User can complete profile
└── Story: User can set preferences
```

### By Data Boundaries

```
Epic: Product Management
├── Story: User can create products
├── Story: User can view products
├── Story: User can update products
└── Story: User can delete products
```

### By User Roles

```
Epic: Content Management
├── Story: Authors can create articles
├── Story: Editors can review articles
├── Story: Admins can publish articles
└── Story: Readers can comment on articles
```

### By Complexity

```
Epic: Payment Processing
├── Story: User can pay with credit card (simple)
├── Story: User can pay with PayPal (medium)
├── Story: User can pay with bank transfer (complex)
```

### INVEST Criteria

| Criteria | Description |
|----------|-------------|
| **Independent** | Can be developed separately |
| **Negotiable** | Details can be discussed |
| **Valuable** | Delivers value to user |
| **Estimable** | Team can estimate effort |
| **Small** | Can be completed in one sprint |
| **Testable** | Has clear acceptance criteria |

## References

- [User Story Mapping](https://www.oreilly.com/library/view/user-story-mapping/9781491904893/) - Jeff Patton
