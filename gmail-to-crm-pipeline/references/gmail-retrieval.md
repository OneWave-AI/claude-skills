# Gmail Connection and Email Retrieval

Use the Gmail MCP Connector (first-party MCP integration in Claude Code, launched February 2026) to access the inbox. The connector handles authentication through Claude's MCP Connectors infrastructure -- no OAuth setup or API key management.

## Available Gmail MCP Tools

- `mcp__claude_ai_Gmail__gmail_search_messages` -- Search messages with Gmail query syntax
- `mcp__claude_ai_Gmail__gmail_read_message` -- Read full message content by ID
- `mcp__claude_ai_Gmail__gmail_read_thread` -- Read an entire email thread
- `mcp__claude_ai_Gmail__gmail_create_draft` -- Create a draft reply
- `mcp__claude_ai_Gmail__gmail_list_drafts` -- List existing drafts
- `mcp__claude_ai_Gmail__gmail_list_labels` -- List Gmail labels
- `mcp__claude_ai_Gmail__gmail_get_profile` -- Get user profile info

## Search Queries to Execute

Run multiple targeted searches to catch all lead types.

```
Query 1 - Form Submissions:
  is:unread subject:(demo OR trial OR "get started" OR "sign up" OR "contact us" OR "request info")

Query 2 - Partnership Inquiries:
  is:unread subject:(partnership OR collaborate OR integration OR "work together" OR referral)

Query 3 - Direct Outreach / RFPs:
  is:unread subject:(proposal OR RFP OR consulting OR engagement OR "looking for" OR "need help")

Query 4 - Warm Referrals:
  is:unread subject:(introduction OR intro OR referral OR "meet" OR "connecting you")

Query 5 - Pricing/Service Inquiries:
  is:unread subject:(pricing OR rates OR "how much" OR services OR scope OR availability)
```

**Time Window:** Default to the last 24 hours. If a different window is specified (e.g., "check the last week"), adjust the `after:` parameter accordingly.

**Deduplication:** Track message IDs across all searches. Process a repeated message ID only once. Assign it to the highest-priority lead category it matched.

## Read and Parse Each Email

For every unique lead email, use `mcp__claude_ai_Gmail__gmail_read_message` to retrieve full content.

Extract these fields:

| Field | Source | Notes |
|---|---|---|
| `sender_name` | From header | Parse "Display Name <email>" format |
| `sender_email` | From header | Normalize to lowercase |
| `sender_domain` | From header | Extract domain from email |
| `subject` | Subject header | Original subject line |
| `received_date` | Date header | ISO 8601 format |
| `body_text` | Message body | Plain text, stripped of signatures and disclaimers |
| `thread_id` | Gmail thread ID | For tracking conversations |
| `message_id` | Gmail message ID | Unique identifier |
| `has_attachments` | Message metadata | Boolean |
| `cc_recipients` | CC header | List of CC'd parties (may indicate stakeholders) |

## Email Parsing Rules

1. **Strip signatures:** Remove everything after common signature delimiters (`--`, `Sent from my iPhone`, `Best regards,` followed by name/title block).
2. **Strip disclaimers:** Remove legal/confidentiality notices at the bottom.
3. **Strip forwarded headers:** If forwarded, extract the original sender info but note it was forwarded.
4. **Preserve formatting intent:** Keep bullet points and numbered lists as structured data.
5. **Handle HTML:** If only an HTML body is available, extract meaningful text content and ignore markup.
