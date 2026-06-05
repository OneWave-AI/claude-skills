# Operational Checklists

## Incident Declaration Checklist

- [ ] Assign severity level using the classification matrix
- [ ] Create incident channel or thread (Slack, Teams, etc.)
- [ ] Assign incident commander (SEV1/SEV2)
- [ ] Notify on-call engineers
- [ ] Start the incident timeline
- [ ] Post initial status page update (if customer-facing)
- [ ] Notify engineering leadership (SEV1/SEV2)
- [ ] Notify executive leadership (SEV1)
- [ ] Begin investigation

## Verification Checklist (post-remediation)

- [ ] Error rates have returned to baseline
- [ ] Response times have returned to baseline
- [ ] Affected functionality has been manually tested
- [ ] Health checks are passing
- [ ] No new error patterns have emerged
- [ ] Monitoring dashboards confirm recovery
- [ ] Affected users can confirm resolution (if applicable)

## Incident Resolution Checklist

Before declaring an incident resolved:

- [ ] Error rates returned to baseline for 15+ minutes
- [ ] Response times returned to baseline
- [ ] All health checks passing
- [ ] Affected functionality manually verified
- [ ] No new error patterns detected
- [ ] Monitoring confirms sustained recovery
- [ ] Status page updated to "Resolved"
- [ ] Internal channels notified
- [ ] Customer communication sent (if applicable)
- [ ] Incident timeline finalized
- [ ] Post-mortem scheduled (within 48 hours for SEV1/SEV2, within 1 week for SEV3)

## Post-Mortem Meeting Checklist

- [ ] Incident report drafted and shared with participants before the meeting
- [ ] All key responders invited
- [ ] Timeline reviewed and corrected
- [ ] Root cause agreed upon
- [ ] Contributing factors identified
- [ ] Action items assigned with owners and deadlines
- [ ] Prevention measures prioritized
- [ ] Report finalized and published to incident archive
- [ ] Action items tracked in issue tracker
