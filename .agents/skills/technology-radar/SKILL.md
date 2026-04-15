---
name: technology-radar
description: Technology evaluation and selection. Use when evaluating new technologies, comparing technology options, creating technology radars, or making technology adoption decisions.
license: Apache 2.0
---

# Technology Evaluation Framework

Systematic technology evaluation, comparison, and selection framework for making informed technology adoption decisions.

## When to Use This Skill

Use this skill when:
- Evaluating new technologies for adoption
- Comparing competing technology options
- Creating technology radar/landscape
- Making technology standardization decisions
- Assessing technology maturity and risks
- Planning technology migrations
- Building proof-of-concepts (PoC)
- Vendor selection and evaluation

## Evaluation Framework

### Phase 1: Requirements Definition
**Functional Requirements:**
- What problems need solving?
- What capabilities are required?
- Integration requirements
- Performance requirements

**Non-Functional Requirements:**
- Scalability targets
- Security requirements
- Compliance needs
- Availability targets
- Performance benchmarks

**Organizational Requirements:**
- Budget constraints
- Timeline constraints
- Team skills and expertise
- Vendor preferences
- Strategic alignment

### Phase 2: Technology Discovery
**Research Sources:**
- Vendor documentation
- Independent reviews (Gartner, Forrester)
- Community feedback (GitHub, Stack Overflow)
- Case studies
- Peer recommendations
- Conference talks and articles

**Technology Landscape:**
- Market leaders
- Emerging alternatives
- Open-source options
- Proprietary solutions
- Build vs buy analysis

### Phase 3: Evaluation Criteria

#### 1. Maturity Assessment
| Factor | Questions | Weight |
|--------|-----------|--------|
| **Technology Readiness Level (TRL)** | How mature is the technology? (1-9) | 15% |
| **Market Adoption** | How widely adopted? (users, companies) | 10% |
| **Community Size** | Active contributors, forums, Q&A | 10% |
| **Release History** | Release frequency, stability | 5% |
| **Vendor Stability** | Company financials, roadmap | 10% |

#### 2. Technical Fit
| Factor | Questions | Weight |
|--------|-----------|--------|
| **Functionality** | Does it meet requirements? | 20% |
| **Performance** | Meets performance targets? | 15% |
| **Scalability** | Can it scale as needed? | 10% |
| **Integration** | Ease of integration with existing stack | 10% |
| **Security** | Security features and track record | 10% |

#### 3. Cost Analysis
| Factor | Questions | Weight |
|--------|-----------|--------|
| **Licensing** | License costs (perpetual, subscription) | 10% |
| **Implementation** | Development and deployment costs | 5% |
| **Training** | Team training requirements | 5% |
| **Maintenance** | Ongoing operational costs | 5% |
| **TCO (3-5 years)** | Total cost of ownership | 10% |

#### 4. Risk Assessment
| Factor | Questions | Weight |
|--------|-----------|--------|
| **Vendor Lock-in** | How difficult to switch? | 10% |
| **Technology Risk** | Risk of obsolescence | 10% |
| **Security Risk** | Security vulnerabilities history | 10% |
| **Support Risk** | Quality of vendor/community support | 5% |
| **Compliance Risk** | Regulatory compliance status | 5% |

### Phase 4: Scoring Model

#### Weighted Scoring Formula
```
Total Score = Σ (Criterion Score × Weight)
```

#### Example Scorecard
| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| **Maturity** | 20% | 8 × 0.20 = 1.60 | 9 × 0.20 = 1.80 | 6 × 0.20 = 1.20 |
| **Functionality** | 25% | 9 × 0.25 = 2.25 | 8 × 0.25 = 2.00 | 7 × 0.25 = 1.75 |
| **Cost** | 20% | 7 × 0.20 = 1.40 | 6 × 0.20 = 1.20 | 9 × 0.20 = 1.80 |
| **Risk** | 20% | 8 × 0.20 = 1.60 | 7 × 0.20 = 1.40 | 6 × 0.20 = 1.20 |
| **Support** | 15% | 8 × 0.15 = 1.20 | 9 × 0.15 = 1.35 | 5 × 0.15 = 0.75 |
| **Total** | 100% | **8.05** | **7.75** | **6.70** |

### Phase 5: Proof of Concept (PoC)

#### PoC Scope
**Must Validate:**
- Core functionality
- Performance benchmarks
- Integration feasibility
- Team learning curve

**Success Criteria:**
- Functional requirements met
- Performance targets achieved
- Integration completed successfully
- Team comfortable with technology

#### PoC Timeline
- Week 1-2: Setup and basic functionality
- Week 3-4: Core use cases
- Week 5-6: Performance testing
- Week 7-8: Integration and documentation

## Technology Radar Format

### Quadrant Structure
```
                    ADOPT
                      │
        ┌─────────────┼─────────────┐
        │             │             │
  HOLD  │   TRIAL     │   ADOPT     │  TRIAL
        │             │             │
        ├─────────────┼─────────────┤
        │             │             │
  HOLD  │   ASSESS    │   TRIAL     │  ADOPT
        │             │             │
        └─────────────┼─────────────┘
                      │
                    HOLD
```

### Ring Definitions
**ADOPT:**
- Proven in production
- Recommended for all teams
- Low risk, high maturity
- Full support available

**TRIAL:**
- Proven in limited production
- Recommended for specific use cases
- Medium risk, growing maturity
- Teams should experiment

**ASSESS:**
- Promising technology
- Limited production use
- Higher risk, emerging
- Worth investigating

**HOLD:**
- Not recommended
- Being deprecated
- Better alternatives exist
- Technical debt risk

### Radar Categories
- **Languages**: Programming languages
- **Frameworks**: Application frameworks
- **Platforms**: Cloud platforms, runtime environments
- **Tools**: Development and operations tools
- **Databases**: Data storage technologies
- **Infrastructure**: Infrastructure technologies
- **Processes**: Methodologies and practices
- **Standards**: Industry standards and protocols

## Comparison Matrix Template

```markdown
# Technology Comparison: {Category}

## Options Evaluated
1. **Option A**: {Brief description}
2. **Option B**: {Brief description}
3. **Option C**: {Brief description}

## Feature Comparison
| Feature | Option A | Option B | Option C |
|---------|----------|----------|----------|
| Feature 1 | ✅ | ✅ | ❌ |
| Feature 2 | Partial | ✅ | ✅ |
| Feature 3 | ✅ | ❌ | ✅ |

## Technical Comparison
| Aspect | Option A | Option B | Option C |
|--------|----------|----------|----------|
| Performance | High | Medium | High |
| Scalability | Excellent | Good | Good |
| Security | Strong | Strong | Medium |
| Ease of Use | Easy | Moderate | Complex |
| Documentation | Excellent | Good | Fair |

## Community & Support
| Aspect | Option A | Option B | Option C |
|--------|----------|----------|----------|
| GitHub Stars | 50k+ | 30k+ | 10k+ |
| Active Contributors | 500+ | 300+ | 100+ |
| Stack Overflow Qs | 10k+ | 5k+ | 1k+ |
| Vendor Support | 24/7 | Business hours | Community |
| Release Frequency | Monthly | Quarterly | Irregular |

## Cost Comparison (Annual)
| Cost Type | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Licensing | $10,000 | $5,000 | $0 (OSS) |
| Implementation | $50,000 | $30,000 | $80,000 |
| Training | $10,000 | $5,000 | $15,000 |
| Maintenance | $20,000 | $15,000 | $40,000 |
| **Total (Year 1)** | **$90,000** | **$55,000** | **$135,000** |
| **Total (Year 3)** | **$210,000** | **$145,000** | **$295,000** |

## Risk Assessment
| Risk | Option A | Option B | Option C |
|------|----------|----------|----------|
| Vendor Lock-in | Medium | High | Low |
| Obsolescence | Low | Low | Medium |
| Security | Low | Low | Medium |
| Support | Low | Low | High |

## Recommendation
**Selected**: Option {X}

**Rationale**:
- {Reason 1}
- {Reason 2}
- {Reason 3}

**Caveats**:
- {Known limitation 1}
- {Known limitation 2}
```

## Build vs Buy Framework

### When to Build
✅ **Build when:**
- Core competitive advantage
- Unique business requirements
- No suitable alternatives exist
- Have necessary expertise in-house
- Long-term strategic investment

### When to Buy
✅ **Buy when:**
- Commodity functionality
- Time-to-market critical
- Vendor has deep expertise
- Lower TCO than building
- Non-differentiating capability

### Decision Matrix
| Factor | Build Score | Buy Score |
|--------|-------------|-----------|
| Strategic importance | High | Low |
| Time to market | Low | High |
| Total cost | Variable | Usually lower |
| Maintenance burden | High | Low |
| Customization needs | High | Medium |

## Migration Assessment

### Migration Complexity
| Factor | Low | Medium | High |
|--------|-----|--------|------|
| **Data Migration** | < 10GB | 10-100GB | > 100GB |
| **Code Changes** | Minimal | Moderate | Extensive |
| **Testing Effort** | Smoke tests | Regression | Full suite |
| **Downtime** | Zero | Minutes | Hours |
| **Training** | None | Some | Extensive |

### Migration Strategy
1. **Parallel Run**: Old and new systems run simultaneously
2. **Phased Rollout**: Migrate incrementally by feature/team
3. **Big Bang**: Single cutover event
4. **Strangler Fig**: Gradually replace old system

## Output Format

When using this skill, create:

1. **Technology Evaluation Report** (`/docs/technology/{category}_Evaluation.md`)
   - Requirements definition
   - Options evaluated
   - Comparison matrix
   - Scoring results
   - Recommendation

2. **Technology Radar** (`/docs/technology/radar.md`)
   - Quadrant visualization
   - Ring assignments
   - Rationale for each technology

3. **PoC Report** (`/docs/technology/{tech}_PoC.md`)
   - PoC objectives
   - Results and findings
   - Recommendation

4. **Migration Plan** (`/docs/technology/{tech}_Migration.md`)
   - Migration strategy
   - Timeline and milestones
   - Risk mitigation

## Best Practices

1. **Define Clear Requirements**: Don't evaluate without criteria
2. **Weight Criteria Appropriately**: Reflect organizational priorities
3. **Include Diverse Perspectives**: Technical, business, operations
4. **Validate with PoC**: Don't rely solely on documentation
5. **Consider Total Cost**: Look beyond licensing
6. **Assess Vendor Health**: Check financials and roadmap
7. **Plan for Exit**: Consider switching costs
8. **Document Decisions**: Use ADR for technology choices
9. **Review Periodically**: Technology landscape changes
10. **Balance Innovation and Stability**: Don't chase every new thing

## Common Evaluation Mistakes

### Avoid These Pitfalls
- ❌ Evaluating without clear requirements
- ❌ Focusing only on features, ignoring TCO
- ❌ Ignoring team skills and learning curve
- ❌ Not involving operations/DevOps teams
- ❌ Skipping PoC validation
- ❌ Underestimating migration effort
- ❌ Vendor lock-in without exit strategy
- ❌ Following hype without business justification
- ❌ Not considering security and compliance
- ❌ Making decision in isolation

## References

- [Technology Radar - ThoughtWorks](https://www.thoughtworks.com/radar)
- [Gartner Hype Cycle](https://www.gartner.com/en/research/methodologies/gartner-hype-cycle)
- [Forrester Wave](https://www.forrester.com/research/forrester-wave/)
- [Build vs Buy Framework](https://www.productplan.com/learn/build-vs-buy-framework/)
- [Technology Selection Best Practices](https://martinfowler.com/bliki/TechnologyRadar.html)

### MCP Interactions
- **GitHub MCP**: Search repository for previous similar actions or related PRs before executing this skill.
- **Brave Search MCP**: Validate current patterns against the live internet if the context is sparse.
- **Context7 MCP**: Extract deep architectural/domain context relevant to the skill's execution.
