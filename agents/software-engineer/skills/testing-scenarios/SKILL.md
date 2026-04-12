---
name: testing-scenarios
description: Testing scenarios for validation, error handling, and edge cases. Use when writing comprehensive tests covering happy paths, errors, and edge cases.
license: Apache 2.0
---

# Testing Scenarios

## When to Use This Skill

- Writing comprehensive tests
- Testing edge cases
- Testing error scenarios

## Core Concepts

### Testing Validation

```typescript
describe('Validation', () => {
  it.each([
    ['invalid email', { email: 'invalid', name: 'Test' }],
    ['empty name', { email: 'test@example.com', name: '' }],
    ['short password', { email: 'test@example.com', password: '123' }],
  ])('should reject %s', (_, invalidData) => {
    expect(() => validator.validate(invalidData))
      .toThrow(ValidationError);
  });
});
```

### Testing Error Handling

```typescript
it('should handle database connection error', async () => {
  mockRepository.create.mockRejectedValue(
    new DatabaseConnectionError('Connection failed')
  );
  
  await expect(service.createUser(userData))
    .rejects
    .toThrow(DatabaseConnectionError);
});
```

### Testing Edge Cases

```typescript
describe('Edge Cases', () => {
  it('should handle empty array', () => {
    expect(service.calculateTotal([])).toBe(0);
  });
  
  it('should handle null/undefined', () => {
    expect(service.process(null)).toEqual(defaultValue);
  });
  
  it('should handle special characters', () => {
    const input = '<script>alert("xss")</script>';
    expect(service.sanitize(input)).not.toContain('<script>');
  });
});
```

### Async Testing

```typescript
it('should fetch user data', async () => {
  const result = await service.getUser('123');
  expect(result).toBeDefined();
});

it('should throw error', async () => {
  await expect(service.invalidOperation())
    .rejects
    .toThrow(ValidationError);
});
```

## References

- [Testing JavaScript Applications](https://www.manning.com/books/testing-javascript-applications)
