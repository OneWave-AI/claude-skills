---
name: reddit-thread-analyzer
description: Analyze Reddit threads for sentiment, consensus opinions, top arguments, and discussion patterns. Use this when users want to understand Reddit community opinions, analyze discussions, or gather insights from subreddit conversations.
---

# Reddit Thread Analyzer

Extract deep insights from Reddit discussions including sentiment, key arguments, and community consensus.

Given a Reddit thread URL or a question about Reddit opinions, analyze the discussion comprehensively to surface meaningful patterns and insights.

## Instructions

### 1. Fetch and Parse Thread Data

Use WebFetch to load the Reddit thread and extract:
- Post title, body, author, score, and timestamp
- All comments (not just top-level)
- Comment scores, awards, and timestamps
- Note verified contributors or expert flair

### 2. Analyze Overall Sentiment

Determine the dominant sentiment and emotional tone:
- **Overall sentiment**: Positive, negative, neutral, or mixed
- **Sentiment distribution**: Approximate percentages
- **Emotional tone**: Excited, frustrated, skeptical, supportive, angry, enthusiastic
- **Shift over time**: Note if sentiment changes throughout discussion

### 3. Extract Key Arguments

Identify the most impactful points:

**Top Arguments in Favor** (3-5 points):
- Quote the argument
- Note comment score
- Identify supporting evidence or reasoning

**Top Arguments Against** (3-5 points):
- Quote the argument
- Note comment score
- Identify counter-points and rebuttals

**Expert or Verified Opinions**:
- Highlight comments from verified experts
- Note OP responses and clarifications

### 4. Find Consensus Points

Determine what the community agrees on:
- Points with broad agreement (high scores, no controversy)
- Emerging patterns across multiple comments
- Common ground between opposing viewpoints

### 5. Identify Controversial Topics

Flag heavily debated points:
- Topics with mixed upvotes/downvotes
- Arguments that sparked long comment chains
- Divisive issues where community is split

### 6. Provide Structured Analysis

Format the analysis clearly:

```markdown
# Reddit Analysis: [Thread Title]

## Executive Summary
[2-3 sentence overview of the discussion and main takeaway]

## Overall Sentiment
- **Dominant Sentiment**: Positive/Negative/Neutral/Mixed (X%)
- **Emotional Tone**: [excited/frustrated/skeptical/etc.]
- **Community Alignment**: High/Medium/Low

## Top Arguments

### In Favor
1. **[Main point]** (+XXX score)
   > "[Direct quote from comment]"
   - [Brief explanation of reasoning]

2. **[Main point]** (+XXX score)
   > "[Direct quote]"

### Against
1. **[Main point]** (+XXX score)
   > "[Direct quote]"

## Community Consensus
- [Point most people agree on]
- [Another consensus point]

## Controversial Topics
- [Divisive issue] - Community split roughly 50/50
- [Another debate point]

## Notable Insights
- **Expert Opinion**: [Quote from verified expert] (+XXX)
- **Surprising Take**: [Unexpected perspective that gained traction]
- **Most Helpful**: [Most practical or actionable advice]

## Key Quotes
> "[Memorable quote]" - u/username (+XXX score)
> "[Another impactful quote]" - u/username (+XXX score)

## Discussion Quality
- Civility: High/Medium/Low
- Depth: Superficial/Moderate/Deep
- Evidence-based: Yes/No/Mixed
```

## Best Practices

- **Focus on highly upvoted comments** for consensus
- **Include exact scores** to show community agreement level
- **Quote directly** rather than paraphrasing
- **Preserve nuance** - avoid oversimplifying complex debates
- **Note OP responses** - original poster often adds important context
- **Distinguish facts from opinions** clearly
- **Highlight constructive vs. unproductive** discussions
- **Consider recency** - early comments may be less informed than later ones

## Example Analysis

**User**: "What does Reddit think about the new iPhone?"

**Analysis steps**:
1. Fetch r/apple or r/iPhone thread
2. Analyze 300+ comments
3. Determine sentiment: Mixed (55% positive, 45% negative)
4. Extract top pros: Camera improvements (+450), Performance (+380)
5. Extract top cons: High price (+420), Incremental updates (+390)
6. Note consensus: Good phone, but expensive for what you get
7. Identify controversy: Whether it's worth upgrading from iPhone 14
8. Surface expert opinions from tech reviewers
9. Deliver structured report with quotes and scores

---

**Remember**: Focus on substance over noise. Prioritize well-reasoned arguments over emotional reactions.
