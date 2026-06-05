# Handoff Protocol

Defines structured task handoff, acceptance, rejection, and chain tracking.

## Structured Handoff Message

When transferring ownership of a task, include the full handoff payload:

```json
{
  "type": "HANDOFF",
  "payload": {
    "action": "TRANSFER_TASK",
    "data": {
      "task": "Clear description of what needs to be done",
      "context_so_far": "Summary of all work completed, decisions made, and current state",
      "what_ive_tried": [
        "Approach 1: [description] -- Result: [outcome]",
        "Approach 2: [description] -- Result: [outcome]"
      ],
      "what_you_should_do": [
        "Specific next step 1",
        "Specific next step 2"
      ],
      "success_criteria": [
        "The output should include X",
        "Performance must meet Y threshold",
        "All tests must pass"
      ],
      "files_modified": [
        "/path/to/file1.ts",
        "/path/to/file2.ts"
      ],
      "open_questions": [
        "Should we use approach A or B for the caching layer?"
      ],
      "estimated_effort": "SMALL | MEDIUM | LARGE",
      "deadline": "<ISO 8601 or null>"
    },
    "priority": "HIGH"
  }
}
```

## Handoff Acceptance

The receiving agent must acknowledge with an ACK:

```json
{
  "type": "ACK",
  "payload": {
    "action": "HANDOFF_ACCEPTED",
    "data": {
      "understood_task": "My understanding of the task in my own words",
      "planned_approach": "How I intend to tackle this",
      "estimated_completion": "My estimate for completion",
      "questions_for_sender": ["Any clarifying questions"]
    }
  }
}
```

If the receiving agent cannot handle the task:

```json
{
  "type": "ERROR",
  "payload": {
    "action": "HANDOFF_REJECTED",
    "data": {
      "reason": "Why I cannot accept this handoff",
      "suggestion": "Alternative agent or approach",
      "partial_capability": "What parts I COULD handle"
    }
  }
}
```

## Handoff Chain Tracking

Maintain a `chain` array on every task recording which agents have worked on it:

```json
{
  "task_id": "abc-123",
  "chain": [
    {"agent": "coordinator", "action": "CREATED", "timestamp": "2025-01-15T10:00:00Z"},
    {"agent": "researcher", "action": "WORKED", "timestamp": "2025-01-15T10:05:00Z", "duration_seconds": 120},
    {"agent": "writer", "action": "HANDOFF_RECEIVED", "timestamp": "2025-01-15T10:07:00Z"},
    {"agent": "writer", "action": "WORKED", "timestamp": "2025-01-15T10:15:00Z", "duration_seconds": 480},
    {"agent": "reviewer", "action": "HANDOFF_RECEIVED", "timestamp": "2025-01-15T10:16:00Z"},
    {"agent": "reviewer", "action": "COMPLETED", "timestamp": "2025-01-15T10:20:00Z", "duration_seconds": 240}
  ]
}
```

The chain provides full traceability for:
- Debugging failures (which agent introduced an issue).
- Performance analysis (which stage took longest).
- Quality tracking (which agent's output needed revision).
