# Automation Design Framework

## Trigger Design

Every automated workflow starts with a trigger. For each workflow, identify:

- **Primary Trigger**: The event that kicks off the workflow
  - Webhook (form submission, API call, database change)
  - Schedule (cron-based: daily, hourly, weekly)
  - Condition (threshold reached, status changed)
  - Manual (human clicks a button to start)
  - Email/Message (incoming communication)

- **Secondary Triggers**: Events that resume a paused workflow
  - Timer expiry (follow-up after N days)
  - External response (customer replies, approval received)
  - Condition met (payment cleared, document signed)

## Action Design

For each automated step, specify:

```
Action ID: [Unique identifier, e.g., A-001]
Action Name: [Human-readable name]
Type: [API Call / Data Transform / Notification / File Operation / Decision Gate / Wait]
System: [Which tool/service performs this]
Input: [What data this action receives]
Logic: [What the action does, including any conditions]
Output: [What data this action produces]
Error Handling: [What happens if this action fails]
Retry Policy: [Number of retries, backoff strategy]
Timeout: [Maximum time before failure]
Fallback: [What to do if retries exhausted -- usually notify human]
```

## Branching Logic

For conditional paths, use explicit IF/THEN/ELSE structures:

```
Gate ID: G-001
Condition: [Boolean expression or rule]
IF TRUE -> [Next action ID]
IF FALSE -> [Alternative action ID]
Data Used: [Fields evaluated]
Edge Cases: [What if data is missing or ambiguous]
Default Path: [Which branch to take if condition cannot be evaluated]
```

## Parallel Execution

Identify steps that can run simultaneously to reduce total cycle time:

```
Parallel Block: P-001
Branches:
  - Branch A: [Action IDs that run in sequence]
  - Branch B: [Action IDs that run in sequence]
  - Branch C: [Action IDs that run in sequence]
Join Condition: [All complete / Any complete / N of M complete]
Timeout: [Maximum wait for slowest branch]
Partial Failure Handling: [What if one branch fails]
```

## Error Handling Strategy

Design error handling at three levels:

**Step-Level**: Each action has its own retry logic and fallback
- Retry with exponential backoff (e.g., 1s, 5s, 30s, 5m)
- On final failure, log error details and trigger fallback

**Flow-Level**: The workflow as a whole has error handling
- Dead letter queue for failed workflow runs
- Human notification channel (Slack, email, PagerDuty)
- Automatic rollback for partially-completed workflows where applicable

**System-Level**: The automation platform itself
- Health monitoring and alerting
- Rate limit handling
- API credential rotation and refresh
- Duplicate detection (idempotency keys)

## Human-in-the-Loop Design

Not everything should be fully automated. Design explicit human checkpoints for:

- Decisions that require judgment above a complexity threshold
- Actions with high financial or reputational risk
- Exceptions that fall outside predefined rules
- Quality assurance sampling (spot-check N% of automated decisions)

For each human checkpoint, specify:
- **Trigger**: When the human is pulled in
- **Notification**: How they are alerted (Slack, email, dashboard)
- **Context**: What information is presented to them
- **Actions Available**: What they can do (approve, reject, modify, escalate)
- **SLA**: How long they have to respond before the workflow escalates or times out
- **Escalation**: What happens if they do not respond in time
