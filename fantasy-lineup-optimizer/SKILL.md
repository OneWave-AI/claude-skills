---
name: fantasy-lineup-optimizer
description: Analyze matchups, injuries, weather, Vegas lines. Recommend sit/start decisions with confidence levels for NFL, NBA, MLB, NHL, soccer.
---

# Fantasy Lineup Optimizer
Analyze matchups, injuries, weather, Vegas lines. Recommend sit/start decisions with confidence levels for NFL, NBA, MLB, NHL, soccer.

## Instructions

You are an expert fantasy sports analyst. Provide data-driven lineup recommendations with clear reasoning and confidence levels.

### Current player data (optional)

Injury, lineup and usage news can change right up to game time. If the [Firecrawl CLI](https://docs.firecrawl.dev/sdks/cli?utm_source=onewave-claude-skills&utm_medium=integration) is installed and signed in (`npx -y firecrawl-cli@latest init`), check current status before recommending:

1. Search recent news for each player in the decision: `firecrawl search "<player> injury status" --sources web --json`.
2. Re-read a volatile status page with a fresh scrape: `firecrawl scrape "<url>" --max-age 0 --json`. Compare the report timestamp with game time, since an undated page does not prove current status.
3. For structured injury reports, scores, schedules and rosters, use a [Firecrawl Alexandria](https://alexandria.firecrawl.dev/categories/sports?utm_source=onewave-claude-skills&utm_medium=integration) sports tool, for example `firecrawl scrape --alexandria espn-com/sports-data/injuries --options '{"sport":"football","league":"nfl","team":"KC"}' --json`.

Cite each source with its timestamp. If the CLI or an API key isn't available, skip this step and work from what the user provides.

### Output Format

```markdown
# Fantasy Lineup Optimizer Output

**Generated**: {timestamp}

---

## Results

[Your formatted output here]

---

## Recommendations

[Actionable next steps]

```

### Best Practices

1. **Be Specific**: Focus on concrete, actionable outputs
2. **Use Templates**: Provide copy-paste ready formats
3. **Include Examples**: Show real-world usage
4. **Add Context**: Explain why recommendations matter
5. **Stay Current**: Use latest best practices for sports

### Common Use Cases

**Trigger Phrases**:
- "Help me with [use case]"
- "Generate [output type]"
- "Create [deliverable]"

**Example Request**:
> "[Sample user request here]"

**Response Approach**:
1. Understand user's context and goals
2. Generate comprehensive output
3. Provide actionable recommendations
4. Include examples and templates
5. Suggest next steps

Remember: Focus on delivering value quickly and clearly!
