# Analysis Framework

## Step 1: Current State Mapping

Break the workflow into a structured table with these columns:

| Step # | Action | Actor | System/Tool | Input | Output | Avg Duration | Wait Time | Failure Modes |
|--------|--------|-------|-------------|-------|--------|-------------|-----------|---------------|

Classify each step as one of:
- **Manual-Repetitive**: Human does the same thing every time (prime automation target)
- **Manual-Judgment**: Human makes a decision based on context (needs rules or AI)
- **Manual-Creative**: Human produces original content (may need AI assist or templates)
- **Already Automated**: Step is handled by software already
- **Handoff**: Work moves from one person/system to another (latency risk)
- **Wait State**: Nothing happens while waiting for something external

## Step 2: Pain Point Identification

Score each step on three dimensions (1-5 scale):

- **Automation Potential**: How easily can this be automated? (5 = trivial, 1 = requires human judgment)
- **Impact if Automated**: How much time/error reduction? (5 = massive, 1 = marginal)
- **Risk if Broken**: What happens if automation fails? (5 = catastrophic, 1 = easily recovered)

Prioritize with these scores. Steps with high automation potential AND high impact AND low risk are Phase 1 targets. Steps with high risk need robust error handling and human-in-the-loop fallbacks.

## Step 3: Decision Point Analysis

For every decision point, document:

```
Decision: [What question is being answered]
Current Method: [How the decision is made today]
Data Required: [What information feeds the decision]
Possible Outcomes: [List each branch]
Automation Approach: [Rule-based / ML-based / Human-in-the-loop]
Confidence Threshold: [When to auto-decide vs escalate to human]
```

## Step 4: Handoff Analysis

For every handoff between people or systems, document:

```
From: [Actor/System A]
To: [Actor/System B]
Mechanism: [Email, Slack, shared doc, API, manual entry, etc.]
Data Transferred: [What gets passed along]
Data Lost: [What context gets dropped in the handoff]
Average Latency: [How long the handoff takes]
Failure Rate: [How often the handoff breaks or stalls]
```
