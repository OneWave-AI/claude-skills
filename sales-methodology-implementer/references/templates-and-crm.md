# Resources, Templates, and CRM Integration

Reusable call scripts, email templates, status-update formats, CRM field definitions, and success metrics.

## Call Scripts by Methodology Component

**[Component 1] Discovery Script**:
```
Rep: "To make sure we're a good fit, I need to understand [specific aspect]. Would you mind if I asked a few questions about [topic]?"

[If yes]

Rep: "Great! [Tier 1 question]?"

Prospect: [Response]

Rep: "[Appropriate follow-up based on response]"

[If prospect pushes back]

Rep: "I understand. The reason I'm asking is [business justification]. Without understanding [aspect], it's hard for me to know if we can actually help. Does that make sense?"
```

## Email Templates

**Qualification Follow-Up Email**:
```
Subject: Quick question about [specific component]

Hi [Name],

Thanks for the call earlier. I'm working on [next step] and realized I'm missing one piece of information.

Quick question: [Tier 1 question from missing component]?

This will help me [specific benefit to them].

[Your Name]
```

## Slack/CRM Status Updates

**Deal Status Update Format**:
```
Deal: [Company Name] - [Deal Size]
[Methodology] Score: [X]/100 (Green/Yellow/Red)

Strengths:
- [Strength 1]
- [Strength 2]

Risks:
- [Risk 1]
- [Risk 2]

Next Action: [Specific next step]
Timeline: [When]
Confidence: [Low/Med/High]
```

---

## CRM Integration

### Salesforce Custom Fields

Create custom fields for each component:
```
MEDDIC_Metrics_Score__c (Number, 0-10)
MEDDIC_Metrics_Evidence__c (Long Text)
MEDDIC_Economic_Buyer_Score__c (Number, 0-10)
MEDDIC_Economic_Buyer_Evidence__c (Long Text)
...
MEDDIC_Overall_Score__c (Formula: SUM of all scores)
MEDDIC_Status__c (Formula: IF >80, "Qualified", IF >50, "Risky", "Disqualified")
```

### HubSpot Properties

Add custom properties:
- `meddic_score` (Number, 0-100)
- `meddic_metrics` (Multi-line text)
- `meddic_decision_process` (Multi-line text)
- `qualification_date` (Date)
- `deal_risk_level` (Dropdown: Low/Med/High)

---

## Success Metrics to Track

**Leading Indicators**:
- % of deals with completed scorecard
- Average qualification score
- Time to complete qualification
- Disqualification rate

**Lagging Indicators**:
- Win rate improvement
- Sales cycle length
- Average deal size
- Forecast accuracy
- Revenue per rep

**Target Benchmarks**:
- Scorecard completion: 95%+
- Average score: 70+ (on 100-point scale)
- Win rate improvement: +10-20% within 6 months
- Forecast accuracy: +15% within 3 months
