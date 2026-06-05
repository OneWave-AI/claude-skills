# Classification, Severity, and Remediation Rubric

## Compliance Status
Classify each finding against each applicable framework requirement:
- COMPLIANT: Requirement fully met with sufficient evidence.
- PARTIAL: Some controls exist but are incomplete or inconsistently applied.
- NON-COMPLIANT: Requirement not met or no evidence of controls exists.
- NOT APPLICABLE: Requirement does not apply to this system.
- UNABLE TO ASSESS: Insufficient information to make a determination (specify what additional information is needed).

## Risk Severity
Assign a severity to each non-compliant or partial finding:

| Severity | Definition | Remediation Timeline |
|----------|-----------|---------------------|
| CRITICAL | Immediate risk of regulatory action, data breach, or significant harm to data subjects | Immediate (0-7 days) |
| HIGH | Significant gap that could lead to enforcement action or substantial fines | Within 30 days |
| MEDIUM | Moderate gap that increases compliance risk | Within 90 days |
| LOW | Minor gap or documentation deficiency | Within 180 days |
| INFORMATIONAL | Best practice recommendation beyond strict regulatory requirements | As capacity allows |

## Remediation Detail
For each non-compliant or partial finding, provide:
1. Description: What the gap is and why it matters.
2. Regulatory Reference: The specific article, section, requirement, or criterion that is not met.
3. Current State: What currently exists, if anything.
4. Required State: What must be in place to achieve compliance.
5. Remediation Steps: Specific, actionable steps to close the gap, including code changes, configuration changes, policy documents, or process changes.
6. Evidence Requirements: What documentation, artifacts, or technical evidence an auditor would need to verify compliance.
7. Estimated Effort: T-shirt size (XS/S/M/L/XL).
8. Dependencies: Other findings or external factors that must be addressed first.
