# Agent Registry, Discovery, and Templates

Covers agent registration, capability-based discovery, and ready-to-use agent templates.

## Agent Registration

Register every agent before it participates. Write registration to the `agents` section of `.a2a-context.json`:

```json
{
  "name": "research-agent",
  "role": "Senior Researcher",
  "capabilities": [
    "web_search",
    "document_analysis",
    "fact_verification",
    "source_evaluation",
    "summarization"
  ],
  "tools": ["WebSearch", "WebFetch", "Read", "Grep", "Glob"],
  "specialization": "Finding, verifying, and synthesizing information from multiple sources",
  "accepts_handoffs_from": ["*"],
  "max_concurrent_tasks": 1
}
```

## Capability Discovery

When an agent needs help, query the registry. Example request: "I need an agent that can review code for security vulnerabilities."

Discovery algorithm:

```
1. Parse the request to extract required capabilities
   - Keywords: "review code" -> code_review, "security" -> security_analysis, "vulnerabilities" -> vulnerability_detection
2. Score each registered agent:
   - Exact capability match: +10 points per match
   - Partial match (semantic similarity): +5 points
   - Tool availability: +3 points per relevant tool
   - Agent status IDLE: +5 points (prefer available agents)
   - Agent status WORKING: -5 points (avoid overloading)
3. Return the top-scoring agent(s) with match reasoning
```

Perform discovery via the Agent tool:

> "Read .a2a-context.json and find the best agent to handle this request: [description]. Score agents on capability match, tool availability, and current status. Return the agent name and your reasoning."

## Built-In Agent Templates

Instantiate these templates for common multi-agent workflows.

Research Agent:
```json
{
  "name": "researcher",
  "role": "Information Gatherer",
  "capabilities": ["web_search", "document_analysis", "summarization", "fact_checking"],
  "tools": ["WebSearch", "WebFetch", "Read", "Grep", "Glob"],
  "specialization": "Gathering and synthesizing information from diverse sources"
}
```

Writer Agent:
```json
{
  "name": "writer",
  "role": "Content Creator",
  "capabilities": ["drafting", "editing", "formatting", "tone_adjustment", "structuring"],
  "tools": ["Read", "Write", "Grep"],
  "specialization": "Transforming research and outlines into polished written content"
}
```

Code Agent:
```json
{
  "name": "coder",
  "role": "Software Engineer",
  "capabilities": ["code_generation", "debugging", "refactoring", "testing", "architecture"],
  "tools": ["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
  "specialization": "Writing, debugging, and optimizing code across languages"
}
```

Review Agent:
```json
{
  "name": "reviewer",
  "role": "Quality Assurance",
  "capabilities": ["code_review", "security_analysis", "performance_analysis", "best_practices"],
  "tools": ["Read", "Grep", "Glob", "Bash"],
  "specialization": "Auditing code and content for quality, security, and correctness"
}
```

Coordinator Agent:
```json
{
  "name": "coordinator",
  "role": "Project Manager",
  "capabilities": ["task_decomposition", "delegation", "progress_tracking", "conflict_resolution"],
  "tools": ["Read", "Write", "Agent", "Bash"],
  "specialization": "Breaking down complex tasks and orchestrating agent collaboration"
}
```
