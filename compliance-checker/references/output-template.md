# Output Template

Generate the final report as `compliance-report.md` in the project root (or a user-specified location). Every section is mandatory. If a section has no findings, state explicitly that none were identified.

```markdown
# Compliance Audit Report

**Audit Date**: [Date of audit]
**Audit Scope**: [Description of what was audited]
**Auditor**: Claude Code Compliance Checker
**Frameworks Assessed**: [List of applicable frameworks]

---

## Executive Summary

[2-3 paragraph summary of overall compliance posture, key risks, and top priority actions. Include a summary table:]

| Framework | Status | Critical | High | Medium | Low | Info |
|-----------|--------|----------|------|--------|-----|------|
| GDPR      | [status] | [n]   | [n]  | [n]    | [n] | [n]  |
| HIPAA     | [status] | [n]   | [n]  | [n]    | [n] | [n]  |
| SOC 2     | [status] | [n]   | [n]  | [n]    | [n] | [n]  |
| CCPA      | [status] | [n]   | [n]  | [n]    | [n] | [n]  |
| PCI-DSS   | [status] | [n]   | [n]  | [n]    | [n] | [n]  |

**Overall Risk Rating**: [Critical / High / Medium / Low]
**Total Findings**: [N] ([breakdown by severity])
**Immediate Actions Required**: [count]

---

## Table of Contents

1. Audit Scope and Methodology
2. Data Inventory
3. Findings by Scan Category
   3.1 PII and Sensitive Data Handling
   3.2 Data Retention
   3.3 Encryption
   3.4 Access Controls
   3.5 Audit Logging
   3.6 Consent Management
   3.7 Data Transfer
4. Gap Analysis by Framework
   4.1 GDPR Gap Analysis
   4.2 HIPAA Gap Analysis
   4.3 SOC 2 Gap Analysis
   4.4 CCPA Gap Analysis
   4.5 PCI-DSS Gap Analysis
5. Remediation Plan
6. Evidence Requirements for Certification
7. Appendices

---

## 1. Audit Scope and Methodology

### Scope
[Describe what was included: repositories, services, infrastructure, documentation]

### Methodology
[Describe the approach: automated scanning, manual code review, configuration review, documentation review]

### Limitations
[Describe any limitations: areas that could not be assessed, information that was unavailable, assumptions made]

### Framework Applicability Determination
[For each framework, explain why it is or is not applicable to this system]

---

## 2. Data Inventory

### Data Categories Identified

| Category | Data Elements | Storage Location(s) | Classification |
|----------|--------------|---------------------|----------------|
| [category] | [elements] | [locations] | [PII/PHI/CHD/Sensitive/Public] |

### Data Flow Summary
[Describe how regulated data flows through the system: ingestion points, processing steps, storage locations, output/transfer points, deletion]

---

## 3. Findings by Scan Category

Repeat the following structure for each of the seven categories (3.1 through 3.7):

### 3.X [Category Name]

#### Positive Findings (Evidence of Compliance)
[List controls and practices that support compliance, with file paths and line numbers]

#### Gaps and Issues

**Finding [ID]: [Title]**
- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW/INFO]
- **Location**: [File path and line numbers]
- **Description**: [What was found or what is missing]
- **Affected Frameworks**: [Which frameworks this impacts]
- **Evidence**: [Code snippet or configuration excerpt]
- **Risk**: [What could go wrong if not addressed]

[Repeat for each finding]

---

## 4. Gap Analysis by Framework

### 4.1 GDPR Gap Analysis

| Article/Requirement | Description | Status | Severity | Finding Ref |
|---------------------|-------------|--------|----------|-------------|
| Art. 5(1)(a) | Lawfulness, fairness, transparency | [status] | [severity] | [ref] |
| Art. 5(1)(b) | Purpose limitation | [status] | [severity] | [ref] |
| Art. 5(1)(c) | Data minimisation | [status] | [severity] | [ref] |
| Art. 5(1)(d) | Accuracy | [status] | [severity] | [ref] |
| Art. 5(1)(e) | Storage limitation | [status] | [severity] | [ref] |
| Art. 5(1)(f) | Integrity and confidentiality | [status] | [severity] | [ref] |
| Art. 5(2) | Accountability | [status] | [severity] | [ref] |
| Art. 6 | Lawful basis for processing | [status] | [severity] | [ref] |
| Art. 7 | Conditions for consent | [status] | [severity] | [ref] |
| Art. 12 | Transparent information | [status] | [severity] | [ref] |
| Art. 13 | Information at collection | [status] | [severity] | [ref] |
| Art. 14 | Information not obtained from data subject | [status] | [severity] | [ref] |
| Art. 15 | Right of access | [status] | [severity] | [ref] |
| Art. 16 | Right to rectification | [status] | [severity] | [ref] |
| Art. 17 | Right to erasure | [status] | [severity] | [ref] |
| Art. 18 | Right to restriction | [status] | [severity] | [ref] |
| Art. 20 | Right to data portability | [status] | [severity] | [ref] |
| Art. 21 | Right to object | [status] | [severity] | [ref] |
| Art. 22 | Automated decision-making | [status] | [severity] | [ref] |
| Art. 25 | Data protection by design/default | [status] | [severity] | [ref] |
| Art. 28 | Processor obligations | [status] | [severity] | [ref] |
| Art. 30 | Records of processing | [status] | [severity] | [ref] |
| Art. 32 | Security of processing | [status] | [severity] | [ref] |
| Art. 33 | Breach notification to authority | [status] | [severity] | [ref] |
| Art. 34 | Breach notification to data subjects | [status] | [severity] | [ref] |
| Art. 35 | Data protection impact assessment | [status] | [severity] | [ref] |
| Art. 37 | Data Protection Officer | [status] | [severity] | [ref] |
| Art. 44-49 | International transfers | [status] | [severity] | [ref] |

### 4.2 HIPAA Gap Analysis

| Standard | Requirement | Status | Severity | Finding Ref |
|----------|-------------|--------|----------|-------------|
| 164.308(a)(1) | Security Management Process | [status] | [severity] | [ref] |
| 164.308(a)(2) | Assigned Security Responsibility | [status] | [severity] | [ref] |
| 164.308(a)(3) | Workforce Security | [status] | [severity] | [ref] |
| 164.308(a)(4) | Information Access Management | [status] | [severity] | [ref] |
| 164.308(a)(5) | Security Awareness Training | [status] | [severity] | [ref] |
| 164.308(a)(6) | Security Incident Procedures | [status] | [severity] | [ref] |
| 164.308(a)(7) | Contingency Plan | [status] | [severity] | [ref] |
| 164.308(a)(8) | Evaluation | [status] | [severity] | [ref] |
| 164.310(a) | Facility Access Controls | [status] | [severity] | [ref] |
| 164.310(b) | Workstation Use | [status] | [severity] | [ref] |
| 164.310(c) | Workstation Security | [status] | [severity] | [ref] |
| 164.310(d) | Device and Media Controls | [status] | [severity] | [ref] |
| 164.312(a) | Access Control | [status] | [severity] | [ref] |
| 164.312(b) | Audit Controls | [status] | [severity] | [ref] |
| 164.312(c) | Integrity | [status] | [severity] | [ref] |
| 164.312(d) | Person or Entity Authentication | [status] | [severity] | [ref] |
| 164.312(e) | Transmission Security | [status] | [severity] | [ref] |
| 164.314(a) | Business Associate Contracts | [status] | [severity] | [ref] |
| 164.316(a) | Policies and Procedures | [status] | [severity] | [ref] |
| 164.316(b) | Documentation | [status] | [severity] | [ref] |
| 164.402-414 | Breach Notification | [status] | [severity] | [ref] |

### 4.3 SOC 2 Gap Analysis

| Criteria | Description | Status | Severity | Finding Ref |
|----------|-------------|--------|----------|-------------|
| CC1.1 | COSO Principle 1: Integrity and Ethics | [status] | [severity] | [ref] |
| CC1.2 | COSO Principle 2: Board Oversight | [status] | [severity] | [ref] |
| CC1.3 | COSO Principle 3: Management Structure | [status] | [severity] | [ref] |
| CC1.4 | COSO Principle 4: Competence Commitment | [status] | [severity] | [ref] |
| CC1.5 | COSO Principle 5: Accountability | [status] | [severity] | [ref] |
| CC2.1 | COSO Principle 13: Quality Information | [status] | [severity] | [ref] |
| CC2.2 | COSO Principle 14: Internal Communication | [status] | [severity] | [ref] |
| CC2.3 | COSO Principle 15: External Communication | [status] | [severity] | [ref] |
| CC3.1 | COSO Principle 6: Risk Objectives | [status] | [severity] | [ref] |
| CC3.2 | COSO Principle 7: Risk Identification | [status] | [severity] | [ref] |
| CC3.3 | COSO Principle 8: Fraud Risk | [status] | [severity] | [ref] |
| CC3.4 | COSO Principle 9: Change Impact | [status] | [severity] | [ref] |
| CC4.1 | COSO Principle 16: Monitoring | [status] | [severity] | [ref] |
| CC4.2 | COSO Principle 17: Deficiency Evaluation | [status] | [severity] | [ref] |
| CC5.1 | COSO Principle 10: Control Selection | [status] | [severity] | [ref] |
| CC5.2 | COSO Principle 11: Technology Controls | [status] | [severity] | [ref] |
| CC5.3 | COSO Principle 12: Control Deployment | [status] | [severity] | [ref] |
| CC6.1 | Logical and Physical Access - Security Software | [status] | [severity] | [ref] |
| CC6.2 | Logical and Physical Access - Credentials | [status] | [severity] | [ref] |
| CC6.3 | Logical and Physical Access - New Access | [status] | [severity] | [ref] |
| CC6.6 | Logical and Physical Access - External Threats | [status] | [severity] | [ref] |
| CC6.7 | Logical and Physical Access - Data Transmission | [status] | [severity] | [ref] |
| CC6.8 | Logical and Physical Access - Malicious Software | [status] | [severity] | [ref] |
| CC7.1 | System Operations - Vulnerability Detection | [status] | [severity] | [ref] |
| CC7.2 | System Operations - Anomaly Monitoring | [status] | [severity] | [ref] |
| CC7.3 | System Operations - Incident Evaluation | [status] | [severity] | [ref] |
| CC7.4 | System Operations - Incident Response | [status] | [severity] | [ref] |
| CC7.5 | System Operations - Incident Recovery | [status] | [severity] | [ref] |
| CC8.1 | Change Management - Authorization | [status] | [severity] | [ref] |
| CC9.1 | Risk Mitigation - Business Disruption | [status] | [severity] | [ref] |
| CC9.2 | Risk Mitigation - Vendor Management | [status] | [severity] | [ref] |
| A1.1 | Availability - Capacity Planning | [status] | [severity] | [ref] |
| A1.2 | Availability - Recovery Infrastructure | [status] | [severity] | [ref] |
| A1.3 | Availability - Recovery Testing | [status] | [severity] | [ref] |
| C1.1 | Confidentiality - Identification | [status] | [severity] | [ref] |
| C1.2 | Confidentiality - Disposal | [status] | [severity] | [ref] |

### 4.4 CCPA Gap Analysis

| Section | Requirement | Status | Severity | Finding Ref |
|---------|-------------|--------|----------|-------------|
| 1798.100(a) | Right to know categories | [status] | [severity] | [ref] |
| 1798.100(b) | Notice at collection | [status] | [severity] | [ref] |
| 1798.100(d) | Purpose limitation | [status] | [severity] | [ref] |
| 1798.100(e) | Data minimization | [status] | [severity] | [ref] |
| 1798.105 | Right to delete | [status] | [severity] | [ref] |
| 1798.106 | Right to correct | [status] | [severity] | [ref] |
| 1798.110 | Right to know specific pieces | [status] | [severity] | [ref] |
| 1798.115 | Right to know sale/sharing | [status] | [severity] | [ref] |
| 1798.120 | Right to opt-out of sale/sharing | [status] | [severity] | [ref] |
| 1798.121 | Right to limit sensitive PI use | [status] | [severity] | [ref] |
| 1798.125 | Non-discrimination | [status] | [severity] | [ref] |
| 1798.130 | Verification of requests | [status] | [severity] | [ref] |
| 1798.135 | Do Not Sell/Share link | [status] | [severity] | [ref] |
| 1798.140(v) | Service provider obligations | [status] | [severity] | [ref] |
| 1798.185 | Reasonable security | [status] | [severity] | [ref] |

### 4.5 PCI-DSS Gap Analysis

| Requirement | Description | Status | Severity | Finding Ref |
|-------------|-------------|--------|----------|-------------|
| 1.1 | Network security controls defined | [status] | [severity] | [ref] |
| 1.2 | Network security controls configured | [status] | [severity] | [ref] |
| 1.3 | Network access restricted | [status] | [severity] | [ref] |
| 1.4 | Network connections controlled | [status] | [severity] | [ref] |
| 1.5 | Risks to CDE mitigated | [status] | [severity] | [ref] |
| 2.1 | Secure configurations applied | [status] | [severity] | [ref] |
| 2.2 | System components configured securely | [status] | [severity] | [ref] |
| 2.3 | Wireless environments secured | [status] | [severity] | [ref] |
| 3.1 | Account data storage minimized | [status] | [severity] | [ref] |
| 3.2 | Sensitive authentication data not stored post-auth | [status] | [severity] | [ref] |
| 3.3 | PAN displayed securely (masked) | [status] | [severity] | [ref] |
| 3.4 | PAN secured when stored | [status] | [severity] | [ref] |
| 3.5 | PAN secured where stored | [status] | [severity] | [ref] |
| 3.6 | Cryptographic keys managed | [status] | [severity] | [ref] |
| 3.7 | Stored account data protected | [status] | [severity] | [ref] |
| 4.1 | Strong cryptography in transit | [status] | [severity] | [ref] |
| 4.2 | PAN secured in end-user messaging | [status] | [severity] | [ref] |
| 5.1 | Malware protection deployed | [status] | [severity] | [ref] |
| 5.2 | Malware prevention maintained | [status] | [severity] | [ref] |
| 5.3 | Anti-malware active and monitored | [status] | [severity] | [ref] |
| 5.4 | Anti-phishing mechanisms | [status] | [severity] | [ref] |
| 6.1 | Secure development processes | [status] | [severity] | [ref] |
| 6.2 | Bespoke software developed securely | [status] | [severity] | [ref] |
| 6.3 | Security vulnerabilities identified and addressed | [status] | [severity] | [ref] |
| 6.4 | Public-facing web apps protected | [status] | [severity] | [ref] |
| 6.5 | Changes managed securely | [status] | [severity] | [ref] |
| 7.1 | Access restricted by need to know | [status] | [severity] | [ref] |
| 7.2 | Access appropriately defined | [status] | [severity] | [ref] |
| 7.3 | Access control system configured | [status] | [severity] | [ref] |
| 8.1 | User identification management | [status] | [severity] | [ref] |
| 8.2 | User identification enforced | [status] | [severity] | [ref] |
| 8.3 | Strong authentication established | [status] | [severity] | [ref] |
| 8.4 | MFA implemented | [status] | [severity] | [ref] |
| 8.5 | MFA systems configured properly | [status] | [severity] | [ref] |
| 8.6 | Application/system accounts managed | [status] | [severity] | [ref] |
| 9.1 | Physical access restricted | [status] | [severity] | [ref] |
| 9.2 | Physical access controls manage entry | [status] | [severity] | [ref] |
| 9.3 | Physical access for personnel authorized | [status] | [severity] | [ref] |
| 9.4 | Media physically secured | [status] | [severity] | [ref] |
| 9.5 | POI devices protected | [status] | [severity] | [ref] |
| 10.1 | Logging mechanisms defined | [status] | [severity] | [ref] |
| 10.2 | Audit logs capture details | [status] | [severity] | [ref] |
| 10.3 | Audit logs protected | [status] | [severity] | [ref] |
| 10.4 | Audit logs reviewed | [status] | [severity] | [ref] |
| 10.5 | Audit log history retained | [status] | [severity] | [ref] |
| 10.6 | Time synchronization mechanisms | [status] | [severity] | [ref] |
| 10.7 | Detection of logging failures | [status] | [severity] | [ref] |
| 11.1 | Wireless access points detected | [status] | [severity] | [ref] |
| 11.2 | Wireless access points authorized | [status] | [severity] | [ref] |
| 11.3 | Vulnerabilities identified and addressed | [status] | [severity] | [ref] |
| 11.4 | Penetration testing performed | [status] | [severity] | [ref] |
| 11.5 | Network intrusions detected and responded | [status] | [severity] | [ref] |
| 11.6 | Unauthorized changes detected | [status] | [severity] | [ref] |
| 12.1 | Security policy established | [status] | [severity] | [ref] |
| 12.2 | Acceptable use policies | [status] | [severity] | [ref] |
| 12.3 | Risks formally identified | [status] | [severity] | [ref] |
| 12.4 | PCI-DSS responsibilities assigned | [status] | [severity] | [ref] |
| 12.5 | PCI-DSS scope documented | [status] | [severity] | [ref] |
| 12.6 | Security awareness program | [status] | [severity] | [ref] |
| 12.7 | Personnel screened | [status] | [severity] | [ref] |
| 12.8 | Third-party service provider risk managed | [status] | [severity] | [ref] |
| 12.9 | TPSPs acknowledge responsibilities | [status] | [severity] | [ref] |
| 12.10 | Incident response plan | [status] | [severity] | [ref] |

---

## 5. Remediation Plan

### Priority Matrix

| Priority | Finding ID | Title | Framework(s) | Severity | Effort | Owner |
|----------|-----------|-------|--------------|----------|--------|-------|
| 1 | [ID] | [title] | [frameworks] | [severity] | [XS-XL] | [TBD] |

### Detailed Remediation Steps

For each finding requiring remediation:

**[Finding ID]: [Title]**
- **Regulatory Reference**: [specific article/section/requirement]
- **Current State**: [what exists today]
- **Required State**: [what must be in place]
- **Remediation Steps**:
  1. [Step 1 with specific technical or process action]
  2. [Step 2]
  3. [Step N]
- **Evidence Required**: [what documentation or artifacts to produce]
- **Estimated Effort**: [XS/S/M/L/XL]
- **Dependencies**: [other findings or external factors]
- **Suggested Timeline**: [specific date range based on severity]

---

## 6. Evidence Requirements for Certification

This section outlines the documentation and technical artifacts needed for each framework's certification or audit process.

### GDPR Evidence Pack
| Evidence Item | Description | Status | Location |
|--------------|-------------|--------|----------|
| Records of Processing Activities (ROPA) | Art. 30 register of all processing activities | [exists/needed] | [path] |
| Privacy Impact Assessments (DPIAs) | Art. 35 impact assessments for high-risk processing | [exists/needed] | [path] |
| Privacy Policy | Art. 12-13 public-facing privacy notice | [exists/needed] | [path] |
| Consent Records | Art. 7 records of consent given and withdrawn | [exists/needed] | [path] |
| Data Subject Request Procedures | Art. 15-22 procedures for handling DSARs | [exists/needed] | [path] |
| Data Processing Agreements | Art. 28 DPAs with all processors | [exists/needed] | [path] |
| Breach Response Plan | Art. 33-34 incident response procedures | [exists/needed] | [path] |
| Transfer Mechanisms | Art. 44-49 SCCs, adequacy, or BCRs | [exists/needed] | [path] |
| Legitimate Interest Assessments | Art. 6(1)(f) LIA documentation | [exists/needed] | [path] |
| Data Protection Officer Appointment | Art. 37 DPO designation (if required) | [exists/needed] | [path] |
| Training Records | Staff privacy training evidence | [exists/needed] | [path] |
| Technical and Organizational Measures | Art. 32 security measures documentation | [exists/needed] | [path] |

### HIPAA Evidence Pack
| Evidence Item | Description | Status | Location |
|--------------|-------------|--------|----------|
| Risk Analysis | 164.308(a)(1) comprehensive risk assessment | [exists/needed] | [path] |
| Risk Management Plan | 164.308(a)(1) risk mitigation strategy | [exists/needed] | [path] |
| Security Policies and Procedures | 164.316 complete policy documentation | [exists/needed] | [path] |
| Business Associate Agreements (BAAs) | 164.314 agreements with all BAs | [exists/needed] | [path] |
| Workforce Training Records | 164.308(a)(5) training evidence | [exists/needed] | [path] |
| Access Authorization Records | 164.308(a)(4) access management evidence | [exists/needed] | [path] |
| Incident Response Plan | 164.308(a)(6) security incident procedures | [exists/needed] | [path] |
| Contingency Plan | 164.308(a)(7) disaster recovery documentation | [exists/needed] | [path] |
| Audit Log Samples | 164.312(b) system activity records | [exists/needed] | [path] |
| Encryption Documentation | 164.312(a)(2)(iv) & 164.312(e)(2)(ii) encryption implementation records | [exists/needed] | [path] |
| Physical Safeguard Documentation | 164.310 facility security measures | [exists/needed] | [path] |
| Breach Notification Procedures | 164.402-414 breach response plan | [exists/needed] | [path] |
| Minimum Necessary Documentation | 164.502(b) minimum necessary determinations | [exists/needed] | [path] |
| Sanctions Policy | 164.308(a)(1)(ii)(C) workforce sanctions | [exists/needed] | [path] |

### SOC 2 Evidence Pack
| Evidence Item | Description | Status | Location |
|--------------|-------------|--------|----------|
| Security Policies | Comprehensive information security policies | [exists/needed] | [path] |
| Risk Assessment Report | Formal risk assessment documentation | [exists/needed] | [path] |
| Access Control Matrix | User access rights and role definitions | [exists/needed] | [path] |
| Change Management Records | Change request, approval, and deployment records | [exists/needed] | [path] |
| Incident Response Plan | Security incident response procedures | [exists/needed] | [path] |
| Vendor Management Documentation | Third-party risk assessment and monitoring | [exists/needed] | [path] |
| Business Continuity Plan | Disaster recovery and continuity documentation | [exists/needed] | [path] |
| Monitoring and Alerting Configuration | System monitoring and alerting setup | [exists/needed] | [path] |
| Penetration Test Reports | Annual penetration testing results | [exists/needed] | [path] |
| Vulnerability Scan Reports | Regular vulnerability scan results | [exists/needed] | [path] |
| Employee Handbook / Code of Conduct | Organizational commitment to integrity | [exists/needed] | [path] |
| Onboarding and Offboarding Checklists | User provisioning and deprovisioning | [exists/needed] | [path] |
| System Description | Description of the system and boundaries | [exists/needed] | [path] |
| Control Activities Documentation | Detailed control descriptions and evidence | [exists/needed] | [path] |

### CCPA Evidence Pack
| Evidence Item | Description | Status | Location |
|--------------|-------------|--------|----------|
| Privacy Policy (CCPA-specific) | Notice at collection with all required disclosures | [exists/needed] | [path] |
| Do Not Sell/Share Page | Consumer-facing opt-out mechanism | [exists/needed] | [path] |
| Data Inventory | Catalog of personal information collected and purposes | [exists/needed] | [path] |
| Consumer Request Procedures | Verified request handling workflows | [exists/needed] | [path] |
| Service Provider Agreements | Contracts restricting use of shared PI | [exists/needed] | [path] |
| Opt-Out Mechanism Documentation | Technical implementation of opt-out signals (GPC) | [exists/needed] | [path] |
| Training Records | Staff training on CCPA obligations | [exists/needed] | [path] |
| Financial Incentive Notices | If offering incentives for PI collection | [exists/needed] | [path] |
| Data Retention Schedule | Retention periods for each category of PI | [exists/needed] | [path] |
| Metrics / Request Log | Records of consumer requests received and fulfilled | [exists/needed] | [path] |

### PCI-DSS Evidence Pack
| Evidence Item | Description | Status | Location |
|--------------|-------------|--------|----------|
| Network Diagram | Current network topology with CDE boundaries | [exists/needed] | [path] |
| Data Flow Diagram | Cardholder data flow documentation | [exists/needed] | [path] |
| System Inventory | All systems in CDE scope | [exists/needed] | [path] |
| Security Policies | Information security policy document | [exists/needed] | [path] |
| Vulnerability Scan Reports | Internal and external (ASV) scan results | [exists/needed] | [path] |
| Penetration Test Reports | Annual internal and external pen test results | [exists/needed] | [path] |
| Access Control Documentation | User access management procedures and logs | [exists/needed] | [path] |
| Change Management Records | System change documentation and approvals | [exists/needed] | [path] |
| Incident Response Plan | Cardholder data breach response procedures | [exists/needed] | [path] |
| Encryption Key Management | Key lifecycle documentation | [exists/needed] | [path] |
| Security Awareness Training | Annual training records for all personnel | [exists/needed] | [path] |
| Vendor Risk Assessments | Third-party service provider evaluations | [exists/needed] | [path] |
| Firewall/NSC Rule Review | Documented review of network security controls | [exists/needed] | [path] |
| Anti-Malware Configuration | Malware protection deployment evidence | [exists/needed] | [path] |
| Log Retention Evidence | 12 months of audit log history (3 months immediately available) | [exists/needed] | [path] |
| Physical Security Documentation | Physical access control measures for CDE | [exists/needed] | [path] |
| Wireless Security Assessment | Wireless access point inventory and testing | [exists/needed] | [path] |
| Segmentation Testing Results | Validation that segmentation controls are effective | [exists/needed] | [path] |

---

## 7. Appendices

### Appendix A: Files Scanned
[List all files that were examined during the audit with their paths]

### Appendix B: Tools and Methods Used
[Describe the scanning approach, patterns searched, and tools used]

### Appendix C: Glossary
[See references/cross-framework-mapping.md for the standard glossary, or reproduce the relevant terms here.]

### Appendix D: Regulatory Reference Links
[See references/frameworks.md for the canonical list of regulatory reference links.]

### Appendix E: Severity Definitions
[See references/classification.md for severity and status definitions, or reproduce them here.]
```
