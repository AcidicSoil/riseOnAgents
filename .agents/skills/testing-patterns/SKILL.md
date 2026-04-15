---
name: testing-patterns
description: Testing patterns including AAA, mocking, and test data management. Use when writing unit tests, integration tests, or test suites.
license: Apache 2.0
---

# Testing Patterns

## When to Use This Skill

- Writing unit tests
- Writing integration tests
- Setting up test infrastructure

## Core Concepts

### AAA Pattern (Arrange-Act-Assert)

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create user with valid data', async () => {
      // Arrange
      const createDto = { email: 'test@example.com', name: 'Test' };
      
      // Act
      const result = await service.createUser(createDto);
      
      // Assert
      expect(result).toBeDefined();
      expect(result.email).toBe(createDto.email);
    });
  });
});
```

### Mocking

```typescript
const mockRepository = {
  findById: jest.fn(),
  create: jest.fn(),
} as jest.Mocked<UserRepository>;

mockRepository.findById.mockResolvedValue({ id: '123' });
```

### Test Data Factory

```typescript
const userFactory = {
  valid: () => ({ email: 'test@example.com', name: 'Test' }),
  withEmail: (email: string) => ({ ...userFactory.valid(), email }),
  invalid: () => ({ email: 'invalid', name: '' }),
};
```

### Test Naming

```typescript
// Good: Describes scenario and expectation
it('should return 404 when user not found', async () => { ... });
it('should reject invalid email format', () => { ... });

// Bad
it('should work', () => { ... });
```

## References

- [Jest Documentation](https://jestjs.io/)
- [Playwright Documentation](https://playwright.dev/)
