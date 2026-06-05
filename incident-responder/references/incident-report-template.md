# Incident Report Template

After the incident is resolved, generate a comprehensive `incident-report.md`. This is the primary deliverable of the incident response process. Follow the exact structure below.

```markdown
# Incident Report: [Brief Title]

**Incident ID**: [INC-YYYY-MM-DD-NNN or organization format]
**Date**: [Date of incident]
**Severity**: [SEV1/SEV2/SEV3/SEV4]
**Duration**: [Total duration from detection to resolution]
**Status**: [Resolved/Monitoring]
**Author**: [Incident responder]
**Reviewers**: [Team leads, stakeholders who should review]

---

## Executive Summary

[3-5 sentences describing the incident in plain language. Include:
what broke, who was affected, how long it lasted, and how it was fixed.
This section should be understandable by anyone in the organization.]

---

## Impact Assessment

### User Impact
- **Users affected**: [number or percentage]
- **Geographic scope**: [global, regional, specific]
- **Affected functionality**: [list of features/services impacted]
- **User-visible symptoms**: [what users experienced]

### Business Impact
- **Revenue impact**: [estimated dollar amount or "none"]
- **SLA impact**: [any SLA breaches, credits owed]
- **Support ticket volume**: [increase in support contacts]
- **Reputational impact**: [social media mentions, press coverage, customer escalations]

### Technical Impact
- **Services affected**: [list of services/components]
- **Data impact**: [any data loss, corruption, or inconsistency]
- **Dependent systems**: [upstream/downstream effects]
- **Error rates**: [peak error rate during incident]

---

## Timeline

All times in UTC.

| Time | Event |
|------|-------|
| HH:MM | [Triggering event -- what change or event started the chain] |
| HH:MM | [First symptoms -- earliest evidence in logs/metrics] |
| HH:MM | [Detection -- how and when the issue was first noticed] |
| HH:MM | [Alert/page fired (if applicable)] |
| HH:MM | [First responder engaged] |
| HH:MM | [Incident declared at SEV level] |
| HH:MM | [Key investigation milestones] |
| HH:MM | [Root cause identified] |
| HH:MM | [Remediation action taken] |
| HH:MM | [Recovery confirmed] |
| HH:MM | [Incident resolved] |

**Time to detect (TTD)**: [time from trigger to detection]
**Time to mitigate (TTM)**: [time from detection to mitigation]
**Time to resolve (TTR)**: [time from detection to full resolution]

---

## Root Cause Analysis

### Summary
[2-3 sentences describing the root cause]

### Detailed Analysis

#### Triggering Event
[What specific change, event, or condition triggered the incident]

#### Failure Chain
[Step-by-step causal chain from trigger to user impact, with evidence]

1. **[Event]**: [Description with evidence]
   - Evidence: [log entry, metric, code reference]
2. **[Cascading effect]**: [Description with evidence]
   - Evidence: [log entry, metric, code reference]
3. **[User impact]**: [Description]
   - Evidence: [error rates, user reports, monitoring data]

#### Contributing Factors
[Conditions that did not directly cause the incident but made it
possible or worsened the impact]

- [Factor 1]: [Description -- e.g., "Missing integration test for
  the affected code path"]
- [Factor 2]: [Description -- e.g., "Alert threshold was set too
  high, delaying detection by 12 minutes"]
- [Factor 3]: [Description -- e.g., "Runbook for this service was
  outdated and did not cover this failure mode"]

---

## Detection

### How was the incident detected?
- [ ] Automated monitoring/alerting
- [ ] Manual observation by engineering
- [ ] Customer report
- [ ] Third-party notification
- [ ] Scheduled health check

### Detection Details
[Description of how the incident was first noticed, including which
alerts fired or who reported the issue]

### Detection Gap Analysis
[Assessment of whether detection could have been faster. Were the
right monitors in place? Were alert thresholds appropriate? Was there
a gap in observability?]

---

## Response

### Actions Taken
[Chronological list of investigation and remediation steps]

1. [Action]: [Who did it] at [time]
   - Result: [What happened]
2. [Action]: [Who did it] at [time]
   - Result: [What happened]

### What Went Well
- [Positive aspect of the response -- e.g., "Alert fired within 2
  minutes of first error"]
- [Positive aspect -- e.g., "Rollback procedure worked flawlessly"]
- [Positive aspect -- e.g., "Cross-team coordination was fast and
  effective"]

### What Could Be Improved
- [Improvement area -- e.g., "Took 20 minutes to identify which
  service was affected due to unclear error messages"]
- [Improvement area -- e.g., "No runbook existed for this failure
  mode"]
- [Improvement area -- e.g., "Status page was not updated for 25
  minutes after detection"]

---

## Remediation

### Immediate Fix
[Description of the fix that resolved the incident]

- **Action taken**: [specific change, rollback, configuration update]
- **Deployed at**: [timestamp]
- **Verified at**: [timestamp]
- **Verification method**: [how it was confirmed the fix worked]

### Permanent Fix (if different from immediate)
[Description of the long-term fix if the immediate fix was a
temporary measure]

- **Planned action**: [description]
- **Owner**: [team/individual]
- **Target date**: [date]
- **Tracking**: [link to issue/ticket]

---

## Prevention Measures

### Action Items

Each action item must have an owner, priority, and target date.
Priority levels: P0 (this week), P1 (this sprint), P2 (this quarter),
P3 (backlog).

| Priority | Action Item | Owner | Target Date | Ticket |
|----------|------------|-------|-------------|--------|
| P0 | [Immediate fix to prevent recurrence] | [team] | [date] | [link] |
| P1 | [Process improvement] | [team] | [date] | [link] |
| P1 | [Monitoring improvement] | [team] | [date] | [link] |
| P2 | [Architectural improvement] | [team] | [date] | [link] |
| P2 | [Testing improvement] | [team] | [date] | [link] |
| P3 | [Long-term hardening] | [team] | [date] | [link] |

### Categories of Prevention

#### Code and Testing
- [Specific test that should be added]
- [Code review process improvement]
- [Static analysis or linting rule to add]

#### Monitoring and Alerting
- [New alert to add or existing alert to tune]
- [Dashboard to create or update]
- [Log aggregation improvement]
- [SLO/SLI to define or adjust]

#### Process and Documentation
- [Runbook to create or update]
- [Deployment process change]
- [Review or approval process change]
- [Training or knowledge sharing needed]

#### Architecture and Infrastructure
- [Redundancy improvement]
- [Circuit breaker or fallback to implement]
- [Capacity planning change]
- [Dependency isolation improvement]

---

## Appendix

### Related Incidents
[Links to similar past incidents, if any]

### Supporting Data
[Links to dashboards, log queries, graphs, or other artifacts that
support the analysis]

### Glossary
[Define any terms that may not be universally understood by all
report readers]
```
