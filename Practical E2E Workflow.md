# Practical E2E Workflow

**Created:** 4/15/2026 11:07:44  
**Updated:** 4/15/2026 12:05:29  
**Exported:** 4/15/2026 17:45:39  
**Link:** [https://chatgpt.com/g/g-p-699e141c586c8191a60c161296bf2ae0-g-chat/c/69dfb7ce-f1d4-83ea-9872-f668387c7a02](https://chatgpt.com/g/g-p-699e141c586c8191a60c161296bf2ae0-g-chat/c/69dfb7ce-f1d4-83ea-9872-f668387c7a02)  

## Prompt:
4/15/2026, 11:07:43 AM

what's the workflow order for practical e2e everyday workflows? 

[RiseOn.Agents](https://github.com/daviholandas/RiseOn.Agents)

## Response:
4/15/2026, 11:07:44 AM

I’m checking the project docs and repo structure first, then I’ll reduce it to an opinionated daily-use order.

I have the repo’s actual agent hierarchy now. Next I’m mapping it to a sane day-to-day order instead of just repeating the taxonomy.

Thought for 1m 26s

Practical-e2e-workflow-order
----------------------------

The repo does **not** define one mandatory end-to-end sequence. It defines a **role stack** and handoffs: Product Manager for discovery/strategy, Product Owner for backlog/sprint execution, Architect for design without code generation, Software Engineer for implementation, and DevOps Engineer for delivery/operations. Subagents sit under those primaries for specialized work like requirements, acceptance criteria, tests, code review, CI/CD, and security. [GitHub+4GitHub+4GitHub+4](https://github.com/daviholandas/RiseOn.Agents)

### Default-daily-order

For a **practical everyday flow**, the conventional order is:

1.  **Product-Manager**  
    Use first when the work is still fuzzy: validate the problem, define vision, scope MVP, write requirements. The PM agent explicitly hands off to Product Owner when the work is “ready for execution.” [GitHub+1](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/product-manager/product-manager.agent.md)
2.  **Product-Owner**  
    Turn that into execution-ready backlog: prioritize stories, write acceptance criteria, plan the sprint, remove blockers. The PO agent is the execution bridge to Architect, Software Engineer, and DevOps. [GitHub+1](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/product-owner/product-owner.agent.md)
3.  **Architect**  
    Use here **only when the change is structurally meaningful**: new service boundaries, API shape, domain model, NFR tradeoffs, diagrams, ADRs. The architect agent explicitly says it provides architectural guidance and **does not generate source code**. [GitHub+1](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/architect/architect.agent.md)
4.  **Software-Engineer**  
    Main implementation pass. This is the repo’s primary coding mode for feature work, testing, refactoring, and code quality. It can hand off to specialist subagents such as `api-architect`, `frontend-developer`, `dotnet-specialist`, `test-writer`, `code-reviewer`, and `refactoring-specialist`. [GitHub+1](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/software-engineer/software-engineer.agent.md)
5.  **Test-Writer**  
    Run during or immediately after implementation, not at the end of the week. The software-engineer handoff model explicitly includes test generation for happy paths, edge cases, and failures. [GitHub](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/software-engineer/software-engineer.agent.md)
6.  **Code-Reviewer**  
    Review after code and tests exist. The generated subagent example is intentionally read-only, focused on quality, security, performance, and maintainability. [GitHub](https://github.com/daviholandas/RiseOn.Agents)
7.  **Refactoring-Specialist**  
    Only if the review turns up complexity or maintainability debt. This is a conditional cleanup pass, not a default first step. [GitHub](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/software-engineer/software-engineer.agent.md)
8.  **DevOps-Engineer**  
    Once the implementation is mergeable, wire build/test/deploy, infra, monitoring, containerization, and operational automation. The devops agent explicitly owns CI/CD, cloud/IaC, monitoring, security/compliance, and automation. [GitHub+1](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/devops-engineer/devops-engineer.agent.md)
9.  **Security-Auditor**  
    Use before rollout when the change touches auth, data, infra, secrets, public surfaces, or compliance-sensitive paths. It is a devops subagent in the repo’s hierarchy. [GitHub+1](https://github.com/daviholandas/RiseOn.Agents)
10.  **Product-Owner-closeout**  
    Final acceptance against backlog + acceptance criteria. This closes the loop operationally. The PO role owns backlog readiness, sprint planning, and acceptance-oriented delivery management. [GitHub+1](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/product-owner/product-owner.agent.md)
11.  **Product-Manager-feedback-loop**  
    After shipping, return to PM for success metrics, learnings, roadmap, and next-cycle prioritization. The PM role explicitly includes measuring success and roadmap/strategy work. [GitHub+1](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/product-manager/product-manager.agent.md)

### Opinionated-recommendation

For most teams, the best **everyday** order is:

`product-manager -> product-owner -> architect(if needed) -> software-engineer -> test-writer -> code-reviewer -> refactoring-specialist(if needed) -> devops-engineer -> security-auditor(if needed) -> product-owner`

That order fits the repo’s actual handoff model better than starting with architecture every time or pushing tests/review to the very end. The key is that **Architect is optional for small work**, while **tests and review are not**. This matches the project’s principles of simplicity, modularity, validation, and test-first development. [GitHub+3GitHub+3GitHub+3](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/product-manager/product-manager.agent.md)

### Two-practical-variants

**Small-existing-feature**  
`product-owner -> software-engineer -> test-writer -> code-reviewer -> devops-engineer -> product-owner`

Use this for routine backlog items where requirements are already clear and there is no meaningful architecture change. This is the fastest everyday path consistent with the repo’s roles. [GitHub+2GitHub+2](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/product-owner/product-owner.agent.md)

**Greenfield-or-major-change**  
`product-manager -> product-owner -> architect -> software-engineer -> test-writer -> code-reviewer -> devops-engineer -> security-auditor -> product-owner -> product-manager`

Use this when problem discovery, architecture, and delivery risk all matter. [GitHub+3GitHub+3GitHub+3](https://github.com/daviholandas/RiseOn.Agents/blob/master/agents/product-manager/product-manager.agent.md)

### Bottom-line

If you want one default to operationalize, use:

`PO -> Architect-if-needed -> SE -> Tests -> Review -> DevOps -> PO`

And only pull **PM** in when the work is not yet well-defined, or when you need roadmap/market/MVP framing first. That is the most practical day-to-day reading of the repo.

**Ambiguity:** 0.14  
The repo provides role definitions and handoffs, but this exact ordering is an opinionated synthesis rather than an explicitly documented single workflow.

Next useful step would be mapping this into a **Codex subagent invocation order** with concrete prompts.

---

**Sources:**

- [GitHub - daviholandas/RiseOn.Agents · GitHub](https://github.com/daviholandas/RiseOn.Agents)

## Prompt:
4/15/2026, 12:04:01 PM

approved , proceed

## Response:
4/15/2026, 12:04:05 PM

I’m mapping the repo roles into a concrete Codex handoff chain and checking current Codex docs so the naming and constraints are current.

Thought for 36s

Codex-workflow-order
--------------------

Use this as the **default daily chain** in Codex:

1.  **Coordinator-main-agent**
2.  **Explore-subagent**
3.  **Plan-subagent**
4.  **Implement-subagent**
5.  **Test-subagent**
6.  **Review-subagent**
7.  **Deploy/ops-subagent**
8.  **Coordinator-final-pass**

That ordering is the safest practical fit for Codex and RiseOn.Agents:

*   Codex subagents are best when you **explicitly** ask for them, and they are especially useful for **read-heavy** work like exploration, triage, tests, and summarization. Parallel write-heavy edits are riskier because they create merge/conflict overhead. [OpenAI Developers+1](https://developers.openai.com/codex/subagents?utm_source=chatgpt.com)
*   Current Codex guidance is to keep the **main agent** focused on requirements, decisions, and final judgment, while offloading noisy intermediate work to subagents. [OpenAI Developers](https://developers.openai.com/codex/concepts/subagents?utm_source=chatgpt.com)
*   RiseOn.Agents naturally maps to this as: **PO/PM intent -> Architect if needed -> SE -> Test -> Review -> DevOps**. [OpenAI Developers](https://developers.openai.com/codex/subagents?utm_source=chatgpt.com)

Recommended-role-mapping
------------------------

| Codex-role | RiseOn-agent |
| --- | --- |
| Explore | Product-Owner + lightweight Architect discovery |
| Plan | Architect |
| Implement | Software-Engineer |
| Test | Test-Writer |
| Review | Code-Reviewer |
| Deploy/ops | DevOps-Engineer |
| Security-check | Security-Auditor when needed |

Why-this-order
--------------

**Explore first** because your main failure mode in daily work is acting before the repo facts are grounded. Codex’s own guidance says subagents are a strong fit for codebase exploration and large-file review, and GPT-5.4 mini is specifically recommended for that kind of lower-reasoning, read-heavy subagent work. Use the stronger coordinator for planning, arbitration, and final judgment. [OpenAI Developers+1](https://developers.openai.com/codex/concepts/subagents?utm_source=chatgpt.com)

**Plan second** so architecture decisions are bounded by actual repo facts, not assumptions.  
**Implement third** in a single writer thread unless the work is trivially separable.  
**Test and review after implementation** because those are classic read-heavy parallel checks and fit Codex subagents well. [OpenAI Developers+1](https://developers.openai.com/codex/concepts/subagents?utm_source=chatgpt.com)

Concrete-invocation-pattern
---------------------------

Use one **main Codex thread** as coordinator, then explicitly delegate.

### Small-change

`explore -> implement -> test -> review -> final`

### Normal-feature

`explore -> plan -> implement -> test -> review -> final`

### Release-sensitive-change

`explore -> plan -> implement -> test -> review -> deploy/ops -> security-check -> final`

Concrete-master-prompt
----------------------

Use this in the main Codex thread:

```
Act as the coordinator.

Workflow:
1. Spawn an explore subagent first to gather codebase facts, current architecture, touched files, tests, and constraints.
2. Spawn a plan subagent only if the change is structurally meaningful.
3. Keep implementation in a single writer subagent unless tasks are fully isolated.
4. After implementation, spawn separate test and review subagents in parallel.
5. Spawn a deploy/ops subagent only if the change affects build, CI, infra, runtime config, or release behavior.
6. Return a final merged answer with:
   - repo facts
   - plan
   - patch summary
   - test results
   - review findings
   - follow-up risks

Rules:
- Explore before editing.
- Prefer parallelism for read-heavy work, not concurrent writes.
- Do not invent architecture; derive it from the repo.
- Escalate to architect-style planning only when necessary.
- Keep the main thread clean; subagents return summaries, not raw noise.
```

This aligns with Codex’s documented subagent model and avoids the usual context-rot problem in long coding sessions. [OpenAI Developers+2OpenAI Developers+2](https://developers.openai.com/codex/subagents?utm_source=chatgpt.com)

Concrete-subagent-prompts
-------------------------

### Explore-subagent

```
Inspect the repository and return only facts:
- relevant modules/files
- entry points
- existing patterns/conventions
- related tests
- likely blast radius
- unknowns/ambiguities
Do not edit files.
```

### Plan-subagent

```
Using the repo facts, produce the minimal implementation plan.
Include:
- touched files
- interface/data-flow changes
- test plan
- rollback/risk notes
Do not edit files.
```

### Implement-subagent

```
Implement the approved minimal change following existing repo conventions.
Avoid unrelated refactors.
Run targeted checks after edits.
Summarize exactly what changed.
```

### Test-subagent

```
Validate the change.
Run the smallest relevant test/check set first, then expand only if needed.
Return:
- commands run
- pass/fail
- failing cases
- likely root cause
Do not edit files unless explicitly asked.
```

### Review-subagent

```
Review the implementation for correctness, regressions, maintainability, and security.
Return prioritized findings only.
Do not rewrite code unless explicitly asked.
```

### Deploy-ops-subagent

```
Assess CI/CD, env/config, migrations, observability, rollout, and rollback impact.
Return only operational concerns and required changes.
Do not edit application code unless explicitly asked.
```

Opinionated-default
-------------------

For **everyday practical work**, use:

`Coordinator -> Explore -> Plan-if-needed -> Implement -> Test+Review -> Deploy-if-needed -> Final`

That is the conventional, lowest-friction shape.

**Ambiguity:** 0.08

---

**Sources:**

- [Subagents – Codex](https://developers.openai.com/codex/subagents?utm_source=chatgpt.com)



---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)