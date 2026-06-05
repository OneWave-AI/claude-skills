# Pattern Recognition and Usage Logging

## Pattern Recognition

Analyze the user's history to identify patterns:

1. **Read session history** from `~/.claude/rules/session-context.md`.
2. **Read memory files** from `~/.claude/projects/` directories.
3. **Identify recurring tasks**: What does the user do repeatedly?
4. **Identify workflow gaps**: What manual steps could be automated?
5. **Detect skill underutilization**: Which skills would help but are never used?

### Pattern Report Format

```
## Usage Patterns Detected

### Recurring Tasks
- [Task description] - happens [frequency]
  Current approach: [how it is done now]
  Recommended: [skill or chain that would help]

### Workflow Gaps
- [Gap description]
  Impact: [time wasted, quality lost, etc.]
  Solution: [skill or chain recommendation]

### Underutilized Skills
- /[skill-name]: [why it would help based on observed patterns]
```

## Usage Logging

Maintain a learning log at `~/.claude/scout-pro-usage-log.json`:

```json
{
  "version": "1.0",
  "last_updated": "2026-04-10T00:00:00Z",
  "recommendations": [
    {
      "id": "rec-001",
      "timestamp": "2026-04-10T00:00:00Z",
      "context": "User wanted to create a sales campaign",
      "recommended_skills": ["/lookalike-customer-finder", "/cold-email-sequence-generator"],
      "recommended_chain": "sales-campaign-chain",
      "user_followed": null,
      "outcome": null
    }
  ],
  "skill_usage": {
    "/code-review-pro": {
      "times_used": 0,
      "times_recommended": 0,
      "success_rate": null,
      "common_contexts": []
    }
  },
  "chain_usage": {
    "sales-campaign-chain": {
      "times_used": 0,
      "times_recommended": 0,
      "avg_completion_rate": null,
      "avg_time_minutes": null
    }
  },
  "patterns": {
    "recurring_tasks": [],
    "peak_usage_times": [],
    "most_productive_chains": []
  }
}
```

### Logging Protocol

1. Before making recommendations, read the existing log (if it exists).
2. Factor past outcomes into current recommendations: boost skills with high success rates, avoid those that failed.
3. After making recommendations, append a new entry to the log.
4. When the user reports an outcome ("that worked great" or "that did not help"), update the relevant entry.

## Learning and Adaptation

Improve recommendations over time by:

1. **Tracking recommendation acceptance**: Did the user follow the recommendation?
2. **Tracking outcomes**: Did the recommended skill/chain produce a good result?
3. **Adjusting confidence**: Boost recommendations that consistently work, downgrade those that do not.
4. **Expanding the chain library**: When the user creates a successful ad-hoc chain, add it to the library.
5. **Personalizing**: Learn the user's preferences (quick results versus thorough analysis, favored tools, etc.).

## Proactive Recommendations

Based on context and patterns, offer unsolicited but valuable suggestions, for example:

- "You have done this 3 times manually. Want me to set up a chain for it?"
- "Based on your recent work on X, you might also want to run Y."
- "The last time you worked on a similar project, this chain worked well: ..."
- "I notice you always do A then B then C. Here is a single chain that combines them."
