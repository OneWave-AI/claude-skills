# Incident Communication Templates

Generate all communications appropriate for the incident severity. Never use emojis in any communication.

## Status Page Update -- Initial

```
Title: [Service/Feature] -- [Impact Description]
Status: Investigating

We are currently investigating reports of [brief impact description].
Users may experience [specific symptoms].

Our engineering team has been engaged and is actively investigating.
We will provide an update within [timeframe based on severity].

Started: [timestamp in UTC]
```

## Status Page Update -- Identified

```
Title: [Service/Feature] -- [Impact Description]
Status: Identified

We have identified the cause of [brief impact description].
The issue is related to [high-level cause without sensitive details].

We are implementing a fix and expect to have an update within [timeframe].

Affected services: [list]
Started: [timestamp]
Last updated: [timestamp]
```

## Status Page Update -- Monitoring

```
Title: [Service/Feature] -- [Impact Description]
Status: Monitoring

A fix has been implemented for [brief impact description].
We are monitoring the situation to ensure full recovery.

Some users may still experience [any residual effects] for [duration].
We will provide a final update once we have confirmed full resolution.

Started: [timestamp]
Last updated: [timestamp]
```

## Status Page Update -- Resolved

```
Title: [Service/Feature] -- [Impact Description]
Status: Resolved

The issue affecting [service/feature] has been fully resolved.
All systems are operating normally.

Duration: [start time] to [end time] ([total duration])
Impact: [brief summary of what users experienced]

We will be conducting a thorough post-mortem review to prevent recurrence.
A summary will be shared within [timeframe, typically 3-5 business days].

Started: [timestamp]
Resolved: [timestamp]
```

## Internal Engineering Update

```
Subject: [SEV level] -- [Service] -- [Brief Description] -- [Status]

Current Status: [Investigating/Identified/Mitigating/Monitoring/Resolved]
Severity: [SEV1/SEV2/SEV3/SEV4]
Incident Commander: [name/role]
Start Time: [timestamp UTC]
Duration: [elapsed time]

Impact:
- [Specific metrics: error rate, affected users count, failed transactions]
- [Affected services and endpoints]

Root Cause (if identified):
- [Technical description of the cause]
- [Link to the triggering change if applicable]

Current Actions:
- [What is being done right now]
- [Who is doing it]
- [Expected completion time]

Next Update: [timestamp]
```

## Executive Summary

```
Subject: Incident Update -- [Service] -- [Business Impact]

Summary:
[2-3 sentences describing what happened in business terms]

Business Impact:
- Users affected: [number or percentage]
- Duration: [time]
- Revenue impact: [estimated, if applicable]
- SLA impact: [any SLA breaches]

Current Status: [Plain language status]
Expected Resolution: [timeframe]

Root Cause: [1-2 sentences, non-technical]
Next Steps: [what the team is doing]
```

## Customer-Facing Email (for SEV1/SEV2)

```
Subject: Service Update -- [Brief Description of Impact]

Dear [Customer/Team],

We want to update you on a service issue that may have affected
your experience with [product/service].

What happened:
[Brief, non-technical description of the issue]

Impact to you:
[Specific description of what the customer experienced]

What we did:
[Brief description of the resolution]

Current status:
[Confirmation that service is restored, or expected resolution time]

Preventing recurrence:
[Brief description of steps being taken to prevent this from happening again]

We understand the importance of [product/service] to your operations
and sincerely apologize for the disruption. If you have any questions
or are still experiencing issues, please contact [support channel].

[Appropriate sign-off]
```
