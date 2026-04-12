---
description: Software development rules and guidelines for clean code, best practices, and maintainable implementations
applyTo: '**/*.ts,**/*.js,**/*.cs,**/*.java,**/*.py,**/src/**'
---

# Coding Rules

Software development rules and guidelines for writing clean, maintainable, and production-ready code.

## Code Quality Standards

### Clean Code Principles

**Meaningful Names:** Use descriptive names that reveal intent
- ✅ Good: `calculateMonthlyInterest`, `daysSinceCreation`, `isValidUser`
- ❌ Bad: `calc`, `d`, `flag`

**Small Functions:** Functions should do ONE thing, < 20 lines
- Break complex functions into smaller, focused pieces

**Single Responsibility:** One reason to change per class
- ✅ Good: `UserService`, `UserRepository`, `EmailService` (separate)
- ❌ Bad: `UserService` that does everything

**DRY (Don't Repeat Yourself):** Extract common logic into reusable functions

## SOLID Principles

### S - Single Responsibility
Each class has only one reason to change.

### O - Open/Closed
Open for extension, closed for modification.

### L - Liskov Substitution
Subtypes must be substitutable for their base types.

### I - Interface Segregation
Many specific interfaces are better than one general interface.

### D - Dependency Inversion
Depend on abstractions, not concretions.

## Code Organization

### File Structure
```
/src
├── /feature-name/
│   ├── feature.service.ts
│   ├── feature.controller.ts
│   └── feature.model.ts
└── /tests/
```

### Naming Conventions
- Classes: `PascalCase` (UserService)
- Functions: `camelCase` (calculateTotal)
- Constants: `UPPER_SNAKE_CASE` (MAX_RETRY_COUNT)
- Booleans: `is/has/can` prefix (isValid, hasPermission)

## Error Handling

### Custom Error Classes
```typescript
class AppError extends Error {
  constructor(public code: string, message: string, public statusCode: number) { }
}
class ValidationError extends AppError { constructor(message: string) { super('VALIDATION_ERROR', message, 400); } }
```

### Exception Handling
- Handle specific errors first
- Log appropriately (WARN for expected, ERROR for unexpected)
- Never expose internal details to users

## Documentation

- Comments should explain **why**, not **what**
- Use JSDoc for public APIs
- Document parameters, returns, and thrown exceptions

## Performance

- Avoid N+1 queries (use eager loading)
- Cache frequently accessed data
- Use efficient array operations (map, filter over forEach)

## Security

- Validate all inputs (use Zod, Joi, etc.)
- Hash passwords (bcrypt)
- Never log sensitive data

## Testing Requirements

- Tests must be independent and repeatable
- Use Arrange-Act-Assert pattern
- Cover happy paths, edge cases, and error scenarios

## References

### Skills
- **coding-standards** - Detailed examples and patterns
- **clean-code-principles** - Clean code guidance
- **solid-principles** - SOLID principles

### Books
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Robert C. Martin
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/) - Andrew Hunt
