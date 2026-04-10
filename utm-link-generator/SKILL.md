---
name: utm-link-generator
description: Generates properly tagged UTM links with consistent naming conventions. Maintains a UTM registry file (utm-registry.json) to enforce naming consistency, prevent duplicates, generate short links, and output ready-to-copy links for LinkedIn, email, social, and ads.
tools: Read, Write, Bash
user_invocable: true
---

# UTM Link Generator

A disciplined UTM link generation system that enforces consistent naming conventions across all campaigns, maintains a registry to prevent duplicates and naming drift, and outputs platform-ready links. This is not a simple URL concatenator -- it is a naming governance system for marketing attribution.

## Why This Exists

UTM chaos is the number one cause of broken marketing attribution. When team members use "linkedin" vs "LinkedIn" vs "linked-in" vs "li" as a source, your analytics become useless. This skill enforces a single source of truth: the UTM registry.

## Capabilities

1. **Generate UTM-tagged URLs** with validated, consistent parameters
2. **Maintain a utm-registry.json** file that tracks all generated links and enforces naming conventions
3. **Prevent duplicates** -- warns when a similar link already exists in the registry
4. **Platform-specific formatting** -- outputs links optimized for LinkedIn, email, social, and ad platforms
5. **Bulk generation** -- create multiple variants for A/B testing or multi-channel campaigns
6. **Validation** -- rejects malformed URLs, empty parameters, and convention violations
7. **Reporting** -- generates campaign tracking summaries from the registry

## UTM Parameter Reference

| Parameter | Required | Purpose | Example |
|-----------|----------|---------|---------|
| `utm_source` | Yes | Where the traffic comes from | `linkedin`, `google`, `newsletter` |
| `utm_medium` | Yes | Marketing medium | `cpc`, `email`, `social`, `organic` |
| `utm_campaign` | Yes | Campaign identifier | `q1-2026-product-launch` |
| `utm_term` | No | Paid keyword (search ads) | `project-management-software` |
| `utm_content` | No | Differentiates similar links | `hero-cta`, `sidebar-banner`, `variant-a` |
| `utm_id` | No | Campaign ID for GA4 | `camp-2026-q1-001` |

## Naming Conventions (Enforced)

These conventions are non-negotiable. The skill will reject or auto-correct any violations.

### General Rules

1. **All lowercase** -- Never `LinkedIn`, always `linkedin`
2. **Hyphens for spaces** -- Never `product launch`, always `product-launch`
3. **No special characters** -- Only alphanumeric and hyphens
4. **No trailing/leading hyphens** -- Never `-campaign-name-`
5. **No double hyphens** -- Never `my--campaign`
6. **Maximum length**: 50 characters per parameter value
7. **Date format in campaigns**: `q[N]-[YYYY]` or `[YYYY]-[MM]` prefix

### Source Values (Canonical List)

Only these source values are allowed. Any new source must be explicitly added to the registry.

| Canonical Source | Aliases (auto-corrected) | Platform |
|-----------------|-------------------------|----------|
| `google` | `goog`, `google-ads`, `adwords` | Google Ads / Organic |
| `linkedin` | `li`, `linked-in`, `linkedin-ads` | LinkedIn |
| `facebook` | `fb`, `meta`, `facebook-ads` | Facebook / Meta |
| `instagram` | `ig`, `insta` | Instagram |
| `twitter` | `x`, `x-com`, `tw` | X (Twitter) |
| `youtube` | `yt`, `you-tube` | YouTube |
| `tiktok` | `tt`, `tik-tok` | TikTok |
| `reddit` | `rd` | Reddit |
| `email` | `mail`, `e-mail`, `em` | Email campaigns |
| `newsletter` | `nl`, `news-letter` | Newsletter specifically |
| `bing` | `microsoft-ads`, `msn` | Bing / Microsoft |
| `direct` | `none`, `(direct)` | Direct traffic |
| `referral` | `ref`, `partner` | Referral traffic |
| `podcast` | `pod`, `spotify` | Podcast channels |
| `slack` | `sl` | Slack communities |
| `producthunt` | `ph`, `product-hunt` | Product Hunt |
| `hackernews` | `hn`, `hacker-news` | Hacker News |

### Medium Values (Canonical List)

| Canonical Medium | Aliases (auto-corrected) | Use Case |
|-----------------|-------------------------|----------|
| `cpc` | `ppc`, `paid-click`, `cost-per-click` | Paid search / paid social clicks |
| `cpm` | `display`, `paid-impression` | Display / impression campaigns |
| `email` | `e-mail`, `mail` | Email campaigns |
| `social` | `social-media`, `organic-social` | Organic social posts |
| `organic` | `seo`, `organic-search` | Organic search traffic |
| `referral` | `ref`, `partner`, `affiliate` | Referral / partner links |
| `video` | `vid`, `youtube`, `pre-roll` | Video ad placements |
| `retargeting` | `remarketing`, `retarget` | Retargeting campaigns |
| `content` | `blog`, `article`, `content-syndication` | Content marketing |
| `webinar` | `web`, `event`, `virtual-event` | Webinar / event registrations |
| `podcast` | `pod`, `audio` | Podcast mentions / ads |
| `sms` | `text`, `mms` | SMS / text campaigns |
| `qr` | `qr-code`, `print` | QR code / print materials |
| `push` | `push-notification`, `notification` | Push notifications |

### Campaign Naming Pattern

Campaigns follow this structure:

```
[quarter-or-month]-[year]-[campaign-name]-[optional-variant]
```

Examples:
- `q1-2026-product-launch`
- `2026-03-spring-webinar`
- `q2-2026-brand-awareness-linkedin`
- `evergreen-demo-request` (for always-on campaigns, skip the date prefix)

## Execution Protocol

### Step 1: Accept Input

The user provides some or all of these:

- **Destination URL** (required) -- The page they want to link to
- **Source** (required) -- Where the traffic comes from
- **Medium** (required) -- The marketing channel type
- **Campaign** (required) -- Campaign name
- **Term** (optional) -- Keyword for paid search
- **Content** (optional) -- Link differentiator
- **Platforms** (optional) -- Which platforms to generate links for (default: all relevant)

If the user provides a brief like "I need links for our Q1 product launch campaign on LinkedIn and email pointing to our pricing page," extract the parameters from natural language.

### Step 2: Validate and Normalize

For each parameter:

1. **Convert to lowercase** -- `LinkedIn` becomes `linkedin`
2. **Replace spaces with hyphens** -- `product launch` becomes `product-launch`
3. **Strip special characters** -- Remove anything not `[a-z0-9-]`
4. **Check against canonical lists** -- Auto-correct known aliases (e.g., `fb` to `facebook`)
5. **Reject unknown values** -- If a source or medium is not in the canonical list and is not a reasonable addition, warn the user and suggest the closest match
6. **Validate URL** -- Ensure the destination URL is well-formed (has protocol, valid domain)
7. **Check length** -- Ensure no parameter exceeds 50 characters

Report any corrections made:
```
## Parameter Validation

- Source: "LinkedIn" -> "linkedin" (normalized to lowercase)
- Medium: "paid" -> "cpc" (corrected to canonical value)
- Campaign: "Q1 Product Launch!" -> "q1-product-launch" (normalized)
- URL: https://example.com/pricing -- Valid
```

### Step 3: Check Registry for Duplicates

Read the utm-registry.json file (or create it if it does not exist). Check for:

1. **Exact duplicates** -- Same URL + same parameters. Warn and return the existing link.
2. **Near duplicates** -- Same URL + same campaign + different content/medium. Warn but allow (this is often intentional for multi-channel tracking).
3. **Naming conflicts** -- Same campaign name but different capitalization or hyphenation. Block and show the existing convention.

### Step 4: Generate Links

Build the UTM-tagged URL:

```
{base_url}?utm_source={source}&utm_medium={medium}&utm_campaign={campaign}[&utm_term={term}][&utm_content={content}][&utm_id={id}]
```

Rules:
- If the base URL already has query parameters, append with `&` not `?`
- URL-encode any parameter values that contain special characters
- Preserve the base URL's existing query parameters and fragment

### Step 5: Generate Platform-Specific Variants

For each platform requested, generate an optimized link:

#### LinkedIn

```
## LinkedIn

**Post Link** (organic social):
https://example.com/pricing?utm_source=linkedin&utm_medium=social&utm_campaign=q1-2026-product-launch&utm_content=organic-post

**Ad Link** (paid):
https://example.com/pricing?utm_source=linkedin&utm_medium=cpc&utm_campaign=q1-2026-product-launch&utm_content=sponsored-post

**Message Link** (InMail/DM):
https://example.com/pricing?utm_source=linkedin&utm_medium=social&utm_campaign=q1-2026-product-launch&utm_content=inmail

**Profile Link** (bio/featured):
https://example.com/pricing?utm_source=linkedin&utm_medium=social&utm_campaign=q1-2026-product-launch&utm_content=profile-link
```

#### Email

```
## Email

**Primary CTA**:
https://example.com/pricing?utm_source=email&utm_medium=email&utm_campaign=q1-2026-product-launch&utm_content=primary-cta

**Secondary CTA**:
https://example.com/pricing?utm_source=email&utm_medium=email&utm_campaign=q1-2026-product-launch&utm_content=secondary-cta

**Header Link**:
https://example.com/pricing?utm_source=email&utm_medium=email&utm_campaign=q1-2026-product-launch&utm_content=header-link

**Footer Link**:
https://example.com/pricing?utm_source=email&utm_medium=email&utm_campaign=q1-2026-product-launch&utm_content=footer-link
```

#### Social (General)

```
## Social

**Twitter/X**:
https://example.com/pricing?utm_source=twitter&utm_medium=social&utm_campaign=q1-2026-product-launch

**Facebook**:
https://example.com/pricing?utm_source=facebook&utm_medium=social&utm_campaign=q1-2026-product-launch

**Instagram** (bio link):
https://example.com/pricing?utm_source=instagram&utm_medium=social&utm_campaign=q1-2026-product-launch&utm_content=bio-link

**Reddit**:
https://example.com/pricing?utm_source=reddit&utm_medium=social&utm_campaign=q1-2026-product-launch
```

#### Ads (Paid)

```
## Paid Ads

**Google Ads**:
https://example.com/pricing?utm_source=google&utm_medium=cpc&utm_campaign=q1-2026-product-launch&utm_term={keyword}

**LinkedIn Ads**:
https://example.com/pricing?utm_source=linkedin&utm_medium=cpc&utm_campaign=q1-2026-product-launch

**Facebook/Meta Ads**:
https://example.com/pricing?utm_source=facebook&utm_medium=cpc&utm_campaign=q1-2026-product-launch

Note: For Google Ads, use {keyword} as a dynamic placeholder that Google will auto-replace.
```

### Step 6: Update Registry

Append all generated links to utm-registry.json:

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

### Step 7: Output Summary

Present the final output in a clean, copy-paste-ready format:

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

## Bulk Generation Mode

For generating links across many campaigns or many URLs at once.

### Input Format (Bulk)

The user can provide a table or list:

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

### Output Format (Bulk)

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

The user can also invoke this skill for registry operations:

### Audit Registry

```
"Audit my UTM registry"
```

Reads utm-registry.json and reports:
- Total campaigns and links
- Naming convention violations (if any crept in manually)
- Stale campaigns (older than 6 months with no new links)
- Unused sources or mediums
- Duplicate or near-duplicate links

### Add Custom Source/Medium

```
"Add 'partnerstack' as a UTM source"
```

Adds the new value to the canonical list in the registry and documents it.

### Campaign Report

```
"Show me all links for the q1-2026-product-launch campaign"
```

Filters the registry and displays all links for that campaign, grouped by platform.

### Export for Google Sheets

```
"Export my UTM registry as CSV"
```

Generates a CSV file with columns: Campaign, URL, Source, Medium, Content, Term, Full Link, Created Date, Status.

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

- **Google Analytics 4**: All parameters map directly to GA4 dimensions. utm_id maps to campaign_id.
- **HubSpot**: Source and medium map to HubSpot's Original Source properties.
- **Salesforce**: Campaign name can map to Salesforce Campaign records via integration.
- **Mixpanel / Amplitude**: UTM params auto-captured on page load via standard SDKs.

## Best Practices Embedded in This Skill

1. **One registry, one truth** -- All UTM links flow through the registry. No ad-hoc link creation.
2. **Convention over configuration** -- Canonical lists prevent naming drift before it starts.
3. **Auto-correction over rejection** -- When possible, fix the input rather than blocking the user.
4. **Platform awareness** -- Different platforms need different utm_content values to distinguish placements.
5. **Date-prefixed campaigns** -- Makes it trivial to filter analytics by time period.
6. **Audit trail** -- Every link is timestamped and attributed in the registry.
