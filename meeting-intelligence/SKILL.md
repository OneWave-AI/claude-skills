---
name: meeting-intelligence-system
description: Analyze meeting transcripts to extract decisions, action items, blockers, sentiment, and generate follow-up emails. Use when user provides meeting notes, transcripts, or recordings and needs structured summaries or action tracking.
---

# Meeting Intelligence System

Transform meeting transcripts into actionable insights, decisions, and follow-ups.

## When to Use This Skill

Activate when the user:
- Provides a meeting transcript or recording
- Asks to "analyze this meeting"
- Needs action items extracted from notes
- Wants to generate meeting minutes
- Asks for decisions made in a meeting
- Needs a follow-up email created
- Mentions meeting notes or transcripts

## Instructions

1. **Extract Meeting Metadata**
   - Identify meeting title/topic
   - Note participants (if mentioned)
   - Determine meeting date/time (if available)
   - Identify meeting type (standup, planning, retrospective, etc.)

2. **Identify Decisions Made**
   - Extract all explicit decisions
   - Note who made each decision (if clear)
   - Include rationale for decisions (if stated)
   - Flag tentative decisions vs. final decisions
   - Note decisions that need follow-up approval

3. **Extract Action Items**
   - List all tasks assigned or volunteered
   - Identify owner for each action item
   - Note deadlines or timeframes mentioned
   - Flag action items without clear owners
   - Prioritize action items (if priority discussed)
   - Note dependencies between action items

4. **Identify Blockers and Risks**
   - Extract mentioned blockers
   - Note risks or concerns raised
   - Identify unresolved issues
   - Flag items needing escalation
   - Note resource constraints mentioned

5. **Analyze Discussion Sentiment**
   - Gauge overall meeting tone (productive, tense, confused, aligned)
   - Identify areas of agreement and disagreement
   - Note team morale indicators
   - Flag conflict or tension points

6. **Extract Key Topics Discussed**
   - Summarize main discussion points
   - Note questions raised
   - Identify topics needing follow-up
   - Highlight important context or background

7. **Generate Follow-Up Communications**
   - Create meeting minutes/summary
   - Draft action item tracking email
   - Suggest calendar invites for follow-ups
   - Recommend next steps

## Output Format

```markdown
# Meeting Summary: [Title]
**Date**: [Date] | **Participants**: [Names]

## Executive Summary
[2-3 sentence overview of meeting purpose and outcome]

## Decisions Made
1. **[Decision]**
   - Owner: [Name]
   - Rationale: [Why]
   - Status: Final / Needs approval

## Action Items
| Priority | Action | Owner | Deadline | Status |
|----------|--------|-------|----------|--------|
| High | [Task] | [Name] | [Date] | Not started |
| Medium | [Task] | [Name] | [Date] | Not started |

## Blockers & Risks
1. **[Blocker]** - [Impact] - Needs: [Action]
2. **[Risk]** - [Mitigation plan]

## Key Discussion Points
- [Topic 1]: [Summary]
- [Topic 2]: [Summary]

## Open Questions
1. [Question] - Owner: [Who will answer]

## Sentiment Analysis
- **Overall Tone**: [productive/tense/etc.]
- **Team Alignment**: [high/medium/low]
- **Concerns Raised**: [Summary]

## Follow-Up Email Draft

Subject: Action Items from [Meeting Title] - [Date]

Hi team,

Thanks for joining today's [meeting type]. Here are our key outcomes:

**Decisions:**
- [Decision 1]

**Your Action Items:**
[Name]: [Task] by [Date]

**Blockers:**
- [Blocker] - please [action]

Next meeting: [Date/Time]

Best,
[Your name]
```

## Examples

**User**: "Analyze this standup transcript"
**Response**: Extract blockers mentioned → List action items per person → Flag impediments → Note team velocity concerns → Generate summary with focus on blockers

**User**: "Create action items from this product planning meeting"
**Response**: Identify all decisions (feature prioritization) → Extract action items (design mockups, tech spec) → Assign owners → Set deadlines → Create tracking table → Draft follow-up email

## Best Practices

- Be specific with action items (not vague "look into X")
- Always try to identify owners (flag if unclear)
- Differentiate between decisions and proposals
- Preserve important context for decisions
- Flag action items without deadlines
- Note commitments made by each participant
- Include relevant quotes for controversial decisions
- Use clear, scannable formatting
- Prioritize action items by urgency
- Flag dependencies between tasks
- Generate professional, actionable follow-up emails
