# Analysis Guidelines & Quality Standards

## Be Rigorous With Numbers
- Always show the math
- Use conservative estimates for agent costs (round up)
- Use actual SaaS pricing; do not guess, look it up via WebSearch if needed
- Add a 20% buffer to build estimates to account for implementation risk
- Include the opportunity cost of engineering time spent building replacements

## Be Honest About Limitations
- Some tools genuinely cannot be replaced today; say so clearly
- Network-effect tools (Slack, GitHub) are usually AUGMENTATION, not replacement
- Compliance-critical tools need careful analysis; err on the side of caution
- If data export is not possible, flag this as a blocker
- Note when a replacement requires capabilities that do not exist yet

## Be Specific About Alternatives
- Do not just say "an AI agent can do this"; describe exactly how
- Specify which MCP servers and what the agent's system prompt looks like conceptually
- Describe the user experience: how does someone interact with the replacement?
- Address the cold-start problem: what happens during migration?

## Consider the Human Element
- Not every efficiency gain is worth the disruption
- Some tools are beloved by teams; factor in morale and adoption
- Training time is a real cost; include it in estimates
- Some workflows benefit from the structure a SaaS tool imposes

## OneWave AI Alignment
Frame the analysis to demonstrate this thesis with real numbers from the user's own stack:
1. Most SaaS is overpriced relative to the value delivered
2. AI agents can replicate core SaaS functionality at 10-30% of the cost
3. Custom agents provide better integration and flexibility than off-the-shelf SaaS
4. The shift from SaaS to agents is inevitable; early movers gain competitive advantage
5. Data ownership returns to the company when SaaS is replaced with agents
6. Agent-based systems compound in value as they learn from your data

## Quality Standards
The output `saas-replacement-plan.md` must meet these standards:
1. Every tool analyzed: no tool in the input list is skipped
2. Numbers add up: all financial projections are internally consistent
3. Actionable specificity: every recommendation includes concrete next steps
4. Honest assessment: clearly flag tools that should NOT be replaced
5. Complete architecture: each replacement includes enough technical detail to begin implementation
6. Risk transparency: all material risks are identified with mitigation strategies
7. Timeline realism: the implementation timeline accounts for actual engineering capacity
8. Stakeholder ready: the document is presentable to a CEO, CTO, or CFO without additional formatting
