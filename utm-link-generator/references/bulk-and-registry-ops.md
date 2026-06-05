# Bulk Generation and Registry Management

## Bulk Generation Mode

For generating links across many campaigns or many URLs at once.

### Input Format

Accept a table or list:

```
Generate UTM links for these pages:
- /pricing -- linkedin, email, twitter -- q1-2026-product-launch
- /demo -- linkedin, google-ads -- q1-2026-demo-push
- /case-studies -- email, linkedin -- q1-2026-social-proof
```

### Processing

1. Parse each line into (URL, platforms, campaign)
2. Validate and normalize all parameters
3. Generate all variant links for each URL/platform combination
4. Deduplicate across the batch
5. Update registry with all new links
6. Output a master table

### Output Format

```
## Bulk UTM Generation -- 3 campaigns, 8 platform variants, 24 total links

| Campaign | URL | Platform | Variant | Full Link |
|----------|-----|----------|---------|-----------|
| q1-2026-product-launch | /pricing | linkedin-organic | organic-post | [URL] |
| q1-2026-product-launch | /pricing | linkedin-paid | sponsored-post | [URL] |
| q1-2026-product-launch | /pricing | email | primary-cta | [URL] |
| ... | ... | ... | ... | ... |

Registry updated: 24 new links added.
```

## Registry Management Commands

### Audit Registry

Trigger: "Audit my UTM registry"

Read `utm-registry.json` and report:
- Total campaigns and links
- Naming convention violations (if any crept in manually)
- Stale campaigns (older than 6 months with no new links)
- Unused sources or mediums
- Duplicate or near-duplicate links

### Add Custom Source/Medium

Trigger: "Add 'partnerstack' as a UTM source"

Add the new value to the canonical list in the registry and document it.

### Campaign Report

Trigger: "Show me all links for the q1-2026-product-launch campaign"

Filter the registry and display all links for that campaign, grouped by platform.

### Export for Google Sheets

Trigger: "Export my UTM registry as CSV"

Generate a CSV file with columns: Campaign, URL, Source, Medium, Content, Term, Full Link, Created Date, Status.

## Error Handling

| Error | Response |
|-------|----------|
| Invalid URL (no protocol) | Auto-prepend `https://` and warn |
| Unknown source | Suggest closest canonical match, ask for confirmation |
| Unknown medium | Suggest closest canonical match, ask for confirmation |
| Campaign name too long | Suggest abbreviated version |
| Duplicate link exists | Show existing link, ask if user wants to create anyway |
| Registry file missing | Create new registry with default conventions |
| Registry file corrupted | Attempt to parse what exists, back up, create fresh |
| Base URL has existing UTMs | Strip existing UTM params, warn user, apply new ones |

## Integration Notes

- Google Analytics 4: All parameters map directly to GA4 dimensions. `utm_id` maps to `campaign_id`.
- HubSpot: Source and medium map to HubSpot's Original Source properties.
- Salesforce: Campaign name can map to Salesforce Campaign records via integration.
- Mixpanel / Amplitude: UTM params auto-captured on page load via standard SDKs.

## Best Practices Embedded in This Skill

1. One registry, one truth -- all UTM links flow through the registry. No ad-hoc link creation.
2. Convention over configuration -- canonical lists prevent naming drift before it starts.
3. Auto-correction over rejection -- when possible, fix the input rather than blocking the user.
4. Platform awareness -- different platforms need different `utm_content` values to distinguish placements.
5. Date-prefixed campaigns -- makes it trivial to filter analytics by time period.
6. Audit trail -- every link is timestamped and attributed in the registry.
