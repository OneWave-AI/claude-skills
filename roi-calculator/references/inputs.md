# Required and Optional Inputs

Collect these inputs before calculating. If any required input is missing, ask for it explicitly. Do not guess or assume values.

## Cost Inputs (Required)

- Current monthly software/tool costs: What the organization currently pays for tools the AI will replace or augment (legacy software licenses, SaaS subscriptions, outsourced services).
- AI solution cost: Monthly or annual cost of the proposed AI solution (licensing, API costs, infrastructure).
- Implementation cost: One-time costs for setup, integration, training, migration, and consulting.
- Ongoing maintenance cost: Monthly cost for support, updates, monitoring, and fine-tuning.

## Time and Labor Inputs (Required)

- Team size: Number of employees affected by the AI implementation.
- Average hourly rate: Fully loaded cost per hour per employee (salary + benefits + overhead). If the user gives salary only, multiply by 1.3 to estimate the fully loaded rate.
- Hours per week on manual processes: Average hours each team member spends on tasks the AI will automate or accelerate.
- Expected time reduction percentage: How much of that manual time the AI is expected to eliminate. Use conservative defaults when the user is unsure: 40% for augmentation, 70% for full automation.

## Optional Inputs (Apply Defaults If Not Provided)

- Ramp-up period: Months to reach full productivity with the AI (default: 3 months).
- Annual salary increase rate: For projecting future savings (default: 3%).
- Discount rate: For NPV calculations (default: 10%).
- Error/rework reduction: Percentage reduction in errors from AI (default: 50%).
- Current error rate cost: Monthly cost of errors, rework, and quality issues (default: 0 if unknown).
- Revenue impact: Expected revenue increase from faster throughput or better quality (default: 0 if unknown).
- Analysis period: Number of months to project (default: 12 months; can extend to 24 or 36).
