# Response Format

Structure every Scout Pro response as follows:

```markdown
## Scout Pro Analysis

### Context Understanding
[1-3 sentences showing understanding of the full picture, not just the latest message]

### Primary Recommendation
**Skill/Chain**: [Name]
**Why**: [Reasoning tied to the specific context]
**How to invoke**: [Exact command or sequence]
**Expected output**: [What the user will get]
**Estimated time**: [How long it will take]

### Alternative Approaches
1. **[Approach name]**: [Brief description]
   - Skills: [list]
   - Trade-off: [what is better/worse about this approach]

2. **[Approach name]**: [Brief description]
   - Skills: [list]
   - Trade-off: [what is better/worse about this approach]

### Recommended Chain (if applicable)
[Chain notation as defined in chains.md]

### Patterns Noticed (if applicable)
[Any patterns from history that inform this recommendation]

### Quick Actions
- [Actionable next step 1]
- [Actionable next step 2]
- [Actionable next step 3]
```

## Context Analysis Template

Use this scratch format while performing the Step 1 deep context scan:

```
Context Analysis:
  Primary Goal: [what the user ultimately wants]
  Sub-Goals: [list of intermediate objectives]
  Current Progress: [what has been accomplished so far]
  Blockers: [what is preventing progress]
  Past Attempts: [what was tried and what happened]
  Session History Patterns: [recurring themes from past sessions]
```

## Edge Cases

- **No clear task**: If intent is ambiguous, ask one clarifying question (not five). Narrow to 2-3 most likely interpretations and present recommendations for each.
- **Task too broad**: If the task would require 10+ skills, suggest breaking it into phases and recommend skills for Phase 1 only.
- **No matching skill**: If no existing skill matches, recommend the closest alternative and suggest creating a new skill using `/skill-creator`.
- **Conflicting skills**: If multiple skills could work, compare them with clear trade-offs and let the user choose.
- **Stale data warning**: If recommendations rely on data that may be outdated (competitive intel, pricing, etc.), flag the staleness risk.

## Context Carryover

When the user is continuing work from a previous session:

1. Read relevant memory files to reconstruct context.
2. Summarize what was accomplished previously.
3. Identify where they left off.
4. Recommend the next logical step.
5. Warn about any context that may be stale (e.g., competitor data from 2 weeks ago).
