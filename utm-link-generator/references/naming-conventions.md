# Naming Conventions (Enforced)

These conventions are non-negotiable. Reject or auto-correct any violations.

## General Rules

1. All lowercase -- never `LinkedIn`, always `linkedin`
2. Hyphens for spaces -- never `product launch`, always `product-launch`
3. No special characters -- only alphanumeric and hyphens
4. No trailing/leading hyphens -- never `-campaign-name-`
5. No double hyphens -- never `my--campaign`
6. Maximum length: 50 characters per parameter value
7. Date format in campaigns: `q[N]-[YYYY]` or `[YYYY]-[MM]` prefix

## UTM Parameter Reference

| Parameter | Required | Purpose | Example |
|-----------|----------|---------|---------|
| `utm_source` | Yes | Where the traffic comes from | `linkedin`, `google`, `newsletter` |
| `utm_medium` | Yes | Marketing medium | `cpc`, `email`, `social`, `organic` |
| `utm_campaign` | Yes | Campaign identifier | `q1-2026-product-launch` |
| `utm_term` | No | Paid keyword (search ads) | `project-management-software` |
| `utm_content` | No | Differentiates similar links | `hero-cta`, `sidebar-banner`, `variant-a` |
| `utm_id` | No | Campaign ID for GA4 | `camp-2026-q1-001` |

## Source Values (Canonical List)

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

## Medium Values (Canonical List)

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

## Campaign Naming Pattern

Campaigns follow this structure:

```
[quarter-or-month]-[year]-[campaign-name]-[optional-variant]
```

Examples:
- `q1-2026-product-launch`
- `2026-03-spring-webinar`
- `q2-2026-brand-awareness-linkedin`
- `evergreen-demo-request` (for always-on campaigns, skip the date prefix)
