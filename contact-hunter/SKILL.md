---
name: contact-hunter
description: Search and extract contact information for people or companies including names, phone numbers, emails, job titles, and LinkedIn profiles. Aggregates data from multiple sources and provides enriched contact details. Use when users need to find contact information, build prospect lists, or enrich existing contact data.
---

# Contact Hunter

Find and enrich publicly available contact information from multiple sources with full source attribution.

This skill guides the search process and organizes results. It does not directly access paid APIs; it produces structured queries, suggests where to look, then validates and formats what is found.

## Contents
- `references/search-queries.md` — per-target search briefs and reusable query patterns
- `references/output-templates.md` — data collection template, contact card, bulk CSV, email-pattern report, export formats
- `references/compliance.md` — allowed/not-allowed rules, best practices, verification steps

## Workflow

1. Identify the search type: person, company, role, email verification, or bulk enrichment.

2. Gather search parameters: name, company, job title, location, industry, LinkedIn URL, email domain, and any other identifiers.

3. Select sources to check: LinkedIn, company website (About/Team/Contact/Leadership), GitHub (developers), Twitter/X, professional directories, public databases, and any paid tools the user has access to (ZoomInfo, Apollo.io, Hunter.io, RocketReach).

4. Build the search plan using the query patterns in `references/search-queries.md`. Produce a per-target brief with LinkedIn, Google, company-website, email-pattern, and GitHub queries.

5. Detect the company email pattern from confirmed addresses, then derive candidate emails. See the email-pattern report in `references/output-templates.md`.

6. Collect and verify results. Cross-reference multiple sources and run the verification steps in `references/compliance.md` before recording any field.

7. Format output using the templates in `references/output-templates.md`: data collection template, individual contact card, or bulk CSV. Export as CSV, JSON, vCard, or CRM-specific CSV (Salesforce, HubSpot) as requested.

8. For enrichment of existing contacts, refresh: current job title, company changes, updated contact info, social profiles, company information, reporting structure, and recent activity.

## Quality bar

Ensure every contact record includes all available fields, cites its sources, carries a confidence/verification level and freshness date, follows data-privacy law, is formatted consistently, notes contact preferences, provides role context (tenure, team), flags uncertainties, and suggests verification steps. Operate only within the rules in `references/compliance.md`.

## Example triggers
- "Find the VP of Sales at Acme Corp"
- "Get contact info for John Smith at Microsoft"
- "Find engineering managers at Stripe"
- "Enrich this list of contacts with emails"
- "What's the email pattern at Google?"
- "Find the marketing team at HubSpot"
