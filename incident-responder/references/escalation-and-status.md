# Escalation Paths and Status Page Management

## When to Escalate

When in doubt, escalate early. Over-communicating beats under-communicating during an incident.

### Escalate to Engineering Leadership When:
- The incident is SEV1 or SEV2
- Resolution time exceeds the target for the current severity level
- Root cause is unknown after 30 minutes of investigation
- Multiple teams need coordination
- A rollback is not possible and a hotfix is required
- Data loss or corruption is suspected

### Escalate to Executive Leadership When:
- The incident is SEV1
- Customer-facing SLA is breached or breach is imminent
- Revenue impact exceeds a material threshold
- Security breach is confirmed or suspected
- Media or public attention is likely
- The incident will require customer credits or contractual remedies

### Escalate to Security Team When:
- Unauthorized access is detected
- Data exfiltration is suspected
- Credentials have been compromised
- A vulnerability is being actively exploited
- Unusual traffic patterns suggest an attack
- A dependency has reported a security breach

### Escalate to Legal/Compliance When:
- Personal data (PII/PHI) has been exposed
- Regulatory notification may be required (GDPR, HIPAA, etc.)
- Contractual obligations are breached
- The incident may result in litigation
- Government or law enforcement notification is required

## Incident Commander Responsibilities

During a SEV1 or SEV2 incident, assign an incident commander (IC). The IC is responsible for:

1. Coordination: ensuring the right people are engaged on the right tasks.
2. Communication: providing regular updates to stakeholders at the cadence defined by severity level.
3. Decision-making: making time-sensitive decisions about remediation approach, rollback, or escalation.
4. Documentation: ensuring the timeline is maintained in real time.
5. Delegation: assigning specific investigation tasks to avoid duplication.
6. De-escalation: declaring the incident resolved and initiating the post-mortem process.

The IC should NOT be the person debugging the issue. The IC role is coordination and communication, not investigation.

## Status Page Update Cadence by Severity

| Severity | First Update | Subsequent Updates | Resolved Update |
|----------|-------------|-------------------|-----------------|
| SEV1 | Within 10 min | Every 15 min | Immediately |
| SEV2 | Within 20 min | Every 30 min | Within 15 min |
| SEV3 | Within 1 hour | Every 2 hours | Within 1 hour |
| SEV4 | Not required | Not required | Not required |

## Status Page Dos and Don'ts

Do:
- Use plain language that customers can understand
- Include specific symptoms customers are experiencing
- Provide realistic ETAs (pad estimates by 50%)
- Acknowledge the impact honestly
- Update even when there is no new information ("We are continuing to investigate")
- Include the incident start time in every update

Do not:
- Use internal jargon, service names, or error codes
- Blame third parties explicitly (say "an upstream provider" instead)
- Provide overly optimistic ETAs
- Share sensitive technical details (IP addresses, internal URLs, database names)
- Leave long gaps between updates during an active incident
- Use vague language ("some users may experience issues" when 100% are affected)
- Use emojis

## Component Status Mapping

| Condition | Component Status |
|-----------|-----------------|
| Fully operational, no issues | Operational |
| Performance below normal but functional | Degraded Performance |
| Intermittent errors, partial availability | Partial Outage |
| Complete unavailability | Major Outage |
| Fix deployed, verifying recovery | Under Maintenance |
