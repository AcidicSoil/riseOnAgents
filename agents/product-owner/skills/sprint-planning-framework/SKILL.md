---
name: sprint-planning-framework
description: Framework for sprint planning, capacity planning, and sprint goal definition. Use to plan effective sprints that deliver value predictably.
---

# Sprint Planning Framework

A structured framework for planning sprints, calculating capacity, and defining sprint goals. Use this to plan effective, predictable sprints.

---

## When to Use This Skill

Use this skill when:
- Planning upcoming sprint
- Calculating team capacity
- Defining sprint goals
- Committing to backlog items
- Managing sprint scope

---

## Sprint Planning Meeting

### Agenda (2 hours for 2-week sprint)

| Section | Time | Participants | Purpose |
|---------|------|--------------|---------|
| **Part 1: What** | 60 min | PO + Team | Select backlog items |
| **Break** | 10 min | - | - |
| **Part 2: How** | 50 min | Team only | Plan implementation |

---

### Part 1: What (60 min)

**Step 1: Review Capacity (10 min)**
```
Team Capacity = (Team size × Sprint days × Focus factor) - Time off

Example:
5 people × 10 days × 0.7 focus = 35 person-days
- 3 days vacation
- 2 days holiday
= 30 person-days available
```

**Step 2: Review Velocity (10 min)**
```
Average Velocity = (Sum of completed points) / (Number of sprints)

Example:
Sprint 1: 25 points
Sprint 2: 28 points
Sprint 3: 23 points
Average: 25.3 points → Plan for 25 points
```

**Step 3: Select Backlog Items (30 min)**
```
For each item:
1. PO presents item and acceptance criteria
2. Team asks clarifying questions
3. Team estimates (if needed)
4. Decide: Include in sprint or not?
5. Repeat until capacity reached
```

**Step 4: Define Sprint Goal (10 min)**
```
Sprint Goal Format:
"We will {achieve outcome} by {building what}"

Examples:
- "We will improve checkout conversion by simplifying the payment flow"
- "We will enable social login by integrating Google and Facebook auth"
- "We will reduce API latency by implementing caching layer"
```

---

### Part 2: How (50 min)

**Step 1: Break Down Items (20 min)**
```
For each selected item:
1. Identify tasks needed
2. Estimate tasks (hours)
3. Assign owners (optional)
```

**Step 2: Identify Dependencies (10 min)**
```
- Internal dependencies (between stories)
- External dependencies (other teams, vendors)
- Technical dependencies (infrastructure, APIs)
```

**Step 3: Confirm Commitment (10 min)**
```
Team confirms:
- Total story points: {X}
- Total task hours: {X}
- Capacity available: {X}
- Commitment: Yes/No
```

**Step 4: Risk Review (10 min)**
```
- What could go wrong?
- What are the unknowns?
- How will we handle scope changes?
```

---

## Capacity Planning

### Focus Factor

| Team Maturity | Focus Factor |
|---------------|--------------|
| New team | 0.5-0.6 |
| Established team | 0.6-0.7 |
| High-performing team | 0.7-0.8 |

### Capacity Deductions

| Activity | Typical Deduction |
|----------|-------------------|
| Sprint ceremonies | 10-15% |
| Email/Slack | 10-15% |
| Meetings (non-sprint) | 5-10% |
| Support/on-call | 5-20% |
| Context switching | 10-15% |

### Capacity Template

```markdown
## Sprint {N} Capacity

### Team Availability
| Team Member | Days Available | Notes |
|-------------|----------------|-------|
| {Name 1} | {X} days | {vacation, etc.} |
| {Name 2} | {X} days | {notes} |
| **Total** | **{X} person-days** | |

### Focus Factor
**Factor:** {0.7}
**Effective Capacity:** {X} person-days × {0.7} = {Y} person-days

### Velocity-Based Planning
**Average Velocity:** {X} points
**Planned Velocity:** {X} points (or adjusted for capacity)

### Committed Stories
| Story | Points | Owner |
|-------|--------|-------|
| {Story 1} | {X} | {name} |
| {Story 2} | {X} | {name} |
| **Total** | **{X} points** | |
```

---

## Sprint Goal Guidelines

### Good Sprint Goals

✅ **Specific:** Clear what will be delivered
✅ **Measurable:** Success can be verified
✅ **Achievable:** Realistic for sprint capacity
✅ **Relevant:** Tied to product goals
✅ **Time-bound:** Achievable within sprint

### Examples

| Bad Sprint Goal | Good Sprint Goal |
|-----------------|------------------|
| "Work on checkout" | "Reduce checkout abandonment by 10% by simplifying payment flow" |
| "Fix bugs" | "Resolve top 5 customer-reported bugs to improve NPS" |
| "Implement features" | "Enable user profile management with avatar upload" |

---

## Sprint Planning Documentation Template

```markdown
# Sprint {N} Plan

## Sprint Details
**Dates:** {start} to {end}
**Sprint Goal:** {goal statement}

## Team Capacity
| Team Member | Availability | Notes |
|-------------|--------------|-------|
| {Name} | {X}% | {notes} |
| **Total Capacity** | **{X} points** | |

## Committed Stories

| Story | Points | Priority | Owner | Status |
|-------|--------|----------|-------|--------|
| {Story 1} | {X} | 1 | {name} | To Do |
| {Story 2} | {X} | 2 | {name} | To Do |
| **Total** | **{X} points** | | | |

## Sprint Backlog (Tasks)

### Story 1: {Name}
- [ ] Task 1 ({X} hours) - {owner}
- [ ] Task 2 ({X} hours) - {owner}
- [ ] Task 3 ({X} hours) - {owner}

### Story 2: {Name}
- [ ] Task 1 ({X} hours) - {owner}
- [ ] Task 2 ({X} hours) - {owner}

## Dependencies & Risks
| Type | Description | Mitigation |
|------|-------------|------------|
| Dependency | {description} | {plan} |
| Risk | {description} | {plan} |

## Definition of Done
- [ ] Code implemented
- [ ] Unit tests passing
- [ ] Code reviewed
- [ ] QA tested
- [ ] Documentation updated
- [ ] PO acceptance

## Notes
{Any additional context or decisions}
```

---

## Common Sprint Planning Mistakes

### ❌ Over-commitment
- Planning more than average velocity
- Not accounting for time off
- Ignoring focus factor

**Solution:** Use historical velocity, apply focus factor

### ❌ Vague Sprint Goal
- "Continue working on X"
- No clear success criteria

**Solution:** Define specific, measurable outcome

### ❌ No Task Breakdown
- Stories not broken into tasks
- No hour estimates

**Solution:** Break down, estimate tasks in Part 2

### ❌ Ignoring Dependencies
- Not identifying blockers
- No mitigation plan

**Solution:** Explicitly review dependencies

---

## Related Skills

- **backlog-prioritization** - Prioritize before planning
- **agile-ceremonies-guide** - Other Scrum ceremonies
- **story-slicing** - Break down large stories

---

## Output Format

When using this skill, provide:
1. **Sprint goal** (specific, measurable)
2. **Team capacity** (person-days, focus factor)
3. **Committed stories** with points
4. **Task breakdown** with hours
5. **Dependencies and risks** with mitigation
6. **Definition of Done** confirmation
