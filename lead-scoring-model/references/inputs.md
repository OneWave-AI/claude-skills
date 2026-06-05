# Inputs and Analysis Process

## Inputs

Request the following inputs. Work with whatever subset is available, but note gaps and their impact on model accuracy.

## Required Inputs

1. **ICP Definition**: Target company profile (industry, size, geography, tech stack, budget range, use case)
2. **Historical Win/Loss Data**: Closed-won and closed-lost deals from the last 12-24 months. Minimum 50 closed deals for statistical relevance; 200+ preferred. Fields needed:
   - Company name, industry, employee count, revenue range
   - Lead source, initial engagement type
   - Deal size, sales cycle length, outcome (won/lost)
   - Loss reason (if lost)
   - Number of touches, stakeholders involved
3. **CRM Export of Current Leads/Opportunities**: The leads to be scored or the pipeline to validate the model against

## Highly Recommended Inputs

4. **Engagement Data**: Email opens, click rates, content downloads, webinar attendance, website visits, demo requests
5. **Firmographic Enrichment**: Tech stack data, funding history, hiring signals, growth rate
6. **Sales Activity Logs**: Call notes, meeting counts, response times, multi-threading depth

## Optional Inputs

7. **Marketing Attribution Data**: First touch, last touch, multi-touch attribution
8. **Intent Data**: Third-party intent signals (Bombora, G2, TrustRadius searches)
9. **Competitive Intelligence**: Which competitors appeared in won vs. lost deals

## Analysis Process

Follow this sequence rigorously. Do not skip steps.

### Step 1: Data Audit

- Inventory all fields available across the provided data
- Identify missing fields and their impact on model completeness
- Check data quality: completeness rates, obvious errors, duplicates
- Flag any survivorship bias (e.g., only seeing leads that made it to opportunity stage)
- Determine sample size adequacy for each dimension
- Document data limitations clearly

### Step 2: Win/Loss Pattern Analysis

- Calculate base conversion rate (closed-won / total closed)
- For each candidate attribute, calculate:
  - Conversion rate when attribute is present vs. absent
  - Lift over base rate (the core metric for assigning points)
  - Statistical significance (chi-square or proportion z-test)
  - Sample size for this attribute
- Rank all attributes by predictive power (lift x statistical confidence)
- Identify interaction effects (e.g., "enterprise + inbound" converts 3x better than either alone)
- Document which attributes do NOT correlate with winning (these are often surprising)

### Step 3: Dimension Construction

- Group correlated attributes into scoring dimensions:
  - **Firmographic Fit**: Company characteristics that match ICP
  - **Behavioral Signals**: Actions the lead has taken
  - **Engagement Depth**: Frequency and recency of interactions
  - **Intent Indicators**: Signals of active buying process
  - **Negative Signals**: Attributes that correlate with losing (subtract points)
- Assign point values proportional to measured lift
- Ensure dimensions are not double-counting the same underlying signal
- Set maximum points per dimension to prevent any single factor from dominating

### Step 4: Threshold Calibration

- Plot score distribution for historical won deals and lost deals
- Find the score thresholds that maximize separation between won and lost
- Define buckets: Hot, Warm, Cool, Cold
- For each bucket, calculate:
  - Expected conversion rate
  - Recommended SLA (response time, channel, rep tier)
  - Volume (what percentage of leads fall in each bucket)
- Ensure Hot bucket is small enough that reps can actually work every lead in it
- Ensure Cold bucket is large enough to meaningfully reduce wasted rep time

### Step 5: Validation

- Hold out 20-30% of historical data for validation (do not use for model building)
- Score holdout deals with the model
- Calculate accuracy metrics: precision, recall, F1 for each threshold
- Compare model ranking to actual outcomes
- Identify false positives (high score, lost deal) and false negatives (low score, won deal)
- Analyze what the model missed in each case
- Iterate if validation reveals problems

### Step 6: Implementation Planning

- Map each scoring signal to a specific CRM field
- Define automation rules (lead assignment, alerts, stage changes)
- Specify data collection requirements for signals not currently tracked
- Create rep-facing documentation (what the score means, how to use it)
- Define recalibration schedule and process

## Batch Scoring Mode

When the user provides a CSV or list of current leads and asks to score them against an existing model:

1. **Load the Model**: Read the `lead-scoring-model.md` file to get current point values and thresholds.
2. **Map Fields**: Match the lead data fields to scoring signals. Note any unmappable fields.
3. **Score Each Lead**: Apply point values for each dimension. Calculate dimension subtotals and total.
4. **Assign Tiers**: Apply threshold definitions to assign Hot/Warm/Cool/Cold.
5. **Generate Output**: Produce the Section 7 tables (see output-template.md) with all scored leads ranked by total score.
6. **Flag Gaps**: For each lead, note which scoring signals could not be evaluated due to missing data and the potential score impact.
7. **Recommend Actions**: For Hot and Warm leads, provide specific next steps. For Cool leads, specify which nurture track. For Cold leads, recommend deprioritize or remove.

## Best Practices

1. **Demand Data**: Do not build a scoring model on vibes. If the user lacks historical win/loss data, help them set up tracking first and revisit in 90 days.
2. **Show Your Work**: Every point value should have a visible rationale. If a signal gets 15 points, surface the underlying lift calculation.
3. **Start Conservative**: It is better to under-score and miss a few Hot leads than to over-score and drown reps in false positives. Reps lose trust fast.
4. **Test Before Deploying**: Always insist on holdout validation before the model goes live. No exceptions.
5. **Plan for Decay**: Markets change, products evolve, buyer behavior shifts. A model built today will be wrong in 6 months without recalibration.
6. **Keep It Implementable**: If a signal cannot be reliably captured in the CRM, it does not belong in the model. Theoretical accuracy is worthless without operational data.
7. **Align With Sales**: The model must make sense to reps. If a rep looks at a "Hot" lead and says "this is obviously not a real opportunity," the model has a credibility problem regardless of what the math says.

## Trigger Phrases and Example

**Trigger Phrases**:
- "Build a lead scoring model for my business"
- "Score these leads against our ICP"
- "Which of my leads should I prioritize?"
- "Our lead scoring is broken, help me fix it"
- "Create a scoring rubric for our sales team"
- "Analyze our win/loss data to find patterns"

**Example Request**:
> "We sell HR software to mid-market companies (200-2000 employees). I have a CSV of 180 closed deals from the last year -- 62 won, 118 lost. I also have 340 current leads I need to prioritize. Build me a scoring model and then score the current leads."

The goal is not a perfect model. The goal is a model that is materially better than whatever the team is doing today -- even if "today" is just gut feel -- and that improves over time through disciplined recalibration.
