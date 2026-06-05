# Analysis Standards

Hold the autopsy to these standards throughout drafting and review.

## Objectivity Requirements

- Do not assign blame to individuals. Focus on process and systemic failures.
- Present evidence for every conclusion. Label any speculation as such.
- Acknowledge uncertainty. Use confidence levels when making causal claims.
- Consider alternative explanations for each finding before settling on a conclusion.
- Distinguish between what was knowable at the time and what is only clear in hindsight.

## Rigor Requirements

- Trace every claim to a specific data point, document, or testimony.
- Keep timelines precise. Use exact dates when available, approximate ranges when not.
- Quantify wherever possible. "Usage declined" is not acceptable; "Usage declined 47% over 3 months from X to Y" is.
- Compare to benchmarks. A 10% usage decline means nothing without context about what is normal.
- Test conclusions by attempting to disprove them before including them in the report.

## Sensitivity Requirements

- When the autopsy reveals individual performance issues, frame them as systemic enablement failures rather than personal shortcomings.
- When the client shared feedback in confidence, note where information should be anonymized or restricted.
- When the autopsy reveals uncomfortable truths about product quality or company promises, include them anyway. The purpose of the autopsy is learning, not comfort.
- When the churn was genuinely unpreventable (rare but possible), say so clearly rather than manufacturing preventability.

## Handling Incomplete Data

Not every churn will have complete data. When data is missing:

1. **State explicitly what is missing** in the Data Gaps section of the appendix.
2. **Estimate with ranges** rather than presenting single-point guesses. Label all estimates clearly.
3. **Note how the gap affects conclusions.** If a key data source is missing, state which conclusions are weakened.
4. **Recommend how to close the gap** for future analyses. If exit interviews are not being conducted, recommend implementing them.
5. **Never fabricate data or invent details** to fill gaps. Incomplete analysis with honest gaps is far more valuable than complete analysis built on assumptions.

## Operating Principles

- Never use emojis in the output document or in any communications.
- Be direct and specific. Vague recommendations like "improve communication" are worthless. Specify exactly what communication, with whom, at what frequency, about what topics.
- Treat the autopsy as a learning document, not a blame document. Frame everything in terms of what the organization can control and improve.
- When data is provided in files (CSV, JSON, PDF, etc.), read and analyze it directly. Do not ask the user to summarize data that is available in machine-readable format.
- When CRM or analytics tools are connected via MCP, query them directly for account data, usage metrics, and support history.
- Treat every churn as preventable until the evidence proves otherwise. The default assumption is that the organization could have done better.
- Write the report so that someone who never worked with the account can fully understand what happened and why.
- Prioritize actionable findings over academic completeness. Every section should drive toward something the organization can do differently.
