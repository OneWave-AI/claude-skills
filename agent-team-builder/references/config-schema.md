# Configuration Schema

The complete `team-config.yaml` follows this schema.

```yaml
# Team Configuration Schema
version: "1.0"
team:
  name: string              # Unique team identifier
  description: string       # Human-readable description
  created: datetime         # ISO 8601 creation timestamp
  updated: datetime         # ISO 8601 last update timestamp
  owner: string             # Team owner email or ID
  communication_pattern: enum[hub-and-spoke, pipeline, mesh, broadcast]
  max_concurrent_tasks: integer  # Maximum parallel task execution
  timeout_seconds: integer       # Default task timeout
  retry_policy:
    max_retries: integer
    backoff_multiplier: float
    max_backoff_seconds: integer

coordinator:
  agent_id: string          # ID of the coordinator agent
  health_check_interval: integer  # Seconds between health checks
  rebalance_threshold: float      # Load imbalance threshold for rebalancing

agents:
  - id: string              # Unique agent identifier
    role: string            # Human-readable role name
    description: string     # What this agent does
    tools: array[string]    # Allowed tools
    model: string           # LLM model to use (default: inherit)
    temperature: float      # Generation temperature (0.0-1.0)
    max_tokens: integer     # Maximum output tokens
    system_prompt: string   # Full system prompt (or path to prompt file)
    input_schema:           # Expected input format
      type: object
      properties: {}
    output_schema:          # Expected output format
      type: object
      properties: {}
    triggers:               # What activates this agent
      - event: string       # Event name
      - schedule: string    # Cron expression
      - condition: string   # Boolean expression
    handoff_rules:          # When to pass work to another agent
      - condition: string
        target: string      # Target agent ID
        data: array[string] # What data to pass
    escalation:             # When to involve humans
      - condition: string
        target: enum[human, manager, on-call]
        channel: enum[slack, email, pagerduty]
        message: string
        sla_minutes: integer
    rate_limits:
      requests_per_minute: integer
      tokens_per_minute: integer
    monitoring:
      log_level: enum[debug, info, warn, error]
      metrics: array[string]
      alerts:
        - condition: string
          channel: string
          severity: enum[info, warning, critical]
    success_criteria:
      - metric: string
        target: string
        measurement_window: string
    failure_modes:
      - scenario: string
        recovery: string
        alert: boolean

workflows:
  - name: string
    description: string
    trigger: string
    steps:
      - agent: string       # Agent ID
        action: string      # What the agent does in this step
        input_from: string  # Where input comes from (trigger, previous step, etc.)
        output_to: string   # Where output goes
        timeout: integer
        on_failure: enum[retry, skip, escalate, abort]

shared_resources:
  knowledge_base: string    # Path to shared knowledge base
  templates: string         # Path to shared templates
  credentials: string       # Path to credentials (encrypted)
  data_stores:
    - name: string
      type: enum[file, database, api]
      connection: string
      access: array[string] # Which agents can access
```

## Advanced Features

### Agent-to-Agent Communication Protocol

When agents need to communicate, they use a standardized message format.

```yaml
message:
  from: agent_id
  to: agent_id
  type: enum[request, response, notification, escalation]
  priority: enum[low, medium, high, critical]
  correlation_id: uuid    # Links related messages
  timestamp: iso8601
  payload:
    action: string
    data: object
    context: object       # Shared context from previous steps
  metadata:
    attempt: integer
    timeout_at: iso8601
    callback: string      # Where to send the response
```

### Dynamic Team Scaling

Teams can scale based on workload.

```yaml
scaling:
  min_instances: 1
  max_instances: 5
  scale_up_threshold: 0.8    # Scale up when queue depth exceeds 80% capacity
  scale_down_threshold: 0.2  # Scale down when queue depth drops below 20%
  cooldown_seconds: 300      # Wait before scaling again
```

### Shared Context Management

Agents share context through a managed state store.

```yaml
shared_context:
  store_type: file           # file, redis, database
  path: ./team-state/
  ttl_seconds: 86400         # Context expires after 24 hours
  access_control:
    - agent: coordinator
      permissions: [read, write, delete]
    - agent: specialist
      permissions: [read, write]
    - agent: validator
      permissions: [read]
```
