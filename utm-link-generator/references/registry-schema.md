# Registry Schema and Output Templates

## utm-registry.json Structure

Append all generated links to `utm-registry.json` using this structure:

```json
{
  "version": "1.0",
  "lastUpdated": "2026-04-10T12:00:00Z",
  "namingConventions": {
    "sources": ["google", "linkedin", "facebook", "instagram", "twitter", "email", "newsletter"],
    "mediums": ["cpc", "cpm", "email", "social", "organic", "referral", "video", "retargeting"]
  },
  "campaigns": [
    {
      "name": "q1-2026-product-launch",
      "createdAt": "2026-04-10T12:00:00Z",
      "description": "Q1 2026 product launch campaign",
      "links": [
        {
          "id": "utm-001",
          "url": "https://example.com/pricing?utm_source=linkedin&utm_medium=social&utm_campaign=q1-2026-product-launch&utm_content=organic-post",
          "source": "linkedin",
          "medium": "social",
          "campaign": "q1-2026-product-launch",
          "content": "organic-post",
          "platform": "linkedin",
          "variant": "organic-post",
          "createdAt": "2026-04-10T12:00:00Z",
          "status": "active"
        }
      ]
    }
  ],
  "stats": {
    "totalLinks": 1,
    "totalCampaigns": 1,
    "sourcesUsed": ["linkedin"],
    "mediumsUsed": ["social"]
  }
}
```

## Parameter Validation Report Template

```
## Parameter Validation

- Source: "LinkedIn" -> "linkedin" (normalized to lowercase)
- Medium: "paid" -> "cpc" (corrected to canonical value)
- Campaign: "Q1 Product Launch!" -> "q1-product-launch" (normalized)
- URL: https://example.com/pricing -- Valid
```

## Final Output Summary Template

```
## UTM Links Generated

**Campaign**: q1-2026-product-launch
**Destination**: https://example.com/pricing
**Generated**: 2026-04-10

### Ready-to-Copy Links

| Platform | Variant | Link |
|----------|---------|------|
| LinkedIn (organic) | organic-post | [full URL] |
| LinkedIn (paid) | sponsored-post | [full URL] |
| Email (primary CTA) | primary-cta | [full URL] |
| Email (secondary CTA) | secondary-cta | [full URL] |
| Twitter | default | [full URL] |
| Facebook | default | [full URL] |

### Registry Updated
- New links added: 6
- Total links in registry: 6
- Registry file: ./utm-registry.json

### Validation Report
- All parameters normalized to convention
- No duplicate links found
- No naming conflicts detected
```
