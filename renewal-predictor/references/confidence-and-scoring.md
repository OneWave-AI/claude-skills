# Confidence Calibration and Missing-Data Scoring

## Composite Score Calculation

```
Health Score = (Engagement * 0.20) + (Support * 0.15) + (Adoption * 0.20) +
              (NPS_CSAT * 0.10) + (Billing * 0.10) + (Stakeholder * 0.10) +
              (Usage * 0.15)
```

Round to the nearest whole number.

### Scoring Thresholds

| Health Score Range | Prediction Category | Confidence Guidance |
|---|---|---|
| 80-100 | Likely to Renew | High confidence when 5+ dimensions score above 75 |
| 60-79 | Neutral / Monitor | Medium confidence; flag dimensions below 50 for targeted intervention |
| 40-59 | At Risk | High confidence when 3+ dimensions score below 50 |
| 0-39 | Likely to Churn | High confidence when usage trend is negative and engagement is declining |

## Confidence Calibration

Every prediction must include a confidence level. Confidence is determined by two factors: the quality of available data and the consistency of signals across dimensions.

High Confidence (80-100%):
- Data is available for 6+ of the 7 dimensions
- Signals are consistent (all pointing in the same direction)
- Trailing data covers 90+ days
- At least one direct human signal (survey response, meeting notes, email sentiment)

Medium Confidence (50-79%):
- Data is available for 4-5 of the 7 dimensions
- Signals are mostly consistent with 1-2 conflicting indicators
- Trailing data covers 30-90 days
- Human signals are indirect or absent

Low Confidence (below 50%):
- Data is available for 3 or fewer dimensions
- Signals are mixed or contradictory
- Trailing data covers less than 30 days
- No direct human signals available

### Adjustments

- If the account is less than 90 days old, cap confidence at Medium regardless of signal consistency. There is not enough history to predict with high confidence.
- If the account is in a known seasonal industry, adjust usage trend scores for seasonality before computing the health score.
- If a critical data source is missing (no NPS data, no support tickets logged, no usage analytics), note it as a data gap and reduce confidence by one level.

## Scoring When Data Is Missing

When data for a dimension is unavailable:

1. Check if indirect signals exist (e.g., no NPS data but QBR notes mention satisfaction levels).
2. If indirect signals exist, score conservatively (cap at 60 for that dimension) and note the inference.
3. If no data exists at all, score the dimension at 50 (neutral) and flag it as a data gap.
4. Reduce overall confidence level by one tier for every 2 dimensions with missing data.
5. Never score a dimension at 0 unless there is affirmative evidence of a problem -- absence of data is not evidence of a problem.

## Edge Cases

- New clients (less than 90 days): Score based on onboarding completion and early engagement signals. Use onboarding health as a proxy for feature adoption. Cap confidence at Medium regardless of signal consistency.
- Multi-product clients: Score each product relationship separately, then roll up to an account-level composite. Note which product line carries the most risk.
- Channel or partner-managed clients: Note that direct signal access may be limited. Weight partner feedback and escalations more heavily. Flag as a data quality limitation.
- Enterprise accounts with long sales cycles: Renewal conversations may start 6-12 months early. Adjust "days until renewal" urgency thresholds accordingly.
- Seasonal businesses: Adjust usage trend scoring for known seasonal patterns before computing health scores. A 30% dip in retail usage during Q1 may be normal, not alarming.
- Recently acquired companies: Treat as high-uncertainty accounts. Stakeholder continuity is likely disrupted. Cap confidence at Low until new organizational structure stabilizes.
