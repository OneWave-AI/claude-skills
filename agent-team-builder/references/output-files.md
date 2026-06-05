# Output Files and Response Format

## Files to Generate

After completing discovery and design, generate these files in the user's specified output directory (default: `./agent-team/`).

### 1. team-config.yaml

The master configuration file containing:
- Team metadata (name, description, version, created date)
- Communication pattern and protocols
- All agent definitions with full specifications
- Workflow triggers and schedules
- Escalation matrix
- Monitoring and alerting rules

See `config-schema.md` for the full schema.

### 2. Individual Agent Prompts

For each agent, generate a separate file at `agents/{agent-id}/prompt.md` containing:
- Role definition and personality
- Domain expertise and knowledge
- Input/output specifications
- Decision frameworks
- Example interactions
- Edge case handling

### 3. Workflow Diagrams

Generate a `workflow.md` file with:
- Mermaid diagram showing agent communication flow
- State machine for the overall process
- Decision tree for routing logic
- Escalation path diagram

### 4. Testing Scenarios

Generate a `test-scenarios.yaml` file with:
- Happy path scenarios for each workflow
- Edge cases and failure scenarios
- Load testing parameters
- Expected outputs for validation

## Response Format

After discovery is complete, present the team design using this structure.

```markdown
## Team Design: [Team Name]

### Architecture Overview
[Mermaid diagram of agent communication]

### Agent Roster
| Agent | Role | Tools | Handoff To |
|-------|------|-------|------------|
| ... | ... | ... | ... |

### Workflow Summary
[Step-by-step description of how work flows through the team]

### Escalation Matrix
[When and how humans are involved]

### Estimated Impact
- Current process time: [X hours/minutes]
- Automated process time: [Y hours/minutes]
- Error reduction: [estimated %]
- Capacity increase: [estimated %]

### Files Generated
- team-config.yaml
- agents/{id}/prompt.md (for each agent)
- workflow.md
- test-scenarios.yaml
```
