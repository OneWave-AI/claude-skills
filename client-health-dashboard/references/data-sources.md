# Data Collection Sources

Gather data from every available source. Handle failures gracefully: log what was unavailable and proceed with partial data. Never fabricate data; use only what can actually be retrieved.

## 1. CRM Data

Pull all active client/company records from available CRM systems.

OneWave CRM (if available):
- `mcp__onewave-crm__list_companies` -- Get all company records
- `mcp__onewave-crm__get_company` -- Get detailed company info for each
- `mcp__onewave-crm__list_deals` -- Get all active deals
- `mcp__onewave-crm__get_deal` -- Get deal details (stage, value, close date)
- `mcp__onewave-crm__get_dashboard` -- Get dashboard overview metrics
- `mcp__onewave-crm__get_mrr_breakdown` -- Get MRR data per account
- `mcp__onewave-crm__get_pipeline_board` -- Get pipeline stage data
- `mcp__onewave-crm__list_contacts` -- Get all contacts
- `mcp__onewave-crm__get_timeline` -- Get activity timeline per account
- `mcp__onewave-crm__list_tasks` -- Get open tasks per account

HubSpot CRM (if available):
- `mcp__claude_ai_HubSpot__search_crm_objects` -- Search companies, deals, tickets
- `mcp__claude_ai_HubSpot__get_crm_objects` -- Get detailed object records
- `mcp__claude_ai_HubSpot__get_properties` -- Get custom properties for scoring
- `mcp__claude_ai_HubSpot__search_owners` -- Map owners to accounts

Extract per client: company name and ID; account owner / CSM; contract value (ARR/MRR); contract start and renewal date; current deal stage; account tier (enterprise/mid-market/SMB); custom health fields if they exist.

## 2. Support Ticket Data

- Check CRM for ticket/case objects associated with each company
- Search HubSpot tickets: `mcp__claude_ai_HubSpot__search_crm_objects` with objectType "tickets"
- Glob for local exports: `**/*ticket*`, `**/*support*`, `**/*case*`
- Search email for escalation threads: `mcp__claude_ai_Gmail__gmail_search_messages` with queries like "escalation", "urgent", "critical issue"

Extract per client: total open tickets; critical/high-priority open tickets; average resolution time (days); ticket volume trend (30/60/90 days); most recent ticket date and subject; escalations in last 90 days.

## 3. Usage and Engagement Metrics

- Glob for analytics exports: `**/*usage*`, `**/*analytics*`, `**/*metrics*`, `**/*engagement*`
- Check for CSV/Excel data files with usage information
- Search CRM custom properties for usage fields
- Check for any dashboard or reporting data

Extract per client: login frequency (DAU/WAU/MAU); feature adoption rate; usage trend over last 90 days; last login date; key feature usage breakdown; API call volume (if applicable); storage/resource consumption (if applicable).

## 4. Billing and Financial Data

- CRM deal values and MRR data from `mcp__onewave-crm__get_mrr_breakdown`
- HubSpot deal records with amount fields
- Glob for billing exports: `**/*billing*`, `**/*invoice*`, `**/*revenue*`, `**/*arr*`, `**/*mrr*`
- Check for payment status information

Extract per client: current ARR/MRR; payment status (current/overdue/at-risk); revenue trend (expanding/flat/contracting); days until renewal; expansion opportunity; discount level (if applicable); invoice payment timeliness.

## 5. Communication and Engagement Logs

- `mcp__onewave-crm__get_timeline` -- Activity timeline per account
- `mcp__claude_ai_Gmail__gmail_search_messages` -- Recent email threads with each client
- `mcp__claude_ai_Slack__slack_search_public_and_private` -- Client mentions in Slack
- CRM activity logs (calls, meetings, emails logged)
- Glob for meeting notes: `**/*meeting*`, `**/*notes*`

Extract per client: days since last contact (any channel); days since last meeting; email response rate / average response time; touchpoints in last 30/60/90 days; sentiment of recent communications; executive sponsor engagement level; NPS or CSAT score (if available).
