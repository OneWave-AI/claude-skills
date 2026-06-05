# Output Template

Generate the report as `tech-dd-report.md` in the current working directory (or a user-specified output path). Follow this exact structure.

```markdown
# Technical Due Diligence Report

**Target**: [Company/Repository Name]
**Date**: [Current Date]
**Analyst**: Claude Technical Due Diligence Agent
**Engagement Type**: [M&A / Investment / Acquisition -- infer from context or state "General Assessment"]
**Confidentiality**: CONFIDENTIAL -- For authorized recipients only

---

## Executive Summary

[2-3 paragraph summary of key findings, overall technical health assessment, and headline recommendation. Write this for a non-technical investment committee member. Lead with the conclusion, then support it.]

**Overall Technical Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

**Headline Recommendation**: [GO / CONDITIONAL GO / NO-GO]

[If CONDITIONAL GO, list the 3-5 conditions that must be met]

**Estimated Total Technical Debt Remediation**: [X] engineer-weeks ([Y] at $8,000/engineer-week = $[Z])

---

## Table of Contents

1. Company and Repository Overview
2. Architecture Assessment
3. Code Quality and Technical Debt
4. Security Posture
5. Scalability and Performance
6. Test Coverage and Quality Assurance
7. Build System and Deployment Maturity
8. Team and Organizational Analysis
9. Dependency and License Risk
10. Documentation and Knowledge Management
11. Risk Register
12. Remediation Roadmap
13. Financial Impact Summary
14. Go/No-Go Recommendation

---

## 1. Company and Repository Overview

### 1.1 Repository Statistics

| Metric | Value |
|--------|-------|
| Repository Age | [X years, Y months] |
| Total Files | [N] |
| Total Lines of Code | [N] (excluding blanks/comments where measurable) |
| Primary Language(s) | [Language 1 (X%), Language 2 (Y%)] |
| Active Contributors (last 6 months) | [N] |
| Total Historical Contributors | [N] |
| Last Commit Date | [Date] |
| Commit Frequency (last 3 months) | [N commits/week average] |

### 1.2 Technology Stack Summary

| Layer | Technology |
|-------|-----------|
| Frontend | [Framework, libraries] |
| Backend | [Language, framework] |
| Database | [Type, specific technology] |
| Caching | [Technology or "None identified"] |
| Message Queue | [Technology or "None identified"] |
| Search | [Technology or "None identified"] |
| Infrastructure | [Cloud provider, orchestration] |
| CI/CD | [Platform, tools] |
| Monitoring | [Tools or "None identified"] |

### 1.3 Repository Structure

[Brief description of top-level organization with directory tree for context]

---

## 2. Architecture Assessment

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

### 2.1 Architectural Style

[Description of the identified architectural style with evidence]

### 2.2 Component Map

[Description of major components, their responsibilities, and how they interact]

### 2.3 Data Flow

[Description of how data moves through the system, from ingestion to storage to presentation]

### 2.4 API Design

[Assessment of API design quality, consistency, versioning strategy]

### 2.5 Architecture Findings

| ID | Finding | Risk | Evidence | Remediation | Effort |
|----|---------|------|----------|-------------|--------|
| ARCH-001 | [Finding] | [Rating] | [File/pattern reference] | [Recommended fix] | [X eng-weeks] |
| ARCH-002 | [Finding] | [Rating] | [File/pattern reference] | [Recommended fix] | [X eng-weeks] |

---

## 3. Code Quality and Technical Debt

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

### 3.1 Code Quality Metrics

| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| Average Function Length | [X lines] | < 30 lines | [PASS/WARN/FAIL] |
| Max File Length | [X lines] | < 500 lines | [PASS/WARN/FAIL] |
| TODO/FIXME Count | [N] | < 50 | [PASS/WARN/FAIL] |
| Type Coverage | [X%] | > 80% | [PASS/WARN/FAIL] |
| Linting Configured | [Yes/No] | Yes | [PASS/WARN/FAIL] |
| Formatting Configured | [Yes/No] | Yes | [PASS/WARN/FAIL] |

### 3.2 Technical Debt Inventory

| Category | Description | Severity | Estimated Remediation |
|----------|-------------|----------|----------------------|
| [Category] | [Specific debt item] | [Rating] | [X eng-weeks] |

### 3.3 Code Quality Findings

| ID | Finding | Risk | Evidence | Remediation | Effort |
|----|---------|------|----------|-------------|--------|
| CQ-001 | [Finding] | [Rating] | [File/pattern reference] | [Recommended fix] | [X eng-weeks] |

---

## 4. Security Posture

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

### 4.1 Security Controls Assessment

| Control | Status | Details |
|---------|--------|---------|
| Authentication | [Implemented/Partial/Missing] | [Description] |
| Authorization | [Implemented/Partial/Missing] | [Description] |
| Input Validation | [Implemented/Partial/Missing] | [Description] |
| SQL Injection Prevention | [Implemented/Partial/Missing] | [Description] |
| XSS Prevention | [Implemented/Partial/Missing] | [Description] |
| CSRF Prevention | [Implemented/Partial/Missing] | [Description] |
| Rate Limiting | [Implemented/Partial/Missing] | [Description] |
| Secrets Management | [Implemented/Partial/Missing] | [Description] |
| Security Headers | [Implemented/Partial/Missing] | [Description] |
| Dependency Vulnerability Scanning | [Implemented/Partial/Missing] | [Description] |

### 4.2 Security Findings

| ID | Finding | Risk | OWASP Category | Evidence | Remediation | Effort |
|----|---------|------|----------------|----------|-------------|--------|
| SEC-001 | [Finding] | [Rating] | [Category] | [File/line reference] | [Recommended fix] | [X eng-weeks] |

### 4.3 Credentials and Secrets Audit

[Report on any credentials, API keys, tokens, or secrets found committed to the repository. If none found, state so explicitly.]

---

## 5. Scalability and Performance

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

### 5.1 Scalability Assessment

| Dimension | Current State | Scaling Strategy | Headroom Estimate |
|-----------|--------------|------------------|-------------------|
| Compute | [Description] | [Strategy] | [Estimate] |
| Database | [Description] | [Strategy] | [Estimate] |
| Storage | [Description] | [Strategy] | [Estimate] |
| Network/API | [Description] | [Strategy] | [Estimate] |

### 5.2 Performance Findings

| ID | Finding | Risk | Evidence | Remediation | Effort |
|----|---------|------|----------|-------------|--------|
| PERF-001 | [Finding] | [Rating] | [File/pattern reference] | [Recommended fix] | [X eng-weeks] |

---

## 6. Test Coverage and Quality Assurance

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

### 6.1 Test Coverage Summary

| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| Test-to-Source File Ratio | [X:1] | > 0.5:1 | [PASS/WARN/FAIL] |
| Estimated Code Coverage | [X%] | > 70% | [PASS/WARN/FAIL] |
| Unit Tests Present | [Yes/No] | Yes | [PASS/WARN/FAIL] |
| Integration Tests Present | [Yes/No] | Yes | [PASS/WARN/FAIL] |
| E2E Tests Present | [Yes/No] | Yes | [PASS/WARN/FAIL] |
| Tests in CI Pipeline | [Yes/No] | Yes | [PASS/WARN/FAIL] |
| Skipped/Disabled Tests | [N] | < 10 | [PASS/WARN/FAIL] |

### 6.2 Test Quality Assessment

[Assessment of test quality based on sampled test files, including specific examples of good and poor testing patterns found]

### 6.3 Testing Findings

| ID | Finding | Risk | Evidence | Remediation | Effort |
|----|---------|------|----------|-------------|--------|
| TEST-001 | [Finding] | [Rating] | [File/pattern reference] | [Recommended fix] | [X eng-weeks] |

---

## 7. Build System and Deployment Maturity

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

**Deployment Maturity Level**: [1-5] / 5

### 7.1 CI/CD Pipeline Assessment

| Stage | Implemented | Details |
|-------|------------|---------|
| Build | [Yes/No] | [Description] |
| Unit Tests | [Yes/No] | [Description] |
| Integration Tests | [Yes/No] | [Description] |
| Linting/Static Analysis | [Yes/No] | [Description] |
| Security Scanning | [Yes/No] | [Description] |
| Staging Deployment | [Yes/No] | [Description] |
| Production Deployment | [Yes/No] | [Description] |
| Approval Gates | [Yes/No] | [Description] |
| Rollback Mechanism | [Yes/No] | [Description] |

### 7.2 Infrastructure Assessment

| Aspect | Status | Details |
|--------|--------|---------|
| Infrastructure as Code | [Yes/Partial/No] | [Description] |
| Containerization | [Yes/Partial/No] | [Description] |
| Environment Parity | [High/Medium/Low] | [Description] |
| Database Migrations | [Managed/Manual/None] | [Description] |
| Feature Flags | [Yes/No] | [Description] |
| Monitoring/Alerting | [Yes/Partial/No] | [Description] |
| Logging Infrastructure | [Yes/Partial/No] | [Description] |

### 7.3 Build and Deploy Findings

| ID | Finding | Risk | Evidence | Remediation | Effort |
|----|---------|------|----------|-------------|--------|
| DEP-001 | [Finding] | [Rating] | [File/pattern reference] | [Recommended fix] | [X eng-weeks] |

---

## 8. Team and Organizational Analysis

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

### 8.1 Team Composition (from Git History)

| Contributor | Commits | First Active | Last Active | Primary Areas |
|------------|---------|--------------|-------------|---------------|
| [Name/Handle] | [N] | [Date] | [Date] | [Directories/components] |

### 8.2 Bus Factor Analysis

| Component/Area | Primary Owner | Backup Owner(s) | Bus Factor | Risk |
|---------------|---------------|------------------|------------|------|
| [Component] | [Contributor] | [Contributor(s) or "None"] | [1-N] | [Rating] |

### 8.3 Development Velocity Trends

[Analysis of commit frequency trends over time -- is velocity increasing, stable, or declining?]

### 8.4 Team Findings

| ID | Finding | Risk | Evidence | Remediation | Effort |
|----|---------|------|----------|-------------|--------|
| TEAM-001 | [Finding] | [Rating] | [Evidence from git history] | [Recommended action] | [X eng-weeks] |

---

## 9. Dependency and License Risk

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

### 9.1 Dependency Statistics

| Metric | Value |
|--------|-------|
| Direct Dependencies | [N] |
| Transitive Dependencies (estimated) | [N] |
| Dependencies with Known CVEs | [N] |
| Unmaintained Dependencies (no update 12+ months) | [N] |
| Single-Maintainer Dependencies | [N identified] |

### 9.2 License Distribution

| License Type | Count | Risk Level | Action Required |
|-------------|-------|------------|-----------------|
| MIT | [N] | LOW | None |
| Apache 2.0 | [N] | LOW | None |
| BSD (2/3-clause) | [N] | LOW | None |
| ISC | [N] | LOW | None |
| LGPL | [N] | MEDIUM | Legal review recommended |
| MPL 2.0 | [N] | MEDIUM | Legal review recommended |
| GPL v2/v3 | [N] | HIGH | Legal review required |
| AGPL | [N] | CRITICAL | Immediate legal review required |
| No License | [N] | CRITICAL | Cannot use without explicit permission |
| Unknown/Custom | [N] | HIGH | Legal review required |

### 9.3 Critical Dependency Assessment

[Assessment of the 10-20 most important dependencies with maintenance status, community health, and risk notes]

### 9.4 Dependency Findings

| ID | Finding | Risk | Evidence | Remediation | Effort |
|----|---------|------|----------|-------------|--------|
| LIC-001 | [Finding] | [Rating] | [Package/license reference] | [Recommended fix] | [X eng-weeks] |

---

## 10. Documentation and Knowledge Management

**Risk Rating**: [CRITICAL / HIGH / MEDIUM / LOW / NEGLIGIBLE]

### 10.1 Documentation Inventory

| Document Type | Present | Quality (1-5) | Notes |
|--------------|---------|---------------|-------|
| README | [Yes/No] | [1-5] | [Assessment] |
| API Documentation | [Yes/No] | [1-5] | [Assessment] |
| Architecture Docs | [Yes/No] | [1-5] | [Assessment] |
| Setup/Onboarding Guide | [Yes/No] | [1-5] | [Assessment] |
| ADRs (Architecture Decision Records) | [Yes/No] | [1-5] | [Assessment] |
| Runbooks/Playbooks | [Yes/No] | [1-5] | [Assessment] |
| Changelog | [Yes/No] | [1-5] | [Assessment] |
| Inline Code Documentation | [Adequate/Sparse/None] | [1-5] | [Assessment] |

### 10.2 Documentation Findings

| ID | Finding | Risk | Evidence | Remediation | Effort |
|----|---------|------|----------|-------------|--------|
| DOC-001 | [Finding] | [Rating] | [Reference] | [Recommended fix] | [X eng-weeks] |

---

## 11. Risk Register

This section consolidates all findings into a single prioritized risk register.

### 11.1 Critical and High Risks

| ID | Category | Finding | Risk | Business Impact | Remediation | Effort | Priority |
|----|----------|---------|------|-----------------|-------------|--------|----------|
| [From above] | [Category] | [Summary] | CRITICAL/HIGH | [Impact description] | [Fix] | [X eng-weeks] | [P0/P1] |

### 11.2 Medium Risks

| ID | Category | Finding | Risk | Remediation | Effort | Priority |
|----|----------|---------|------|-------------|--------|----------|
| [From above] | [Category] | [Summary] | MEDIUM | [Fix] | [X eng-weeks] | [P2] |

### 11.3 Low and Negligible Risks

[Summarized in paragraph form -- these do not require individual tracking but are noted for completeness]

---

## 12. Remediation Roadmap

### 12.1 Immediate (Pre-Close or First 30 Days)

[Items that must be addressed before closing the deal or within the first month post-close]

| Priority | Item | Effort | Cost Estimate |
|----------|------|--------|---------------|
| P0 | [Item] | [X eng-weeks] | $[Y] |

### 12.2 Short-Term (30-90 Days Post-Close)

[Items that should be addressed in the first quarter after closing]

| Priority | Item | Effort | Cost Estimate |
|----------|------|--------|---------------|
| P1 | [Item] | [X eng-weeks] | $[Y] |

### 12.3 Medium-Term (90-180 Days Post-Close)

[Items that can be addressed in the second quarter after closing]

| Priority | Item | Effort | Cost Estimate |
|----------|------|--------|---------------|
| P2 | [Item] | [X eng-weeks] | $[Y] |

### 12.4 Long-Term (6-12 Months Post-Close)

[Strategic improvements and technical vision items]

| Priority | Item | Effort | Cost Estimate |
|----------|------|--------|---------------|
| P3 | [Item] | [X eng-weeks] | $[Y] |

---

## 13. Financial Impact Summary

### 13.1 Technical Debt Remediation Costs

| Category | Engineer-Weeks | Cost at $8,000/week |
|----------|---------------|---------------------|
| Architecture | [X] | $[Y] |
| Code Quality | [X] | $[Y] |
| Security | [X] | $[Y] |
| Scalability | [X] | $[Y] |
| Testing | [X] | $[Y] |
| DevOps/Deployment | [X] | $[Y] |
| Documentation | [X] | $[Y] |
| Dependencies/Licensing | [X] | $[Y] |
| **Total** | **[X]** | **$[Y]** |

### 13.2 Ongoing Maintenance Estimate

[Estimate of ongoing engineering effort required to maintain the codebase at its current scale, expressed in FTE (full-time equivalent) engineers]

### 13.3 Scaling Investment Estimate

[Estimate of engineering investment required to scale the platform to 2x, 5x, and 10x current capacity]

| Scale Target | Estimated Investment | Timeline | Key Changes Required |
|-------------|---------------------|----------|---------------------|
| 2x current | [X eng-months] | [Y months] | [Summary] |
| 5x current | [X eng-months] | [Y months] | [Summary] |
| 10x current | [X eng-months] | [Y months] | [Summary] |

---

## 14. Go/No-Go Recommendation

### 14.1 Recommendation

**[GO / CONDITIONAL GO / NO-GO]**

### 14.2 Rationale

[3-5 paragraphs explaining the recommendation, structured as:]

**Strengths**: [What the codebase does well that supports a positive investment thesis]

**Concerns**: [Material risks that could impact the investment thesis]

**Mitigating Factors**: [Factors that reduce the severity of identified concerns]

**Deal Considerations**: [How technical findings should influence deal terms -- escrow, reps and warranties, earnout structure, retention packages for key engineers]

### 14.3 Conditions (if Conditional Go)

[Numbered list of specific, measurable conditions that must be met or agreed upon for the deal to proceed]

1. [Condition 1]
2. [Condition 2]
3. [Condition N]

### 14.4 Due Diligence Gaps

[List any areas that could not be fully assessed from the codebase alone and recommend follow-up actions]

| Gap | Recommended Follow-Up | Priority |
|-----|----------------------|----------|
| [Gap] | [Action -- e.g., interview CTO, request access to monitoring dashboards] | [HIGH/MEDIUM/LOW] |

---

## Appendix A: Files Examined

[List of specific files that were read and analyzed during this assessment, organized by investigation phase]

## Appendix B: Tools and Methods

[Description of the analysis methodology, tools used, and any limitations of the assessment]

## Appendix C: Glossary

| Term | Definition |
|------|-----------|
| Bus Factor | The minimum number of team members who would need to leave before critical project knowledge is lost |
| Engineer-Week | 40 hours of senior software engineer time, estimated at $8,000 blended cost |
| Tech Debt | Implementation shortcuts or deferred maintenance that increase future development cost |
| OWASP Top 10 | The ten most critical web application security risks as defined by the Open Web Application Security Project |
| IaC | Infrastructure as Code -- managing infrastructure through machine-readable definition files |
| CVE | Common Vulnerabilities and Exposures -- a catalog of publicly known security vulnerabilities |
| SAST | Static Application Security Testing -- analyzing source code for security vulnerabilities |
| SLA | Service Level Agreement -- contractual commitment to service availability and performance |
```
