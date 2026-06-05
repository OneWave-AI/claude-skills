# Assessment Methodology

## Phase 1: Information Gathering

Collect information through one or more of these channels.

1. **Conversational Assessment**: Ask the key questions listed under each dimension in `dimensions.md`. Adapt questions to the business context. Do not ask all questions at once; prioritize based on what you learn.

2. **Document Review**: When the user provides documentation, codebases, or other materials, review them to inform the assessment:
   - Technical architecture documents
   - Data dictionaries or schema definitions
   - Process documentation or SOPs
   - Organizational charts
   - Technology vendor lists
   - Previous audit or assessment reports
   - Strategic plans mentioning AI or digital transformation

3. **Codebase Analysis**: When a codebase is available, examine:
   - Technology stack and framework choices
   - Database schemas and data models
   - API structure and documentation
   - Test coverage and CI/CD configuration
   - Logging and monitoring setup
   - Data pipeline implementations

## Phase 2: Scoring

Assign each dimension a score from 1 to 5 using the criteria in `dimensions.md`. Follow these rules:

- **Be honest and conservative**: Do not inflate scores. A realistic assessment is more valuable than an optimistic one.
- **Use half-points when appropriate**: When a business falls clearly between two levels (e.g., 2.5), use the half-point to reflect nuance.
- **Document evidence**: For each score, note the specific evidence that supports it.
- **Note uncertainties**: When information is insufficient to confidently score a dimension, flag it and explain what additional information would help.

### Calculating the Overall Score

The overall AI Readiness Score is a weighted average:

```
Overall Score = (Data Maturity x 0.25) + (Tech Stack x 0.20) + (Team Skills x 0.20) +
                (Process Documentation x 0.15) + (Budget x 0.10) + (Culture x 0.10)
```

**Overall Score Interpretation**:

| Score Range | Readiness Level | Recommendation |
|-------------|----------------|----------------|
| 1.0 - 1.5 | Not Ready | Focus on foundational digital transformation before considering AI |
| 1.6 - 2.0 | Early Stage | Address critical gaps in data and technology; AI is 18-24 months away |
| 2.1 - 2.5 | Developing | Targeted investments needed; begin with narrow AI use cases in 12-18 months |
| 2.6 - 3.0 | Approaching Ready | Strong foundation exists; pilot projects can begin in 6-12 months |
| 3.1 - 3.5 | Ready for Pilots | Organization can begin AI pilots immediately with proper scoping |
| 3.6 - 4.0 | Ready for Scale | Organization can pursue multiple AI initiatives simultaneously |
| 4.1 - 4.5 | Advanced | Organization is well-positioned for advanced AI and ML workloads |
| 4.6 - 5.0 | Leading | Organization is at the frontier of AI adoption in its industry |

## Phase 3: Gap Analysis

For each dimension scored below 4.0, identify:

1. **Current State**: What exists today (with evidence)
2. **Target State**: What is needed for AI readiness (score of 4.0)
3. **Gap Description**: The specific deficiency
4. **Impact**: How this gap affects AI adoption (High / Medium / Low)
5. **Effort to Close**: Estimated time and resources to address (Quick Win / Medium Effort / Major Initiative)

## Phase 4: Recommendations

Generate prioritized recommendations following the OneWave AI methodology.

**Priority 1 - Prerequisite Steps (Must Do Before AI)**:
- Items that are absolute blockers to any AI initiative
- Typically data quality, basic infrastructure, or critical skills gaps
- Timeline: 0-6 months

**Priority 2 - Foundation Building (Prepare for AI)**:
- Items that enable successful AI pilots
- Typically process documentation, team upskilling, or infrastructure modernization
- Timeline: 3-12 months

**Priority 3 - AI Quick Wins (First AI Projects)**:
- Low-risk, high-visibility AI use cases that build organizational confidence
- Should leverage existing strengths identified in the assessment
- Timeline: 6-18 months

**Priority 4 - Strategic AI Initiatives (Scale AI)**:
- Larger AI projects that require the foundation to be in place
- Cross-functional initiatives with significant business impact
- Timeline: 12-24 months

**Priority 5 - Advanced AI / Innovation (Lead with AI)**:
- Cutting-edge applications that differentiate the business
- Requires mature AI capabilities and organizational readiness
- Timeline: 18-36 months

## Tailoring the Assessment

### By Company Size

**Startups (1-50 employees)**:
- Weight culture and team skills more heavily in recommendations
- Recognize that formal processes may not yet be needed
- Focus on building the right foundations rather than enterprise maturity
- Recommend cloud-native, SaaS-first approaches

**Mid-Market (50-500 employees)**:
- Balance formalization with agility
- Look for shadow IT and data silos between departments
- Assess whether growth has outpaced process documentation
- Recommend establishing a small dedicated AI team or partnership

**Enterprise (500+ employees)**:
- Assess cross-departmental data sharing and governance
- Evaluate change management capabilities thoroughly
- Look for competing priorities and political dynamics
- Recommend center of excellence model with federated execution

### By Industry

Adjust assessment focus based on industry-specific considerations:

- **Healthcare**: Emphasize HIPAA compliance, data privacy, clinical validation requirements
- **Financial Services**: Focus on regulatory compliance, model explainability, audit trails
- **Manufacturing**: Evaluate IoT data maturity, operational technology (OT) integration
- **Retail/E-commerce**: Assess customer data platforms, real-time analytics capabilities
- **Professional Services**: Focus on knowledge management, process standardization
- **SaaS/Technology**: Evaluate existing ML infrastructure, data engineering maturity

## Conversation Flow

When conducting the assessment conversationally, follow this structure.

### Opening

Introduce the assessment and explain the process:

"I will be conducting an AI Readiness Assessment for your organization. This evaluates six dimensions critical to successful AI adoption: data maturity, technology stack, team skills, process documentation, budget, and organizational culture. Each dimension is scored 1-5, and the final report will include your overall readiness score, a detailed gap analysis, and prioritized recommendations for moving forward. Let's begin."

### Gathering Information

- Start with **Data Maturity** as it carries the highest weight and most frequently blocks AI initiatives
- Ask 2-3 questions at a time, not all at once
- Listen for signals that inform multiple dimensions (e.g., "we use Salesforce" informs both data maturity and tech stack)
- Adapt questions based on the industry and company size
- When the user provides documents or codebase access, analyze those before asking redundant questions
- Probe deeper when answers are vague ("Can you give me a specific example?")

### During Assessment

- Summarize what has been learned periodically
- Flag significant red flags early
- Offer preliminary observations to keep the conversation productive
- Indicate which dimensions have enough information and which need more detail

### Closing

- Present a summary of findings before generating the full report
- Ask if there is any context that may have been missed
- Generate the `ai-readiness-report.md` file
- Highlight the top 3 actions the organization should take immediately
