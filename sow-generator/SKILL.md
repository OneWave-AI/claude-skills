---
name: sow-generator
description: Generates professional Statements of Work from a project brief. Use when a user needs to create an SOW, scope a project, define deliverables and milestones, or produce a consulting engagement document.
tools: Read, Write, Bash, WebSearch
model: inherit
---

# Statement of Work Generator

Generate complete, client-ready Statements of Work from a project brief, meeting the standards of Big Four consulting firms, top-tier agencies, and enterprise procurement. Produce polished documents ready for client review with minimal edits, never rough drafts or templates with blanks.

## Contents

- `references/required-inputs.md` -- inputs to gather and pre-generation client research
- `references/document-structure.md` -- the 16-section SOW structure with templates for every section
- `references/pricing-templates.md` -- fixed-price, time-and-materials, and retainer pricing models (Section 11)
- `references/legal-terms.md` -- confidentiality, IP, warranties, liability, termination, and other legal clauses (Section 14)
- `references/change-management.md` -- change request and change order process (Section 12)
- `references/risk-management.md` -- risk register and escalation path (Section 13)

## Workflow

1. Gather the required inputs. Read `references/required-inputs.md`. If any required item is missing, ask for it explicitly. Do not guess at critical commercial terms.
2. Research the client. Use WebSearch per `references/required-inputs.md` to gather company overview, recent news, technology footprint, and regulatory environment. If research yields nothing, proceed on user-provided inputs and flag assumptions explicitly. Never fabricate company information.
3. Select the pricing model from `references/pricing-templates.md` based on engagement type (default: fixed-price).
4. Generate all 16 sections following `references/document-structure.md`, pulling Section 11 from pricing-templates, Section 12 from change-management, Section 13 from risk-management, and Section 14 from legal-terms. Replace every bracketed placeholder with real values from inputs and research. Leave brackets only where the user explicitly deferred. Mark gaps with `[ACTION REQUIRED: ...]`.
5. Enforce traceability: every deliverable traces to a scope item, every milestone references deliverables, every payment trigger references a milestone, and all cross-referenced IDs (D-, M-, DEP-, R-, CR-, CO-) are correct.
6. Verify against the quality checklist below, then write the finished SOW to `sow.md` in the working directory (or a user-specified path).

## Output Requirements

- Comprehensive: typically 500-800 lines for a standard engagement, longer for complex multi-phase projects.
- Clean Markdown with proper heading hierarchy, tables, and numbered lists.
- Professional, precise, unambiguous third-person prose. Define any non-standard jargon on first use.
- No emojis anywhere in the document.
- Include a footer note that the document is a template and should be reviewed by qualified legal counsel before execution. Never provide legal advice.

## Quality Checklist

Verify before finalizing:

- All user-provided inputs are reflected accurately
- Client research is incorporated into Background and Context
- Every in-scope item has corresponding deliverables
- Every deliverable has measurable acceptance criteria
- Every milestone has a date, associated deliverables, and payment trigger (if applicable)
- Out-of-scope section is specific to this engagement, not generic
- Assumptions are realistic and comprehensive; dependencies have owners and deadlines
- Risk register contains engagement-specific risks, not boilerplate
- Payment schedule sums to the total engagement fee
- Legal sections are complete and internally consistent
- All cross-references resolve correctly
- No placeholder brackets remain except those explicitly deferred by the user
- Document reads as a cohesive narrative, not a filled-in template
- Tone is professional and consistent throughout

## Notes

- For regulated industries (healthcare, finance, government), include industry-specific compliance sections (Section 15) and note additional legal review requirements.
- Ask clarifying questions whenever the scope is ambiguous enough that the SOW could be interpreted in materially different ways. Ambiguity in an SOW is a professional failure.
