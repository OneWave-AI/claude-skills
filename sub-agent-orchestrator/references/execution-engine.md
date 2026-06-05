# Execution Engine

The orchestrator follows this execution model when processing a workflow.

## Parse Phase

1. Load workflow YAML -- Read and parse the workflow definition.
2. Validate schema -- Ensure all required fields are present, agent IDs are referenced correctly, and there are no circular dependencies in sequential steps.
3. Resolve inputs -- Collect all required inputs from the user, apply defaults for optional inputs.
4. Build execution graph -- Convert steps into a directed acyclic graph (DAG) for execution ordering.

## Execute Phase

Process each step in topological order.

### Sequential Step

1. Resolve input template (replace `{{variables}}` with actual values).
2. Build the agent prompt from the agent definition plus resolved input.
3. Deploy the agent using the Agent tool.
4. Wait for completion.
5. Validate output against the agent's validation rules.
6. Store output in step context.
7. Proceed to the next step.

### Parallel Step

1. Resolve all input templates.
2. Build all agent prompts.
3. Deploy ALL agents simultaneously (single message, multiple Agent tool calls).
4. Wait based on the wait policy:
   - `all`: wait for every agent to complete.
   - `any`: proceed when the first agent completes.
   - `N`: proceed when N agents complete.
5. Collect and validate all outputs.
6. Store outputs (keyed by `output_key`) in step context.
7. Proceed to the next step.

### Conditional Step

1. Resolve the condition expression.
2. Evaluate: parse the expression and determine true/false.
3. Route to the appropriate agent/step based on the result.
4. Execute that branch.
5. Store output in step context.
6. Proceed to the next step.

### Loop Step

1. Execute the primary agent.
2. Pass output to the validator agent.
3. If the validator returns `passed=true`: exit the loop, store output.
4. If the validator returns `passed=false`:
   a. Extract feedback from the validator.
   b. Re-execute the primary agent with the original input plus feedback.
   c. Repeat from step 2.
5. If `max_iterations` is reached: store the last output, flag as "max iterations reached".

### Map Step

1. Resolve the array to iterate over.
2. For each element, deploy an agent instance (parallel, batched if more than 20).
3. Collect all results.
4. Pass collected results to the reducer agent.
5. Store the reducer's output in step context.

## Retry Logic

When an agent fails:

```
attempt = 1
while attempt <= max_attempts:
    result = deploy_agent(brief)
    if result.success:
        return result
    attempt += 1
    if backoff == "linear":
        wait(attempt * 5 seconds)  # conceptual; actual implementation uses re-deploy timing
    elif backoff == "exponential":
        wait(2^attempt seconds)

# All retries exhausted
if on_failure == "skip":
    store null output, continue workflow
elif on_failure == "abort":
    stop entire workflow, report failure
elif on_failure starts with "fallback:":
    deploy fallback agent with same input
```

## Timeout Handling

Three levels of timeout:

1. Global timeout -- If the entire workflow exceeds this, abort all running agents and report partial results.
2. Per-agent timeout -- If a single agent exceeds this, trigger its retry/failure policy.
3. Step timeout -- For parallel steps, the timeout applies to the wait policy (for example, if `wait=all` and one agent times out, apply that agent's failure policy).

## Result Validation

After each agent completes, validate its output:

1. Schema check -- If a JSON schema is provided, validate the output structure.
2. Rule check -- Evaluate each plain-English rule against the output:
   - "Must include X field" -- check field presence.
   - "Must identify exactly N items" -- check array length.
   - "Score must be between 0 and 100" -- check value range.
3. Type check -- Verify output format matches the expected format (json, text, markdown).

If validation fails, treat the output as a failure and trigger the retry/failure policy.

## Error Handling and Edge Cases

| Scenario | Handling |
|----------|---------|
| Required input missing | Prompt user before starting |
| Agent returns empty output | Treat as failure, trigger retry/fallback |
| Circular dependency in steps | Reject workflow at parse time with clear error |
| Parallel step with one failure | Apply that agent's failure policy; others continue |
| Loop exceeds max_iterations | Exit loop, store last output, flag in report |
| Global timeout reached | Abort all running agents, collect partial results, report |
| Workflow YAML syntax error | Report the error line and suggest correction |
| Agent references undefined variable | Report at parse time, not runtime |
| Conditional eval is ambiguous | Default to false branch, log warning |
| Fallback agent also fails | Treat as abort for that step |
