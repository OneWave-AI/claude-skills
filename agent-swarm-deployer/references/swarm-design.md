# Swarm Design: Schemas, Batch Sizing, Swarm Sizing

## Schema Detection and Definition

### Input Schema (from sampled items)

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

### Output Schema (defined by the task)

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

## Calculate Batch Size

The batch size determines how many items each agent processes.

| Factor | Guideline |
|--------|-----------|
| Token budget per item | Input tokens + expected output tokens + instruction overhead |
| Agent context limit | ~200K usable tokens per agent (conservative) |
| Instruction overhead | ~2K tokens for the agent's brief |
| Safety margin | Use 70% of theoretical capacity |

Formula:
```
usable_tokens = 200,000 * 0.70 = 140,000
tokens_per_item = input_tokens + output_tokens + 100 (overhead)
batch_size = floor(usable_tokens / tokens_per_item)
```

Practical limits:
- Minimum batch size: 5 items (agent overhead is not worth it for fewer)
- Maximum batch size: 200 items (beyond this, agent context gets cluttered)
- Sweet spot: 20-80 items per agent for most text processing tasks

## Determine Swarm Size

```
total_items = 1,247
batch_size = 50
swarm_size = ceil(1,247 / 50) = 25 agents
```

Practical limits:
- Maximum parallel agents: 20 per wave (prevents system overload)
- If swarm_size > 20: deploy in waves. Wave 1: agents 1-20. Wave 2: agents 21-25.

## Present Swarm Plan

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

## Scaling Guidelines

| Total Items | Recommended Batch Size | Swarm Size | Waves | Notes |
|-------------|----------------------|------------|-------|-------|
| 10-50 | 10-25 | 2-5 | 1 | Small job, minimal overhead |
| 50-200 | 25-50 | 4-10 | 1 | Standard processing |
| 200-500 | 40-60 | 5-15 | 1 | Moderate scale |
| 500-1000 | 50-80 | 10-20 | 1-2 | Large scale, may need waves |
| 1000-5000 | 50-100 | 20+ | 2-5 | Multi-wave deployment |
| 5000+ | 100-200 | 50+ | 5+ | Enterprise scale, consider chunking |
