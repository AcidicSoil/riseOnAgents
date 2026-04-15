---
name: agile-ceremonies-guide
description: Guide for facilitating Agile/Scrum ceremonies including sprint planning, daily standup, sprint review, and retrospective. Use to run effective ceremonies.
---

# Agile Ceremonies Guide

A comprehensive guide for facilitating Agile/Scrum ceremonies. Use this to run effective, valuable ceremonies.

---

## When to Use This Skill

Use this skill when:
- Facilitating Scrum ceremonies
- Improving ceremony effectiveness
- Training team on Agile practices
- Troubleshooting ceremony issues
- Onboarding new team members

---

## Scrum Ceremonies Overview

| Ceremony | Frequency | Duration | Participants | Purpose |
|----------|-----------|----------|--------------|---------|
| **Sprint Planning** | Per sprint | 2 hrs (2-week sprint) | PO + Team + SM | Plan sprint work |
| **Daily Standup** | Daily | 15 min | Team + SM | Sync and blockers |
| **Sprint Review** | End of sprint | 1 hr | All stakeholders | Demo and feedback |
| **Sprint Retrospective** | End of sprint | 1 hr | Team + SM | Improve process |
| **Backlog Refinement** | Weekly/Mid-sprint | 1 hr | PO + Team | Prepare backlog |

---

## 1. Daily Standup

### Purpose
- Sync on progress
- Identify blockers
- Commit to daily goals

### Format (15 min)

**Each team member answers:**
1. What did I do yesterday?
2. What will I do today?
3. Any blockers?

### Best Practices

✅ **Do:**
- Stand up (keeps it short)
- Same time, same place daily
- 15 min timebox (use timer)
- Focus on commitments, not status reporting
- Take discussions offline

❌ **Don't:**
- Turn into status meeting
- Problem-solve during standup
- Allow lengthy updates
- Skip if "nothing to report"

### Remote Standup Tips
- Video on (if possible)
- Use async standup tools (Slack, Teams)
- Rotate time for global teams
- Record for absent members

---

## 2. Sprint Planning

**See `sprint-planning-framework` skill for detailed guide.**

### Quick Reference

| Part | Focus | Duration | Output |
|------|-------|----------|--------|
| **Part 1** | What to build | 60 min | Sprint goal + committed stories |
| **Part 2** | How to build | 50 min | Task breakdown + assignments |

---

## 3. Sprint Review

### Purpose
- Demo completed work
- Gather feedback
- Adapt backlog

### Agenda (1 hr)

| Section | Time | Description |
|---------|------|-------------|
| **Welcome** | 5 min | Review sprint goal, agenda |
| **Demo** | 30 min | Show completed work |
| **Feedback** | 15 min | Gather stakeholder input |
| **Backlog Update** | 10 min | Adjust backlog based on feedback |

### Best Practices

✅ **Do:**
- Demo working software (not slides)
- Invite all stakeholders
- Celebrate wins
- Capture feedback
- Show incomplete work (transparency)

❌ **Don't:**
- Skip if "nothing to show"
- Present slides instead of demo
- Make it a status meeting
- Defend work (listen to feedback)

### Documentation Template

```markdown
# Sprint Review: Sprint {N}

## Attendees
{List of participants}

## Sprint Goal
**Goal:** {sprint goal}
**Status:** ✅ Achieved / ⚠️ Partially / ❌ Not achieved

## Completed Work
| Story | Demo By | Feedback |
|-------|---------|----------|
| {Story 1} | {name} | {feedback} |
| {Story 2} | {name} | {feedback} |

## Incomplete Work
| Story | Reason | Next Steps |
|-------|--------|------------|
| {Story 1} | {reason} | {plan} |

## Backlog Updates
| Change | Description | Priority |
|--------|-------------|----------|
| New item | {description} | {priority} |
| Reprioritized | {description} | {new priority} |

## Next Sprint Preview
{Brief preview of next sprint focus}
```

---

## 4. Sprint Retrospective

### Purpose
- Reflect on sprint
- Identify improvements
- Commit to action items

### Agenda (1 hr)

| Section | Time | Description |
|---------|------|-------------|
| **Check-in** | 5 min | Set the stage |
| **Gather Data** | 15 min | What happened? |
| **Generate Insights** | 20 min | Why did it happen? |
| **Decide Actions** | 15 min | What will we do? |
| **Close** | 5 min | Wrap up |

### Retrospective Formats

#### Start-Stop-Continue

```
START: What should we start doing?
STOP: What should we stop doing?
CONTINUE: What should we continue doing?
```

#### Mad-Sad-Glad

```
MAD: What made us frustrated?
SAD: What made us disappointed?
GLAD: What made us happy?
```

#### 4 L's

```
LIKED: What did we like?
LEARNED: What did we learn?
LACKED: What was lacking?
LONGED FOR: What did we want?
```

#### Timeline

```
Create timeline of sprint:
- High points
- Low points
- Key events
- Patterns
```

### Best Practices

✅ **Do:**
- Create safe space (no blame)
- Rotate facilitators
- Focus on process, not people
- Commit to specific actions
- Follow up on previous actions

❌ **Don't:**
- Allow blame/gossip
- Let same people dominate
- Skip action items
- Make it a complaint session
- Ignore psychological safety

### Documentation Template

```markdown
# Sprint Retrospective: Sprint {N}

## Attendees
{List of participants}

## Format Used
{Start-Stop-Continue / Mad-Sad-Glad / etc.}

## What Went Well
- ✅ {Item 1}
- ✅ {Item 2}
- ✅ {Item 3}

## What Could Be Improved
- ⚠️ {Item 1}
- ⚠️ {Item 2}
- ⚠️ {Item 3}

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| {Action 1} | {name} | {date} | □ |
| {Action 2} | {name} | {date} | □ |

## Previous Sprint Actions
| Action | Status | Notes |
|--------|--------|-------|
| {Action 1} | ✅ Done | {notes} |
| {Action 2} | ⚠️ In Progress | {notes} |
| {Action 3} | ❌ Not Done | {reason} |
```

---

## 5. Backlog Refinement

### Purpose
- Prepare backlog for planning
- Clarify requirements
- Estimate items
- Ensure readiness

### Agenda (1 hr)

| Section | Time | Description |
|---------|------|-------------|
| **Review Items** | 30 min | Walk through upcoming stories |
| **Clarify** | 15 min | Answer questions, add details |
| **Estimate** | 15 min | Size the stories |
| **Prioritize** | 10 min | Confirm ordering |

### Definition of Ready

Checklist for story readiness:

- [ ] User story format (As a... I want... So that...)
- [ ] Acceptance criteria defined
- [ ] Dependencies identified
- [ ] Estimated by team
- [ ] Fits in sprint (not too large)
- [ ] Testable

---

## Common Ceremony Anti-Patterns

### Standup Issues

| Problem | Solution |
|---------|----------|
| Takes too long | Enforce 15 min, take discussions offline |
| People late | Start on time, every time |
| Status reporting | Refocus on commitments and blockers |
| Remote team disengaged | Video on, async option |

### Sprint Review Issues

| Problem | Solution |
|---------|----------|
| No stakeholders attend | Schedule at convenient time, send invites early |
| Nothing to demo | Show incomplete work, be transparent |
| Turns into status meeting | Focus on demo, not slides |

### Retrospective Issues

| Problem | Solution |
|---------|----------|
| Same complaints every sprint | Focus on actionable items |
| No follow-through | Track actions, review previous |
| Blame game | Facilitate, set ground rules |
| Low engagement | Rotate formats, rotate facilitators |

---

## Related Skills

- **sprint-planning-framework** - Detailed sprint planning
- **backlog-prioritization** - Prioritize backlog items
- **story-slicing** - Break down large stories

---

## Output Format

When using this skill, provide:
1. **Ceremony type** and agenda
2. **Facilitation guide** with timing
3. **Best practices** for the ceremony
4. **Templates** for documentation
5. **Troubleshooting** for common issues
