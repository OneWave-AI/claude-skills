# Practical Workflow Implementations

Worked end-to-end examples of common multi-agent workflows.

## Research + Writer Pipeline

Use case: Research a topic and produce a polished article.

```
Step 1: Initialize shared context

Create .a2a-context.json with:
- Register "researcher" agent (capabilities: web_search, summarization)
- Register "writer" agent (capabilities: drafting, editing)
- Register "editor" agent (capabilities: proofreading, fact_checking)
- Create task: { description: "Research and write article on [topic]" }

Step 2: Dispatch Researcher

Use Agent tool:
"You are the Research Agent. Your task:
 1. Read .a2a-context.json for your assignment
 2. Search the web for authoritative sources on [topic]
 3. Compile findings: key facts, statistics, expert quotes, counterarguments
 4. Write your findings to .a2a-context.json under sections.researcher
 5. Create a HANDOFF message for the writer with:
    - task: 'Write a 1500-word article based on my research'
    - context_so_far: [your compiled findings]
    - success_criteria: ['Accurate', 'Engaging', 'Well-structured', 'Cites sources']
 6. Update task status to HANDED_OFF"

Step 3: Dispatch Writer

Use Agent tool:
"You are the Writer Agent. Your task:
 1. Read .a2a-context.json for the HANDOFF from the researcher
 2. Review all research findings in sections.researcher
 3. Draft a compelling article: hook, body sections, conclusion
 4. Write the draft to sections.writer.artifacts
 5. Create a HANDOFF to the editor
 6. Update task chain"

Step 4: Dispatch Editor

Use Agent tool:
"You are the Editor Agent. Your task:
 1. Read the draft from sections.writer.artifacts
 2. Check: factual accuracy, clarity, grammar, flow, tone
 3. Make corrections and improvements
 4. Write the final version to conclusions
 5. Mark task as COMPLETED"

Step 5: Coordinator collects final article from conclusions
```

## Code + Review Workflow

Use case: Write a feature and have it reviewed before merging.

```
Step 1: Initialize context with coder and reviewer agents

Step 2: Dispatch Coder
"You are the Code Agent. Your task:
 1. Read .a2a-context.json for the feature request
 2. Implement the feature following the codebase's patterns
 3. Write tests for your implementation
 4. Log all files modified in the HANDOFF to the reviewer
 5. Include: what you built, design decisions, known limitations"

Step 3: Dispatch Reviewer
"You are the Review Agent. Your task:
 1. Read the HANDOFF from the coder
 2. Review EVERY file listed in files_modified
 3. Check for: security issues, performance problems, code style, test coverage
 4. Write your review as structured feedback:
    - MUST FIX: [blocking issues]
    - SHOULD FIX: [important improvements]
    - NICE TO HAVE: [suggestions]
    - APPROVED: [yes/no]
 5. If not approved, create a HANDOFF back to the coder with specific fix requests"

Step 4: If review fails, iterate (max 3 rounds)

Step 5: Final APPROVED status written to conclusions
```

## Sales + Technical Specialist Handoff

Use case: A sales agent qualifies a lead and routes technical questions to a specialist.

```
Step 1: Register agents
- "sales-agent": capabilities: [lead_qualification, objection_handling, relationship_building]
- "technical-agent": capabilities: [architecture_review, integration_planning, security_assessment]

Step 2: Sales Agent processes the lead
"You are the Sales Agent. Your prospect: [company/person info].
 1. Qualify using BANT framework (Budget, Authority, Need, Timeline)
 2. Identify technical questions you cannot answer
 3. HANDOFF technical questions to the technical agent with:
    - Prospect context and pain points
    - Specific technical questions asked
    - What has been promised so far (be precise -- do not overcommit)
    - Tone and relationship context"

Step 3: Technical Agent provides answers
"You are the Technical Agent. A sales colleague needs technical support.
 1. Read the HANDOFF from sales-agent
 2. Research and answer each technical question with accuracy
 3. Provide: architecture diagrams (as text), integration steps, security considerations
 4. Flag any questions where the answer might be a dealbreaker
 5. RESPONSE back to sales-agent with answers formatted for customer-facing use"

Step 4: Sales Agent incorporates answers and continues the deal
```
