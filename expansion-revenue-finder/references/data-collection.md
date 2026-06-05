# Data Collection Reference

## File patterns to search

```
*.csv, *.json, *.md, *.txt, *.xlsx, *.tsv
```

## Keywords to search for

```
usage, seats, licenses, ARR, MRR, revenue, plan, tier, feature, adoption,
expansion, upsell, cross-sell, renewal, contract, billing, department, team,
growth, headcount, integration, API, module, add-on, premium, enterprise
```

## Data needed per account

### Core Account Data
- Company name and account ID
- Current ARR/MRR and contract terms
- Product(s) and plan/tier
- Contract start date and renewal date
- Licensed seats vs. active seats
- CSM or account owner

### Usage Data
- Feature usage breakdown (which features, how often)
- Usage volume vs. plan limits (API calls, storage, seats, transactions)
- Usage trend over time (growing, flat, declining)
- Power users vs. casual users
- Peak usage patterns

### Product Data
- Current product(s) in use
- Available products/modules not purchased
- Current tier vs. available tiers
- Add-ons or premium features not activated
- Integration capabilities in use vs. available

### Company Context
- Industry and company size
- Recent growth signals (hiring, funding, new offices)
- Organizational structure (departments, teams, business units)
- Known initiatives or strategic priorities
- Competitive products in use alongside yours

### Relationship Data
- Champion and sponsor contacts
- Multi-threading depth (how many contacts across how many departments)
- NPS/CSAT scores
- Support health
- Engagement level with CS team

If no structured data exists, ask the user to describe their accounts. Narrative descriptions are workable, but note the reduced confidence in opportunity scoring.

## Product catalog inputs

Before identifying expansion opportunities, establish what can be sold. Gather from the user or available documentation:

- **Product lines**: Distinct products or platforms that exist
- **Tier structure**: Available tiers (Free, Starter, Pro, Enterprise, etc.) and what differentiates them
- **Modules/Add-ons**: Optional capabilities addable to a base subscription
- **Seat-based pricing**: How pricing scales with user count
- **Usage-based pricing**: Which usage dimensions are metered and billed
- **Professional services**: Implementation, training, consulting, custom development
- **Support tiers**: Standard vs. premium vs. dedicated support offerings
- **Partner/integration ecosystem**: Marketplace, integrations, or partner solutions that generate revenue

If catalog information is unavailable, ask the user to describe their pricing model and expansion levers. At minimum, establish: what can a customer buy more of?
