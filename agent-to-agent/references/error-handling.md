# Error Handling

Recovery procedures for timeouts, rejections, deadlocks, and failures.

## Agent Timeout

If an agent does not produce a result within the expected timeframe:

```
1. The Agent tool has its own timeout (Claude Code manages this)
2. If the spawned agent times out, the coordinator receives an error
3. Recovery procedure:
   a. Log the timeout in .a2a-context.json message_log
   b. Read any partial results the agent may have written to shared context
   c. OPTION A: Retry the same agent with a simplified task
   d. OPTION B: Route to a different agent
   e. OPTION C: Break the task into smaller pieces
4. Maximum 3 retries per task before escalating to the user
```

## Task Rejection

An agent may decline a task if it lacks the required capabilities:

```json
{
  "type": "ERROR",
  "payload": {
    "action": "TASK_REJECTED",
    "data": {
      "reason": "I don't have access to the WebSearch tool needed for this task",
      "required_capabilities": ["web_search"],
      "my_capabilities": ["code_generation", "debugging"],
      "suggested_agent": "researcher"
    }
  }
}
```

Coordinator response to rejection:
1. Log the rejection.
2. Query the registry for an agent with the missing capabilities.
3. Reroute the task.
4. If no suitable agent exists, report to the user.

## Deadlock Detection

Deadlock occurs when two or more agents are waiting on each other.

Detection algorithm:

```
1. Read all tasks in .a2a-context.json
2. Build a dependency graph:
   - For each task with status IN_PROGRESS, check if it's blocked waiting for another task
   - For each BLOCKED task, check what it's waiting for
3. Detect cycles in the dependency graph
4. If cycle found:
   a. Log the deadlock with involved agents and tasks
   b. BREAK the cycle by:
      - Picking the lowest-priority task in the cycle
      - Cancelling it and informing its agent
      - The cancelled agent writes partial results and releases
   c. Notify the coordinator for re-planning
```

Deadlock prevention rules:
- Never let an agent wait on a response from an agent that is waiting on it.
- Give all QUERY messages a TTL; if no response by TTL, proceed without it.
- Have the Coordinator review the task dependency graph before dispatching.

## Graceful Degradation

When an agent fails entirely:

```
1. Log the failure with error details
2. Save any partial results from the failed agent's context section
3. Assess impact:
   a. Was this a critical-path task? (blocks other tasks)
   b. Was this a parallel task? (other agents can compensate)
4. Recovery options:
   a. RETRY: Spawn a new instance of the same agent type
   b. REROUTE: Assign to a different agent with overlapping capabilities
   c. SIMPLIFY: Reduce task scope and retry
   d. ESCALATE: Inform the user that this subtask could not be completed
   e. SKIP: Mark as skipped and proceed (for non-critical tasks)
5. Update .a2a-context.json with the recovery action taken
```

## Error Escalation Matrix

| Severity | Condition                        | Action                              |
|----------|----------------------------------|-------------------------------------|
| LOW      | Agent timeout, first occurrence   | Retry with same agent               |
| MEDIUM   | Agent timeout, second occurrence  | Reroute to different agent          |
| HIGH     | Agent rejection                   | Find alternative agent or simplify  |
| HIGH     | Agent produces invalid output     | Retry with clearer instructions     |
| CRITICAL | Deadlock detected                 | Break cycle, re-plan                |
| CRITICAL | All retries exhausted             | Escalate to user                    |
| CRITICAL | Shared context corruption         | Restore from archive, restart       |
