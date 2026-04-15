---
name: acceptance-criteria-gherkin
description: Acceptance criteria writing using Gherkin syntax (Given/When/Then). Use when writing user stories, acceptance criteria, or BDD tests.
license: Apache 2.0
---

# Acceptance Criteria with Gherkin

## When to Use This Skill

- Writing acceptance criteria
- Creating user stories
- Writing BDD tests

## Core Concepts

### Gherkin Syntax

```gherkin
Feature: Password Reset

Scenario: User successfully resets password
  Given I am on the login page
  When I click "Forgot Password"
  And I enter my registered email
  And I click "Send Reset Link"
  Then I should receive a password reset email
  And I should see a confirmation message
```

### Types of Scenarios

**Functional:**
```gherkin
Scenario: User successfully logs in
  Given I am a registered user
  When I enter valid credentials
  Then I should be redirected to dashboard
```

**Validation:**
```gherkin
Scenario: Invalid email format
  Given I am on the registration page
  When I enter "invalid-email"
  And I click "Submit"
  Then I should see error "Invalid email format"
```

**Error Handling:**
```gherkin
Scenario: Email not found
  Given I am on the password reset page
  When I enter "nonexistent@example.com"
  And I click "Send Reset Link"
  Then I should see generic success message
  But no email should be sent
```

**Security:**
```gherkin
Scenario: Rate limiting
  Given I have requested 5 password resets in the last hour
  When I request another password reset
  Then I should see "Too many attempts, try again later"
  And no email should be sent
```

## Best Practices

- One scenario per behavior
- Clear Given-When-Then structure
- Cover happy path, errors, and edge cases

## References

- [Cucumber Gherkin Reference](https://cucumber.io/docs/gherkin/)
