---
name: product-market-fit-analysis
description: Framework for analyzing Product-Market Fit (PMF). Use to assess if your product satisfies market demand and to identify improvements needed to achieve PMF.
---

# Product-Market Fit Analysis Framework

A structured framework for analyzing and achieving Product-Market Fit (PMF). Use this to measure if you've built something the market wants.

---

## When to Use This Skill

Use this skill when:
- MVP has launched
- You have active users
- You need to measure PMF
- You want to identify improvement areas
- You're considering pivots or iterations

---

## PMF Measurement Methods

### 1. Sean Ellis Test (The 40% Rule)

**Question:** "How would you feel if you could no longer use [product]?"

**Response Options:**
- Very disappointed
- Somewhat disappointed
- Not disappointed

**Interpretation:**
| % Very Disappointed | Status | Action |
|---------------------|--------|--------|
| **>40%** | ✅ PMF Achieved | Scale and grow |
| **25-40%** | ⚠️ Close | Iterate on feedback |
| **<25%** | ❌ No PMF | Pivot or reposition |

**Follow-up Questions:**
1. What type of people do you think would most benefit from [product]?
2. What is the main benefit you receive from [product]?
3. How can we improve [product] for you?

---

### 2. Retention Analysis

**Cohort Retention Curves:**
```
Week 0: 100% ─────┐
Week 1:  60% ──────┤
Week 2:  45% ───────┤ → Should flatten (PMF signal)
Week 3:  38% ────────┤
Week 4:  35% ─────────┘
```

**PMF Signal:** Retention curve flattens (users stick around)

**No PMF Signal:** Retention curve approaches zero (users churn)

**Targets by Product Type:**

| Product Type | D1 Retention | D7 Retention | D30 Retention |
|--------------|--------------|--------------|---------------|
| Consumer App | 40% | 20% | 10% |
| SaaS B2B | 60% | 40% | 30% |
| Marketplace | 50% | 30% | 20% |
| E-commerce | 30% | 15% | 10% |

---

### 3. Usage Intensity

**Measure: Active Usage Frequency**

| Frequency | PMF Signal |
|-----------|------------|
| Daily | ✅ Strong PMF |
| Weekly | ✅ Good PMF |
| Monthly | ⚠️ Weak PMF |
| Quarterly | ❌ No PMF |

**Measure: Core Action Frequency**

What % of users perform core action regularly?

| % Users | PMF Signal |
|---------|------------|
| >50% | ✅ Strong PMF |
| 25-50% | ⚠️ Moderate PMF |
| <25% | ❌ Weak PMF |

---

### 4. Growth Metrics

**Organic Growth:**
| Metric | PMF Signal |
|--------|------------|
| Viral coefficient >1 | ✅ Strong PMF |
| Referral rate >20% | ✅ Good PMF |
| Word-of-mouth growth | ✅ Good signal |

**Paid Growth Efficiency:**
| Metric | PMF Signal |
|--------|------------|
| LTV:CAC >3:1 | ✅ Sustainable |
| Payback period <12 months | ✅ Good |
| Low churn (<5% monthly) | ✅ Good |

---

### 5. Customer Love

**Qualitative Signals:**
- ✅ Customers advocate unprompted
- ✅ Feature requests (they want more)
- ✅ Integration requests (want to use more)
- ✅ Pricing feedback ("too cheap" is good sign)
- ✅ Case studies and testimonials

**Negative Signals:**
- ❌ Indifference ("it's fine")
- ❌ Constant complaints about basics
- ❌ No engagement with updates
- ❌ Can't articulate value

---

## PMF Analysis Template

```markdown
# PMF Analysis: {Product Name}

## Executive Summary
**PMF Status:** {Achieved / Close / Not Achieved}
**Confidence:** {High / Medium / Low}
**Recommendation:** {Scale / Iterate / Pivot}

## Sean Ellis Test Results
**Survey Date:** {date}
**Responses:** {number}

| Response | % | Benchmark |
|----------|---|-----------|
| Very Disappointed | {X}% | Target: 40% |
| Somewhat Disappointed | {X}% | - |
| Not Disappointed | {X}% | - |

**Insight:** {Interpretation}

## Retention Analysis
**Analysis Period:** {date range}

| Cohort | D1 | D7 | D30 | D90 |
|--------|----|----|----|-----|
| {Cohort 1} | {X}% | {X}% | {X}% | {X}% |
| {Cohort 2} | {X}% | {X}% | {X}% | {X}% |

**Insight:** {Are curves flattening?}

## Usage Intensity
**DAU/MAU Ratio:** {X}%
**Core Action Completion:** {X}% of users
**Frequency:** {Daily/Weekly/Monthly}

**Insight:** {Usage pattern analysis}

## Customer Love
**NPS Score:** {X}
**Positive Feedback:** {themes}
**Negative Feedback:** {themes}
**Feature Requests:** {top requests}

**Insight:** {Qualitative summary}

## Recommendations
### If PMF Achieved:
1. Scale acquisition
2. Invest in growth
3. Expand market

### If PMF Close:
1. Double down on what works
2. Address top friction points
3. Focus on high-value segments

### If No PMF:
1. Revisit problem validation
2. Consider pivot
3. Talk to "very disappointed" users
```

---

## PMF Improvement Strategies

### If Sean Ellis <40%

**Step 1: Segment Responses**
- Who answered "very disappointed"?
- What do they have in common?
- What's their use case?

**Step 2: Deep Dive Interviews**
- Interview 5-10 "very disappointed" users
- Understand what they love
- Understand what's missing for others

**Step 3: Double Down**
- Focus on features "very disappointed" users love
- Consider narrowing target market
- Consider repositioning

---

### If Retention is Low

**Step 1: Identify Drop-off Points**
- Where do users churn?
- What's the "aha moment"?
- How long does it take to reach "aha"?

**Step 2: Improve Onboarding**
- Reduce time to value
- Guide users to "aha moment"
- Remove friction points

**Step 3: Increase Engagement**
- Email/push re-engagement
- New feature announcements
- Personalized recommendations

---

### If Usage is Low

**Step 1: Understand Use Cases**
- When do users need the product?
- Is it a "nice to have" or "need to have"?
- Can usage frequency be increased?

**Step 2: Increase Value**
- Add high-value features
- Improve core experience
- Integrate into user workflow

**Step 3: Consider Pivot**
- Is problem frequent enough?
- Should we target different segment?
- Should we solve different problem?

---

## Related Skills

- **problem-validation-framework** - Validate problem early
- **mvp-definition-framework** - Define MVP scope
- **product-metrics-framework** - Comprehensive metrics
- **go-to-market-playbook** - Scale after PMF

---

## Output Format

When using this skill, provide:
1. **PMF Status** (Achieved/Close/Not Achieved)
2. **Sean Ellis Test results** with analysis
3. **Retention analysis** with cohort data
4. **Usage intensity** metrics
5. **Customer love** qualitative insights
6. **Recommendations** with specific actions
7. **Next steps** with timeline
