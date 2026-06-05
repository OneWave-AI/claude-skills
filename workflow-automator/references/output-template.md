# Output Document Template

Generate a file called `workflow-automation.md` in the current working directory with the structure below. The document must be comprehensive and actionable -- self-contained enough that someone could implement the automation from it alone. Target 500+ lines of substantive content. Never produce a summary or abbreviated version.

```markdown
# Workflow Automation: [Workflow Name]

Generated: [Date]
Analyst: Workflow Automator (Claude)

---

## Executive Summary

[2-3 paragraph overview: what the workflow does today, what problems exist,
what the automated version will achieve, and projected time savings.
Include a single key metric: "This automation will save approximately
X hours per week / reduce processing time from Y to Z / eliminate N%
of manual errors."]

---

## 1. Current State Analysis

### 1.1 Workflow Overview

[Narrative description of the workflow as it exists today. Write it as a
story: "When X happens, Person A does Y, then sends it to Person B,
who checks Z..."]

### 1.2 Current State Diagram

```mermaid
flowchart TD
    [Complete Mermaid diagram of the current manual workflow.
     Include all steps, decision points, handoffs, and wait states.
     Use different node shapes:
     - Rectangles for actions
     - Diamonds for decisions
     - Parallelograms for inputs/outputs
     - Circles for start/end
     Use color coding:
     - style nodeX fill:#ff9999 for bottlenecks
     - style nodeX fill:#99ff99 for already-efficient steps
     - style nodeX fill:#ffff99 for handoff points]
```

### 1.3 Step-by-Step Breakdown

[Detailed table of every step with all columns from the analysis framework]

### 1.4 Actors and Systems

[Table listing every person/role and every system involved,
with their responsibilities and access levels]

### 1.5 Volume and Frequency

[How often the workflow runs, how many items it processes,
peak vs average load, growth trends]

---

## 2. Pain Point Analysis

### 2.1 Bottlenecks

[Each bottleneck identified, with data on how much time it wastes
and why it exists]

### 2.2 Error-Prone Steps

[Steps where errors occur most frequently, the types of errors,
their downstream impact, and current mitigation]

### 2.3 Redundant Steps

[Steps that duplicate work or could be eliminated entirely]

### 2.4 Handoff Delays

[Analysis of every handoff point with latency data and failure modes]

### 2.5 Automation Scoring Matrix

[Table scoring each step on Automation Potential, Impact, and Risk]

---

## 3. Automated Workflow Design

### 3.1 Design Principles

[List the principles guiding the automation design, e.g.,
"Automate the happy path, escalate exceptions",
"Fail fast and notify",
"Preserve audit trail"]

### 3.2 Automated Flow Diagram

```mermaid
flowchart TD
    [Complete Mermaid diagram of the automated workflow.
     Include triggers, automated actions, decision gates,
     parallel paths, human checkpoints, and error handlers.
     Use color coding:
     - style nodeX fill:#4CAF50,color:#fff for fully automated steps
     - style nodeX fill:#2196F3,color:#fff for API integrations
     - style nodeX fill:#FF9800,color:#fff for human-in-the-loop
     - style nodeX fill:#f44336,color:#fff for error handlers]
```

### 3.3 Trigger Configuration

[Detailed specification of what triggers the workflow,
including primary and secondary triggers]

### 3.4 Action Specifications

[Every automated action specified using the Action Design template]

### 3.5 Decision Gates

[Every conditional branch specified using the Branching Logic template]

### 3.6 Parallel Execution Blocks

[Any steps that run in parallel, specified using the Parallel Execution template]

### 3.7 Human-in-the-Loop Checkpoints

[Every point where a human is involved, with full specification]

### 3.8 Error Handling

[Complete error handling design at step, flow, and system levels]

---

## 4. Tool Recommendations

### 4.1 Recommended Platform

[Primary recommendation with detailed justification]

### 4.2 Platform Comparison for This Workflow

[Comparison table evaluating platforms against this specific workflow's needs]

### 4.3 Architecture Diagram

```mermaid
flowchart LR
    [System architecture showing how automation tools connect
     to existing systems, APIs, databases, and notification channels]
```

### 4.4 Required Integrations

[Table listing every integration needed: source system, target system,
integration method (native, API, webhook, custom), and any limitations]

### 4.5 Alternative Approaches

[Other valid ways to automate this workflow, with trade-offs]

---

## 5. Implementation Plan

### 5.1 Phases

[Break implementation into phases. Phase 1 should deliver value
within 1-2 weeks. Later phases add complexity.]

**Phase 1: Quick Wins (Week 1-2)**
- [Highest-impact, lowest-risk automations]
- [Expected time savings from Phase 1 alone]

**Phase 2: Core Automation (Week 3-4)**
- [Main workflow logic and integrations]
- [Cumulative time savings]

**Phase 3: Error Handling and Edge Cases (Week 5-6)**
- [Robust error handling, monitoring, edge case coverage]
- [Reliability improvements]

**Phase 4: Optimization and Monitoring (Week 7-8)**
- [Performance tuning, dashboards, alerting]
- [Long-term maintainability]

### 5.2 Prerequisites

[What needs to be in place before implementation:
API access, credentials, accounts, permissions, data cleanup]

### 5.3 Testing Strategy

[How to test each phase before going live:
parallel run with manual process, staged rollout,
canary testing, rollback plan]

### 5.4 Migration Plan

[How to transition from manual to automated:
parallel running period, cutover criteria, rollback triggers]

### 5.5 Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
[Risks specific to this automation project]

---

## 6. Impact Assessment

### 6.1 Time Savings

| Step | Current Time (manual) | Automated Time | Savings per Run | Monthly Savings |
|------|-----------------------|----------------|-----------------|-----------------|
[Detailed time savings for each step]

**Total Monthly Time Savings: [X hours]**
**Annual Time Savings: [X hours] ([X FTE equivalent])**

### 6.2 Error Reduction

[Quantified reduction in errors at each step]

### 6.3 Throughput Improvement

[How many more items per day/week the workflow can handle]

### 6.4 Cost Analysis

| Item | Monthly Cost |
|------|-------------|
| Automation platform subscription | $X |
| API/integration costs | $X |
| Hosting (if self-hosted) | $X |
| Maintenance time | $X |
| **Total Automation Cost** | **$X** |
| **Manual Labor Cost Saved** | **$X** |
| **Net Monthly Savings** | **$X** |
| **ROI Period** | **X months** |

### 6.5 Qualitative Benefits

[Non-quantifiable improvements: consistency, employee satisfaction,
faster customer response, better data quality, scalability]

---

## 7. Maintenance and Monitoring

### 7.1 Monitoring Dashboard

[What metrics to track: success rate, execution time,
error rate, queue depth, SLA compliance]

### 7.2 Alerting Rules

[When to alert humans: failure rate above threshold,
execution time anomaly, queue backup, credential expiry]

### 7.3 Maintenance Schedule

[Regular maintenance tasks: credential rotation,
integration health checks, rule updates, performance review]

### 7.4 Runbook

[Step-by-step procedures for common issues:
"Workflow is stuck", "Integration is failing",
"Data is malformed", "Volume spike"]

---

## Appendix

### A. Data Flow Map

[Complete data flow showing every field from source to destination]

### B. Integration Credentials Needed

[List of API keys, OAuth apps, service accounts required --
DO NOT include actual credentials, only what is needed]

### C. Glossary

[Terms specific to this workflow or business domain]
```
