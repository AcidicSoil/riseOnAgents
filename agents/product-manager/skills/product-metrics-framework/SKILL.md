---
name: product-metrics-framework
description: Framework for defining and tracking product metrics. Use to establish KPIs, North Star metrics, and measurement frameworks for product success.
---

# Product Metrics Framework

A comprehensive framework for defining and tracking product metrics. Use this to establish KPIs and measure product success.

---

## When to Use This Skill

Use this skill when:
- Defining product success metrics
- Setting up analytics
- Creating dashboards
- Reporting to stakeholders
- Making data-driven decisions

---

## Metrics Hierarchy

### Level 1: North Star Metric

**Definition:** Single metric that captures core value delivered to customers

**Examples:**
| Company | North Star Metric |
|---------|-------------------|
| Spotify | Time spent listening |
| Airbnb | Nights booked |
| Slack | Messages sent |
| Amazon | Purchases |
| Facebook | Daily Active Users |

**Characteristics:**
- ✅ Leads to revenue (eventually)
- ✅ Measures customer value
- ✅ Actionable by teams
- ✅ Easy to understand

---

### Level 2: Input Metrics (3-5)

**Definition:** Metrics that drive the North Star

**Example (for "Time spent listening"):**
- New user activations
- Playlist creations per user
- Songs discovered per session
- Return listener rate

**Characteristics:**
- ✅ Directly influence North Star
- ✅ Teams can impact directly
- ✅ Measurable frequently
- ✅ Lead indicators (not lagging)

---

### Level 3: Health Metrics

**Definition:** Metrics that ensure sustainable growth

**Categories:**

| Category | Metrics | Purpose |
|----------|---------|---------|
| **Acquisition** | Sign-ups, CAC, Traffic | Growth |
| **Activation** | Time to value, Aha moment rate | Onboarding |
| **Engagement** | DAU/MAU, Session frequency | Usage |
| **Retention** | D1/D7/D30 retention, Churn | Stickiness |
| **Revenue** | MRR, ARPU, LTV | Business |
| **Referral** | NPS, Viral coefficient | Growth |

---

## AARRR Framework (Pirate Metrics)

### 1. Acquisition
**How users find you**

| Metric | Formula | Target |
|--------|---------|--------|
| Sign-ups | Count | {X}/month |
| CAC | Marketing spend / New customers | < ${X} |
| Organic % | Organic / Total sign-ups | > {X}% |

### 2. Activation
**First valuable experience**

| Metric | Formula | Target |
|--------|---------|--------|
| Activation rate | Users who complete key action / Sign-ups | > {X}% |
| Time to value | Time from sign-up to "aha" | < {X} days |
| Onboarding completion | Completed onboarding / Started | > {X}% |

### 3. Retention
**Users coming back**

| Metric | Formula | Target |
|--------|---------|--------|
| D1 Retention | Users active day 1 / Day 0 cohort | > {X}% |
| D7 Retention | Users active day 7 / Day 0 cohort | > {X}% |
| Churn rate | Lost customers / Total customers | < {X}% |

### 4. Revenue
**Making money**

| Metric | Formula | Target |
|--------|---------|--------|
| MRR | Monthly recurring revenue | ${X} |
| ARPU | Revenue / Active users | ${X} |
| LTV | ARPU / Churn rate | > ${X} |
| LTV:CAC | LTV / CAC | > 3:1 |

### 5. Referral
**Users recommending you**

| Metric | Formula | Target |
|--------|---------|--------|
| NPS | % Promoters - % Detractors | > {X} |
| Viral coefficient | Invites sent × Conversion rate | > 1.0 |
| Referral rate | Users who refer / Total users | > {X}% |

---

## HEART Framework (Google)

| Category | Metrics | Example |
|----------|---------|---------|
| **Happiness** | NPS, CSAT, Ratings | "How satisfied are users?" |
| **Engagement** | DAU, Session frequency | "How often do users engage?" |
| **Adoption** | New users, Feature adoption | "Are users adopting?" |
| **Retention** | Churn, Return rate | "Do users come back?" |
| **Task Success** | Completion rate, Error rate | "Can users complete tasks?" |

---

## Metrics Documentation Template

```markdown
# Product Metrics: {Product Name}

## North Star Metric
**Metric:** {metric name}
**Definition:** {how it's calculated}
**Current:** {current value}
**Target:** {target value}
**Why this matters:** {rationale}

## Input Metrics (3-5)
| Metric | Definition | Current | Target | Owner |
|--------|------------|---------|--------|-------|
| {Metric 1} | {def} | {value} | {target} | {owner} |
| {Metric 2} | {def} | {value} | {target} | {owner} |

## Health Metrics

### Acquisition
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| Sign-ups | {X} | {X} | ↑/↓/→ |
| CAC | ${X} | ${X} | ↑/↓/→ |

### Activation
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| Activation rate | {X}% | {X}% | ↑/↓/→ |
| Time to value | {X} days | {X} days | ↑/↓/→ |

### Retention
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| D7 Retention | {X}% | {X}% | ↑/↓/→ |
| Churn rate | {X}% | {X}% | ↑/↓/→ |

### Revenue
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| MRR | ${X} | ${X} | ↑/↓/→ |
| LTV:CAC | {X}:1 | 3:1 | ↑/↓/→ |

## Measurement Plan
### Tools
- Analytics: {tool}
- Surveys: {tool}
- Dashboard: {tool}

### Review Cadence
- Daily: {metrics}
- Weekly: {metrics}
- Monthly: {metrics}

### Alerts
| Metric | Threshold | Action |
|--------|-----------|--------|
| {Metric} | {threshold} | {action} |
```

---

## Metric Selection Guidelines

### Good Metrics (SMART)
- ✅ **Specific**: Clear definition
- ✅ **Measurable**: Can be quantified
- ✅ **Actionable**: Teams can influence
- ✅ **Relevant**: Tied to business goals
- ✅ **Time-bound**: Measured frequently

### Bad Metrics (Vanity)
- ❌ Cumulative totals (always go up)
- ❌ Can't be acted upon
- ❌ Don't tie to value
- ❌ Easy to game

---

## Related Skills

- **problem-validation-framework** - Validate before measuring
- **mvp-definition-framework** - Define MVP success criteria
- **product-market-fit-analysis** - PMF measurement
- **success-metrics-frameworks** - Existing skill (HEART, AARRR)

---

## Output Format

When using this skill, provide:
1. **North Star Metric** with rationale
2. **Input metrics** (3-5) that drive North Star
3. **Health metrics** by category (AARRR or HEART)
4. **Current values** and targets
5. **Measurement plan** (tools, cadence)
6. **Alert thresholds** for anomalies
