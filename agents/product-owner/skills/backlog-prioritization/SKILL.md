---
name: backlog-prioritization
description: Framework for prioritizing product backlog items. Use techniques like RICE, MoSCoW, WSJF to make data-driven prioritization decisions.
---

# Backlog Prioritization Framework

A comprehensive framework for prioritizing product backlog items using proven techniques. Use this to make data-driven prioritization decisions.

---

## When to Use This Skill

Use this skill when:
- Planning sprints or quarters
- Deciding what to build next
- Managing competing priorities
- Communicating priorities to stakeholders
- Saying "no" or "not now"

---

## Prioritization Techniques

### 1. RICE Scoring

**Formula:**
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

**Components:**

| Component | Scale | Description |
|-----------|-------|-------------|
| **Reach** | Number | How many users affected per period |
| **Impact** | 0.25-3 | 3=Massive, 2=High, 1=Medium, 0.5=Low, 0.25=Minimal |
| **Confidence** | 50-100% | 100%=Data-backed, 80%=Intuition, 50%=Guess |
| **Effort** | Person-months | Total team effort required |

**Example:**
```
Feature: Password Reset

Reach: 10,000 users/month
Impact: 2 (High)
Confidence: 80%
Effort: 2 person-months

RICE = (10,000 × 2 × 0.80) / 2 = 8,000
```

**When to Use:**
- ✅ Data-driven prioritization
- ✅ Comparing very different initiatives
- ✅ Quarterly planning

---

### 2. MoSCoW Prioritization

**Categories:**

| Priority | Description | % of Effort |
|----------|-------------|-------------|
| **Must Have** | Critical for success, non-negotiable | ~60% |
| **Should Have** | Important, significant value | ~20% |
| **Could Have** | Desirable, nice to have | ~20% |
| **Won't Have** | Agreed to exclude for now | 0% |

**Examples:**

| Feature | Priority | Rationale |
|---------|----------|-----------|
| User authentication | Must | Can't launch without it |
| Social login | Should | Important but not critical |
| Dark mode | Could | Nice to have |
| AI recommendations | Won't | Out of scope for MVP |

**When to Use:**
- ✅ MVP scoping
- ✅ Sprint planning
- ✅ Stakeholder alignment

---

### 3. Value vs. Effort Matrix

**4-Quadrant Matrix:**

```
        High Value
            │
  ┌─────────┴─────────┐
  │  DO FIRST         │  SCHEDULE
  │  (Quick Wins)     │  (Major Projects)
────┼─────────┼─────────┼──── Effort
  │  MAYBE            │  DON'T DO
  │  (Fill-ins)       │  (Thankless Tasks)
  └─────────┴─────────┘
            │
        Low Value
```

**Scoring:**

| Dimension | Scale |
|-----------|-------|
| **Value** | 1-10 (10=highest value) |
| **Effort** | 1-10 (10=highest effort) |

**Prioritization:**
1. **Do First:** High Value, Low Effort (quick wins)
2. **Schedule:** High Value, High Effort (major projects)
3. **Maybe:** Low Value, Low Effort (fill-ins)
4. **Don't Do:** Low Value, High Effort (avoid)

**When to Use:**
- ✅ Quick prioritization
- ✅ Visual alignment
- ✅ Team workshops

---

### 4. WSJF (Weighted Shortest Job First)

**Formula:**
```
WSJF = Cost of Delay / Job Duration
```

**Cost of Delay Components:**
```
CoD = User-Business Value + Time Criticality + Risk Reduction/Opportunity Enablement
```

**Scoring (1-10 for each):**

| Component | Description |
|-----------|-------------|
| **User-Business Value** | How valuable is this to users/business? |
| **Time Criticality** | Is there a deadline or urgency? |
| **Risk Reduction** | Does this reduce risk or enable opportunity? |

**Example:**
```
Feature: Security Audit

User-Business Value: 8
Time Criticality: 9 (compliance deadline)
Risk Reduction: 10 (security risk)
Job Duration: 5 (weeks)

CoD = 8 + 9 + 10 = 27
WSJF = 27 / 5 = 5.4
```

**When to Use:**
- ✅ SAFe environments
- ✅ Complex prioritization
- ✅ Risk-sensitive projects

---

### 5. Kano Model

**Categories:**

| Category | Description | Impact on Satisfaction |
|----------|-------------|------------------------|
| **Basic** | Expected features | Absence causes dissatisfaction |
| **Performance** | More is better | Linear satisfaction |
| **Excitement** | Delighters | Presence causes delight |

**Examples:**

| Feature | Category | Priority |
|---------|----------|----------|
| Login functionality | Basic | Must Have |
| Fast load times | Performance | Should Have |
| Personalized recommendations | Excitement | Could Have |

**When to Use:**
- ✅ Feature categorization
- ✅ Customer satisfaction focus
- ✅ MVP definition

---

## Prioritization Workshop Template

```markdown
# Prioritization Workshop: {Initiative}

## Participants
- {Product Manager}
- {Engineering Lead}
- {Design Lead}
- {Key Stakeholders}

## Pre-Work
- [ ] Backlog items documented
- [ ] Estimates available
- [ ] Data gathered (reach, impact)

## Agenda (90 min)

### 1. Context (10 min)
- Review goals and constraints
- Confirm prioritization criteria

### 2. Review Items (20 min)
- Walk through all backlog items
- Clarify questions

### 3. Score Items (30 min)
- Apply chosen framework (RICE, WSJF, etc.)
- Discuss and align on scores

### 4. Prioritize (20 min)
- Rank by score
- Discuss trade-offs
- Confirm top priorities

### 5. Next Steps (10 min)
- Confirm sprint/quarter plan
- Document decisions
- Schedule follow-up

## Output
- Prioritized backlog
- Rationale for top items
- Items deferred (and why)
```

---

## Prioritization Documentation Template

```markdown
# Prioritized Backlog: {Product/Quarter}

## Top Priorities (This {Sprint/Quarter})

| Rank | Item | Score | Rationale |
|------|------|-------|-----------|
| 1 | {Item 1} | {score} | {why} |
| 2 | {Item 2} | {score} | {why} |
| 3 | {Item 3} | {score} | {why} |

## Next Up (After Top Priorities)

| Rank | Item | Score | Notes |
|------|------|-------|-------|
| 4 | {Item 4} | {score} | {notes} |
| 5 | {Item 5} | {score} | {notes} |

## Deferred (Not Now)

| Item | Score | Reason for Deferral |
|------|-------|---------------------|
| {Item A} | {score} | {reason} |
| {Item B} | {score} | {reason} |

## Framework Used
**Method:** {RICE/MoSCoW/Value-Effort/WSJF/Kano}
**Date:** {date}
**Participants:** {list}
```

---

## Related Skills

- **mvp-definition-framework** - MVP prioritization
- **sprint-planning-framework** - Sprint-level prioritization
- **story-slicing** - Breaking down large items

---

## Output Format

When using this skill, provide:
1. **Prioritization framework** used and why
2. **Scored backlog items** with rationale
3. **Top priorities** (this sprint/quarter)
4. **Deferred items** with explanation
5. **Trade-offs** documented
6. **Next steps** for execution
