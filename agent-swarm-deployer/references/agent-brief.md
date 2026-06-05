# Agent Brief Template and Data Distribution

## Brief Requirements

Each swarm agent receives a self-contained brief that includes:

1. Role: "You are a data processing agent in a swarm of 25. Your job is to process items 51-100."
2. Task description: exactly what to do with each item (the operation).
3. Input data: the actual data items for this batch (embedded in the brief or read from a file range).
4. Output schema: the exact format for results, with a concrete example.
5. Quality rules: validation criteria, edge case handling, what to do with malformed items.
6. Error protocol: "If an item cannot be processed, mark it as failed with a reason. Do not skip items silently."
7. Output format: "Return your results as a JSON array. Each element must match the output schema."

## Brief Template

```
You are swarm-agent-{N}, processing batch {N} of {TOTAL_BATCHES} in a data processing swarm.

## Your Task
{TASK_DESCRIPTION}

## Input Data
You will process the following {BATCH_SIZE} items:

{ITEMS_AS_STRUCTURED_DATA}

## Output Schema
For each item, produce a result matching this schema:
{OUTPUT_SCHEMA_WITH_EXAMPLE}

## Example
Input:
{EXAMPLE_INPUT}

Expected output:
{EXAMPLE_OUTPUT}

## Quality Rules
- {RULE_1}
- {RULE_2}
- {RULE_3}
- Every item MUST appear in your output, even if processing failed.
- For failed items, set processing_status to "failed" and include an error_reason field.

## Error Handling
- Malformed input: Mark as "failed", reason: "malformed input: {description}"
- Ambiguous data: Make your best judgment, set confidence to < 0.5
- Missing required field: Mark as "skipped", reason: "missing {field}"

## Output Format
Return a JSON object with this structure:
{
  "agentId": "swarm-agent-{N}",
  "batchRange": "{START}-{END}",
  "totalProcessed": {NUMBER},
  "totalSuccess": {NUMBER},
  "totalFailed": {NUMBER},
  "totalSkipped": {NUMBER},
  "results": [
    {OUTPUT_SCHEMA_ITEM_1},
    {OUTPUT_SCHEMA_ITEM_2},
    ...
  ],
  "errors": [
    {"itemIndex": N, "reason": "description"}
  ],
  "notes": "Any observations about the data quality or patterns"
}
```

## Data Distribution

Choose a distribution method based on the data source:

| Source Type | Distribution Method |
|-------------|-------------------|
| Directory of files | Tell each agent which file paths to Read |
| Single large CSV | Pre-split into batch files using Bash, tell each agent its file |
| Single JSON array | Pre-split into batch files using Bash |
| Inline data | Embed directly in the agent brief (for small datasets) |
| Database export | Export to CSV first, then split |

For CSVs and large files, pre-split before deploying:

```bash
# Split a CSV into batches of 50 rows (preserving header)
head -1 data.csv > header.csv
tail -n +2 data.csv | split -l 50 - batch_
for f in batch_*; do cat header.csv "$f" > "batches/${f}.csv" && rm "$f"; done
rm header.csv
```

## Progress Tracking

As agents complete, report progress:

```
## Swarm Progress

Wave 1 (20 agents):
[################----] 16/20 complete

| Agent | Status | Processed | Success | Failed | Duration |
|-------|--------|-----------|---------|--------|----------|
| swarm-01 | DONE | 50 | 48 | 2 | 45s |
| swarm-02 | DONE | 50 | 50 | 0 | 38s |
| swarm-03 | RUNNING | -- | -- | -- | -- |
| ... | ... | ... | ... | ... | ... |

Cumulative: 800/1247 items processed (64%)
```
