# Content Review Mode

Use when reviewing content against an existing brand voice guide.

## Review Process

1. **Load the guide**: Read the brand-voice-guide.md file (ask for its location if not obvious)
2. **Analyze the draft**: Read the content to be reviewed
3. **Score across dimensions**: Rate the content on each tone spectrum dimension and compare to the guide's targets
4. **Flag violations**: Identify specific words, phrases, or structures that deviate from the guide
5. **Suggest fixes**: For every flagged issue, provide a rewritten alternative that matches the voice
6. **Overall assessment**: Provide a voice compliance score (0-100) with breakdown

## Review Output Format

```markdown
## Brand Voice Review

**Content**: [Title or description of reviewed content]
**Voice Compliance Score**: [X]/100

### Tone Alignment
| Dimension | Target | Actual | Delta | Status |
|-----------|--------|--------|-------|--------|
| Formality | X | Y | +/-Z | [On/Off] |
| ... | ... | ... | ... | ... |

### Flagged Issues

#### Issue 1: [Category]
- **Location**: [Quote from the content]
- **Problem**: [What is wrong and why]
- **Suggested fix**: [Rewritten version]
- **Guide reference**: [Which section of the guide this violates]

[Repeat for all issues]

### Positive Highlights
[What the content does well -- reinforce good patterns]

### Summary Recommendations
[Top 3-5 changes that would have the most impact]
```

## Review Principles

- Be specific. "This feels off-brand" is not useful. "The word 'synergy' in paragraph 3 conflicts with the taboo words list" is useful.
- Reference the exact guide section for every flagged issue.
- Reinforce good patterns, not only violations.
