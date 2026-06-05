# Aggregation, Recovery, and Error Handling

## Gather Agent Outputs

As each agent completes, collect its JSON output, then parse and validate:

1. Schema validation: does each result match the output schema?
2. Completeness check: does the agent's result count match its batch size?
3. Duplicate detection: check for duplicate item IDs across agents.
4. Error extraction: pull out all failed/skipped items for the retry queue.

## Merge Results

Combine all agent results into a single unified output:

```python
# Conceptual merge logic
merged_results = []
failed_items = []
skipped_items = []

for agent_output in all_agent_outputs:
    for result in agent_output["results"]:
        if result["processing_status"] == "success":
            merged_results.append(result)
        elif result["processing_status"] == "failed":
            failed_items.append(result)
        elif result["processing_status"] == "skipped":
            skipped_items.append(result)

# Sort by original item order
merged_results.sort(key=lambda x: x["original_index"])
```

## Validate Completeness

```
## Aggregation Report

- Total items in input: 1,247
- Total results received: 1,247
- Successful: 1,198 (96.1%)
- Failed: 34 (2.7%)
- Skipped: 15 (1.2%)

### Coverage Check
- Items with results: 1,247 / 1,247 (100% coverage)
- Missing items: 0
- Duplicate results: 0

### Failure Analysis
| Failure Reason | Count |
|---------------|-------|
| Malformed input | 12 |
| Missing required field | 8 |
| Ambiguous data | 14 |

Proceed to retry failed items? (Y / skip / manual review)
```

## Error Recovery

### Retry Queue

Collect all failed and skipped items into a retry batch:

```
Retry batch: 49 items (34 failed + 15 skipped)
Retry strategy: Single agent with enhanced instructions
```

### Enhanced Retry Brief

```
You are the retry agent. These items failed or were skipped in the first pass.
For each item, I am providing the original item AND the failure reason from the first attempt.

Your job:
1. Try harder -- use more creative interpretation for ambiguous items
2. For truly malformed items, extract whatever you can and note what is missing
3. For items that failed due to missing fields, infer the field if possible or mark as "unrecoverable"

The bar is lower for retries: partial results are better than no results.
```

### Retry Limits

- Maximum retries: 2 (original attempt + 2 retries = 3 total attempts)
- After max retries: mark item as "unrecoverable" and include in the final report
- Unrecoverable threshold: if > 10% of items are unrecoverable, flag to the user for manual review

## Error Handling Reference

| Error | Cause | Response |
|-------|-------|----------|
| Agent returns no output | Agent timeout or crash | Re-deploy that batch with a fresh agent |
| Agent returns partial results | Context overflow or mid-processing failure | Identify processed items, re-deploy unprocessed items |
| Agent returns malformed JSON | Output parsing failure | Attempt to extract results from raw text, re-deploy if impossible |
| Duplicate results across agents | Batch overlap miscalculation | Deduplicate by item ID, keep first occurrence |
| All agents fail | Systemic issue (bad brief, impossible task) | Abort, report to user, suggest task reformulation |
| Retry agent also fails | Item is truly unprocessable | Mark as unrecoverable, include raw input in failure report |
| Data source unavailable | File missing, permission denied | Abort before deploying swarm, report to user |
| Output file write fails | Disk space, permissions | Attempt alternative location, or return results in conversation |
