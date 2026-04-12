---
description: User story writing rules and guidelines for creating well-formed stories with acceptance criteria following INVEST principles
applyTo: '**/docs/product/**,**/docs/stories/**,**/*.stories.md'
---

# User Story Rules

User story writing rules and guidelines for creating well-formed user stories with clear acceptance criteria following INVEST principles and agile best practices.

## User Story Format

### Standard Format
✅ **All user stories must follow:**
```
As a {type of user}
I want {goal/desire}
So that {benefit/value}
```

### User Type Guidelines
✅ **Be specific:**
- Registered user
- First-time visitor
- Premium subscriber
- Administrator
- Customer support representative
- Content creator

❌ **Avoid generic:**
- User (too vague)
- Person (too vague)
- Someone (too vague)

### Goal/Desire Guidelines
✅ **Be specific about what:**
- Reset my password
- Filter products by price range
- Export my data to CSV
- View order history
- Update profile information

❌ **Avoid vague:**
- Do stuff
- Use the system
- Make it work
- Better functionality

### Benefit/Value Guidelines
✅ **Articulate clear value:**
- So that I can regain access to my account
- So that I can find products within my budget
- So that I can analyze my data in external tools
- So that I can track my orders

❌ **Avoid meaningless:**
- So that it works
- So that the system is complete
- So that users are happy
- So that we have this feature

## INVEST Criteria

### Independent
✅ **Story must be:**
- Self-contained
- Can be developed separately
- No dependencies on other stories
- Can be released independently
- Delivers value on its own

**Check:**
- Can this story be implemented without waiting for other stories?
- Does this story deliver value independently?
- Can this story be tested in isolation?

### Negotiable
✅ **Story must be:**
- Not overly prescriptive
- Leaves room for team discussion
- Focuses on what, not how
- A conversation starter

**Check:**
- Is there room for the team to discuss implementation approach?
- Are the details flexible?
- Is this a contract or a conversation starter?

### Valuable
✅ **Story must:**
- Deliver value to user
- User can perceive the value
- Not be technical infrastructure only
- Have clear benefit

**Check:**
- Would the user care about this story?
- Does this deliver observable value?
- Can you articulate the benefit in user terms?

### Estimable
✅ **Story must:**
- Have enough detail to estimate
- Be understood by team
- Have no major unknowns
- Be feasible to implement

**Check:**
- Can the team provide a story point estimate?
- Is the scope clear enough?
- Are there any major unknowns or blockers?

### Small
✅ **Story must:**
- Be completable in one sprint
- Be less than 5 story points (ideal)
- Not be an epic in disguise
- Be small enough to manage

**Check:**
- Can this be completed in one sprint?
- Is it smaller than 5 story points?
- Should this be split into multiple stories?

### Testable
✅ **Story must:**
- Have clear acceptance criteria
- Be verifiable
- Have observable outcomes
- Be testable by QA

**Check:**
- Can QA write test cases from this story?
- Are acceptance criteria clear and testable?
- Can you demonstrate when the story is complete?

## Acceptance Criteria

### Gherkin Format
✅ **All acceptance criteria must use:**
```gherkin
Feature: {Feature name}

Scenario: {Scenario name}
  Given {precondition}
  When {action}
  Then {expected outcome}
  And {additional outcome}
```

### Scenario Coverage
✅ **Must include:**
- Happy path (main success scenario)
- Alternative paths (variations)
- Error scenarios (failure handling)
- Edge cases (boundary conditions)
- Validation scenarios (input validation)
- Performance scenarios (if applicable)
- Security scenarios (if applicable)

### Scenario Quality
✅ **Each scenario must:**
- Have clear, descriptive name
- Be independent from other scenarios
- Use Given/When/Then correctly
- Be testable (pass/fail)
- Include all necessary data
- Be understandable by non-technical stakeholders

### Given-When-Then Guidelines

**Given (Precondition):**
✅ **Do:**
- Set up initial state
- Be specific about context
- Include only relevant information

❌ **Don't:**
- Include multiple unrelated conditions
- Be vague about state
- Include implementation details

**When (Action):**
✅ **Do:**
- Describe user action
- Be specific and clear
- Use active voice

❌ **Don't:**
- Describe system behavior
- Be vague about action
- Use passive voice

**Then (Outcome):**
✅ **Do:**
- Describe expected result
- Be specific and measurable
- Include observable behavior

❌ **Don't:**
- Be vague about outcome
- Include implementation details
- Mix multiple unrelated outcomes

## Story Writing Best Practices

### One Story, One Value
✅ **Each story should:**
- Deliver single unit of value
- Be focused on one user goal
- Not be combined with "AND"
- Stand alone

❌ **Avoid:**
- "As a user, I want to login AND view my profile" (two stories)
- "As a user, I want to create AND delete items" (two stories)

### User-Centric Language
✅ **Use:**
- User terminology
- Business language
- Ubiquitous language

❌ **Avoid:**
- Technical jargon in story
- Database terminology
- Implementation details

### Technical Stories
✅ **If technical story is necessary:**
- Frame in terms of user benefit
- Explain why it's needed
- Link to business value

**Example:**
```
As a development team
We want to upgrade the database
So that we can improve query performance by 50%
```

## Story Slicing

### Slicing Techniques
✅ **Slice by:**
- Workflow steps
- Data boundaries
- User roles
- Functionality (simple to complex)
- Quality/completeness

### Workflow Slicing
```
Epic: User Registration
Slice 1: User can enter email and password
Slice 2: User can verify email address
Slice 3: User can complete profile
Slice 4: User can set preferences
```

### Data Slicing
```
Epic: Product Management
Slice 1: User can create products (basic fields)
Slice 2: User can add product images
Slice 3: User can add product variants
Slice 4: User can manage inventory
```

### Role Slicing
```
Epic: Content Management
Slice 1: Authors can create drafts
Slice 2: Editors can review and edit
Slice 3: Admins can approve and publish
Slice 4: Readers can comment
```

## Definition of Ready

### Story is READY when:
- ✅ Clear and understandable
- ✅ Follows standard format
- ✅ Meets INVEST criteria
- ✅ Acceptance criteria defined
- ✅ Dependencies identified
- ✅ Estimated by team
- ✅ Sized appropriately (< 5 points)
- ✅ Testable
- ✅ UX/design available (if needed)
- ✅ Technical feasibility confirmed
- ✅ No major unknowns

### Ready Checklist
```markdown
## Definition of Ready Checklist

- [ ] User story format correct
- [ ] User type clearly defined
- [ ] Goal is specific
- [ ] Benefit is clear
- [ ] Acceptance criteria in Gherkin
- [ ] Covers happy path
- [ ] Covers error scenarios
- [ ] Dependencies identified
- [ ] Story points estimated
- [ ] < 5 story points
- [ ] UX mockups available (if needed)
- [ ] Team confirms feasibility
```

## Definition of Done

### Story is DONE when:
- ✅ Code implemented
- ✅ Acceptance criteria met
- ✅ Unit tests written and passing
- ✅ Integration tests passing
- ✅ Code reviewed and approved
- ✅ Documentation updated
- ✅ Deployed to staging
- ✅ Product Owner acceptance
- ✅ No critical bugs
- ✅ Performance criteria met
- ✅ Security review (if applicable)

### Done Checklist
```markdown
## Definition of Done Checklist

- [ ] Code implemented per requirements
- [ ] All acceptance criteria passing
- [ ] Unit tests written (>80% coverage)
- [ ] Integration tests passing
- [ ] Code reviewed (2+ approvals)
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Product Owner demonstrated and accepted
- [ ] No critical/high priority bugs
- [ ] Performance criteria met
- [ ] Security review completed (if applicable)
```

## Story Estimation

### Story Point Scale
| Points | Complexity | Time | Example |
|--------|------------|------|---------|
| **1** | Trivial | < 2 hours | Fix typo, change text |
| **2** | Simple | 2-4 hours | Add field to form |
| **3** | Moderate | 4-8 hours | Add new API endpoint |
| **5** | Complex | 1-2 days | Implement payment integration |
| **8** | Very Complex | 2-4 days | Multi-system integration |
| **13** | Too Large | Should split | Epic needing breakdown |

### Estimation Factors
✅ **Consider:**
- Complexity of logic
- Amount of code
- Uncertainty/unknowns
- Dependencies
- Testing effort

❌ **Don't consider:**
- Who will implement
- How long in hours
- Priority/value
- External deadlines

## Story Documentation

### Story Document Structure
```markdown
# User Story: {Story ID} - {Story Name}

## Story
**As a** {user type}
**I want** {goal}
**So that** {benefit}

## Acceptance Criteria
{Gherkin scenarios}

## Non-Functional Requirements
- Performance: {requirement}
- Security: {requirement}
- Usability: {requirement}

## Technical Notes
{Technical context or constraints}

## Dependencies
{List any dependencies}

## Story Points
{Estimate}

## Definition of Done
{DoD checklist}
```

### Story Location
✅ **Stories must be stored in:**
- `/docs/product/{feature}_Stories.md`
- Project management tool (Jira, Azure DevOps)
- Linked to PRD

## Quality Checklist

### Story Quality
- [ ] Follows standard format
- [ ] Meets all INVEST criteria
- [ ] Has clear acceptance criteria
- [ ] Appropriately sized
- [ ] Testable
- [ ] Valuable to user
- [ ] Estimated by team

### Acceptance Criteria Quality
- [ ] Written in Gherkin format
- [ ] Covers happy path
- [ ] Covers error scenarios
- [ ] Covers edge cases
- [ ] Testable (pass/fail)
- [ ] Clear pass/fail criteria
- [ ] Includes non-functional requirements

## Common Mistakes

### Format Mistakes
- ❌ Missing user type
- ❌ Missing benefit
- ❌ Too vague
- ❌ Technical focus
- ❌ Multiple users in one story

### Acceptance Criteria Mistakes
- ❌ No acceptance criteria
- ❌ Untestable criteria
- ❌ Too few scenarios
- ❌ Missing error scenarios
- ❌ Missing edge cases

### INVEST Violations
- ❌ Dependencies on other stories (not Independent)
- ❌ Overly prescriptive (not Negotiable)
- ❌ No user value (not Valuable)
- ❌ Too vague to estimate (not Estimable)
- ❌ Too large for one sprint (not Small)
- ❌ Cannot be tested (not Testable)

### Sizing Mistakes
- ❌ Epics disguised as stories
- ❌ Multiple features in one story
- ❌ Technical tasks instead of user stories
- ❌ Infrastructure work without user value

## References

- [User Stories Applied](https://www.oreilly.com/library/view/user-stories-applied/0321205685/) - Mike Cohn
- [User Story Mapping](https://www.oreilly.com/library/view/user-story-mapping/9781491904893/) - Jeff Patton
- [Specification by Example](https://www.oreilly.com/library/view/specification-by-example/9781617290084/) - Gojko Adzic
- [BDD in Action](https://www.manning.com/books/bdd-in-action-second-edition) - John Ferguson Smart
- [Agile Modeling](https://www.oreilly.com/library/view/agile-modeling/0471202827/) - Scott W. Ambler

## MCP Integrations & Tools Required

**Always use available MCPs** when implementing or verifying rules:
- 🎯 Use **GitHub MCP** to find existing codebase examples matching this rule
- 🎯 Use **Brave Search MCP** to lookup latest documentation or official best practices
- 🎯 Use **Context7 MCP** to query historical context related to codebase structure before making decisions
