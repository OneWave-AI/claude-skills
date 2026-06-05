# Lead Data Extraction

For each email, extract the lead profile below using the body, subject, sender info, and contextual clues.

## Lead Profile Schema

```json
{
  "contact": {
    "name": "string -- full name of the person reaching out",
    "email": "string -- sender email address",
    "phone": "string|null -- phone number if mentioned in email or signature",
    "role": "string|null -- job title or role if mentioned",
    "linkedin": "string|null -- LinkedIn URL if included in signature"
  },
  "company": {
    "name": "string|null -- company name from domain, signature, or email body",
    "domain": "string -- extracted from email domain",
    "size_estimate": "string|null -- startup/smb/midmarket/enterprise based on clues",
    "industry": "string|null -- industry if determinable from context"
  },
  "inquiry": {
    "type": "string -- one of: demo_request, partnership, rfp, referral, pricing_inquiry, general_inquiry, support_question",
    "summary": "string -- 1-2 sentence summary of what they need",
    "specific_services": ["string -- list of specific services or capabilities mentioned"],
    "pain_points": ["string -- specific problems or challenges mentioned"],
    "timeline": "string|null -- any timeline or deadline mentioned",
    "budget_signals": "string|null -- any budget or pricing context mentioned"
  },
  "metadata": {
    "source": "string -- gmail",
    "source_detail": "string -- which search query matched",
    "message_id": "string",
    "thread_id": "string",
    "received_date": "string -- ISO 8601",
    "forwarded_by": "string|null -- if this was a forwarded intro",
    "cc_stakeholders": ["string -- CC'd email addresses that may be stakeholders"]
  }
}
```

## Extraction Guidelines

- **Company name:** First check the email domain (ignore generic domains like gmail.com, yahoo.com, outlook.com, hotmail.com). Then the email signature. Then the body text.
- **Role/Title:** Check the email signature block first. Then check if they mention their role in the body ("I'm the CTO at..." or "As head of marketing...").
- **Company size:** Infer from signals -- domain recognition, language used ("our team of 5" vs "our enterprise"), email signature complexity, presence of standardized disclaimers.
- **Industry:** Infer from company name, domain, services mentioned, or explicit industry references.
- **Timeline:** Look for explicit dates, relative time references ("next quarter", "by end of month", "ASAP", "exploring for 2026"), or urgency language.
- **Budget signals:** Look for references to budget, pricing expectations, "allocated budget", "looking to spend", or comparison to existing vendor costs.

## Handling Ambiguous or Incomplete Data

1. Set the field to `null` rather than guessing.
2. Add a note in the `extraction_notes` field explaining what is missing.
3. Flag the lead for manual review if critical fields (name, company, what they need) are missing.
4. For generic email domains (gmail, yahoo, etc.), flag that company identification requires manual lookup.
