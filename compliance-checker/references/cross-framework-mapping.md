# Cross-Framework Requirement Mapping

Many regulatory requirements overlap. Use this mapping to identify when a single control satisfies multiple frameworks, and note in the remediation plan when one action closes gaps across several regulations.

| Control Area | GDPR | HIPAA | SOC 2 | CCPA | PCI-DSS |
|-------------|------|-------|-------|------|---------|
| Encryption at rest | Art. 32 | 164.312(a)(2)(iv) | CC6.1, CC6.7 | 1798.185 | Req 3.4-3.5 |
| Encryption in transit | Art. 32 | 164.312(e)(1) | CC6.7 | 1798.185 | Req 4.1 |
| Access controls | Art. 32 | 164.312(a)(1) | CC6.1-CC6.3 | 1798.185 | Req 7, 8 |
| Audit logging | Art. 30 | 164.312(b) | CC7.1-CC7.2 | -- | Req 10 |
| Breach notification | Art. 33-34 | 164.402-414 | CC7.3-CC7.4 | 1798.150 | Req 12.10 |
| Data retention | Art. 5(1)(e) | 164.530(j) | C1.2 | 1798.100(d) | Req 3.1 |
| Data minimization | Art. 5(1)(c) | 164.502(b) | C1.1 | 1798.100(e) | Req 3.1 |
| Consent management | Art. 6-7 | 164.508 | P1.1 | 1798.120 | -- |
| Right to access | Art. 15 | 164.524 | P1.1 | 1798.110 | -- |
| Right to delete | Art. 17 | -- | P1.1 | 1798.105 | -- |
| Data portability | Art. 20 | -- | -- | 1798.100 | -- |
| Vendor management | Art. 28 | 164.314 | CC9.2 | 1798.140(v) | Req 12.8 |
| Incident response | Art. 33 | 164.308(a)(6) | CC7.3-CC7.5 | -- | Req 12.10 |
| Risk assessment | Art. 35 | 164.308(a)(1) | CC3.1-CC3.2 | -- | Req 12.3 |
| Training | Art. 39 | 164.308(a)(5) | CC1.4 | -- | Req 12.6 |
| Change management | -- | 164.308(a)(8) | CC8.1 | -- | Req 6.5 |
| Vulnerability management | -- | 164.308(a)(1) | CC7.1 | -- | Req 6.3, 11.3 |
| Password/auth policy | Art. 32 | 164.312(d) | CC6.1-CC6.2 | 1798.185 | Req 8.3 |
| MFA | Art. 32 | 164.312(d) | CC6.1 | -- | Req 8.4 |
| Network security | Art. 32 | 164.312(e) | CC6.6 | -- | Req 1 |
| Backup/recovery | Art. 32 | 164.308(a)(7) | A1.2-A1.3 | -- | Req 12.10 |

## Glossary
| Term | Definition |
|------|-----------|
| PII | Personally Identifiable Information - any data that can identify a natural person |
| PHI | Protected Health Information - health data linked to an individual (HIPAA) |
| CHD | Cardholder Data - primary account number and related payment card data (PCI-DSS) |
| CDE | Cardholder Data Environment - systems that store, process, or transmit CHD |
| DSAR | Data Subject Access Request - individual's request to access their personal data |
| DPA | Data Processing Agreement - contract governing processor's handling of personal data |
| DPIA | Data Protection Impact Assessment - assessment of high-risk processing activities |
| SCC | Standard Contractual Clauses - EU-approved contract terms for international data transfers |
| BAA | Business Associate Agreement - HIPAA contract with entities handling PHI |
| ASV | Approved Scanning Vendor - PCI-approved external vulnerability scanning provider |
| ROPA | Records of Processing Activities - register required under GDPR Art. 30 |
| GPC | Global Privacy Control - browser signal for opting out of data sale/sharing |
| LIA | Legitimate Interest Assessment - documentation of Art. 6(1)(f) balancing test |
| TIA | Transfer Impact Assessment - evaluation of data protection in recipient country |
| NSC | Network Security Controls - firewalls and equivalent network protection mechanisms |
