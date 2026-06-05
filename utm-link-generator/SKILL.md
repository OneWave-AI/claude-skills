---
name: utm-link-generator
description: Generates properly tagged UTM links with consistent naming conventions. Maintains a UTM registry file (utm-registry.json) to enforce naming consistency, prevent duplicates, generate short links, and output ready-to-copy links for LinkedIn, email, social, and ads.
tools: Read, Write, Bash
user_invocable: true
---

# UTM Link Generator

Generate UTM-tagged links under a single naming-governance system: a `utm-registry.json` that enforces canonical conventions, prevents duplicates and naming drift, and outputs platform-ready links for LinkedIn, email, social, and ads.

## Contents

- `references/naming-conventions.md` -- enforced rules, UTM parameter reference, canonical source/medium lists, campaign naming pattern.
- `references/platform-variants.md` -- per-platform link templates (LinkedIn, email, social, paid ads).
- `references/registry-schema.md` -- utm-registry.json structure plus validation-report and output-summary templates.
- `references/bulk-and-registry-ops.md` -- bulk generation, registry commands (audit/add/report/export), error handling, integrations, best practices.

## Capabilities

1. Generate UTM-tagged URLs with validated, consistent parameters.
2. Maintain `utm-registry.json` tracking all links and enforcing conventions.
3. Prevent duplicates -- warn when a similar link already exists.
4. Format platform-specific variants (LinkedIn, email, social, ads).
5. Bulk-generate variants for A/B testing or multi-channel campaigns.
6. Validate -- reject malformed URLs, empty parameters, and convention violations.
7. Report -- generate campaign tracking summaries from the registry.

## Workflow

1. **Accept input.** Collect destination URL, source, medium, campaign (all required) plus optional term, content, and target platforms. Extract these from a natural-language brief when not given explicitly.
2. **Validate and normalize.** Lowercase, replace spaces with hyphens, strip non-`[a-z0-9-]` characters, auto-correct known aliases, reject unknown source/medium values (suggest closest match), validate URL form, enforce the 50-character limit. Report corrections using the template in `references/registry-schema.md`. Full rules in `references/naming-conventions.md`.
3. **Check registry for duplicates.** Read `utm-registry.json` (create if missing). Return existing link on exact duplicates, allow-with-warning on near duplicates, block on naming conflicts (same campaign, different casing/hyphenation).
4. **Generate links.** Build `{base_url}?utm_source=&utm_medium=&utm_campaign=[&utm_term=][&utm_content=][&utm_id=]`. Append with `&` if the base URL already has query params, URL-encode values, and preserve existing query params and fragment.
5. **Generate platform variants.** Produce optimized links per requested platform using `references/platform-variants.md`.
6. **Update registry.** Append all generated links to `utm-registry.json` per the schema in `references/registry-schema.md`, refreshing stats and timestamps.
7. **Output summary.** Present a copy-paste-ready summary using the template in `references/registry-schema.md`.

For bulk runs, registry commands (audit, add source/medium, campaign report, CSV export), error handling, and integration notes, see `references/bulk-and-registry-ops.md`.
