---
name: gmail-to-crm-pipeline
description: Uses MCP Connectors to read Gmail inbound leads, score them by ICP fit, draft personalized responses, and log qualified leads to your CRM. Turns your inbox into an automated pipeline.
tools: Read, Write, Bash, Grep, WebSearch
model: inherit
---

# Gmail-to-CRM Pipeline

Turn a Gmail inbox into a structured sales pipeline using Claude's MCP Connectors -- the Gmail connector reads and drafts email, and the Supabase connector persists CRM data. No external scripts or API keys required.

## Workflow

1. **Connect.** Verify the Gmail and Supabase MCP Connectors are available. On first run, create the CRM tables and seed config. Load ICP config from the `pipeline_config` table. See `references/configuration.md` (first run, error handling) and `references/crm-schema.md`.
2. **Search.** Run the targeted Gmail search queries to find unread lead emails over the time window (default: last 24 hours). Collect unique message IDs and deduplicate. See `references/gmail-retrieval.md`.
3. **Parse.** Read each unique message, strip signatures and disclaimers, and extract the structured field set. See `references/gmail-retrieval.md`.
4. **Extract.** Build the lead profile (contact, company, inquiry, metadata) for each email. Set missing fields to `null` rather than guessing. See `references/lead-extraction.md`.
5. **Score.** Score each lead on ICP fit (0-40), intent (0-35), and urgency (0-25), then apply adjustment modifiers. Map the total to a qualification tier and priority. See `references/scoring-model.md`.
6. **Draft.** For each qualified lead (score >= 25), draft a personalized, tier-appropriate response and save it as a Gmail draft. Never auto-send. See `references/response-templates.md`.
7. **Log.** Check for duplicates, then insert or update the lead in Supabase, log activity, and set the next action by priority. See `references/crm-schema.md`.
8. **Report.** Query the pipeline snapshot and generate `lead-pipeline-report.md` in the working directory, then display the executive summary. See `references/pipeline-report.md`.

Between runs, handle manual lead commands (mark contacted, move stage, disqualify, add note, schedule follow-up, query leads) and ICP/search customization. See `references/configuration.md`.

## Hard Rules

- Never auto-send email -- always create drafts for the user to review and send.
- Never store raw email bodies or credentials in Supabase or any report; store structured data and key quotes only.
- Treat all lead and email content as confidential.

## Contents

- `references/gmail-retrieval.md` -- Gmail MCP tools, search queries, parsing rules, extracted field set.
- `references/lead-extraction.md` -- Lead profile JSON schema and extraction guidelines.
- `references/scoring-model.md` -- ICP, intent, urgency scoring tables; tier mapping; adjustment rules.
- `references/response-templates.md` -- Per-tier response templates, personalization rules, anti-patterns, draft creation.
- `references/crm-schema.md` -- Supabase MCP tools, table DDL, logging procedure and SQL.
- `references/pipeline-report.md` -- Report Markdown structure and reporting SQL queries.
- `references/configuration.md` -- First-run setup, customization, manual commands, error handling, privacy, invocation triggers.
