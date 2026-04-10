---
name: agent-swarm-deployer
description: Deploys swarms of sub-agents for massive parallel data processing tasks. Unlike agent-army (which is for code changes), this is for DATA tasks -- processing 1000 documents, analyzing datasets, bulk content generation. Configurable swarm size, task distribution, result aggregation, progress tracking, and error recovery.
tools: Read, Write, Bash, Agent, Glob, Grep
user_invocable: true
---

# Agent Swarm Deployer

A high-throughput parallel data processing framework that deploys swarms of sub-agents to handle massive data tasks. While Agent Army is built for code changes (edit files, respect dependency graphs, verify builds), Agent Swarm is built for data operations where individual units of work are independent and results need aggregation.

## Agent Army vs Agent Swarm

| Dimension | Agent Army | Agent Swarm |
|-----------|-----------|-------------|
| **Purpose** | Code changes across files | Data processing at scale |
| **Units of work** | Files in a codebase | Documents, records, rows, items |
| **Dependencies** | Import graph matters | Items are independent |
| **Output** | Modified source files | Aggregated results (reports, datasets, content) |
| **Verification** | Build check, pattern scan | Result validation, completeness check |
| **Error handling** | Fix and re-verify code | Retry failed items, collect partial results |
| **Typical scale** | 10-200 files | 100-10,000+ items |
| **Key risk** | Breaking the build | Data loss, incomplete processing |

## Use Cases

### Document Processing
- Analyze 500 customer support tickets for sentiment and categorization
- Extract key information from 200 legal contracts
- Summarize 1000 research paper abstracts
- Parse 300 resumes for qualification matching

### Dataset Analysis
- Score and rank 2000 leads by ICP fit
- Classify 5000 product reviews by topic and sentiment
- Audit 1000 blog posts for SEO compliance
- Grade 500 sales call transcripts against a methodology

### Bulk Content Generation
- Generate personalized email first lines for 500 prospects
- Create product descriptions for 1000 SKUs
- Write social media posts for 200 blog articles
- Generate meta descriptions for 800 web pages

### Data Transformation
- Convert 1000 CSV rows into structured JSON objects
- Normalize 500 address records
- Translate 300 support articles into 5 languages
- Reformat 2000 database records from schema A to schema B

## Architecture

```
You (Commander)
 |
 |-- Phase 1: Intake & Inventory
 |    |-- Count total items
 |    |-- Sample items for schema detection
 |    |-- Estimate token budget per item
 |
 |-- Phase 2: Swarm Design
 |    |-- Calculate optimal batch size
 |    |-- Determine number of swarm agents
 |    |-- Define result schema
 |
 |-- Phase 3: Deploy Swarm (parallel)
 |    |-- Agent S1: items 1-50      ---\
 |    |-- Agent S2: items 51-100     ---|
 |    |-- Agent S3: items 101-150    ---|-- All run in parallel
 |    |-- Agent S4: items 151-200    ---|
 |    |-- ...                       ---/
 |
 |-- Phase 4: Collect & Aggregate
 |    |-- Gather all agent results
 |    |-- Merge into unified output
 |    |-- Identify failures
 |
 |-- Phase 5: Recovery (if needed)
 |    |-- Retry failed items
 |    |-- Fill gaps
 |
 |-- Phase 6: Deliver
 |    |-- Write final output
 |    |-- Generate summary report
```

## Execution Protocol

### Step 0: Understand the Task

Before deploying any agents, fully understand what the user needs:

1. **Data source** -- Where is the data? Files on disk? A CSV? A directory of documents? Inline in the conversation?
2. **Operation** -- What should be done to each item? Summarize? Classify? Extract? Transform? Generate?
3. **Output format** -- What should the result look like? JSON? CSV? Markdown? Individual files?
4. **Output destination** -- Where should results go? Single file? Directory of files? Returned in conversation?
5. **Quality requirements** -- Are there validation rules? Schemas? Scoring criteria?

If any of these are ambiguous, ask the user before proceeding. Getting the spec wrong wastes all agent compute.

### Step 1: Intake and Inventory

#### 1a. Discover and Count Items

Locate all data items and count them:

```
Glob/Bash: Find all files matching the pattern
Read: Sample first 3-5 items to understand structure
Bash: Count total items (wc -l for CSVs, file count for directories, etc.)
```

Report:
```
## Intake Report
- Data source: /path/to/data/ (or inline, or CSV)
- Total items found: 1,247
- Item format: JSON files, avg 2KB each
- Sample item structure: { name, email, company, title, linkedin_url }
- Estimated tokens per item: ~500
- Total estimated tokens: ~623,500
```

#### 1b. Detect Schema

From the sample items, define the input schema:

```json
{
  "inputSchema": {
    "type": "object",
    "fields": {
      "name": "string",
      "email": "string",
      "company": "string",
      "title": "string",
      "linkedin_url": "string"
    }
  }
}
```

#### 1c. Define Output Schema

Based on the task, define what each processed item should look like:

```json
{
  "outputSchema": {
    "type": "object",
    "fields": {
      "name": "string (from input)",
      "company": "string (from input)",
      "personalized_first_line": "string (generated, 1-2 sentences)",
      "pain_point_guess": "string (inferred from title + company)",
      "confidence": "number (0-1)",
      "processing_status": "enum: success | failed | skipped"
    }
  }
}
```

### Step 2: Swarm Design

#### 2a. Calculate Batch Size

The batch size determines how many items each agent processes. Factors:

| Factor | Guideline |
|--------|-----------|
| **Token budget per item** | Input tokens + expected output tokens + instruction overhead |
| **Agent context limit** | ~200K usable tokens per agent (conservative, leaves room for instructions) |
| **Instruction overhead** | ~2K tokens for the agent's brief |
| **Safety margin** | Use 70% of theoretical capacity |

Formula:
```
usable_tokens = 200,000 * 0.70 = 140,000
tokens_per_item = input_tokens + output_tokens + 100 (overhead)
batch_size = floor(usable_tokens / tokens_per_item)
```

Practical limits:
- **Minimum batch size**: 5 items (agent overhead is not worth it for fewer)
- **Maximum batch size**: 200 items (beyond this, agent context gets cluttered)
- **Sweet spot**: 20-80 items per agent for most text processing tasks

#### 2b. Determine Swarm Size

```
total_items = 1,247
batch_size = 50
swarm_size = ceil(1,247 / 50) = 25 agents
```

Practical limits:
- **Maximum parallel agents**: 20 per wave (prevents system overload)
- **If swarm_size > 20**: Deploy in waves. Wave 1: agents 1-20. Wave 2: agents 21-25.

#### 2c. Present Swarm Plan

```
## Swarm Plan

- Total items: 1,247
- Batch size: 50 items per agent
- Swarm size: 25 agents
- Waves: 2 (Wave 1: 20 agents, Wave 2: 5 agents)
- Estimated processing: All items covered
- Output format: Single CSV file with all results

### Agent Assignments
| Agent | Items | Range | Notes |
|-------|-------|-------|-------|
| swarm-01 | 50 | items 1-50 | -- |
| swarm-02 | 50 | items 51-100 | -- |
| ... | ... | ... | -- |
| swarm-25 | 47 | items 1201-1247 | Partial batch |

Proceed? (Y to deploy / N to adjust batch size)
```

### Step 3: Prepare Agent Briefs

Each swarm agent receives a self-contained brief. The brief must include:

1. **Role**: "You are a data processing agent in a swarm of 25. Your job is to process items 51-100."
2. **Task description**: Exactly what to do with each item (the operation).
3. **Input data**: The actual data items for this batch (embedded in the brief or read from a file range).
4. **Output schema**: The exact format for results. Include a concrete example.
5. **Quality rules**: Validation criteria, edge case handling, what to do with malformed items.
6. **Error protocol**: "If an item cannot be processed, mark it as failed with a reason. Do not skip items silently."
7. **Output format**: "Return your results as a JSON array. Each element must match the output schema."

### Agent Brief Template

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

### Step 4: Deploy Swarm

#### 4a. Wave Deployment

Deploy agents in waves to manage system load:

**Wave 1**: Launch up to 20 agents in parallel using the Agent tool with `run_in_background: true`. Send ALL agent calls in a single message.

```
Launch swarm-agent-01 through swarm-agent-20 in parallel.
Each receives its batch of items and the standardized brief.
```

**Wave 2+ (if needed)**: After Wave 1 completes, launch remaining agents.

#### 4b. Data Distribution

How to get data to each agent depends on the data source:

| Source Type | Distribution Method |
|-------------|-------------------|
| **Directory of files** | Tell each agent which file paths to Read |
| **Single large CSV** | Pre-split into batch files using Bash, tell each agent its file |
| **Single JSON array** | Pre-split into batch files using Bash |
| **Inline data** | Embed directly in the agent brief (for small datasets) |
| **Database export** | Export to CSV first, then split |

For CSVs and large files, pre-split before deploying:

```bash
# Split a CSV into batches of 50 rows (preserving header)
head -1 data.csv > header.csv
tail -n +2 data.csv | split -l 50 - batch_
for f in batch_*; do cat header.csv "$f" > "batches/${f}.csv" && rm "$f"; done
rm header.csv
```

#### 4c. Progress Tracking

As agents complete, track progress:

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

### Step 5: Collect and Aggregate Results

#### 5a. Gather Agent Outputs

As each agent completes, collect its JSON output. Parse and validate:

1. **Schema validation** -- Does each result match the output schema?
2. **Completeness check** -- Does the agent's result count match its batch size?
3. **Duplicate detection** -- Check for duplicate item IDs across agents.
4. **Error extraction** -- Pull out all failed/skipped items for the retry queue.

#### 5b. Merge Results

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

#### 5c. Validate Completeness

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

### Step 6: Error Recovery

#### 6a. Retry Queue

Collect all failed and skipped items into a retry batch:

```
Retry batch: 49 items (34 failed + 15 skipped)
Retry strategy: Single agent with enhanced instructions
```

#### 6b. Enhanced Retry Brief

The retry agent gets special instructions:

```
You are the retry agent. These items failed or were skipped in the first pass.
For each item, I am providing the original item AND the failure reason from the first attempt.

Your job:
1. Try harder -- use more creative interpretation for ambiguous items
2. For truly malformed items, extract whatever you can and note what is missing
3. For items that failed due to missing fields, infer the field if possible or mark as "unrecoverable"

The bar is lower for retries: partial results are better than no results.
```

#### 6c. Retry Limits

- **Maximum retries**: 2 (original attempt + 2 retries = 3 total attempts)
- **After max retries**: Mark item as "unrecoverable" and include in the final report
- **Unrecoverable threshold**: If > 10% of items are unrecoverable, flag to the user for manual review

### Step 7: Write Final Output

Based on the user's requested output format:

#### CSV Output
```bash
# Write header + all successful results as CSV
# Include a separate failures.csv for failed items
```

#### JSON Output
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

#### Markdown Report
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

#### Individual Files
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

### Step 8: Summary Report

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

## Swarm Configurations for Common Tasks

### Sentiment Analysis (1000 reviews)

```yaml
task: Classify each review as positive/negative/neutral with confidence score
batch_size: 100  # Reviews are short, pack more per agent
swarm_size: 10
output_schema:
  review_id: string
  sentiment: enum(positive, negative, neutral, mixed)
  confidence: float(0-1)
  key_phrases: string[]
  summary: string(1 sentence)
```

### Lead Scoring (2000 contacts)

```yaml
task: Score each lead 1-100 based on ICP fit criteria
batch_size: 40  # Each lead needs more analysis context
swarm_size: 50
waves: 3
output_schema:
  lead_id: string
  score: int(1-100)
  icp_match: object
    company_size: bool
    industry: bool
    tech_stack: bool
    title_seniority: bool
  buying_signals: string[]
  recommended_action: enum(hot, warm, nurture, disqualify)
```

### Content Generation (500 product descriptions)

```yaml
task: Write a 100-word product description from product data
batch_size: 25  # Output is longer, needs more generation tokens
swarm_size: 20
output_schema:
  product_id: string
  title: string
  description: string(100 words)
  key_features: string[3]
  seo_keywords: string[5]
```

### Document Summarization (300 papers)

```yaml
task: Summarize each paper in 3 bullet points with key findings
batch_size: 15  # Papers are long, fewer per agent
swarm_size: 20
output_schema:
  paper_id: string
  title: string
  summary_bullets: string[3]
  key_finding: string
  methodology: string
  relevance_score: float(0-1)
```

## Error Handling

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

## Scaling Guidelines

| Total Items | Recommended Batch Size | Swarm Size | Waves | Notes |
|-------------|----------------------|------------|-------|-------|
| 10-50 | 10-25 | 2-5 | 1 | Small job, minimal overhead |
| 50-200 | 25-50 | 4-10 | 1 | Standard processing |
| 200-500 | 40-60 | 5-15 | 1 | Moderate scale |
| 500-1000 | 50-80 | 10-20 | 1-2 | Large scale, may need waves |
| 1000-5000 | 50-100 | 20+ | 2-5 | Multi-wave deployment |
| 5000+ | 100-200 | 50+ | 5+ | Enterprise scale, consider chunking |

## Anti-Patterns to Avoid

1. **Do not use swarm for sequential tasks** -- If item N depends on the result of item N-1, a swarm is the wrong tool. Use a chain instead.
2. **Do not deploy 100 agents for 100 items** -- One item per agent wastes overhead. Batch them.
3. **Do not skip the schema definition** -- Without a schema, merging results from 25 agents becomes a nightmare.
4. **Do not ignore failures** -- Even at 99% success rate, 1% of 10,000 items is 100 failures. Always run retries.
5. **Do not deploy without a sample run** -- Process 5 items manually first to validate the task definition and output quality before scaling.
