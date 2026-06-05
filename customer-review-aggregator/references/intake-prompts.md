# Intake Prompts

## Scope prompt (Step 1)

```
Let me help you aggregate and analyze customer reviews.

Please specify:
1. Your Product/Company: [Name]
2. Platforms to Analyze:
   - [ ] G2
   - [ ] Capterra
   - [ ] Trustpilot
   - [ ] App Store
   - [ ] Google Play
   - [ ] ProductHunt
   - [ ] Reddit
   - [ ] Twitter/X

3. Competitors to Compare (optional): [Names]
4. Analysis Focus:
   - [ ] Overall sentiment trends
   - [ ] Feature-specific feedback
   - [ ] Pain point identification
   - [ ] Marketing claims extraction
   - [ ] Competitive comparison
   - [ ] Feature request analysis

5. Time Period: Last [30/60/90/180] days
```

## Data collection prompt (Step 2)

```
To analyze reviews, I need access to review data. Here are the options:

Option A: Manual Copy/Paste
- Copy reviews from the platforms into a text file and I will analyze the content.

Option B: CSV Export
- Export reviews from platforms (if available) and upload the CSV files.

Option C: URLs
- Provide URLs to review pages and I will use WebFetch to analyze public reviews.

Which method works best for you?
```

## Example use cases

### Use Case 1: Competitive Review Analysis
```
User: "Analyze our G2 reviews vs. Competitor A and Competitor B"
```
Aggregate reviews for all three products, build the competitor comparison table, surface competitor weaknesses, and recommend positioning.
