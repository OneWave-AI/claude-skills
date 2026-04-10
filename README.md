# Claude Skills Library

Production-ready skills for Claude Code. Built and maintained by [OneWave AI](https://www.onewave-ai.com) -- AI consulting for small and mid-size businesses.

**160+ skills** across business operations, sales, engineering, consulting, and AI agent architecture.

---

## Getting Started

```bash
# Install a single skill
claude skill install OneWave-AI/claude-skills/<skill-name>

# Or clone the full library
git clone https://github.com/OneWave-AI/claude-skills.git ~/.claude/skills
```

Each skill is a self-contained `SKILL.md` file that Claude Code loads as a system prompt. No dependencies, no build step.

---

## Categories

### AI Agent Architecture
Skills for building, orchestrating, and managing autonomous AI agents.

| Skill | Description |
|-------|-------------|
| `agent-army` | 2-layer parallel agent hierarchy for large tasks at maximum speed |
| `agent-to-agent` | A2A communication protocol -- message passing, shared context, handoffs |
| `agent-swarm-deployer` | Deploy swarms of sub-agents for massive parallel data processing |
| `agent-team-builder` | Design and deploy custom agent teams for business workflows |
| `sub-agent-orchestrator` | Parent/child agent orchestration with task delegation |
| `scout` | Recommends the best skill for any task |
| `scout-pro` | Enhanced scout with skill chains, pattern recognition, usage learning |
| `skill-navigator` | Guide to all skills with combination recommendations |
| `skill-composer-studio` | Chain multiple skills into custom workflows |

### Anthropic / Claude Products
Skills built around specific Anthropic product releases.

| Skill | Description |
|-------|-------------|
| `overnight-repo-auditor` | Uses Managed Agents (14.5hr runtime) for autonomous overnight codebase audits |
| `multi-agent-client-onboarding` | Agent SDK: 3 parallel agents for client assessment |
| `cowork-deal-room` | Cowork-style multi-step deal room document analysis |
| `gmail-to-crm-pipeline` | MCP Connectors: Gmail to CRM lead qualification pipeline |
| `full-codebase-migrator` | 1M context window: ingest entire codebases for migration planning |

### Sales and Revenue
| Skill | Description |
|-------|-------------|
| `deal-closer-playbook` | Closing strategy with buying committee mapping and objection handling |
| `renewal-predictor` | Predict renewal likelihood from health score signals |
| `expansion-revenue-finder` | Identify upsell and cross-sell opportunities in existing accounts |
| `pipeline-health-analyzer` | Identify stalled deals, predict close probability |
| `deal-review-framework` | MEDDIC/BANT deal assessment with risk scoring |
| `deal-momentum-analyzer` | Score deal velocity from engagement patterns |
| `sales-forecast-builder` | Weighted pipeline forecast with scenario modeling |
| `sales-call-prep-assistant` | Pre-call research briefs with discovery questions |
| `sales-methodology-implementer` | MEDDIC, BANT, Sandler, Challenger, SPIN implementation |
| `lead-scoring-model` | Build custom lead scoring from historical win/loss data |
| `inbound-lead-qualifier` | Score inbound leads by ICP fit, intent, and urgency |
| `cold-email-sequence-generator` | Multi-touch outbound campaigns optimized for response |
| `personalization-at-scale` | Personalized first lines for hundreds of prospects |
| `champion-identifier` | Find internal champions in target accounts |
| `intent-signal-aggregator` | Monitor buyer intent signals across the web |
| `objection-pattern-detector` | Mine lost deals for recurring objection patterns |
| `lookalike-customer-finder` | Find companies matching your best customer profile |
| `quota-setting-calculator` | Top-down vs bottom-up quota models |
| `sales-comp-plan-designer` | Variable compensation design with accelerators |
| `sales-coaching-plan-generator` | Individualized rep development plans |
| `ramping-rep-tracker` | 30/60/90/120 day ramp milestones |
| `rep-performance-scorecard` | Multi-dimensional rep evaluation |
| `territory-planning-optimizer` | Account assignment by revenue potential |

### Consulting and Professional Services
| Skill | Description |
|-------|-------------|
| `client-proposal-generator` | Full consulting proposals from a brief |
| `sow-generator` | Professional Statements of Work with legal boilerplate |
| `client-health-dashboard` | RAG status across all client accounts |
| `churn-autopsy` | Post-mortem analysis when a client churns |
| `onboarding-checklist` | Customized client onboarding plans |
| `ai-readiness-assessment` | Assess how ready a business is for AI adoption |
| `saas-replacement-planner` | Evaluate which SaaS tools can be replaced with AI agents |
| `roi-calculator` | AI implementation ROI with sensitivity analysis |
| `meeting-intelligence` | Extract decisions, action items, and sentiment from transcripts |
| `meeting-to-tasks` | Convert transcripts to action items with owner assignment |
| `weekly-business-report` | Auto-generated weekly KPI reports |

### Engineering and DevOps
| Skill | Description |
|-------|-------------|
| `code-review-pro` | Security, performance, and best practices review |
| `debug-like-expert` | Methodical investigation with hypothesis testing |
| `api-load-tester` | Progressive load testing with bottleneck analysis |
| `database-migrator` | Cross-provider database migration with validation |
| `incident-responder` | Production incident response automation |
| `runbook-generator` | Operational runbooks from codebase analysis |
| `data-pipeline-builder` | ETL/ELT pipeline design and implementation |
| `dependency-auditor` | Security vulnerabilities and outdated packages |
| `test-coverage-improver` | Find and fill test coverage gaps |
| `docker-debugger` | Container troubleshooting and optimization |
| `typescript-migrator` | JavaScript to TypeScript migration |
| `env-setup-wizard` | Environment variable management |
| `error-boundary-creator` | React error boundaries and fallback UIs |
| `git-pr-reviewer` | Pull request quality review |
| `regex-debugger` | Visual regex breakdown and debugging |
| `performance-profiler` | Application performance profiling |
| `api-endpoint-scaffolder` | REST API endpoint generation |
| `responsive-layout-builder` | CSS Grid, Flexbox, container queries |
| `react-component-generator` | React components with TypeScript and a11y |
| `design-system-generator` | Design tokens, components, documentation |
| `css-animation-creator` | Professional animations and micro-interactions |
| `database-schema-designer` | Optimized schemas with ERD diagrams |
| `screenshot-to-code` | Convert UI screenshots to working code |
| `landing-page-optimizer` | Conversion and performance optimization |

### Security and Compliance
| Skill | Description |
|-------|-------------|
| `compliance-checker` | GDPR, HIPAA, SOC2, CCPA, PCI-DSS audit |
| `security-pentest-planner` | Penetration test planning (OWASP Top 10) |
| `tech-due-diligence` | Technical due diligence for M&A/investment |
| `contract-analyzer` | Review contracts for concerning clauses |
| `contract-redliner` | Generate redline suggestions with replacement language |

### Marketing and Content
| Skill | Description |
|-------|-------------|
| `seo-optimizer` | Keyword analysis, readability, competitor comparison |
| `seo-keyword-cluster-builder` | Topic cluster architecture |
| `landing-page-copywriter` | High-converting copy using PAS, AIDA, StoryBrand |
| `brand-voice-analyzer` | Extract and codify brand voice from existing content |
| `content-repurposer` | Transform content into 8+ formats |
| `social-repurposer` | Adapt content for different platforms |
| `social-selling-content-generator` | LinkedIn thought leadership posts |
| `linkedin-post-optimizer` | Professional narrative with hooks |
| `utm-parameter-generator` | Standardized UTM tracking |
| `competitor-content-analyzer` | Track competitor content strategy |
| `competitor-price-tracker` | Monitor competitor pricing changes |
| `competitor-intel-agent` | Comprehensive competitor monitoring |
| `customer-review-aggregator` | Aggregate and analyze reviews from G2, Capterra, etc. |
| `podcast-content-suite` | Transform podcasts into content marketing |
| `webinar-content-repurposer` | Webinar to blog, social, email |
| `email-template-generator` | Professional email templates |
| `email-subject-line-optimizer` | A/B test subject lines |

### Strategy and Finance
| Skill | Description |
|-------|-------------|
| `pricing-strategy` | Pricing model design with competitive analysis |
| `market-sizing` | TAM/SAM/SOM with top-down and bottom-up estimates |
| `pitch-deck-reviewer` | Investor deck review with scoring |
| `board-deck-generator` | Board meeting presentation content |
| `investor-update-writer` | Monthly/quarterly investor updates |
| `executive-dashboard-generator` | Data to executive-ready reports |
| `financial-parser` | Extract data from invoices, receipts, statements |
| `portfolio-analyzer` | Investment portfolio risk and diversification |
| `budget-optimizer` | Spending analysis and savings strategies |
| `financial-goal-planner` | Savings targets and investment strategies |
| `tax-strategy-optimizer` | Pre-tax, Roth, charitable giving optimization |

### Operations and People
| Skill | Description |
|-------|-------------|
| `workflow-automator` | Design automated workflows from manual processes |
| `okr-generator` | OKRs following Google/Intel methodology |
| `customer-journey-mapper` | Full journey from first touch to advocacy |
| `hiring-scorecard` | Structured scorecards for any role |
| `knowledge-base-builder` | FAQ identification and tutorial creation |
| `technical-writer` | User guides, architecture docs, onboarding materials |
| `doc-coauthoring` | Structured documentation co-authoring workflow |
| `job-application-optimizer` | Tailor resumes to job postings |
| `raise-negotiation-prep` | Salary research and negotiation scripts |

---

## Skill Format

Every skill is a single `SKILL.md` file with YAML frontmatter:

```yaml
---
name: skill-name
description: What the skill does and when to use it.
tools: Read, Write, Bash, Agent
model: inherit
---

# Skill prompt content here...
```

Claude Code loads this as a system prompt when the skill is invoked. The `tools` field declares which Claude Code tools the skill needs access to.

---

## About OneWave AI

[OneWave AI](https://www.onewave-ai.com) is a boutique AI consulting firm based in Florida, specializing in Claude and the Anthropic ecosystem. We help small and mid-size businesses implement AI that ships real results -- from Claude for Enterprise deployment to custom agent architecture.

- [Claude Consulting](https://www.onewave-ai.com/claude-consulting)
- [Services](https://www.onewave-ai.com/services)
- [Blog](https://www.onewave-ai.com/blog)
- [Contact](https://www.onewave-ai.com/contact)

---

## Contributing

1. Fork the repository
2. Create a new folder with your skill name
3. Add a `SKILL.md` following the format above
4. Submit a pull request

Skills should be production-ready, well-documented, and solve a real problem. No placeholder or stub skills.

---

## License

MIT
