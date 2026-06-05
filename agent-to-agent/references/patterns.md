# Communication Patterns

Five coordination patterns for multi-agent collaboration. Select the pattern that fits the task structure.

## Request/Response

The simplest pattern. Agent A asks Agent B to do something and waits for the result.

```
Agent A                          Agent B
  |                                |
  |--- REQUEST (do X) ----------->|
  |                                |--- ACK
  |                                |--- [works on X]
  |<-- RESPONSE (result of X) ----|
  |                                |
```

Implementation:

```
1. Agent A writes a REQUEST to .a2a-context.json message_log
2. Agent A spawns Agent B via the Agent tool with instructions:
   "You are [Agent B role]. Read .a2a-context.json for the latest REQUEST addressed to you.
    Execute the requested action. Write your RESPONSE to the message_log.
    Update your agent section with findings."
3. Agent A reads the updated .a2a-context.json to get the RESPONSE
4. Agent A proceeds with the result
```

## Pipeline

Sequential processing where each agent transforms the output and passes it forward.

```
Agent A -----> Agent B -----> Agent C -----> Final Result
(research)    (draft)        (review)
```

Implementation:

```
1. Coordinator decomposes task into pipeline stages
2. For each stage:
   a. Write a HANDOFF message to the next agent
   b. Spawn the next agent via Agent tool
   c. Agent reads context, performs work, writes results
   d. Agent writes HANDOFF to next stage (or RESPONSE if final)
3. Coordinator collects final result from .a2a-context.json
```

Example pipeline prompt for the Coordinator:

> "Orchestrate a 3-stage pipeline:
>  Stage 1 (researcher): Search the web for [topic], compile findings into .a2a-context.json
>  Stage 2 (writer): Read researcher's findings, draft a blog post, write to .a2a-context.json
>  Stage 3 (reviewer): Read the draft, provide feedback, write final version
>  Execute each stage sequentially. After all stages complete, compile the final output."

## Fan-Out / Fan-In

Parallel execution where multiple agents work simultaneously, and results are collected.

```
              +--> Agent B (subtask 1) --+
              |                          |
Agent A ------+--> Agent C (subtask 2) --+-----> Agent A (merge)
              |                          |
              +--> Agent D (subtask 3) --+
```

Implementation:

```
1. Coordinator decomposes task into independent subtasks
2. For EACH subtask, spawn a separate Agent:
   - Each agent gets: task description, shared context reference, output location
   - Each agent writes results to its own section in .a2a-context.json
3. After ALL agents complete, Coordinator reads all sections
4. Coordinator merges results into conclusions section
```

To achieve parallelism, dispatch multiple Agent tool calls in a single response. Each agent runs in its own context:

```
[Agent call 1]: "You are researcher-alpha. Investigate [subtopic A]. Write findings to .a2a-context.json under sections.researcher-alpha."
[Agent call 2]: "You are researcher-beta. Investigate [subtopic B]. Write findings to .a2a-context.json under sections.researcher-beta."
[Agent call 3]: "You are researcher-gamma. Investigate [subtopic C]. Write findings to .a2a-context.json under sections.researcher-gamma."
```

After all three return, read `.a2a-context.json` and merge.

## Conversation (Multi-Turn Dialogue)

Two agents engage in a structured back-and-forth to solve a problem collaboratively.

```
Agent A                          Agent B
  |                                |
  |--- "I think we should..." --->|
  |<-- "Good point, but..." ------|
  |--- "What about..." ---------->|
  |<-- "That works. Let's go" ----|
  |                                |
  [Consensus reached]
```

Implementation:

```
1. Initialize a conversation_id in .a2a-context.json
2. Set max_turns (default: 6) to prevent infinite loops
3. Agent A writes opening message (type: QUERY)
4. Spawn Agent B to read and respond
5. Read Agent B's response, spawn Agent A to continue
6. Repeat until:
   - An agent writes a message with payload.action = "CONSENSUS_REACHED"
   - max_turns is exhausted
   - An agent writes an ERROR
7. Coordinator extracts the conclusion from the final messages
```

Conversation rules:
- Each turn must advance the discussion (no repeating previous points).
- Agents must explicitly state agreement or disagreement.
- If max_turns is reached without consensus, escalate to a supervisor or the user.

## Supervisor Pattern

One agent monitors and redirects others. The supervisor coordinates and does not do the work itself.

```
              Supervisor
             /    |    \
            /     |     \
        Agent A  Agent B  Agent C
```

Supervisor responsibilities:

1. Decompose the task into subtasks.
2. Assign each subtask to the best-matched agent (via discovery).
3. Monitor progress by reading .a2a-context.json periodically.
4. Redirect if an agent is stuck (reassign to a different agent or provide guidance).
5. Merge results when all subtasks complete.
6. Report the final outcome.

Supervisor prompt template:

> "You are the Supervisor agent. Your task: [high-level goal].
>
> Protocol:
> 1. Read .a2a-context.json to see registered agents and their capabilities
> 2. Decompose the task into subtasks (write them to the tasks section)
> 3. Assign each subtask to the best agent
> 4. Spawn each agent with clear instructions
> 5. After agents complete, read their results
> 6. If any agent failed or produced low-quality results, reassign or provide feedback
> 7. Merge all results into the conclusions section
> 8. Write the final summary
>
> You must NOT do the work yourself. Delegate everything."
