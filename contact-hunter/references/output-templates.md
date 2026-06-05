# Output Templates

Fill these once contact data is found. Cite every source and note verification date.

## Data collection template

```
Full Name: [First Last]
Job Title: [Exact title]
Company: [Company name]
Email: [email@domain.com]
Phone: [(xxx) xxx-xxxx]
LinkedIn: [linkedin.com/in/username]
Location: [City, State/Country]
Department: [Engineering, Sales, etc.]

Additional Info:
- Reports to: [Manager name]
- Team size: [Number]
- Start date: [When they joined]
- Previous companies: [List]
- Education: [Degree, School]

Data Sources:
- [LinkedIn profile URL]
- [Company website URL]
- [Other sources]
```

## Individual contact card

```
+-------------------------------------------+
| JOHN SMITH                                |
| VP of Engineering @ Acme Corp             |
+-------------------------------------------+
| Email:    john.smith@acme.com             |
| Phone:    (415) 555-0123                  |
| LinkedIn: linkedin.com/in/johnsmith       |
| Location: San Francisco, CA               |
+-------------------------------------------+
| Department: Engineering                   |
| Reports to: Sarah Chen (CTO)              |
| Team size:  ~45 engineers                 |
| Tenure:     2+ years at Acme              |
+-------------------------------------------+
| Sources:                                  |
| - LinkedIn (verified)                     |
| - Company website                         |
| - Verified: 2024-01-15                    |
+-------------------------------------------+
```

## Bulk results (CSV)

```csv
Name,Title,Company,Email,Phone,LinkedIn,Location,Source,Verified
John Smith,VP Engineering,Acme Corp,john.smith@acme.com,(415) 555-0123,linkedin.com/in/johnsmith,San Francisco,LinkedIn,2024-01-15
Jane Doe,Director Marketing,Acme Corp,jane.doe@acme.com,(415) 555-0124,linkedin.com/in/janedoe,San Francisco,Company Website,2024-01-15
```

## Email pattern report

```
DETECTED EMAIL PATTERN: Acme Corp

Confirmed emails found:
- john.smith@acme.com
- sarah.chen@acme.com
- michael.jones@acme.com

Detected pattern: firstname.lastname@acme.com
Confidence: 95%

Alternative patterns (if primary fails):
- firstname@acme.com
- firstnamelastname@acme.com
- f.lastname@acme.com

To verify an unknown email:
1. Use an email verification tool
2. Check for bounce/invalid response
3. Inspect SMTP response
4. Cross-check on LinkedIn
```

## Export formats

- CSV: for generic CRM import
- JSON: for API integration
- vCard: for contact managers
- Salesforce CSV: pre-formatted for SFDC
- HubSpot CSV: pre-formatted for HubSpot
