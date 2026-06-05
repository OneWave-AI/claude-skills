# Configuration, Commands, and Operations

## First Run Setup

On the very first run:

1. **Check Supabase connection:** Use `mcp__claude_ai_Supabase__list_projects` to verify connectivity.
2. **Create tables:** Run the schema migration if tables do not exist (see `crm-schema.md`).
3. **Seed config:** Insert default ICP configuration.
4. **Ask the user** for:
   - Their name (for email signatures)
   - Their calendar link (for booking calls)
   - Primary industries they serve
   - Target company sizes
   - Any custom lead source search queries
5. **Store config** in the `pipeline_config` table.

## Customizing ICP Scoring

Users can update their ICP at any time by saying things like:
- "We only work with enterprise companies"
- "Add healthcare to our target industries"
- "Ignore leads from education sector"

Update the `pipeline_config` table accordingly and recalculate scores for recent leads if needed.

## Adjusting Search Queries

Users can add custom Gmail search queries:
- "Also check for emails with subject 'audit' or 'compliance'"
- "Ignore emails from recruiters"
- "Add a filter for emails mentioning 'Kubernetes'"

## Manual Lead Actions

Support these commands when the user provides direction:

- **"Mark [lead] as contacted"** -- Update stage, log activity.
- **"Move [lead] to proposal stage"** -- Update stage, prompt for proposal details.
- **"Disqualify [lead]"** -- Set stage to 'lost', log reason.
- **"Add note to [lead]"** -- Append to notes field, log activity.
- **"Schedule follow-up for [lead] on [date]"** -- Update next_action_date, log activity.
- **"Show me all hot leads"** -- Query and display P1 leads.
- **"What happened with [company]?"** -- Show full lead history and activity log.

## Error Handling

- **Gmail connector not available:** Inform the user they need to enable the Gmail MCP Connector in Claude Code settings. Provide setup instructions.
- **Supabase connector not available:** Offer to output lead data as local JSON/CSV files instead of database logging.
- **No matching emails found:** Report "No new lead emails found in the last 24 hours" and show the pipeline snapshot from existing CRM data.
- **Rate limiting:** If Gmail API limits are hit, pause and resume. Process in batches of 10 if more than 20 emails found.
- **Malformed emails:** Log parsing errors, skip the email, and flag it for manual review in the report.
- **Duplicate detection failure:** Default to creating a new lead record with a note about a potential duplicate.

## Privacy and Security

- **Never log email passwords or auth tokens** in any output.
- **Never include full email bodies** in the pipeline report -- only summaries and key quotes.
- **Draft responses stay as drafts** -- never auto-send.
- **Supabase connection** uses the MCP Connector's managed auth -- no raw credentials in the skill.
- **PII handling:** Treat lead data in Supabase as confidential; do not include it in any files shared externally.
- **Email content:** Do not store raw email HTML/body in Supabase; store only extracted structured data and summaries.

## Invocation Triggers

Invoke this skill when the user says things like:
- "Check my email for leads"
- "Process my inbox"
- "Run the lead pipeline"
- "Any new leads today?"
- "Check Gmail for demo requests"
- "Score my inbound leads"
- "Draft responses to new leads"
- "Generate a pipeline report"
- "How's my pipeline looking?"
