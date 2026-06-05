# Quality Standards and Adaptation

## What Makes This a Real Consulting Deliverable

1. **Specificity over generality**: Tie every recommendation to a specific finding. "Consider implementing AI" is worthless. "Deploy an LLM-based email triage system to classify the 200+ daily support emails currently handled manually by 3 FTEs" is valuable.
2. **Quantified impact**: Give every opportunity a dollar or time-savings estimate. Even rough estimates beat none. Show the math.
3. **Realistic timelines**: Phase 1 is never "deploy a full AI platform." It is "set up the data pipeline and run a 2-week pilot with one team." Be honest about what takes time.
4. **Risk awareness**: State what could go wrong for every recommendation. Clients trust consultants who acknowledge uncertainty.
5. **Actionable next steps**: End the report with "Here is what to do Monday morning," not vague aspirations.
6. **Visual communication**: Use Mermaid diagrams liberally (architecture, Gantt, flow, sequence). Executives skim text but study diagrams.
7. **Layered detail**: Executive summary for the CEO, detailed findings for the VP, appendices for the engineers.

## Common Mistakes to Avoid

- Do NOT use generic recommendations that could apply to any company.
- Do NOT leave template placeholders in the final report (no `[X]` or `[...]`).
- Do NOT invent specific revenue numbers; use ranges and stated assumptions.
- Do NOT recommend technologies without explaining why they fit THIS client.
- Do NOT ignore constraints (budget, team size, timeline, technical debt).
- Do NOT produce a report shorter than 500 lines; this is a comprehensive assessment.
- Do NOT use emojis anywhere in the report or output.
- Do NOT include the Supabase token or any credentials in the report.

## Handling Limited Information

When the user provides only a company name with minimal context:

1. Use WebSearch to research the company thoroughly.
2. Be transparent about what is inferred vs. confirmed.
3. Mark assumptions clearly: "[ASSUMPTION: Based on public information...]".
4. Weight the strategy section more heavily, since workflow and tech detail may be limited.
5. Include an "Information Gaps" section listing what additional access would reveal.
6. Recommend a follow-up assessment with access to internal systems.

## Adapting to Different Client Types

**Startup (< 50 employees)**:
- Focus on foundational automation.
- Recommend cost-effective tools.
- Emphasize speed-to-value.
- Use shorter phases (weeks, not months).

**Growth Stage (50-500 employees)**:
- Focus on scaling what works.
- Identify manual processes that do not scale.
- Recommend integration consolidation.
- Balance build vs. buy decisions.

**Enterprise (500+ employees)**:
- Focus on cross-functional optimization.
- Address organizational complexity.
- Recommend governance frameworks.
- Use longer phases with more stakeholders.

## Agent SDK Orchestration Patterns

This skill follows the fan-out/fan-in pattern from the Anthropic Agent SDK.

Fan-out phase:
- Commander dispatches work to specialist agents.
- Each agent has its own tools, context, and objectives.
- Agents run independently and in parallel, with no inter-agent communication during execution.

Fan-in phase:
- Commander collects all results.
- Cross-references findings for consistency.
- Resolves conflicts (for example, Agent 1 says manual, Agent 2 says automated).
- Synthesizes into a unified deliverable.

Error handling: when an agent fails or returns incomplete results, the Commander notes the gap, fills it from other agents' findings where possible, marks affected sections as "Partial Assessment -- Additional Access Recommended", and does NOT block the entire report for one agent's failure.

Context window management: give each agent only what it needs (not the full conversation), keep the context brief concise, have agents return structured output that is easy to parse, and let the Commander handle narrative flow and report polish.

## Example Invocation

User input:

```
Client: Acme Corp
Context: B2B SaaS company, 120 employees, series B. They sell a project management
tool for construction companies. Main stack is React/Node/PostgreSQL on AWS. They are
growing fast but operations are breaking -- support is overwhelmed, onboarding takes
too long, and the engineering team is drowning in manual deployments.
Docs: /Users/gabe/clients/acme/
Focus: Specifically interested in AI opportunities for customer support and onboarding
```

Commander response:
1. Research Acme Corp online for additional context.
2. Build the context brief.
3. Deploy all three agents pointing at `/Users/gabe/clients/acme/`.
4. Agent 1 scans the docs directory for workflow evidence.
5. Agent 2 scans for package.json, Dockerfiles, CI/CD configs, and similar.
6. Agent 3 researches AI in construction SaaS and drafts strategy.
7. Commander synthesizes into the final report.
8. Write `client-onboarding-report.md`.
9. Present a summary to the user.
