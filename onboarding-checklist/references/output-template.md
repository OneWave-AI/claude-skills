# Output Template

Generate `onboarding-checklist.md` with the structure below. Every section is mandatory. The final document must exceed 300 lines.

## Header Block

```markdown
# Client Onboarding Checklist

**Client**: [Client name/type]
**Engagement Type**: [Consulting | SaaS | Agency]
**Services**: [Services purchased]
**Timeline**: [Start date/duration]
**Generated**: [Current date]

---

## Team Roster

| Role | Name (TBD) | Organization | Email |
|------|-----------|--------------|-------|
| [Role] | [Placeholder] | [Provider/Client] | [Placeholder] |

---
```

## Phase 1: Pre-Kickoff (Before Day 1)

Generate 8-12 tasks that must be completed before the kickoff meeting. Each task follows this format:

```markdown
### Task [number]: [Task title]
- **Owner**: [Role responsible]
- **Deadline**: [Relative date, e.g., "Day -5", "Day -3"]
- **Dependencies**: [What must be done first, or "None"]
- **Acceptance Criteria**: [Specific, measurable completion standard]
- **Notes**: [Context or tips for execution]
```

Pre-kickoff tasks must include (adapt to engagement type):
- Internal team briefing and role assignment
- Client background research and account review
- Access provisioning and tool setup
- Contract and SOW confirmation
- Kickoff meeting agenda preparation and calendar invites
- Welcome packet or onboarding guide preparation
- Stakeholder mapping on the client side
- Risk and dependency identification

## Phase 2: Week 1 (Days 1-5)

Generate 10-15 tasks covering the first week. This is the highest-intensity phase. Must include:
- Kickoff meeting execution
- Discovery sessions or requirements gathering
- Technical environment setup or platform walkthrough
- Communication cadence establishment (standups, Slack channels, status reports)
- Initial deliverable or milestone planning
- Access verification and permissions testing
- Document sharing and knowledge base setup
- Quick wins identification and execution
- Escalation path and point-of-contact confirmation
- First status report or check-in

## Phase 3: Weeks 2-4 (Days 6-20)

Generate 12-18 tasks covering the remaining onboarding period. Organize by week where appropriate. Must include:
- Core deliverable production or configuration work
- Review and feedback cycles
- Training sessions (if applicable)
- Integration testing or QA
- Stakeholder demos or progress presentations
- Documentation and runbook creation
- Process optimization based on Week 1 learnings
- Client satisfaction check-in
- Risk mitigation actions
- Preparation for handoff or steady-state transition

## Phase 4: Handoff Criteria

Generate a clear, binary checklist of conditions that must ALL be true before onboarding is considered complete:

```markdown
## Handoff Criteria

All of the following must be verified before transitioning to steady-state:

- [ ] [Criterion 1]
- [ ] [Criterion 2]
...
```

Include 10-15 handoff criteria covering:
- All deliverables accepted and signed off
- Access and permissions verified for all users
- Documentation complete and accessible
- Training completed with attendance confirmed
- Communication channels transitioned to BAU (business-as-usual)
- Escalation paths documented and tested
- Outstanding issues logged and assigned
- Client satisfaction survey sent and baseline recorded
- Internal retrospective completed
- Billing and invoicing confirmed

## Formatting Rules

- Use Markdown throughout
- No emojis anywhere in the document
- Use tables for structured data (team roster, timeline summaries)
- Use checkboxes `- [ ]` for actionable items in handoff criteria
- Use `###` for individual tasks, `##` for phase headers, `#` for document title
- Include horizontal rules `---` between major sections
- Every task must have all five fields: Owner, Deadline, Dependencies, Acceptance Criteria, Notes
- Deadlines use relative format: "Day -5", "Day 1", "Day 3", "Day 10", etc.
- Owner fields use role titles, not names (e.g., "Project Manager", "Client IT Lead", "Account Executive")
- The final document must be self-contained and immediately usable without further editing beyond filling in names and dates
