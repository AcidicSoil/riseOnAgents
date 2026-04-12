---
name: mvp-definition-framework
description: Framework for defining Minimum Viable Product scope, success criteria, and launch plan. Use after problem validation to scope the smallest product that delivers value.
---

# MVP Definition Framework

A structured framework for defining the Minimum Viable Product - the smallest product that delivers value and enables learning. Use this after problem validation.

---

## When to Use This Skill

Use this skill when:
- Problem has been validated
- You need to scope initial product
- You want to minimize time to market
- You need to define success criteria
- You're planning a launch strategy

---

## MVP Definition Process

### Step 1: Define Value Proposition
```
For [target customer]
Who [has this problem/need]
Our product [what it does]
Unlike [alternative]
We [unique value/differentiator]
```

### Step 2: Identify Core Jobs-to-be-Done
```
Primary Job: [main problem solved]
Related Jobs: [adjacent problems]
Emotional Jobs: [how user wants to feel]
```

### Step 3: Define MVP Features
| Feature | Type | Priority | MVP? |
|---------|------|----------|------|
| {Feature 1} | Core/Differentiator/Tablestakes | Must/Should/Could | ✅/❌ |
| {Feature 2} | ... | ... | ... |

### Step 4: Define Success Criteria
| Metric | Baseline | Target | Measurement Method |
|--------|----------|--------|-------------------|
| Activation rate | 0% | {target}% | {method} |
| Retention (D7) | 0% | {target}% | {method} |
| NPS | N/A | {target} | Survey |

### Step 5: Define Constraints
- **Time:** {launch date}
- **Budget:** ${amount}
- **Team:** {number} people
- **Quality:** {minimum quality bar}

---

## MVP Feature Prioritization

### Feature Categories

| Category | Description | Include in MVP? |
|----------|-------------|-----------------|
| **Core** | Essential to solve the problem | ✅ Yes |
| **Differentiator** | Unique value proposition | ✅ If core depends on it |
| **Tablestakes** | Expected by users | ❌ Unless critical |
| **Nice-to-have** | Enhancements | ❌ No |

### Prioritization Questions

For each feature, ask:

1. **Value Question:**
   - Does this directly solve the validated problem?
   - Can we launch without this?
   - Will users pay for this specifically?

2. **Effort Question:**
   - How complex is this to build?
   - Do we have the skills/capability?
   - Are there technical dependencies?

3. **Risk Question:**
   - What's the risk if we get this wrong?
   - Can we fix this post-launch?
   - Is this a one-way or two-way door decision?

### Prioritization Matrix

```
        High Value
            │
    ┌───────┼───────┐
    │  DO   │ SCHEDULE│
    │ NOW   │  LATER  │
────┼───────┼───────┼──── Effort
    │ SIMPLIFY│  DON'T  │
    │   OR   │  DO     │
    │ CUT    │         │
    └───────┼───────┘
            │
        Low Value
```

---

## MVP Success Criteria

### Activation Metrics
| Metric | Definition | Target |
|--------|------------|--------|
| Sign-up rate | % who create account | {X}% |
| Activation rate | % who complete key action | {X}% |
| Time to value | Time from sign-up to "aha" | < {X} days |

### Engagement Metrics
| Metric | Definition | Target |
|--------|------------|--------|
| DAU/MAU | Daily active / Monthly active | {X}% |
| Session frequency | Sessions per user per week | {X} |
| Session duration | Minutes per session | {X} min |

### Retention Metrics
| Metric | Definition | Target |
|--------|------------|--------|
| D1 Retention | % returning day 1 | {X}% |
| D7 Retention | % returning day 7 | {X}% |
| D30 Retention | % returning day 30 | {X}% |

### Satisfaction Metrics
| Metric | Definition | Target |
|--------|------------|--------|
| NPS | Net Promoter Score | {X} |
| CSAT | Customer Satisfaction | {X}/5 |
| CES | Customer Effort Score | < {X} |

---

## MVP Launch Plan

### Pre-Launch (2-4 weeks)
- [ ] Beta testing with {number} users
- [ ] Bug fixes from beta feedback
- [ ] Documentation created
- [ ] Support processes ready
- [ ] Analytics instrumented

### Launch (Week 0)
- [ ] Launch to {target audience}
- [ ] Marketing/communication sent
- [ ] Support team briefed
- [ ] Monitoring active

### Post-Launch (Weeks 1-4)
- [ ] Daily metrics review
- [ ] User feedback collection
- [ ] Weekly iteration planning
- [ ] Bug fixes deployed
- [ ] Success criteria evaluation

---

## MVP Documentation Template

```markdown
# MVP Definition: {Product Name}

## Value Proposition
{Value proposition statement}

## Target Customer
{Customer segment and persona}

## Problem Solved
{Validated problem description}

## MVP Features
| Feature | Description | Priority | Estimated Effort |
|---------|-------------|----------|------------------|
| {Feature 1} | {desc} | Must | {effort} |
| {Feature 2} | {desc} | Must | {effort} |

## Out of Scope (Post-MVP)
- {Feature A}
- {Feature B}

## Success Criteria
| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| {Metric 1} | {baseline} | {target} | {method} |
| {Metric 2} | {baseline} | {target} | {method} |

## Constraints
- **Timeline:** {date}
- **Budget:** ${amount}
- **Team:** {number} people

## Launch Plan
- **Beta:** {date range}
- **Launch:** {date}
- **Post-launch review:** {date}

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | {H/M/L} | {H/M/L} | {plan} |
| {Risk 2} | {H/M/L} | {H/M/L} | {plan} |

## Next Steps
1. {Step 1} - {owner} - {due date}
2. {Step 2} - {owner} - {due date}
```

---

## Common MVP Mistakes

### ❌ Too Much Scope
- Adding "just one more feature"
- Building for edge cases
- Solving multiple problems at once

### ❌ Too Little Validation
- Skipping problem validation
- Not talking to customers
- Building in stealth mode

### ❌ Wrong Success Metrics
- Vanity metrics (downloads, sign-ups)
- Not measuring behavior
- No baseline for comparison

### ❌ No Learning Plan
- Not instrumenting analytics
- No feedback collection
- No iteration plan

---

## Related Skills

- **problem-validation-framework** - Validate problem before MVP
- **product-market-fit-analysis** - Assess PMF after launch
- **go-to-market-playbook** - Plan launch strategy
- **product-metrics-framework** - Define comprehensive metrics

---

## Output Format

When using this skill, provide:
1. **Value proposition** statement
2. **MVP features** (prioritized list)
3. **Out of scope** items
4. **Success criteria** with targets
5. **Launch plan** with timeline
6. **Risks and mitigations**
7. **Next steps** with owners
