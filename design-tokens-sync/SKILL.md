---
name: design-tokens-sync
description: Audit and sync design tokens between the source of truth (tokens.json, Figma variables export) and the code that should consume them (Tailwind config, CSS custom properties, theme files). Finds drift -- hardcoded values, orphan tokens, out-of-date copies -- and fixes it in the right direction.
tools: Read, Glob, Grep, Write, Edit, Bash
model: inherit
---

# Design Tokens Sync

Keep one source of truth actually true. Every design system decays the same way: a hex gets hardcoded in a hurry, a token gets renamed in Figma but not in Tailwind, a second half-copy of the palette appears in a one-off CSS file. This skill finds the drift, decides direction with the user, and reconciles.

## Workflow

1. **Locate the truths.** Find every place tokens are defined: `tokens.json`/`*.tokens.json` (W3C format), Figma variables export, `tailwind.config.*` theme, CSS custom properties, TS theme objects, SCSS variable files. If more than one claims to be canonical, ask which wins before touching anything -- direction of sync is a human decision.
2. **Build the graph.** For each token: canonical value, every downstream definition, and every consumption site. For each raw value in code (hex, px, rem, ms, cubic-bezier): whether a token exists for it.
3. **Drift report.** Output `token-drift-report.md` in four buckets:
   - `STALE COPIES` -- downstream definitions that no longer match canonical (with both values)
   - `HARDCODED` -- raw values in components where a matching token exists (exact match, then near-match within perceptual distance for colors)
   - `ORPHANS` -- tokens defined but consumed nowhere
   - `UNTOKENIZED` -- raw values appearing 3+ times with no token; these are tokens waiting to be named
4. **Reconcile on approval.** Stale copies: regenerate downstream from canonical. Hardcoded: replace with token references -- exact matches automatically, near-matches only with per-case confirmation (that slightly-off blue might be intentional). Untokenized: propose names following the existing convention and add to canonical. Orphans: list for deletion; never auto-delete.
5. **Guard.** Offer to add the cheap tripwire: a script (`npm run tokens:check`) that re-runs the drift detection and fails CI on new stale copies or hardcoded near-matches, so the system stays synced after you leave.

## Rules

- Never sync both directions in one run. Canonical wins; anything flowing the other way (a designer wants the code's newer value) is an explicit canonical edit first.
- Near-match replacement is per-case, never bulk. `#0B1121` vs `#0b1220` may be drift or may be a decision.
- Preserve semantic layering: if the system has `color.blue.500 -> color.accent -> button.bg`, fix references at the right layer instead of flattening everything to primitives.
- Renames propagate everywhere or nowhere -- a half-renamed token is worse than the old name.
- Respect generated files: if `theme.css` is built from `tokens.json`, fix the source and rebuild; never hand-edit output.
- The report quantifies health: token coverage percentage (tokenized vs. raw values in components) is the number to move release over release.

## Quick Commands

- "Audit my tokens" -- steps 1-3, report only
- "Sync from [source]" -- full reconciliation with the named canonical
- "What's hardcoded?" -- the HARDCODED bucket only
- "Add the CI guard" -- step 5 standalone
