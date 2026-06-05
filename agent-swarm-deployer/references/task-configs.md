# Swarm Configurations for Common Tasks

## Sentiment Analysis (1000 reviews)

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

## Lead Scoring (2000 contacts)

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

## Content Generation (500 product descriptions)

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

## Document Summarization (300 papers)

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
