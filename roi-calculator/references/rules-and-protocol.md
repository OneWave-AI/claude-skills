# Calculation Rules, Interaction Protocol, and Quality Checklist

## Calculation Rules

1. Never inflate numbers. Use the user's inputs as-is. If inputs seem unrealistic, note this in the Risk Factors section but still calculate based on what was provided.
2. Always show the work. The Appendix must contain enough detail to reproduce every number.
3. Round currency to the nearest dollar. Round percentages to one decimal place. Round hours to one decimal place.
4. Use commas in numbers over 999 (for example, $1,000 not $1000).
5. Default to conservative. When the user does not specify a value and a default is required, use the conservative end of the range and note this.
6. Flag unrealistic inputs. If the user provides inputs that seem too optimistic (for example, 95% time reduction or $0 implementation cost), add a warning in the Executive Summary.
7. Treat negative ROI as valid. If the numbers do not justify the investment, say so clearly. Do not spin a negative ROI as positive.
8. Account for opportunity cost. The time saved has value only if the team can redeploy that time productively. Note this assumption.

## Interaction Protocol

1. If the user provides all inputs in their message: Proceed directly to calculation and generate the full `roi-analysis.md`.
2. If inputs are missing: Ask for the missing required inputs in a single organized message. Group questions by category (Cost, Time/Labor). Provide examples to help the user estimate.
3. If the user says "use defaults" or "estimate": Use conservative defaults for optional parameters. For required parameters (team size, hourly rate, manual hours, AI cost, implementation cost), ask explicitly. These cannot be defaulted because they vary too widely.
4. After generating the report: Summarize the top 3 findings in the response message and mention the file path where the report was saved.

## Quality Checklist

Before delivering the report, verify:

- [ ] All tables render correctly in Markdown
- [ ] All numbers are internally consistent (monthly * 12 = annual, and so on)
- [ ] Payback period matches the monthly projection table
- [ ] Sensitivity analysis shows materially different outcomes across scenarios
- [ ] At least 3 comparison scenarios are included
- [ ] Risk factors are honest and include mitigation strategies
- [ ] Executive summary matches the detailed findings
- [ ] Recommendation is clear and defensible based on the numbers
- [ ] No emojis anywhere in the output
- [ ] All currency values have $ signs and commas where appropriate
