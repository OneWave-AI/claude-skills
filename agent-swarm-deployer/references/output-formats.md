# Output Formats and Final Summary

Write the final output in the format the user requested.

## CSV Output

```bash
# Write header + all successful results as CSV
# Include a separate failures.csv for failed items
```

## JSON Output

```json
{
  "metadata": {
    "task": "description of what was processed",
    "totalItems": 1247,
    "successfulItems": 1210,
    "failedItems": 22,
    "unrecoverableItems": 15,
    "processingDate": "2026-04-10T12:00:00Z",
    "swarmSize": 25,
    "waves": 2
  },
  "results": [...],
  "failures": [...],
  "summary": {
    "key_patterns": "...",
    "notable_findings": "...",
    "data_quality_notes": "..."
  }
}
```

## Markdown Report

```markdown
# Processing Results: [Task Name]

## Summary
- Processed: 1,247 items
- Success rate: 97%
- Key findings: [aggregated insights]

## Results Table
| Item | Result Field 1 | Result Field 2 | Status |
|------|---------------|----------------|--------|
| ... | ... | ... | ... |

## Failures
| Item | Reason | Attempted Retries |
|------|--------|-------------------|
| ... | ... | ... |
```

## Individual Files

For tasks where each item produces a standalone document (e.g., generating 500 blog post outlines):

```
output/
  001-item-name.md
  002-item-name.md
  ...
  500-item-name.md
  _summary.md
  _failures.md
```

## Final Summary Report

Always end with a comprehensive summary:

```
## Swarm Processing Complete

### Execution Summary
- Task: [description]
- Data source: [source]
- Total items: 1,247
- Swarm size: 25 agents across 2 waves
- Total processing time: ~3 minutes

### Results
- Successful: 1,210 (97.0%)
- Failed (recovered on retry): 22 (1.8%)
- Unrecoverable: 15 (1.2%)
- Output written to: [path]

### Quality Metrics
- Schema compliance: 100% of successful results match output schema
- Average confidence: 0.82
- Items flagged for review: 37 (low confidence < 0.5)

### Patterns Observed
- [Any interesting patterns the swarm noticed across the data]
- [Data quality issues found]
- [Recommendations for future processing]

### Cost
- Agents deployed: 25 (Wave 1) + 1 (retry) = 26
- Estimated tokens consumed: ~1.2M input + ~400K output
```
