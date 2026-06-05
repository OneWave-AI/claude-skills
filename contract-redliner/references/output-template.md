# contract-review.md Output Template

Generate `contract-review.md` containing ALL of the following sections in this order. Favor thoroughness over brevity.

```markdown
# Contract Redline Review

LEGAL DISCLAIMER: This analysis is informational only and does not constitute legal advice.
Contract interpretation is jurisdiction-specific and fact-dependent. Always consult a qualified
attorney before signing or modifying any legal agreement. This tool is designed to surface
potential issues and suggest alternative language for discussion purposes only.

---

## Contract Overview

| Field | Details |
|-------|---------|
| Contract Type | [Type] |
| Party A (Drafter) | [Name and role] |
| Party B (Signer) | [Name and role] |
| Effective Date | [Date or "Upon execution"] |
| Initial Term | [Duration] |
| Renewal Terms | [Auto-renewal details or "None"] |
| Governing Law | [Jurisdiction] |
| Dispute Resolution | [Method and forum] |
| Total Contract Value | [If determinable] |

---

## Executive Summary

### Overall Risk Assessment: [CRITICAL / HIGH / MEDIUM / LOW]

[3-5 paragraph summary of the contract's overall posture. Who does it favor? What are
the most significant issues? What is the recommended course of action? Is this contract
within market norms for its type, or does it deviate significantly?]

### Risk Distribution

| Rating | Count |
|--------|-------|
| CRITICAL | [N] |
| HIGH | [N] |
| MEDIUM | [N] |
| LOW | [N] |
| ACCEPTABLE | [N] |

### Top 5 Priority Issues

1. **[Issue name]** (Section [X]) -- [One-line description]. Rating: [RATING]
2. **[Issue name]** (Section [X]) -- [One-line description]. Rating: [RATING]
3. **[Issue name]** (Section [X]) -- [One-line description]. Rating: [RATING]
4. **[Issue name]** (Section [X]) -- [One-line description]. Rating: [RATING]
5. **[Issue name]** (Section [X]) -- [One-line description]. Rating: [RATING]

---

## Clause-by-Clause Analysis

[For EVERY section of the contract, include an entry. Sections with no issues still
get listed with an ACCEPTABLE rating and brief note.]

### Section [Number]: [Title]

**Risk Rating: [RATING]**

**Risk Categories Triggered:** [List applicable categories, or "None" if acceptable]

#### Current Language

> "[Exact quote from the contract]"

#### Analysis

[Detailed analysis of the clause. What does it mean in practice? What are the legal
implications? How does it compare to market standard? Who benefits and who is at risk?]

#### Issues Identified

[Numbered list of specific problems, each tagged with its risk category]

1. **[Category]**: [Description of issue]
2. **[Category]**: [Description of issue]

#### Redline

CURRENT:
> "[Original text]"

TRACKED CHANGES:
> "[-deleted text-] [+replacement text+]"

CLEAN:
> "[Final suggested text after all changes accepted]"

#### Negotiation Talking Point

[How to raise this issue with the counterparty. Frame as mutual benefit where possible.
Include fallback positions and compromise language.]

---

[Repeat for every section]

---

## Missing Provisions

The following standard provisions are absent from this contract and should be added:

### [Missing Provision Name]

**Risk Category:** Missing Standard Protections
**Risk Rating:** [RATING]

**Why This Matters:**
[Explanation of why this provision is important and what risk its absence creates]

**Suggested Language to Add:**

> "[Complete draft language for the missing provision]"

**Placement:** [Where in the contract this should be inserted]

---

[Repeat for every missing provision]

---

## Defined Terms Audit

The following terms are used in the contract but not defined, or are defined ambiguously:

| Term | Where Used | Problem | Suggested Definition |
|------|-----------|---------|---------------------|
| [Term] | Section [X] | [Not defined / Ambiguous / Circular] | "[Suggested definition]" |

---

## Cross-Reference Issues

[Identify any internal inconsistencies, conflicting provisions, or broken cross-references
within the contract]

| Section A | Section B | Conflict Description | Recommended Resolution |
|-----------|-----------|---------------------|----------------------|
| [Ref] | [Ref] | [Description] | [Fix] |

---

## Compliance Checklist

Verify the contract addresses the following regulatory and compliance requirements
(mark as Present, Absent, or Insufficient):

| Requirement | Status | Section | Notes |
|------------|--------|---------|-------|
| Data protection / privacy | [Status] | [Ref] | [Notes] |
| GDPR compliance (if EU data) | [Status] | [Ref] | [Notes] |
| CCPA compliance (if CA data) | [Status] | [Ref] | [Notes] |
| Anti-bribery / FCPA | [Status] | [Ref] | [Notes] |
| Export controls | [Status] | [Ref] | [Notes] |
| Accessibility requirements | [Status] | [Ref] | [Notes] |
| Insurance requirements | [Status] | [Ref] | [Notes] |
| Background check provisions | [Status] | [Ref] | [Notes] |
| Subcontractor flow-down | [Status] | [Ref] | [Notes] |
| Record retention | [Status] | [Ref] | [Notes] |

---

## Financial Impact Analysis

| Clause | Best Case | Worst Case | Expected | Notes |
|--------|-----------|------------|----------|-------|
| Liability exposure | [Amount] | [Amount] | [Amount] | [Notes] |
| Termination penalties | [Amount] | [Amount] | [Amount] | [Notes] |
| Auto-renewal cost | [Amount] | [Amount] | [Amount] | [Notes] |
| Indemnification exposure | [Amount] | [Amount] | [Amount] | [Notes] |
| IP value at risk | [Qualitative] | [Qualitative] | [Qualitative] | [Notes] |

---

## Negotiation Strategy

### Tier 1: Must-Have Changes (Non-Negotiable)

[List changes that should be treated as conditions of signing. These are CRITICAL-rated
issues. For each, provide the specific ask and the walk-away position.]

1. **[Change]**
   - Ask: [What to request]
   - Justification: [Why it is reasonable]
   - Walk-away: [At what point this becomes a deal-breaker]

### Tier 2: Strong Requests (High Priority)

[List changes that should be pushed hard in negotiation. These are HIGH-rated issues.
For each, provide the ask, justification, and compromise position.]

1. **[Change]**
   - Ask: [What to request]
   - Justification: [Why it is reasonable]
   - Compromise: [Acceptable middle ground]

### Tier 3: Improvement Requests (Medium Priority)

[List changes that improve the contract but can be traded away for concessions on
higher-priority items. These are MEDIUM-rated issues.]

1. **[Change]**
   - Ask: [What to request]
   - Trade value: [What concession this could be exchanged for]

### Tier 4: Cleanup Items (Low Priority)

[List minor clarifications and improvements. These are LOW-rated issues that can be
raised as "housekeeping" items.]

1. **[Change]** -- [Brief description]

---

## Recommended Negotiation Sequence

[Provide a recommended order for raising redline items with the counterparty. Group
related issues together. Suggest which items to lead with and which to hold in reserve
as trading chips.]

1. **Open with**: [Items to raise first -- typically mutual benefit items that build goodwill]
2. **Core asks**: [The critical and high-priority changes]
3. **Trading chips**: [Medium items to concede in exchange for core asks]
4. **Cleanup round**: [Low-priority items to sweep up at the end]

---

## Pre-Signature Checklist

Before signing, confirm:

- [ ] All CRITICAL issues have been resolved or accepted with eyes open
- [ ] All HIGH issues have been negotiated or consciously accepted
- [ ] Defined terms are clear and consistent
- [ ] Cross-references are accurate
- [ ] Exhibits, schedules, and attachments are complete and attached
- [ ] Signature blocks are correct (proper entity names, authority)
- [ ] Governing law and venue are acceptable
- [ ] Insurance requirements can be met
- [ ] Compliance obligations can be satisfied
- [ ] Internal approvals have been obtained
- [ ] Effective date and term are correct
- [ ] Payment terms and amounts are verified
- [ ] All negotiated changes are reflected in the final version
- [ ] Legal counsel has reviewed the final version

---

## Appendix A: Full Redline Summary Table

| # | Section | Issue | Category | Rating | Current | Suggested Change |
|---|---------|-------|----------|--------|---------|-----------------|
| 1 | [Ref] | [Brief] | [Cat] | [Rating] | [Key phrase] | [Key change] |
| 2 | [Ref] | [Brief] | [Cat] | [Rating] | [Key phrase] | [Key change] |
[Continue for all identified issues]

---

## Appendix B: Tracked Changes Quick Reference

For easy copy-paste into negotiation markup:

### Change 1: [Section Ref] -- [Brief Title]

DELETE: "[Text to remove]"
INSERT: "[Text to add]"

### Change 2: [Section Ref] -- [Brief Title]

DELETE: "[Text to remove]"
INSERT: "[Text to add]"

[Continue for all changes]
```
