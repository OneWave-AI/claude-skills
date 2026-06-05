# Data Format Templates

If no data is available, provide these templates for the user to populate, then re-run the forecast.

## Account Overview Template

```csv
account_name,arr,renewal_date,contract_start,contract_term_months,tier,seats_purchased,csm_name,executive_sponsor_client,champion_name,champion_title,champion_email
```

## Usage Metrics Template

```csv
account_name,date,dau,wau,mau,sessions,avg_session_duration_min,api_calls,data_volume_gb,features_used_count,total_features_available
```

## Support Ticket Template

```csv
account_name,ticket_id,created_date,resolved_date,severity,category,sentiment,csat_score,escalated,summary
```

## NPS/CSAT Template

```csv
account_name,survey_date,survey_type,score,verbatim_comment,respondent_name,respondent_title
```

## Billing Template

```csv
account_name,invoice_date,amount,due_date,paid_date,days_late,dispute_flag,discount_pct,notes
```

## Stakeholder Template

```csv
account_name,contact_name,title,role_in_deal,last_activity_date,status,linkedin_url,notes
```

## Engagement Log Template

```csv
account_name,date,activity_type,initiated_by,attendees,summary,next_steps
```
