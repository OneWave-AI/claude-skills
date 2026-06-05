# CRM Logging (Supabase)

Use the Supabase MCP Connector to log all lead data to the CRM database.

## Available Supabase MCP Tools

- `mcp__claude_ai_Supabase__execute_sql` -- Execute SQL queries
- `mcp__claude_ai_Supabase__list_tables` -- List existing tables
- `mcp__claude_ai_Supabase__apply_migration` -- Apply schema migrations
- `mcp__claude_ai_Supabase__list_projects` -- List Supabase projects

On first run, check if the required tables exist. If not, create them with `mcp__claude_ai_Supabase__apply_migration`.

## Table: `leads`

```sql
CREATE TABLE IF NOT EXISTS leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),

  -- Contact info
  contact_name TEXT NOT NULL,
  contact_email TEXT NOT NULL,
  contact_phone TEXT,
  contact_role TEXT,
  contact_linkedin TEXT,

  -- Company info
  company_name TEXT,
  company_domain TEXT,
  company_size TEXT CHECK (company_size IN ('startup', 'smb', 'midmarket', 'enterprise', 'unknown')),
  company_industry TEXT,

  -- Inquiry details
  inquiry_type TEXT NOT NULL CHECK (inquiry_type IN (
    'demo_request', 'partnership', 'rfp', 'referral',
    'pricing_inquiry', 'general_inquiry', 'support_question'
  )),
  inquiry_summary TEXT NOT NULL,
  specific_services TEXT[],
  pain_points TEXT[],
  timeline TEXT,
  budget_signals TEXT,

  -- Scoring
  score_total INTEGER NOT NULL DEFAULT 0,
  score_icp INTEGER NOT NULL DEFAULT 0,
  score_intent INTEGER NOT NULL DEFAULT 0,
  score_urgency INTEGER NOT NULL DEFAULT 0,
  qualification TEXT NOT NULL CHECK (qualification IN ('sql', 'mql', 'iql', 'unqualified')),
  priority TEXT NOT NULL CHECK (priority IN ('P1', 'P2', 'P3', 'P4')),
  score_adjustments JSONB DEFAULT '[]'::jsonb,

  -- Source tracking
  source TEXT NOT NULL DEFAULT 'gmail',
  source_detail TEXT,
  gmail_message_id TEXT UNIQUE,
  gmail_thread_id TEXT,
  received_date TIMESTAMPTZ,
  forwarded_by TEXT,

  -- Response tracking
  response_drafted BOOLEAN DEFAULT false,
  response_draft_id TEXT,
  response_draft_text TEXT,
  response_sent BOOLEAN DEFAULT false,
  response_sent_date TIMESTAMPTZ,

  -- Pipeline tracking
  stage TEXT NOT NULL DEFAULT 'new' CHECK (stage IN (
    'new', 'contacted', 'qualifying', 'proposal', 'negotiation', 'won', 'lost', 'nurture'
  )),
  next_action TEXT,
  next_action_date TIMESTAMPTZ,
  assigned_to TEXT,
  notes TEXT,
  tags TEXT[]
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(contact_email);
CREATE INDEX IF NOT EXISTS idx_leads_company ON leads(company_domain);
CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score_total DESC);
CREATE INDEX IF NOT EXISTS idx_leads_stage ON leads(stage);
CREATE INDEX IF NOT EXISTS idx_leads_created ON leads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_qualification ON leads(qualification);
CREATE INDEX IF NOT EXISTS idx_leads_gmail_msg ON leads(gmail_message_id);
```

## Table: `lead_activity_log`

```sql
CREATE TABLE IF NOT EXISTS lead_activity_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT now(),
  activity_type TEXT NOT NULL CHECK (activity_type IN (
    'email_received', 'email_drafted', 'email_sent',
    'score_updated', 'stage_changed', 'note_added',
    'call_scheduled', 'call_completed', 'meeting_booked',
    'proposal_sent', 'follow_up_scheduled'
  )),
  description TEXT NOT NULL,
  metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_activity_lead ON lead_activity_log(lead_id);
CREATE INDEX IF NOT EXISTS idx_activity_type ON lead_activity_log(activity_type);
CREATE INDEX IF NOT EXISTS idx_activity_created ON lead_activity_log(created_at DESC);
```

## Table: `pipeline_config`

```sql
CREATE TABLE IF NOT EXISTS pipeline_config (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  config_key TEXT UNIQUE NOT NULL,
  config_value JSONB NOT NULL,
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Default ICP configuration
INSERT INTO pipeline_config (config_key, config_value) VALUES
  ('icp_primary_industries', '["Technology", "SaaS", "Financial Services", "Healthcare Tech", "Professional Services"]'::jsonb),
  ('icp_secondary_industries', '["E-commerce", "Manufacturing", "Education", "Real Estate Tech", "Media"]'::jsonb),
  ('icp_target_company_sizes', '["midmarket", "enterprise"]'::jsonb),
  ('icp_target_roles', '["C-suite", "VP", "Director", "Head of"]'::jsonb),
  ('response_calendar_link', '"https://calendly.com/PLACEHOLDER"'::jsonb),
  ('response_sender_name', '"PLACEHOLDER"'::jsonb),
  ('daily_report_recipients', '[]'::jsonb)
ON CONFLICT (config_key) DO NOTHING;
```

## Logging Procedure

For each processed lead, execute these steps in order.

### Step a: Check for Duplicates

```sql
SELECT id, score_total, stage FROM leads
WHERE gmail_message_id = '[message_id]'
   OR (contact_email = '[email]' AND company_domain = '[domain]' AND created_at > now() - interval '30 days')
LIMIT 1;
```

If a duplicate is found:
- Same `gmail_message_id`: Skip (already processed).
- Same contact + company within 30 days: Update the existing lead with the new interaction, log to `lead_activity_log`, and apply the Repeat Inquiry Bonus (+8 points).

### Step b: Insert New Lead

```sql
INSERT INTO leads (
  contact_name, contact_email, contact_phone, contact_role, contact_linkedin,
  company_name, company_domain, company_size, company_industry,
  inquiry_type, inquiry_summary, specific_services, pain_points, timeline, budget_signals,
  score_total, score_icp, score_intent, score_urgency, qualification, priority,
  score_adjustments,
  source, source_detail, gmail_message_id, gmail_thread_id, received_date, forwarded_by,
  response_drafted, response_draft_text, next_action, next_action_date
) VALUES (
  -- [extracted values from lead profile]
);
```

### Step c: Log Activity

```sql
INSERT INTO lead_activity_log (lead_id, activity_type, description, metadata)
VALUES (
  '[new_lead_id]',
  'email_received',
  'Inbound [inquiry_type] from [contact_name] at [company_name]',
  '{"subject": "[subject]", "score": [score], "qualification": "[qual]"}'::jsonb
);
```

If a draft was created:

```sql
INSERT INTO lead_activity_log (lead_id, activity_type, description, metadata)
VALUES (
  '[new_lead_id]',
  'email_drafted',
  'Auto-drafted [priority] response for review',
  '{"draft_id": "[gmail_draft_id]", "template_tier": "[hot/warm/cool]"}'::jsonb
);
```

### Step d: Set Next Action

Based on lead priority, set the appropriate next action:

```
P1 (HOT):  next_action = "Review and send draft response"
           next_action_date = now()

P2 (WARM): next_action = "Review draft, personalize, and send"
           next_action_date = now() + interval '4 hours'

P3 (COOL): next_action = "Review and send nurture response"
           next_action_date = now() + interval '24 hours'

P4 (COLD): next_action = "Review -- may not require response"
           next_action_date = now() + interval '48 hours'
```
