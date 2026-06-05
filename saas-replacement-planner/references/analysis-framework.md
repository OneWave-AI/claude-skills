# Analysis Framework

Run this full framework for every SaaS tool in the stack. Do not skip tools or give superficial analysis.

## 1. Tool Classification

Categorize the tool into one functional domain:

- Communication & Collaboration: Slack, Teams, Zoom, email tools
- CRM & Sales: Salesforce, HubSpot, Pipedrive, Apollo, Outreach
- Marketing & Content: Mailchimp, Buffer, Hootsuite, SEMrush, Ahrefs
- Project Management: Asana, Monday, Jira, Linear, ClickUp
- Customer Support: Zendesk, Intercom, Freshdesk, Help Scout
- Analytics & BI: Mixpanel, Amplitude, Tableau, Looker, Google Analytics
- Finance & Accounting: QuickBooks, Xero, Stripe, Brex
- HR & People: Gusto, BambooHR, Rippling, Lattice
- Developer Tools: GitHub, Vercel, AWS, Datadog, PagerDuty
- Document & Knowledge: Notion, Confluence, Google Workspace, Dropbox
- Design: Figma, Canva, Adobe CC
- Security & Compliance: Okta, 1Password, Vanta, Drata
- Data & Integration: Zapier, Make, Segment, Fivetran

## 2. Replacement Feasibility Assessment

Rate each tool on a four-tier scale.

FULL REPLACEMENT -- An AI agent can completely replace this tool within 3 months.
- Core functionality is primarily data processing, content generation, routing, or decision-making
- No proprietary network effects or marketplace dependencies
- API access to underlying data sources is available
- Examples: most email marketing tools, basic CRM, content scheduling, expense categorization

PARTIAL REPLACEMENT -- An AI agent can replace 50-80% of functionality, with the remainder handled by a simpler/cheaper alternative or custom integration.
- Core workflows automate, but some UI-heavy or collaborative features require a lightweight frontend
- Some integration lock-in but data is exportable
- Examples: project management (agent handles routing/updates, simple UI for boards), analytics (agent handles queries/reports, lightweight dashboard for visualization)

AUGMENTATION -- Keep the tool but layer an AI agent on top to reduce seats, automate workflows, and cut costs by 30-60%.
- The tool provides essential infrastructure or has strong network effects
- An agent can automate repetitive tasks within the tool via API
- Examples: Slack (keep, add agent for triage/routing), GitHub (keep, add agent for reviews/CI)

NOT FEASIBLE -- Replacement is not practical today due to regulatory requirements, deep platform lock-in, or infrastructure dependencies.
- Compliance mandates require the specific vendor
- The tool IS the platform (e.g., AWS for hosting, Stripe for payments processing)
- Switching cost exceeds 3-year savings
- Examples: core cloud infrastructure, payment processors, identity providers with SOC2/compliance requirements

## 3. Build Cost Estimation

For each FULL or PARTIAL tool, estimate the build cost.

One-Time Build Costs:
- Engineering hours (at $150/hr blended rate, adjustable)
- Claude API costs during development and testing
- Infrastructure setup (Supabase, Vercel, etc.)
- Data migration effort
- Integration development with remaining tools

Ongoing Operating Costs:
- Claude API usage (estimate tokens/month based on workflow volume)
- Infrastructure hosting (typically $20-100/month for most agent workloads)
- Maintenance engineering hours (estimate 2-4 hrs/month per agent)
- MCP server hosting if applicable

Cost Calculation Formula:
```
Annual SaaS Cost = (monthly_price * seats * 12)
Year 1 Agent Cost = build_cost + (monthly_operating * 12)
Year 2+ Agent Cost = monthly_operating * 12
Break-Even Month = build_cost / (monthly_saas - monthly_operating)
3-Year ROI = ((annual_saas * 3) - (year1_cost + year2_cost + year3_cost)) / (year1_cost + year2_cost + year3_cost) * 100
```

## 4. Claude + MCP Alternative Architecture

For each replaceable tool, design the agent-based alternative.

Agent Architecture:
- Claude model tier (Haiku for simple routing, Sonnet for most workflows, Opus for complex reasoning)
- System prompt and tool configuration the agent needs
- MCP servers that provide the required integrations
- Whether the agent should be autonomous, human-in-the-loop, or scheduled

Required MCP Integrations -- map each replacement to specific MCP servers:

| SaaS Category | MCP Servers | Key Capabilities |
|---|---|---|
| CRM | Supabase, Gmail, Google Calendar, Slack, Apollo | Contact management, email sequences, meeting scheduling |
| Marketing | Gmail, Slack, WebSearch, WebFetch | Content creation, distribution, analytics |
| Project Management | GitHub, Slack, Google Calendar, Supabase | Task tracking, sprint management, status updates |
| Customer Support | Gmail, Slack, Supabase, WebFetch | Ticket routing, response generation, knowledge base |
| Analytics | Supabase, Google Sheets, WebFetch | Data queries, report generation, anomaly detection |
| Sales Outreach | Apollo, Gmail, LinkedIn, Clay | Prospecting, sequencing, personalization |
| Documentation | GitHub, Supabase, Slack | Auto-documentation, knowledge management |
| Scheduling | Google Calendar, Slack, Gmail | Meeting coordination, availability management |
| Finance | Supabase, Gmail, Google Sheets | Invoice processing, expense tracking, reporting |

Data Migration Path:
- How to export data from the current tool
- Where to store it (typically Supabase Postgres)
- Schema design for the replacement
- Migration timeline and rollback plan

## 5. Risk Assessment

Evaluate each replacement on a 1-5 scale:

- Data Loss Risk: Can all critical data be exported and preserved?
- Workflow Disruption: How much will daily workflows change?
- Team Adoption: Will the team resist the change?
- Reliability Gap: Is the agent solution as reliable as the SaaS?
- Compliance Impact: Any regulatory implications of switching?
- Vendor Lock-in Escape: How difficult is it to leave the current tool?
- Feature Gap: What capabilities are lost in the transition?

Aggregate risk score: (sum of all scores) / 35 * 100 = risk percentage.

## 6. Priority Matrix

Score each opportunity on two axes.

Impact Score (1-10):
- Annual cost savings (1-3 points based on dollar amount)
- Workflow improvement potential (1-3 points)
- Strategic alignment with AI-first operations (1-2 points)
- Data ownership and portability gain (1-2 points)

Effort Score (1-10):
- Engineering complexity (1-3 points, lower is easier)
- Integration dependencies (1-3 points, lower is fewer)
- Data migration complexity (1-2 points, lower is simpler)
- Team change management (1-2 points, lower is easier)

Priority Quadrants:
- Q1 Quick Wins (High Impact, Low Effort): do these first
- Q2 Strategic Bets (High Impact, High Effort): plan and resource these
- Q3 Fill-ins (Low Impact, Low Effort): do when convenient
- Q4 Reconsider (Low Impact, High Effort): probably not worth it
