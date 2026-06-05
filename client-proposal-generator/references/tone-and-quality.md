# Tone Variants, Quality Check, and Error Handling

## Proposal Tone Variants

### Consultative (Default)
- Partner language ("we will work together to...")
- Questions woven in ("have you considered...?")
- Empathetic problem framing
- Moderate formality

### Enterprise
- Formal language throughout
- Risk mitigation emphasis
- Governance and compliance focus
- Reference to established methodologies by name
- Higher perceived authority

### Startup
- Direct and energetic
- Speed and iteration emphasis
- Lean methodology references
- Budget-conscious framing
- Practical over polished

### Technical
- Architecture diagrams and system design
- Technical trade-off analysis
- Detailed technology recommendations
- Less business context, more implementation detail
- Aimed at technical decision-makers

## Quality Check

Before delivering, verify:

- [ ] Client name is correct and consistent throughout
- [ ] Contact name is correct
- [ ] Company research is accurate (no hallucinated facts)
- [ ] All sections are present and complete
- [ ] Pricing tiers are internally consistent (each tier adds to the previous)
- [ ] Timeline is realistic (phases add up, dependencies make sense)
- [ ] No placeholder text remains (no `[TODO]` or `{variable}` markers)
- [ ] Tone matches the selected style (consultative, enterprise, startup, technical)
- [ ] Terms and conditions are reasonable
- [ ] Out-of-scope section is present (prevents expectation mismatch)
- [ ] Next steps are clear and actionable
- [ ] No fabricated case studies, team bios, or credentials
- [ ] Dates are current (proposal date, validity period)
- [ ] Currency is correct
- [ ] Document reads well end-to-end (no jarring transitions between sections)

## Error Handling

| Issue | Response |
|-------|----------|
| No client name provided | Ask before proceeding -- this is the one required field |
| Minimal problem description | Generate a proposal with broader framing; flag sections that need client input |
| Web research returns nothing | Proceed without personalization, note it, suggest the user add details |
| User provides no pricing guidance | Use mid-market rates from the calibration table |
| Scope is extremely vague | Create a "Discovery Phase" as the first tier, full engagement as tiers 2-3 |
| User asks for a one-page version | Generate an executive summary version (Section 1 + pricing + next steps) |
| User wants a different format (PDF, DOCX) | Generate the markdown and suggest using a PDF/DOCX conversion skill |
| Client is a competitor | Warn the user (in case it is accidental) but proceed if confirmed |
