# Overview: Swarm vs Army, Use Cases, Architecture

## Agent Army vs Agent Swarm

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

## Architecture

```
Commander (you)
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
