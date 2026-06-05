# Runbook Output Template

Generate `runbook.md` using the structure below. Adapt content to what discovery actually found -- do not include sections that are entirely speculative with no basis in the codebase. The runbook should be 500+ lines and cover all 9 major sections.

```markdown
# [System Name] Operational Runbook

**Last Updated**: [date]
**Maintained By**: [team/owner from codebase]
**On-Call Rotation**: [link or description if found]
**Escalation Contact**: [if found in config]

---

## Table of Contents

[Auto-generated TOC with all sections]

---

## 1. System Overview

### 1.1 Purpose
[What this system does, derived from README and code analysis]

### 1.2 Architecture Diagram
[ASCII or Mermaid diagram showing components and data flow]

### 1.3 Service Inventory
| Service | Language/Runtime | Port | Purpose |
|---------|-----------------|------|---------|
[Populated from discovery]

### 1.4 Dependencies
#### Internal Dependencies
[Other internal services this system depends on]

#### External Dependencies
[Third-party services, APIs, databases]

### 1.5 Data Flow
[How data moves through the system, request lifecycle]

### 1.6 Environment Matrix
| Environment | URL/Endpoint | Cluster/Region | Notes |
|-------------|-------------|----------------|-------|
[Populated from config files]

---

## 2. Access and Authentication

### 2.1 Required Access
[Cloud provider accounts, VPN, SSH keys, kubectl contexts]

### 2.2 Service Accounts
[Service account details found in config]

### 2.3 Secrets Management
[How secrets are stored and rotated -- Vault, AWS SSM, etc.]

### 2.4 Common Access Commands
[kubectl config, AWS profile switching, VPN connection]

---

## 3. Common Operations

### 3.1 Deployment

#### Standard Deployment
```bash
# Step-by-step deployment commands derived from CI/CD config
```

**Pre-deployment Checklist:**
- [ ] [Items derived from pipeline gates and checks]

**Post-deployment Verification:**
- [ ] [Health checks, smoke tests, metric verification]

#### Canary Deployment
[If canary/progressive deployment is configured]

#### Hotfix Deployment
```bash
# Emergency deployment bypassing normal gates
```

### 3.2 Rollback

#### Automated Rollback
```bash
# Commands to trigger automated rollback
```

#### Manual Rollback
```bash
# Step-by-step manual rollback procedure
```

#### Database Rollback
```bash
# How to revert database migrations
```

**Rollback Decision Matrix:**
| Symptom | Action | Rollback? |
|---------|--------|-----------|
[Common scenarios and whether to rollback]

### 3.3 Scaling

#### Horizontal Scaling
```bash
# Commands to scale service instances
```

#### Vertical Scaling
[Procedure for increasing resource limits]

#### Auto-scaling Configuration
[Current auto-scaling rules and how to modify them]

#### Scaling Decision Guide
| Metric | Threshold | Action |
|--------|-----------|--------|
[CPU, memory, request rate thresholds]

### 3.4 Restart Procedures

#### Graceful Restart
```bash
# Commands for graceful restart with zero downtime
```

#### Hard Restart
```bash
# Commands for forced restart when graceful fails
```

#### Restart Individual Components
[Per-service restart commands]

### 3.5 Database Operations

#### Run Migrations
```bash
# Migration commands
```

#### Connection Management
```bash
# Check active connections, kill stuck queries
```

#### Emergency Read-Only Mode
```bash
# How to switch to read-only if needed
```

### 3.6 Cache Operations

#### Cache Flush
```bash
# Commands to flush cache safely
```

#### Cache Warmup
```bash
# Commands to warm cache after flush
```

### 3.7 Log Management

#### Viewing Logs
```bash
# Commands to tail/search logs per service
```

#### Log Level Changes
```bash
# How to change log levels at runtime
```

#### Log Retention
[Current retention policies and how to retrieve archived logs]

### 3.8 Configuration Changes

#### Feature Flags
[How to toggle feature flags]

#### Environment Variable Updates
[Procedure for updating env vars without full redeploy]

#### Config Reload
```bash
# Hot-reload config without restart if supported
```

---

## 4. Monitoring and Alerts

### 4.1 Dashboards
| Dashboard | URL | Purpose |
|-----------|-----|---------|
[Populated from monitoring config]

### 4.2 Key Metrics
| Metric | Normal Range | Warning | Critical |
|--------|-------------|---------|----------|
[Derived from alerting config and application metrics]

### 4.3 Health Checks
| Endpoint | Expected Response | Check Interval |
|----------|------------------|----------------|
[From health check configuration]

### 4.4 Alert Response Procedures

For each alert discovered in the codebase, provide:

#### ALERT: [Alert Name]
- **Severity**: P1/P2/P3/P4
- **Meaning**: What this alert indicates
- **Impact**: User-facing impact
- **Diagnosis**:
  1. [Step-by-step diagnosis commands]
- **Resolution**:
  1. [Step-by-step fix]
- **Escalation**: When and who to escalate to

---

## 5. Troubleshooting Guide

### 5.1 Symptom-Based Troubleshooting

For each common failure mode, provide a structured diagnosis flow:

#### Symptom: [Description]
**Possible Causes (check in order):**

1. **[Most likely cause]**
   - Diagnosis:
     ```bash
     # diagnostic command
     ```
   - Expected output: [what healthy looks like]
   - Fix:
     ```bash
     # fix command
     ```

2. **[Next likely cause]**
   - Diagnosis: ...
   - Fix: ...

3. **[Less common cause]**
   - Diagnosis: ...
   - Fix: ...

Common symptom categories to cover:
- High latency / slow responses
- 5xx errors / service unavailable
- Connection timeouts
- Memory pressure / OOM kills
- CPU saturation
- Disk space exhaustion
- Database connection pool exhaustion
- Queue backup / consumer lag
- Certificate expiration
- DNS resolution failures
- Authentication / authorization failures
- Data inconsistency
- Deployment failures
- Pod crash loops (Kubernetes)
- Network connectivity issues

### 5.2 Dependency Failure Modes
[What happens when each dependency fails and how to mitigate]

### 5.3 Known Issues and Workarounds
[Document any known issues found in code comments, TODOs, or issue trackers]

---

## 6. Escalation Procedures

### 6.1 Severity Definitions
| Severity | Definition | Response Time | Examples |
|----------|-----------|---------------|----------|
| P1 - Critical | Complete service outage | 15 min | [specific examples] |
| P2 - High | Major feature degraded | 30 min | [specific examples] |
| P3 - Medium | Minor feature impacted | 4 hours | [specific examples] |
| P4 - Low | Cosmetic / non-urgent | Next business day | [specific examples] |

### 6.2 Escalation Matrix
| Level | Who | When | Contact |
|-------|-----|------|---------|
[Derived from config or templated for completion]

### 6.3 Communication Templates

#### Internal Status Update
```
Subject: [P1/P2] [Service] - [Brief Description]
Status: Investigating / Identified / Monitoring / Resolved
Impact: [User-facing impact]
Current Actions: [What is being done]
Next Update: [Time of next update]
```

#### External Customer Communication
```
We are aware of an issue affecting [feature/service].
Our team is actively investigating.
We will provide an update by [time].
```

### 6.4 Incident Management Process
1. **Detect**: Alert fires or user report received
2. **Triage**: Assess severity using definitions above
3. **Assemble**: Page appropriate responders
4. **Diagnose**: Use troubleshooting guide section 5
5. **Mitigate**: Apply fix or rollback
6. **Resolve**: Confirm service restoration
7. **Communicate**: Send resolution notice
8. **Review**: Schedule post-incident review within 48 hours

---

## 7. Disaster Recovery

### 7.1 Backup Inventory
| Data Store | Backup Method | Frequency | Retention | Location |
|-----------|--------------|-----------|-----------|----------|
[Derived from backup configuration]

### 7.2 Recovery Point Objective (RPO)
[Maximum acceptable data loss, derived from backup frequency]

### 7.3 Recovery Time Objective (RTO)
[Maximum acceptable downtime]

### 7.4 Recovery Procedures

#### Database Recovery
```bash
# Step-by-step database restore from backup
```

#### Full Service Recovery
```bash
# Steps to rebuild the entire service from scratch
```

#### Partial Recovery
[Procedures for recovering individual components]

### 7.5 Failover Procedures
[If multi-region or HA is configured]

#### Automatic Failover
[How automatic failover works and when it triggers]

#### Manual Failover
```bash
# Commands to manually trigger failover
```

#### Failback
```bash
# Commands to return to primary after failover
```

### 7.6 DR Testing Schedule
[Recommended DR test cadence and procedure]

---

## 8. Scheduled Maintenance

### 8.1 Recurring Tasks
| Task | Schedule | Procedure | Owner |
|------|----------|-----------|-------|
[Derived from cron jobs, scheduled tasks]

### 8.2 Certificate Rotation
```bash
# Certificate renewal procedure
```

### 8.3 Secret Rotation
```bash
# Secret rotation procedure
```

### 8.4 Dependency Updates
[Procedure for updating dependencies safely]

### 8.5 Capacity Review
[Monthly/quarterly capacity planning checklist]

---

## 9. Reference

### 9.1 Glossary
[System-specific terminology]

### 9.2 Architecture Decision Records
[Key architectural decisions that affect operations]

### 9.3 Related Runbooks
[Links to dependent service runbooks]

### 9.4 External Documentation
[Links to cloud provider docs, framework docs, vendor docs]

### 9.5 Change Log
| Date | Author | Change |
|------|--------|--------|
[Runbook revision history]
```
