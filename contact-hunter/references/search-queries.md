# Search Query Templates

Use these query patterns once search parameters (name, company, title, location, domain) are gathered. Replace bracketed values.

## Per-target search brief

Format the search plan as follows for a single target (example: John Smith, VP of Engineering, Acme Corp, San Francisco):

### Search parameters
- Target: John Smith
- Company: Acme Corp
- Title: VP of Engineering
- Location: San Francisco, CA

### Recommended queries

LinkedIn:
1. Search: "John Smith VP Engineering Acme Corp"
2. Apply company filter: "Acme Corp"
3. Apply title filter: "VP of Engineering"
4. Apply location: "San Francisco Bay Area"

Google:
1. "John Smith" "VP of Engineering" "Acme Corp"
2. "John Smith" "Acme Corp" email
3. site:linkedin.com/in "John Smith" "Acme"
4. site:acme.com "John Smith"

Company website:
1. https://acme.com/about
2. https://acme.com/team
3. https://acme.com/leadership
4. https://acme.com/contact

Email pattern candidates at acme.com:
- john.smith@acme.com
- john@acme.com
- jsmith@acme.com
- j.smith@acme.com
- smithj@acme.com

GitHub (technical roles):
- Search: "John Smith Acme"
- Inspect bio for company affiliation

## Reusable query patterns

For company employees:
```
site:linkedin.com/in "[Company Name]"
OR
site:[company-domain.com] "team" OR "about" OR "leadership"
```

For specific roles:
```
"[Job Title]" "[Company]" email
OR
"[Job Title]" site:linkedin.com "[Company]"
```

For email validation:
- Check company website for email format
- Use an email verification service
- Look for the pattern in existing confirmed emails
- Test with email finder tools

For phone numbers:
- Company website contact page
- LinkedIn profile (when public)
- Professional directories
- Industry associations
