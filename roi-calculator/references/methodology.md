# Calculation Methodology

Compute every metric below. Round currency to the nearest dollar, percentages to one decimal place, and hours to one decimal place. Use commas in numbers over 999.

## 1. Monthly Time Savings

```
weekly_hours_saved_per_person = hours_per_week_manual * time_reduction_percentage
monthly_hours_saved_per_person = weekly_hours_saved_per_person * 4.33
total_monthly_hours_saved = monthly_hours_saved_per_person * team_size
```

## 2. Monthly Labor Cost Savings

```
monthly_labor_savings = total_monthly_hours_saved * hourly_rate
```

## 3. Monthly Error Reduction Savings

```
monthly_error_savings = current_error_rate_cost * error_reduction_percentage
```

## 4. Total Monthly Savings (Gross)

```
total_monthly_savings = monthly_labor_savings + monthly_error_savings + monthly_revenue_impact
```

## 5. Net Monthly Savings

```
net_monthly_savings = total_monthly_savings - ai_solution_monthly_cost - ongoing_maintenance_cost
net_monthly_savings += current_tool_costs_eliminated
```

## 6. Ramp-Up Adjustment

Reduce savings linearly during the ramp-up period:

```
month_1_savings = net_monthly_savings * (1 / ramp_months)
month_2_savings = net_monthly_savings * (2 / ramp_months)
...
month_N_savings = net_monthly_savings * (N / ramp_months) [until N >= ramp_months]
```

After ramp-up, apply full net_monthly_savings.

## 7. Payback Period

```
cumulative_savings = sum of ramp-adjusted monthly savings over time
payback_month = first month where cumulative_savings >= implementation_cost
```

If payback never occurs within the analysis period, state this clearly.

## 8. 12-Month ROI

```
total_12_month_savings = sum of ramp-adjusted monthly savings for months 1-12
total_12_month_cost = implementation_cost + (ai_monthly_cost * 12) + (maintenance_cost * 12)
total_12_month_benefit = total_12_month_savings + (current_tool_costs_eliminated * 12)
roi_percentage = ((total_12_month_benefit - total_12_month_cost) / total_12_month_cost) * 100
```

## 9. Net Present Value (NPV)

```
monthly_discount_rate = (1 + annual_discount_rate)^(1/12) - 1
npv = -implementation_cost + sum( net_monthly_savings_month_i / (1 + monthly_discount_rate)^i ) for i=1 to N
```

## 10. Productivity Gain Percentage

```
current_productive_hours = (40 - hours_per_week_manual) * team_size
new_productive_hours = (40 - hours_per_week_manual + weekly_hours_saved_per_person) * team_size
productivity_gain = (new_productive_hours - current_productive_hours) / current_productive_hours * 100
```

## 11. Sensitivity Analysis

Run calculations across three scenarios:

| Parameter | Conservative | Base Case | Optimistic |
|-----------|-------------|-----------|------------|
| Time reduction | base * 0.6 | base | base * 1.2 (cap at 95%) |
| Ramp-up period | base + 2 months | base | base - 1 month (min 1) |
| AI cost | base * 1.2 | base | base * 0.9 |
| Error reduction | base * 0.5 | base | base * 1.3 (cap at 95%) |

## 12. Comparison Scenarios

Generate at minimum three comparison scenarios:

1. Do Nothing: Project costs of maintaining the status quo over the analysis period, including salary inflation, growing error costs, and opportunity cost of manual work.
2. Partial Implementation: Implement AI for only the highest-value use case (50% of team, highest-impact process only).
3. Full Implementation: The proposed full rollout.
4. Phased Rollout (include only if team_size > 10): Stagger implementation across departments over 6 months.
