# Agent Army vs Agent Swarm

Use Agent Army for code changes; use Agent Swarm for data processing at scale.

| Dimension | Agent Army | Agent Swarm |
|-----------|-----------|-------------|
| Purpose | Code changes across files | Data processing at scale |
| Units of work | Files in a codebase | Documents, records, rows, items |
| Dependencies | Import graph matters | Items are independent |
| Output | Modified source files | Aggregated results (reports, datasets, content) |
| Verification | Build check, pattern scan | Result validation, completeness check |
| Error handling | Fix and re-verify code | Retry failed items, collect partial results |
| Typical scale | 10-200 files | 100-10,000+ items |
| Key risk | Breaking the build | Data loss, incomplete processing |

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

## Anti-Patterns to Avoid

1. Do not use a swarm for sequential tasks. If item N depends on the result of item N-1, use a chain instead.
2. Do not deploy one agent per item. Batch items; one item per agent wastes overhead.
3. Do not skip the schema definition. Without a schema, merging results from many agents becomes unmanageable.
4. Do not ignore failures. Even at 99% success, 1% of 10,000 items is 100 failures. Always run retries.
5. Do not deploy without a sample run. Process 5 items manually first to validate the task definition and output quality before scaling.
