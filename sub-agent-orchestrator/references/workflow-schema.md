# Workflow Definition Language (YAML)

Workflows are defined in YAML. The orchestrator parses this definition and executes it step by step.

## Schema

```yaml
workflow:
  name: string                    # Human-readable workflow name
  description: string             # What this workflow accomplishes
  version: string                 # Workflow version (semver)
  timeout: string                 # Global timeout (e.g., "30m", "2h")

  # Input variables available to all agents
  inputs:
    - name: string                # Variable name
      type: string                # string | number | boolean | json | file_path
      required: boolean
      default: any                # Default value if not provided
      description: string

  # Agent role definitions
  agents:
    agent_id:                     # Unique identifier (snake_case)
      name: string                # Human-readable name
      role: string                # Brief role description
      prompt: string              # Full prompt template (supports {{variable}} interpolation)
      tools: string[]             # Tools this agent can use (Read, Write, Bash, etc.)
      timeout: string             # Per-agent timeout (overrides global)
      retry:
        max_attempts: number      # Maximum retry attempts (default: 1, no retry)
        backoff: string           # none | linear | exponential
        on_failure: string        # skip | abort | fallback:{agent_id}
      validation:
        schema: object            # JSON schema for expected output
        rules: string[]           # Plain-English validation rules

  # Execution steps
  steps:
    - id: string                  # Step identifier
      agent: string               # Agent ID to execute
      type: string                # sequential | parallel | conditional | loop | map

      # For sequential steps
      input: string               # "{{inputs.variable}}" or "{{steps.prev_step.output}}"

      # For parallel steps
      parallel:
        - agent: string
          input: string
        - agent: string
          input: string
      wait: all | any | N         # Wait for all, any one, or N to complete

      # For conditional steps
      condition:
        eval: string              # Expression to evaluate (e.g., "{{steps.classify.output.category}} == 'hot'")
        true: string              # Step ID or agent ID to run if true
        false: string             # Step ID or agent ID to run if false

      # For loop steps
      loop:
        agent: string             # Agent to loop
        validator: string         # Validator agent ID
        max_iterations: number    # Safety limit
        feedback_path: string     # Where to get feedback from validator

      # For map steps
      map:
        over: string              # Array to iterate over (e.g., "{{steps.split.output.chunks}}")
        agent: string             # Agent to run for each element
        reduce: string            # Reducer agent ID

      # Output handling
      output:
        store_as: string          # Variable name to store result
        format: string            # json | text | markdown
```
