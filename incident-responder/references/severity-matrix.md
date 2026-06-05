# Severity Classification Matrix

Classify every incident using this matrix. Apply the highest severity that matches ANY criterion in a given level.

## SEV1 -- Critical

- User Impact: Complete service outage for all or most users. Core business functionality unavailable.
- Revenue Impact: Direct, measurable revenue loss in real time. Transactions failing, purchases blocked, billing broken.
- Data Impact: Data loss or corruption occurring or imminent. Data integrity compromised.
- Security Impact: Active security breach, data exfiltration, or unauthorized access in progress.
- SLA Impact: SLA breach has occurred or will occur within 1 hour.
- Response Expectations:
  - Incident commander assigned immediately
  - All-hands engineering response
  - Executive notification within 15 minutes
  - Status page updated within 10 minutes
  - Customer communication within 30 minutes
  - War room / bridge call opened immediately
  - Updates every 15 minutes until resolved

## SEV2 -- High

- User Impact: Major feature degraded or unavailable. Significant subset of users affected. Core workflows impaired but partial workarounds exist.
- Revenue Impact: Revenue impact likely but not yet confirmed, or occurring for a subset of users.
- Data Impact: Data inconsistency detected but no active data loss. Replication lag causing stale reads.
- Security Impact: Vulnerability discovered that could be actively exploited. Suspicious activity detected but not confirmed as breach.
- SLA Impact: SLA breach will occur within 4 hours without intervention.
- Response Expectations:
  - Incident commander assigned within 15 minutes
  - On-call engineers engaged immediately
  - Engineering leadership notified within 30 minutes
  - Status page updated within 20 minutes
  - Customer communication within 1 hour
  - Updates every 30 minutes until resolved

## SEV3 -- Moderate

- User Impact: Minor feature degraded. Small subset of users affected. Clear workarounds available.
- Revenue Impact: No direct revenue impact. Indirect impact possible if prolonged.
- Data Impact: No data loss. Minor data inconsistencies that are self-correcting or easily remedied.
- Security Impact: Low-severity vulnerability discovered. No evidence of exploitation.
- SLA Impact: No immediate SLA risk. Could become SLA risk if unresolved for 24+ hours.
- Response Expectations:
  - On-call engineer investigates within 1 hour
  - Team lead notified within 2 hours
  - Status page updated if customer-facing
  - Updates every 2 hours during business hours
  - Resolution target: 24 hours

## SEV4 -- Low

- User Impact: Cosmetic issues, minor bugs, non-critical feature degradation. Very small number of users affected.
- Revenue Impact: None.
- Data Impact: None.
- Security Impact: Informational security finding. No risk of exploitation.
- SLA Impact: None.
- Response Expectations:
  - Tracked in issue tracker
  - Addressed during normal sprint work
  - No status page update required
  - Resolution target: next sprint or scheduled maintenance window

## Escalation and De-escalation

- Escalate when: impact grows, workarounds fail, resolution time exceeds target, new information reveals greater scope, or the issue transitions from one domain to another (e.g., a performance issue reveals data corruption).
- De-escalate when: impact is contained, affected user count decreases, a reliable workaround is deployed, or root cause is identified and a fix is in progress with high confidence.
- Document all severity changes in the incident timeline with justification.
