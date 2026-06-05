# A2A Protocol Specification

Defines the message format, message types, message lifecycle, shared context file, and concurrency safeguards for the Agent-to-Agent protocol.

## Message Format

Conform every inter-agent message to this schema:

```json
{
  "id": "<uuid>",
  "from": "<agent_name>",
  "to": "<agent_name | '*' for broadcast>",
  "type": "REQUEST | RESPONSE | HANDOFF | BROADCAST | QUERY | ACK | ERROR",
  "timestamp": "<ISO 8601>",
  "conversation_id": "<uuid linking related messages>",
  "parent_message_id": "<id of message this responds to, or null>",
  "payload": {
    "action": "<what is being requested or reported>",
    "data": {},
    "priority": "LOW | NORMAL | HIGH | CRITICAL"
  },
  "context": {
    "task_id": "<uuid>",
    "chain": ["<ordered list of agents who have touched this task>"],
    "shared_refs": ["<keys into shared context>"]
  },
  "metadata": {
    "ttl_seconds": 300,
    "retry_count": 0,
    "max_retries": 3
  }
}
```

## Message Types

| Type        | Direction     | Purpose                                                      |
|-------------|---------------|--------------------------------------------------------------|
| `REQUEST`   | A -> B        | Ask agent B to perform a task and return results             |
| `RESPONSE`  | B -> A        | Return results for a prior REQUEST                           |
| `HANDOFF`   | A -> B        | Transfer full ownership of a task to agent B                 |
| `BROADCAST` | A -> *        | Inform all registered agents of something                    |
| `QUERY`     | A -> B        | Ask for information without delegating work                  |
| `ACK`       | B -> A        | Acknowledge receipt of a message (especially HANDOFF)        |
| `ERROR`     | B -> A        | Report failure to complete a REQUEST or HANDOFF              |

## Message Lifecycle

```
REQUEST  -->  ACK  -->  [processing]  -->  RESPONSE
REQUEST  -->  ACK  -->  [processing]  -->  ERROR
HANDOFF  -->  ACK  -->  [agent B takes over]
QUERY    -->  RESPONSE (lightweight, no ownership transfer)
BROADCAST --> [no response expected, agents act on it if relevant]
```

## Shared Context File: `.a2a-context.json`

Treat this file at the project root (or specified working directory) as the single source of truth. All agents read from and write to it.

```json
{
  "version": "1.0.0",
  "created_at": "<ISO 8601>",
  "last_modified": "<ISO 8601>",
  "last_modified_by": "<agent_name>",
  "lock": null,
  "agents": {
    "<agent_name>": {
      "role": "<string>",
      "capabilities": ["<list>"],
      "tools": ["<list>"],
      "status": "IDLE | WORKING | BLOCKED | COMPLETED | FAILED",
      "registered_at": "<ISO 8601>",
      "last_active": "<ISO 8601>"
    }
  },
  "tasks": {
    "<task_id>": {
      "description": "<string>",
      "status": "PENDING | IN_PROGRESS | BLOCKED | COMPLETED | FAILED | HANDED_OFF",
      "assigned_to": "<agent_name>",
      "created_by": "<agent_name>",
      "created_at": "<ISO 8601>",
      "updated_at": "<ISO 8601>",
      "chain": ["<agent_name>"],
      "result": null,
      "error": null
    }
  },
  "sections": {
    "<agent_name>": {
      "findings": [],
      "notes": "",
      "artifacts": []
    }
  },
  "conclusions": {
    "summary": "",
    "decisions": [],
    "open_questions": [],
    "next_steps": []
  },
  "message_log": []
}
```

## Atomic Read-Modify-Write

Follow this procedure to prevent concurrent write corruption:

```
1. READ the full .a2a-context.json
2. CHECK the `lock` field:
   - If null, proceed
   - If locked by another agent AND lock is < 30 seconds old, WAIT and retry (up to 3 times)
   - If locked by another agent AND lock is > 30 seconds old, BREAK the lock (stale lock recovery)
3. ACQUIRE lock: set `lock` to { "agent": "<your_name>", "acquired_at": "<ISO 8601>" }
4. WRITE the updated file with your changes
5. RELEASE lock: set `lock` back to null
6. WRITE the final file
```

Read with `cat .a2a-context.json`, then modify in memory and write the complete file via the Write tool in a single operation. Because Claude Code agents execute sequentially rather than truly concurrently, treat the lock mechanism primarily as a protocol safeguard for future multi-process scenarios. In practice, agents coordinate through the Agent tool's sequential dispatch.

## Context Size Management

When `.a2a-context.json` exceeds 50KB:

1. Summarize completed task results (replace verbose data with summaries).
2. Archive the full message_log to `.a2a-context-archive-<timestamp>.json`.
3. Keep only the last 20 messages in the active log.
4. Compress agent sections: keep only current findings, archive historical data.

Run summarization via the Agent tool:

> "Read .a2a-context.json. The file is too large. Summarize all completed task results to 2-3 sentences each. Archive the message log. Preserve all active tasks, agent registrations, and conclusions. Write the compressed version back."
