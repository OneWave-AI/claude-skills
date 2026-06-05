# Document Structure

Every SOW follows this structure. Do not omit sections. Do not abbreviate. Each section must contain substantive, engagement-specific content.

## Section 1: Cover Page

```
STATEMENT OF WORK

[SOW Reference Number: SOW-YYYY-NNN]

Between

[Provider Legal Name]
("Provider" or "Consultant")

and

[Client Legal Name]
("Client")

Effective Date: [Date]
Document Version: 1.0
Classification: Confidential
```

## Section 2: Document Control

| Field | Value |
|---|---|
| Document ID | SOW-YYYY-NNN |
| Version | 1.0 |
| Status | Draft |
| Author | [Provider contact] |
| Reviewer | [Client contact] |
| Last Updated | [Date] |

Include a version history table with columns: Version, Date, Author, Description of Changes.

## Section 3: Executive Summary

Two to four paragraphs covering:

- The business context driving this engagement
- High-level description of what will be delivered
- The value proposition and expected business outcomes
- Any research-informed context about the client's market position or strategic direction

Write for executive readers who will not read the full document. It must stand alone as a complete summary.

## Section 4: Background and Context

- Client company background (informed by research)
- Business problem or opportunity being addressed
- Current state description
- Desired future state
- How this engagement fits into the client's broader strategy
- Any predecessor work or related initiatives

## Section 5: Scope of Work

### 5.1 In-Scope

Organize by workstream or phase. Each in-scope item must include:

- Clear description of the work to be performed
- The approach or methodology to be used
- Expected outputs from that work item
- Any specific standards or frameworks to be followed

Use a numbered hierarchy (5.1.1, 5.1.2, etc.) for traceability. Every deliverable and milestone must trace back to a scope item.

### 5.2 Out of Scope

Explicitly enumerate what is NOT included. This section prevents scope creep and manages expectations. Be specific and anticipate common assumptions. Examples:

- Ongoing maintenance and support beyond the warranty period
- Data migration from legacy systems not specified in Section 5.1
- Third-party software licensing costs
- End-user training beyond the sessions specified in the deliverables
- Hardware procurement or infrastructure provisioning
- Content creation or copywriting unless explicitly stated
- Integration with systems not identified in this document

Tailor these to the specific engagement. Generic exclusions are insufficient.

### 5.3 Assumptions

Number each assumption. These are conditions that must hold true for the SOW to be executed as planned. Group them by category:

Client-Side Assumptions
- Timely access to personnel, systems, and environments
- Decision-making authority and response times
- Data quality and availability
- Infrastructure readiness

Provider-Side Assumptions
- Resource availability and skill sets
- Tool and methodology access
- Subcontractor availability if applicable

Technical Assumptions
- Platform versions and compatibility
- API availability and stability
- Performance baselines
- Environment specifications

Commercial Assumptions
- Budget sufficiency for stated scope
- Payment timing and cash flow
- Currency and tax treatment

### 5.4 Dependencies

Numbered list of external factors that could impact delivery. Each dependency must specify what it is, who owns it, when it must be resolved, and the impact if not resolved.

Format: `DEP-NNN: [Description] | Owner: [Party] | Required By: [Date/Phase] | Risk if Unmet: [Impact]`

## Section 6: Deliverables

Present as a detailed table:

| ID | Deliverable | Description | Format | Acceptance Criteria | Due Date | Phase |
|---|---|---|---|---|---|---|
| D-001 | [Name] | [Detailed description] | [File type / medium] | [Specific, measurable criteria] | [Date] | [Phase #] |

Every deliverable must have:
- A unique identifier for traceability
- A description detailed enough that both parties agree on what "done" means
- Specific format requirements (PDF report, working code in Git repository, Figma file, etc.)
- Measurable acceptance criteria -- not "client is satisfied" but specific, testable conditions
- A due date tied to the milestone schedule

## Section 7: Milestones and Timeline

### 7.1 Phase Overview

```
Phase 1: [Name] .............. [Start Date] - [End Date] ([Duration])
Phase 2: [Name] .............. [Start Date] - [End Date] ([Duration])
Phase 3: [Name] .............. [Start Date] - [End Date] ([Duration])
...
```

### 7.2 Detailed Milestone Schedule

| Milestone ID | Milestone | Phase | Target Date | Deliverables | Payment Trigger | Dependencies |
|---|---|---|---|---|---|---|
| M-001 | [Name] | [Phase] | [Date] | [D-IDs] | [Yes/No + Amount] | [DEP-IDs] |

### 7.3 Critical Path

Identify the critical path through the project. List activities where delays will directly impact the final delivery date. This informs both parties about where schedule risk is concentrated.

### 7.4 Schedule Assumptions and Risks

- Buffer time built into the schedule (if any)
- Holiday and blackout periods
- Parallel vs sequential phase dependencies
- Client review and approval cycle durations assumed

## Section 8: Acceptance Criteria and Process

### 8.1 General Acceptance Criteria

Define the overall quality standards that apply to all deliverables:

- Conformance to specifications outlined in this SOW
- Freedom from material defects
- Compliance with applicable industry standards
- Completeness as defined by deliverable descriptions

### 8.2 Acceptance Process

1. Submission: Provider delivers the deliverable to the designated Client contact with a Delivery Notice
2. Review Period: Client has [N] business days to review from date of Delivery Notice
3. Acceptance or Rejection: Client provides written acceptance or a detailed Rejection Notice specifying deficiencies
4. Remediation: If rejected, Provider has [N] business days to cure identified deficiencies
5. Re-submission: Corrected deliverable is re-submitted and a new review period begins
6. Deemed Acceptance: If Client does not respond within the review period, the deliverable is deemed accepted
7. Escalation: If parties cannot agree on acceptance after [N] remediation cycles, the matter is escalated per Section 14

### 8.3 Acceptance Criteria by Deliverable

For each major deliverable, specify the precise acceptance criteria. These must be:
- Specific: No ambiguity about what is being measured
- Measurable: Can be verified through testing, review, or demonstration
- Achievable: Within the scope and capabilities defined
- Relevant: Directly tied to the deliverable's purpose
- Time-bound: Testable within the review period

## Section 9: Project Governance

### 9.1 Project Organization

Steering Committee (if applicable): composition, meeting cadence, decision authority.

Project Managers:
- Provider PM: [Name, contact]
- Client PM: [Name, contact]
- Responsibilities and authority levels

### 9.2 Communication Plan

| Communication | Frequency | Format | Participants | Owner |
|---|---|---|---|---|
| Status Report | Weekly | Written (email) | PMs, Stakeholders | Provider PM |
| Status Meeting | Weekly | Video call, 30 min | PMs, Leads | Provider PM |
| Steering Committee | Bi-weekly/Monthly | In-person or video | Executives, PMs | Client PM |
| Ad-hoc Escalation | As needed | Email + call | As required | Either PM |

### 9.3 Reporting

Specify what the weekly/monthly status report contains:
- Work completed in the period
- Work planned for next period
- Risks and issues log (updated)
- Budget consumption (for T&M engagements)
- Milestone status (on track / at risk / delayed)
- Change request status
- Decisions needed

### 9.4 Tools and Collaboration

- Project tracking (Jira, Asana, Monday, etc.)
- Communication (Slack, Teams, email)
- Document management (SharePoint, Google Drive, Confluence)
- Code repository (GitHub, GitLab, Bitbucket) if applicable
- Design tools (Figma, Miro) if applicable

## Section 10: Team and Resource Allocation

### 10.1 Provider Team

| Role | Name | Allocation | Responsibilities | Duration |
|---|---|---|---|---|
| Engagement Lead | [Name] | [%] | Overall delivery accountability | Full engagement |
| Project Manager | [Name] | [%] | Day-to-day management, reporting | Full engagement |
| [Specialist Role] | [Name/TBD] | [%] | [Specific responsibilities] | [Phase/Duration] |

### 10.2 Client Team

| Role | Name | Allocation | Responsibilities |
|---|---|---|---|
| Executive Sponsor | [Name] | As needed | Strategic decisions, escalation |
| Project Manager | [Name] | [%] | Client-side coordination |
| Subject Matter Expert | [Name] | [%] | Domain knowledge, requirements validation |
| Technical Lead | [Name] | [%] | Technical decisions, environment access |

### 10.3 Resource Substitution

- Provider must give [N] business days written notice before substituting key personnel
- Replacement must have equivalent qualifications and experience
- Client has right to approve or reject substitutions for key roles
- Knowledge transfer period of [N] days required for transitions

## Section 11: Pricing and Payment

Varies by engagement type. See references/pricing-templates.md and generate the appropriate model.

## Section 12: Change Management

See references/change-management.md.

## Section 13: Risk Management

See references/risk-management.md.

## Section 14: Legal and Contractual Terms

See references/legal-terms.md.

## Section 15: Data Protection and Security

Include this section when the engagement involves handling personal data, client systems access, or sensitive information.

### 15.1 Data Handling

- Types of data to be accessed or processed
- Data classification levels
- Storage and transmission requirements (encryption at rest and in transit)
- Data retention and destruction policies
- Cross-border data transfer considerations

### 15.2 Security Requirements

- Access controls and authentication requirements
- Background check requirements for Provider personnel
- Secure development practices (if applicable)
- Vulnerability assessment and penetration testing (if applicable)
- Incident response and breach notification procedures (within [24/48/72] hours)

### 15.3 Compliance

- Applicable regulations (GDPR, HIPAA, SOX, PCI-DSS, CCPA, etc.)
- Audit rights
- Data Processing Agreement reference (if applicable)

## Section 16: Signatures

```
IN WITNESS WHEREOF, the parties have caused this Statement of Work to be
executed by their duly authorized representatives as of the Effective Date.


FOR [PROVIDER LEGAL NAME]:


_______________________________________
Name:
Title:
Date:


FOR [CLIENT LEGAL NAME]:


_______________________________________
Name:
Title:
Date:
```

## Appendices

Include as needed:

- Appendix A: Detailed Technical Requirements or Specifications
- Appendix B: Rate Card (for T&M engagements)
- Appendix C: Change Request Form Template
- Appendix D: Acceptance Certificate Template
- Appendix E: Status Report Template
- Appendix F: Data Processing Agreement (if applicable)
- Appendix G: Service Level Agreement (if applicable)
