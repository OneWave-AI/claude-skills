# Supported Regulatory Frameworks

Audit against the following frameworks. When the user does not specify which frameworks to check, audit against all of them and note which apply based on the nature of the codebase or business process.

## 1. GDPR (General Data Protection Regulation)
- Scope: Any system that processes personal data of EU/EEA residents
- Key Articles: Art. 5 (principles), Art. 6 (lawful basis), Art. 7 (consent), Art. 12-23 (data subject rights), Art. 25 (data protection by design), Art. 28 (processors), Art. 30 (records of processing), Art. 32 (security), Art. 33-34 (breach notification), Art. 35 (DPIA), Art. 44-49 (international transfers)
- Penalties: Up to 4% of annual global turnover or EUR 20 million

## 2. HIPAA (Health Insurance Portability and Accountability Act)
- Scope: Covered entities and business associates handling Protected Health Information (PHI)
- Key Rules: Privacy Rule, Security Rule (Administrative/Physical/Technical Safeguards), Breach Notification Rule, Enforcement Rule
- Key Standards: 164.308 (Administrative), 164.310 (Physical), 164.312 (Technical), 164.314 (Organizational), 164.316 (Policies/Documentation)
- Penalties: $100 to $50,000 per violation, up to $1.5 million per year per category

## 3. SOC 2 (Service Organization Control 2)
- Scope: Service organizations that store, process, or transmit customer data
- Trust Service Criteria: Security (CC1-CC9), Availability (A1), Processing Integrity (PI1), Confidentiality (C1), Privacy (P1)
- Common Criteria: CC1 (Control Environment), CC2 (Communication), CC3 (Risk Assessment), CC4 (Monitoring), CC5 (Control Activities), CC6 (Logical/Physical Access), CC7 (System Operations), CC8 (Change Management), CC9 (Risk Mitigation)

## 4. CCPA (California Consumer Privacy Act) / CPRA
- Scope: Businesses collecting personal information of California residents meeting revenue/data thresholds
- Key Rights: Right to Know, Right to Delete, Right to Opt-Out of Sale/Sharing, Right to Non-Discrimination, Right to Correct, Right to Limit Use of Sensitive PI
- Key Sections: 1798.100 (general duties), 1798.105 (deletion), 1798.110 (disclosure), 1798.115 (sale/sharing disclosure), 1798.120 (opt-out), 1798.121 (limit sensitive PI), 1798.125 (non-discrimination)
- Penalties: $2,500 per unintentional violation, $7,500 per intentional violation

## 5. PCI-DSS (Payment Card Industry Data Security Standard) v4.0
- Scope: Any entity that stores, processes, or transmits cardholder data
- Requirements: Req 1 (Network Security Controls), Req 2 (Secure Configurations), Req 3 (Protect Stored Account Data), Req 4 (Cryptography in Transit), Req 5 (Malware Protection), Req 6 (Secure Development), Req 7 (Restrict Access), Req 8 (Identify Users/Auth), Req 9 (Physical Access), Req 10 (Log/Monitor), Req 11 (Security Testing), Req 12 (Security Policies)
- Penalties: $5,000 to $100,000 per month of non-compliance, potential loss of card processing privileges

## Regulatory Reference Links
- GDPR Full Text: https://eur-lex.europa.eu/eli/reg/2016/679/oj
- HIPAA Security Rule: https://www.hhs.gov/hipaa/for-professionals/security/index.html
- SOC 2 Trust Service Criteria: https://us.aicpa.org/interestareas/frc/assuranceadvisoryservices/trustservicescriteria
- CCPA/CPRA Text: https://leginfo.legislature.ca.gov/faces/codes_displayText.xhtml?division=3.&part=4.&lawCode=CIV&title=1.81.5
- PCI-DSS v4.0: https://www.pcisecuritystandards.org/document_library/
