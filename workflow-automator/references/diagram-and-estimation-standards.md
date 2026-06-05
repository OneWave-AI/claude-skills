# Diagram and Estimation Standards

## Mermaid Diagram Standards

Follow these rules for all Mermaid diagrams:

1. **Use descriptive node IDs**: `processOrder` not `A1`
2. **Label all edges**: Every arrow should have a label explaining the transition
3. **Color code by type**:
   - Manual steps: `fill:#e0e0e0` (gray)
   - Automated steps: `fill:#4CAF50,color:#fff` (green)
   - Decision points: `fill:#2196F3,color:#fff` (blue)
   - Human-in-the-loop: `fill:#FF9800,color:#fff` (orange)
   - Error/failure paths: `fill:#f44336,color:#fff` (red)
   - Wait states: `fill:#9C27B0,color:#fff`
4. **Show swim lanes** when multiple actors are involved (use subgraph)
5. **Include timing annotations** on edges where wait times exist
6. **Mark the critical path** through the workflow
7. **Keep diagrams readable**: If a workflow has more than 20 nodes, split into sub-diagrams by phase or functional area

## Estimation Standards

When estimating time savings:

- **Be conservative**: Use median times, not best-case
- **Account for automation overhead**: Include time to handle exceptions that the automation cannot process
- **Distinguish active time from wait time**: Automation eliminates wait time between steps almost entirely
- **Use ranges**: "Saves 8-12 hours per week" is more honest than "Saves 10 hours per week"
- **Calculate ROI realistically**: Include platform costs, setup time, and ongoing maintenance
- **Show break-even point**: When does the automation investment pay for itself?
