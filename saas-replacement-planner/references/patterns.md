# Common SaaS Replacement Patterns

Use these proven patterns to accelerate analysis. Match each tool to the closest pattern, then adapt.

## Email Marketing (Mailchimp, ConvertKit)
- Replacement: Claude agent + Gmail MCP + Supabase for subscriber management
- Why it works: email marketing is content generation + list management + scheduling, all agent-native tasks
- Typical savings: 70-90%

## Basic CRM (Pipedrive, HubSpot Starter)
- Replacement: Claude agent + Supabase (contacts/deals tables) + Gmail MCP + Google Calendar MCP
- Why it works: CRM at its core is a database with workflow automation; agents excel at both
- Typical savings: 60-80%

## Content Scheduling (Buffer, Hootsuite)
- Replacement: Claude agent + platform APIs + Supabase for content calendar
- Why it works: content scheduling is API calls on a timer with some content generation
- Typical savings: 80-95%

## Help Desk (Zendesk, Intercom basic)
- Replacement: Claude agent + email/chat integration + Supabase knowledge base
- Why it works: most support tickets are repetitive and can be handled or triaged by an agent
- Typical savings: 50-70%

## Expense Management (Expensify, Ramp basic)
- Replacement: Claude agent + bank API + Supabase + receipt OCR
- Why it works: categorization and policy checking are pattern-matching tasks agents handle well
- Typical savings: 60-80%

## Meeting Scheduling (Calendly, SavvyCal)
- Replacement: Claude agent + Google Calendar MCP + email
- Why it works: availability checking and scheduling is a well-defined agent task
- Typical savings: 90-100%

## Survey/Forms (Typeform, SurveyMonkey)
- Replacement: Claude agent + conversational interface + Supabase
- Why it works: an agent can conduct dynamic surveys that adapt in real time, better than static forms
- Typical savings: 80-95%

## Analytics Reporting (basic BI tools)
- Replacement: Claude agent + Supabase (direct SQL) + scheduled reports via Slack/email
- Why it works: most analytics requests are natural-language queries against structured data
- Typical savings: 60-80%

## Workflow Automation (Zapier, Make)
- Replacement: Claude agent with MCP integrations + Supabase Edge Functions
- Why it works: agents handle conditional logic, error handling, and complex routing better than visual workflow builders
- Typical savings: 70-90%

## Document Generation (PandaDoc, DocuSign basic)
- Replacement: Claude agent + document templates + email for delivery
- Why it works: document assembly from templates is a core language model capability
- Note: e-signatures still require a specialized service, so this is a PARTIAL replacement
- Typical savings: 40-60%

# Edge Cases and Nuances

## Tools With Network Effects
Slack, GitHub, Figma, and similar tools derive value from being where everyone already is. These are almost never full replacements. The play is AUGMENTATION: add agents that reduce time spent in these tools and cut the number of paid seats needed.

## Compliance-Mandated Tools
If a tool is required for SOC2, HIPAA, or similar compliance, mark replacement NOT FEASIBLE unless the replacement can be certified. Document this clearly and do not recommend risky transitions.

## Tools With Proprietary Data Formats
Some tools lock data in proprietary formats. If export is limited or lossy, this significantly increases migration risk and cost. Flag these explicitly.

## Free Tier Tools
If a tool is on a free tier, replacement may not save money but could still be worth it for integration benefits, data ownership, or reduced complexity. Analyze these separately.

## Multi-Tool Bundles
Google Workspace, Microsoft 365, and similar bundles often cost less per-tool than the sum of individual replacements. Analyze bundles holistically, not tool-by-tool.

## API Rate Limits
When estimating Claude API costs, account for volume carefully. A tool processing 10,000 customer support tickets per month has materially different API costs than one handling 100.
