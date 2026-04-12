---
description: Testing rules and guidelines for unit tests, integration tests, and test coverage standards
applyTo: '**/*.test.ts,**/*.test.js,**/*.spec.ts,**/*.spec.js,**/tests/**'
---

# Testing Rules

Testing rules and guidelines for writing comprehensive, maintainable tests with proper coverage.

## Test Structure

### Test File Organization
Match source file structure:
```
/src/user/user.service.ts  →  /tests/user/user.service.test.ts
```

### Test Naming
```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => { ... });
    it('should throw ValidationError for invalid email', async () => { ... });
    it('should throw ConflictException for duplicate email', async () => { ... });
  });
});
```

### AAA Pattern
```typescript
it('should calculate total correctly', () => {
  // Arrange
  const items = [{ price: 10, quantity: 2 }];
  
  // Act
  const total = calculateTotal(items);
  
  // Assert
  expect(total).toBe(20);
});
```

## Coverage Targets

| Type | Minimum | Target | Critical Files |
|------|---------|--------|----------------|
| **Line Coverage** | 70% | 80% | 100% |
| **Branch Coverage** | 60% | 70% | 100% |
| **Function Coverage** | 70% | 80% | 100% |

### Critical Files (100% Required)
- Authentication/Authorization logic
- Payment processing
- Data validation
- Business rules
- Security-sensitive code

## What to Test

### ✅ Test
- Business logic
- Validation logic
- Error handling
- Edge cases
- API contracts

### ❌ Don't Test
- Simple getters/setters
- Framework code
- Third-party libraries
- Implementation details

## Unit Testing

### Mocking Dependencies
```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = { create: jest.fn() } as any;
    service = new UserService(mockRepository);
  });

  it('should create user and send email', async () => {
    // Arrange
    mockRepository.create.mockResolvedValue({ id: '123', email: 'test@example.com' });

    // Act
    const result = await service.create({ email: 'test@example.com' });

    // Assert
    expect(result).toBeDefined();
    expect(mockRepository.create).toHaveBeenCalled();
  });
});
```

### Testing Async Code
```typescript
// Success case
it('should fetch user from database', async () => {
  const user = await service.getUser('123');
  expect(user).toBeDefined();
});

// Error case
it('should throw NotFoundError for invalid ID', async () => {
  await expect(service.getUser('invalid'))
    .rejects
    .toThrow(NotFoundError);
});
```

### Parameterized Tests
```typescript
it.each([
  ['invalid email', { email: 'invalid', name: 'Test' }],
  ['empty name', { email: 'test@example.com', name: '' }],
])('should reject %s', (_, invalidData) => {
  expect(() => validator.validate(invalidData))
    .toThrow(ValidationError);
});
```

## Integration Testing

### API Testing
```typescript
describe('POST /api/users', () => {
  it('should create user and return 201', async () => {
    const userData = { email: 'test@example.com', name: 'Test' };

    const response = await request(app)
      .post('/api/users')
      .send(userData)
      .expect(201);

    expect(response.body).toHaveProperty('id');
  });
});
```

## Test Data Management

### Factories
```typescript
const userFactory = {
  valid: () => ({ email: 'test@example.com', name: 'Test' }),
  withEmail: (email: string) => ({ ...userFactory.valid(), email }),
  invalid: () => ({ email: 'invalid', name: '' }),
};

// Usage
it('should create user', () => {
  const userData = userFactory.valid();
  // ...
});
```

## Quality Standards

### Test Quality Checklist
- [ ] Tests are independent (run in any order)
- [ ] Tests are repeatable (same result always)
- [ ] Tests are fast (< 100ms per unit test)
- [ ] Test names describe scenario and expectation
- [ ] Uses Arrange-Act-Assert pattern
- [ ] No test interdependencies
- [ ] No flaky tests

### Warning Signs
- ❌ Tests break with minor refactoring
- ❌ Multiple tests fail for same reason
- ❌ Tests are hard to understand
- ❌ Test code more complex than production code

## References

### Skills
- **testing-patterns** - AAA, mocking, test data management
- **testing-scenarios** - Validation, error handling, edge cases

### Books
- [The Art of Unit Testing](https://www.manning.com/books/the-art-of-unit-testing-third-edition) - Roy Osherove
- [Unit Testing Principles, Practices, and Patterns](https://www.manning.com/books/unit-testing) - Vladimir Khorikov

### Documentation
- [Jest Documentation](https://jestjs.io/)
- [Playwright Documentation](https://playwright.dev/)
