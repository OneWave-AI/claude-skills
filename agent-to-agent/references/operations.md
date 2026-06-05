# Operations: Commands, Best Practices, Monitoring, Security

Reference for coordination commands, best practices, observability, and security boundaries.

## Coordination Commands

The user or a supervisor agent can issue these high-level commands:

| Command                          | Action                                                     |
|----------------------------------|------------------------------------------------------------|
| `register <agent_spec>`          | Add a new agent to the registry                            |
| `assign <task> to <agent>`       | Create a task and assign it                                |
| `handoff <task> from <A> to <B>` | Transfer task ownership                                    |
| `status`                         | Show all agents, tasks, and current state                  |
| `broadcast <message>`            | Send a message to all agents                               |
| `query <agent> <question>`       | Ask an agent a question without delegating                 |
| `pipeline <A> -> <B> -> <C>`     | Set up a sequential pipeline                               |
| `fan-out <task> to <A,B,C>`      | Distribute subtasks in parallel                            |
| `converge`                       | Merge all agent findings into conclusions                  |
| `reset`                          | Clear all state and start fresh                            |
| `archive`                        | Archive current context and start clean                    |

## Best Practices

### Task Decomposition

- Break tasks into pieces where each piece can be completed by one agent independently.
- Give each subtask clear inputs, outputs, and success criteria.
- Prefer pipeline over fan-out when order matters.
- Prefer fan-out over pipeline when tasks are independent.

### Context Discipline

- Write findings incrementally, not all at the end.
- Include a timestamp on every write to shared context.
- Keep sections self-contained (another agent should understand a section without external context).
- Keep the conclusions section as the canonical current state of truth.

### Handoff Quality

- A handoff is only as good as its context_so_far field.
- Always include what was tried and what failed to save the receiving agent from repeating work.
- Make success criteria measurable, not vague.
- When handing off due to failure, be explicit about what went wrong.

### Agent Prompt Engineering

Structure prompts spawned via the Agent tool as:

```
1. IDENTITY: "You are [Agent Name], a [Role]."
2. CONTEXT: "Read .a2a-context.json at [path] for your assignment."
3. TASK: Clear, specific instructions for what to do.
4. OUTPUT: "Write your results to [specific location in shared context]."
5. PROTOCOL: "Follow the A2A protocol: update your status, log messages, track your chain entry."
6. CONSTRAINTS: Any limitations, deadlines, or scope boundaries.
```

### Avoiding Common Failures

| Failure Mode                 | Prevention                                                |
|------------------------------|-----------------------------------------------------------|
| Agent ignores shared context | Always include "Read .a2a-context.json first" in prompts  |
| Agent overwrites others' data| Each agent writes ONLY to its own section                 |
| Infinite agent loops         | Set max_turns for conversations, max_retries for tasks    |
| Bloated context file         | Run summarization when file exceeds 50KB                  |
| Lost handoff context         | Require all HANDOFF messages to include context_so_far    |
| Silent failures              | Require ERROR messages for all failures, never fail silently |

## Monitoring and Observability

### Status Report

Generate a status report at any time by reading `.a2a-context.json`:

```
A2A Status Report
=================
Agents:   3 registered, 2 active, 1 idle
Tasks:    5 total, 2 completed, 2 in-progress, 1 pending
Messages: 12 in log
Chain:    coordinator -> researcher -> writer (current)

Active Tasks:
  [task-001] "Research competitors" - IN_PROGRESS (researcher) - 3m elapsed
  [task-002] "Draft comparison table" - PENDING (writer) - waiting on task-001

Recent Messages:
  10:05 researcher -> coordinator: RESPONSE "Found 8 competitor profiles"
  10:03 coordinator -> researcher: REQUEST "Research top 10 competitors in [space]"
```

### Performance Metrics

Track across tasks:
- Time per stage: how long each agent takes.
- Handoff quality: how often receiving agents ask clarifying questions (fewer is better).
- Retry rate: how often tasks need to be retried.
- Error rate: how often agents fail.
- Chain length: average number of agents touching a task.

## Security and Boundaries

### Agent Isolation

- Restrict agents to reading and writing only their own section and the shared conclusions.
- Prevent any agent from modifying another agent's registration.
- Allow only the Coordinator to modify task assignments.

### Sensitive Data

- Never write secrets, API keys, or credentials to `.a2a-context.json`.
- For tasks involving sensitive data, pass it through the Agent tool's prompt (in-memory) rather than the shared file.
- Add `.a2a-context.json` to `.gitignore`.

### Scope Boundaries

- Keep agents within their declared capabilities.
- When an agent discovers it needs capabilities it does not have, have it REQUEST help or HANDOFF, never attempt to use tools it was not given.
- Have the Coordinator enforce scope by checking agent declarations before assigning tasks.

## Initialization Detail

### Context File Template

Create `.a2a-context.json` with this template:

```json
{
  "version": "1.0.0",
  "created_at": "<now>",
  "last_modified": "<now>",
  "last_modified_by": "coordinator",
  "lock": null,
  "agents": {},
  "tasks": {},
  "sections": {},
  "conclusions": {
    "summary": "",
    "decisions": [],
    "open_questions": [],
    "next_steps": []
  },
  "message_log": []
}
```

### Agent Bootstrapping

For each agent requested or determined to be needed:

```
1. Select from built-in templates or create a custom registration
2. Write the agent entry to .a2a-context.json
3. Validate: no duplicate names, capabilities cover the task requirements
4. Report the team composition to the user
```
