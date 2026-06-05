# Scan Categories and Search Patterns

For each category, document what was found, where it was found, and how it relates to each applicable framework. Many findings are about what is missing, not what is present, so actively check for the absence of required controls.

## 2.1 PII / Sensitive Data Handling
Scan for:
- Database schemas containing personal data fields (name, email, phone, address, SSN, DOB, IP address, device identifiers, biometric data, genetic data, health data, financial data, location data)
- Code that reads, writes, transforms, or transmits personal data
- Hardcoded personal data in source code, configuration files, or test fixtures
- Personal data in log output, error messages, or debug statements
- Data classification labels or lack thereof
- Data inventory or Records of Processing Activities (ROPA) documentation

Search patterns:
```
- Field names: email, phone, ssn, social_security, date_of_birth, dob, address, credit_card, card_number, cvv, pan, first_name, last_name, ip_address, device_id, location, latitude, longitude, biometric, health, diagnosis, prescription, medical
- Table/collection names: users, customers, patients, members, accounts, profiles, contacts, employees, cardholders, beneficiaries
- Code patterns: PII, PHI, personally_identifiable, protected_health, cardholder_data, sensitive_data
- File patterns: .env, .env.*, config.*, secrets.*, credentials.*, *.pem, *.key, *.cert
```

## 2.2 Data Retention
Scan for:
- Retention policies defined in code or documentation
- TTL (time-to-live) configurations on database records or cache entries
- Scheduled deletion jobs, data purge scripts, or archival processes
- Backup retention policies
- Log retention configurations
- Absence of retention policies (which is itself a finding)
- Data lifecycle management documentation

Search patterns:
```
- Keywords: retention, ttl, expire, expiry, expiration, purge, archive, delete_after, cleanup, data_lifecycle, retention_period, dispose, destroy
- Cron jobs or scheduled tasks related to data cleanup
- Database migration files that add or modify retention-related columns
- Configuration for log rotation and retention
```

## 2.3 Encryption
Scan for:
- Encryption at rest: database encryption, file encryption, disk encryption configuration
- Encryption in transit: TLS/SSL configuration, certificate management, HTTPS enforcement
- Key management: key storage, rotation policies, key derivation functions
- Cryptographic algorithm choices (flag weak algorithms: MD5, SHA1 for security purposes, DES, 3DES, RC4, RSA < 2048 bits, ECC < 256 bits)
- Password hashing algorithms (flag weak: MD5, SHA1, plain SHA256 without salt; approve: bcrypt, scrypt, Argon2, PBKDF2 with sufficient iterations)
- Secrets management (hardcoded secrets, environment variable handling, secrets vault integration)
- Certificate pinning in mobile or API client code

Search patterns:
```
- Keywords: encrypt, decrypt, cipher, aes, rsa, tls, ssl, https, certificate, cert, key_management, kms, vault, secret, hash, bcrypt, scrypt, argon2, pbkdf2, md5, sha1, sha256, hmac, salt, iv, nonce, padding
- Configuration: ssl_mode, sslmode, require_ssl, force_ssl, min_tls_version, cipher_suite
- Files: *.pem, *.key, *.cert, *.crt, *.pfx, *.p12, *.jks, *.keystore
```

## 2.4 Access Controls
Scan for:
- Authentication mechanisms (password policies, MFA/2FA, session management, token handling)
- Authorization models (RBAC, ABAC, ACLs, permission systems)
- Principle of least privilege implementation
- Service account management
- API key management and rotation
- Admin/superuser access controls and segregation
- Identity provider integration (SSO, SAML, OIDC, OAuth)
- Access review and recertification processes
- Default credentials or overly permissive configurations

Search patterns:
```
- Keywords: auth, authenticate, authorize, permission, role, rbac, abac, acl, access_control, privilege, admin, superuser, root, sudo, service_account, api_key, token, session, jwt, oauth, saml, oidc, sso, mfa, 2fa, totp, password_policy, login, logout
- Configuration: cors, allowed_origins, allowed_hosts, csrf, rate_limit, throttle, brute_force
- Middleware/decorators: @auth, @login_required, @requires_permission, @admin_only, requireAuth, isAuthenticated, checkPermission
```

## 2.5 Audit Logging
Scan for:
- Logging of authentication events (login, logout, failed attempts, password changes)
- Logging of authorization decisions (access granted, access denied)
- Logging of data access events (read, create, update, delete of regulated data)
- Logging of administrative actions (configuration changes, user management)
- Logging of data export or data transfer events
- Log integrity protection (tamper-evident logging, write-once storage, log signing)
- Log monitoring and alerting configuration
- Log aggregation and SIEM integration
- Absence of audit logging for critical operations

Search patterns:
```
- Keywords: audit, audit_log, audit_trail, event_log, activity_log, access_log, security_log, log_event, track, record_action, compliance_log, siem, splunk, datadog, cloudwatch, elastic
- Functions: logger, log.info, log.warn, log.error, audit.log, createAuditEntry, recordEvent, trackActivity
- Tables/collections: audit_logs, event_logs, activity_logs, access_logs, security_events
```

## 2.6 Consent Management
Scan for:
- Cookie consent implementation (banner, preference center, granular controls)
- Marketing consent collection and storage
- Privacy policy acceptance tracking
- Consent withdrawal mechanisms
- Purpose limitation enforcement (using data only for consented purposes)
- Consent versioning (tracking which version of terms/policy a user consented to)
- Age verification and parental consent (if processing minor's data)
- Legitimate interest assessments
- Double opt-in for email marketing

Search patterns:
```
- Keywords: consent, opt_in, opt_out, cookie_consent, cookie_banner, privacy_policy, terms_of_service, tos, gdpr_consent, marketing_consent, unsubscribe, preference, cookie_preference, purpose, legitimate_interest, dsar, data_subject, age_verification, parental_consent, double_opt_in
- Components/templates: CookieBanner, ConsentManager, PrivacyModal, OptOutForm, PreferenceCenter, UnsubscribeLink
- Database fields: consented_at, consent_version, marketing_opt_in, cookie_preferences, privacy_accepted
```

## 2.7 Data Transfer
Scan for:
- Cross-border data transfer mechanisms (Standard Contractual Clauses, adequacy decisions, Binding Corporate Rules, derogations)
- Third-party data sharing (analytics, advertising, subprocessors)
- API integrations that transmit regulated data
- Data export functionality
- Backup replication to other regions/jurisdictions
- CDN configuration and data caching locations
- Cloud provider region configuration
- Data Processing Agreements (DPAs) with subprocessors
- Transfer Impact Assessments (TIAs)

Search patterns:
```
- Keywords: transfer, export, share, third_party, subprocessor, vendor, analytics, tracking, pixel, beacon, cdn, region, jurisdiction, cross_border, scc, standard_contractual, adequacy, bcr, dpa, data_processing_agreement
- Services: google_analytics, segment, mixpanel, amplitude, hotjar, intercom, zendesk, stripe, twilio, sendgrid, mailchimp, aws_region, gcp_region, azure_region, cloudflare
- Configuration: region, availability_zone, data_residency, geo_restriction
```

## Scan Execution Rules
1. Be thorough. Search across all file types, not just source code. Include configuration files, infrastructure-as-code templates, documentation, CI/CD pipelines, Docker files, and dependency manifests.
2. Use multiple search strategies. Combine filename patterns, content patterns, and directory structure analysis. A single grep is never sufficient.
3. Check for absence. Actively check for the absence of required controls.
4. Note context. A finding in a test file has different significance than the same pattern in production code.
5. Follow the data. Trace regulated data from ingestion through processing to storage and deletion. Every touchpoint is a potential compliance checkpoint.
6. Check dependencies. Review package manifests (package.json, requirements.txt, Gemfile, go.mod, pom.xml) for libraries related to compliance functions (encryption, auth, logging, consent).
7. Review infrastructure. Check infrastructure-as-code files (Terraform, CloudFormation, Pulumi, Ansible, Kubernetes manifests) that define security controls, network isolation, encryption settings, and access policies.
8. Examine CI/CD. Review pipeline configurations for security scanning, dependency checking, secrets detection, and deployment controls.
9. Do not assume. If you cannot find evidence of a control, report it as a gap. Do not assume controls exist outside the codebase unless documentation or configuration references them.
10. Preserve evidence. Record exact file paths, line numbers, and code snippets for every finding, both positive (evidence of compliance) and negative (evidence of gaps).

## Common Compliance Pitfalls to Always Check
1. Logging PII: Applications often log personal data in debug/error output without redaction.
2. Test data leakage: Real PII used in test fixtures, seed data, or staging environments.
3. Overly broad data collection: Collecting more data than necessary for the stated purpose.
4. Missing deletion cascades: User deletion not propagating to all data stores, backups, logs, and third-party systems.
5. Stale access: No process for revoking access when employees leave or change roles.
6. Unencrypted backups: Database backups stored without encryption.
7. Missing HTTPS redirects: HTTP endpoints not redirecting to HTTPS.
8. Weak session management: Long-lived tokens, missing session invalidation on password change.
9. Missing CORS configuration: Overly permissive cross-origin policies.
10. Hardcoded secrets: API keys, passwords, or tokens in source code.
11. Missing rate limiting: No protection against brute force or enumeration attacks.
12. Insecure defaults: Debug mode enabled, verbose error messages in production, default credentials.
13. Missing cookie flags: Secure, HttpOnly, SameSite flags not set on session cookies.
14. No CSP headers: Missing Content-Security-Policy headers.
15. Unvalidated redirects: Open redirect vulnerabilities that could be used in phishing.
16. Missing data classification: No system for classifying data sensitivity levels.
17. Shadow data stores: Data copied to caches, search indexes, or analytics systems without the same protections.
18. Incomplete consent flows: Consent collected but not enforced in data processing logic.
19. Missing GPC/DNT support: Not honoring Global Privacy Control or Do Not Track signals (CCPA requirement).
20. Insecure direct object references: Accessing other users' data by changing IDs in URLs/requests.
