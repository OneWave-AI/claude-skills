---
name: churn-autopsy
description: Post-mortem analysis when a client churns. Takes client history, engagement data, support tickets, usage logs, and exit feedback to produce a comprehensive churn autopsy with root cause classification, timeline of decline, and preventive measures.
tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch
model: inherit
---

# Churn Autopsy

Dissect a client departure with forensic rigor and produce `churn-autopsy.md`: a historical record and retention playbook that turns a loss into organizational learning.

## Contents

- `references/inputs.md` -- required and optional data to gather before analysis
- `references/analysis-framework.md` -- the six-phase forensic method
- `references/root-cause-taxonomy.md` -- root cause categories and subcategories
- `references/output-template.md` -- full `churn-autopsy.md` report structure
- `references/standards.md` -- objectivity, rigor, sensitivity, incomplete-data, and operating rules

## Workflow

1. **Collect.** Gather all available inputs per `references/inputs.md`. Read provided files directly; query connected CRM and analytics MCP tools for account, usage, and support data. Note any gaps.
2. **Organize.** Build the full chronological timeline from first touch to cancellation before attempting analysis.
3. **Analyze.** Apply the six phases in `references/analysis-framework.md` systematically, without skipping: baseline, timeline of decline, root cause classification, missed warning signs, counterfactual analysis, lessons learned.
4. **Classify.** Assign one primary root cause and any contributing causes using `references/root-cause-taxonomy.md`.
5. **Draft.** Write the report in the structure defined in `references/output-template.md`.
6. **Challenge.** Review every conclusion against `references/standards.md`; attempt to disprove each finding before keeping it.
7. **Finalize.** Produce `churn-autopsy.md` with all sections complete in the current working directory or a user-specified location.
