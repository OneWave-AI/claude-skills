# Scaling Rules, Pitfalls, and Quality Standards

## Timeline Scaling Rules

Adapt the checklist timeline based on the user's specified duration:

- **2-week onboarding**: Compress Weeks 2-4 into Week 2. Reduce tasks per phase by 30%. Combine related tasks. Pre-kickoff period is 3 days maximum.
- **4-week onboarding** (standard): Use the default structure.
- **6-week onboarding**: Expand Weeks 2-4 into Weeks 2-6. Add a dedicated "Optimization and Fine-Tuning" phase in Weeks 5-6. Increase tasks per phase by 20%.
- **8+ week onboarding**: Add monthly milestone reviews. Include a formal "Phase Gate" review at the midpoint. Add change management tasks. Include a "Lessons Learned" session at Week 4 before continuing.

## Team Size Scaling Rules

Adapt the checklist based on the number of people involved:

- **Small team (1-3 per side)**: Individual task assignments. Fewer handoff points. Combined roles (e.g., PM doubles as account lead). Shorter meetings.
- **Medium team (4-8 per side)**: Dedicated roles for each major function. Sub-team leads for client and provider. Weekly all-hands plus daily standups for active workstreams.
- **Large team (9+ per side)**: Workstream-specific onboarding tracks. RACI matrix required. Executive sponsor check-ins. Dedicated change management tasks. Communication plan as a standalone deliverable.

## Common Pitfalls to Avoid

Actively guard against these common onboarding failures:

1. **Front-loading all work onto the client**: Ensure the provider team owns the majority of early tasks. Clients are busy -- reduce their burden in Week 1.
2. **Vague acceptance criteria**: "Set up the platform" is not an acceptance criterion. "All 5 integrations return 200 status on test API calls" is.
3. **Missing dependencies**: If Task 12 requires Task 8's output, that dependency must be explicit. Never assume the reader will infer the order.
4. **No escalation path**: Every checklist must include at least one task for defining and documenting the escalation process.
5. **Ignoring the client's internal approvals**: Enterprise clients often need internal sign-offs that add 2-5 days. Build buffer into deadlines.
6. **Training as an afterthought**: Training tasks should appear in Week 2 at the latest, not crammed into the final days.
7. **No success metrics**: The handoff criteria must include at least one quantitative measure (e.g., "90% of users have logged in at least once").
8. **Forgetting the internal retrospective**: The provider team needs a post-onboarding debrief to improve the process for future clients.

## Quality Standards

Before finalizing output, verify:
1. The document exceeds 300 lines
2. Every task has all five required fields populated
3. Dependencies form a logical chain (no circular dependencies, no references to nonexistent tasks)
4. Deadlines progress chronologically within each phase
5. Owners are balanced across provider and client roles
6. All five email templates are present with complete body text
7. Handoff criteria are specific and binary (pass/fail, not subjective)
8. The engagement type classification is reflected throughout the document structure
9. Tech stack items from the input appear in relevant tasks (e.g., "Configure Slack channel" if Slack is in the stack)
10. No emojis appear anywhere in the output
