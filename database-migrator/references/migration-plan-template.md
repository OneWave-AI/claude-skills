# migration-plan.md Template

Write the final deliverable using this structure.

```markdown
# Database Migration Plan: [Source Provider] to [Target Provider]

**Generated**: [timestamp]
**Source**: [provider] [version] at [host/connection]
**Target**: [provider] [version] at [host/connection]
**Total tables**: [N]
**Total estimated rows**: [N]
**Total estimated data size**: [N GB]
**Estimated downtime**: [N hours N minutes]
**Migration strategy**: [Offline / Online with dual-write / Replication-based]

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Migration Scope](#migration-scope)
3. [Schema Inventory](#schema-inventory)
4. [Data Type Mapping](#data-type-mapping)
5. [Incompatibilities and Workarounds](#incompatibilities-and-workarounds)
6. [Migration Scripts](#migration-scripts)
7. [Data Migration Procedure](#data-migration-procedure)
8. [Trigger and Procedure Translation](#trigger-and-procedure-translation)
9. [Validation Plan](#validation-plan)
10. [Rollback Procedures](#rollback-procedures)
11. [Downtime Estimate](#downtime-estimate)
12. [Risk Assessment](#risk-assessment)
13. [Pre-Migration Checklist](#pre-migration-checklist)
14. [Step-by-Step Execution Guide](#step-by-step-execution-guide)
15. [Post-Migration Verification](#post-migration-verification)
16. [Application Changes Required](#application-changes-required)

## Executive Summary

[2-3 paragraphs: what is being migrated, why, key risks, data volume,
estimated downtime, recommended strategy, and critical incompatibilities
that require attention.]

## Migration Scope

- **Source**: [provider, version, host, schema/database name]
- **Target**: [provider, version, host, schema/database name]
- **Tables included**: [N] (list or "all")
- **Tables excluded**: [list, if any, with reasons]
- **Data scope**: [Full / Partial (e.g., last 90 days)]
- **Includes triggers**: [Yes/No -- count]
- **Includes stored procedures**: [Yes/No -- count]
- **Includes views**: [Yes/No -- count]

## Schema Inventory

### Table Summary
| # | Table Name | Columns | Rows (est.) | Size (est.) | Foreign Keys | Indexes | Triggers | Notes |
|---|-----------|---------|-------------|-------------|-------------|---------|----------|-------|
| 1 | users | 12 | 50,000 | 15 MB | 0 | 3 | 1 | -- |
| 2 | orders | 18 | 1,200,000 | 890 MB | 3 | 7 | 2 | Largest table |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

### Enums and Custom Types
[List all enums, custom types, and their translation strategy]

### Sequences
[List all sequences and their translation strategy]

## Data Type Mapping

[Table showing every column's source type, target type, and any transformation needed]

| Table | Column | Source Type | Target Type | Transformation | Risk |
|-------|--------|-----------|-------------|----------------|------|
| users | id | UUID | CHAR(36) | None | Low |
| users | metadata | JSONB | JSON | Loses GIN index; add generated columns | Medium |
| orders | total | NUMERIC(12,4) | DECIMAL(12,4) | None | Low |
| ... | ... | ... | ... | ... | ... |

## Incompatibilities and Workarounds

[List every feature that does not translate directly, with the recommended workaround]

| Feature | Source Behavior | Target Limitation | Workaround |
|---------|---------------|-------------------|------------|
| JSONB GIN indexes | Native indexed JSON queries | JSON type without GIN | Add generated columns + B-tree indexes |
| Array columns | Native ARRAY type | No native arrays | Store as JSON array |
| ... | ... | ... | ... |

## Migration Scripts

[Include or reference the generated DDL scripts, organized by execution order]

### Table Creation Order
1. [table with no FK dependencies]
2. [table with no FK dependencies]
3. [table depending on #1]
4. ...

### DDL Scripts
[Full CREATE TABLE, INDEX, CONSTRAINT statements]

### Deferred Constraints
[ALTER TABLE statements for cyclic foreign keys, to run after all tables exist]

## Data Migration Procedure

[Step-by-step data export, transform, load instructions]

## Trigger and Procedure Translation

[For each trigger and procedure: original source code, translated target code, behavioral differences]

## Validation Plan

### Row Count Checks
[Queries to compare row counts between source and target]

### Data Checksum Checks
[Queries to compare checksums of critical tables]

### Referential Integrity Checks
[Queries to verify foreign key integrity in the target]

### Index Verification
[Queries to verify all indexes exist in the target]

### Sample Data Spot-Checks
[Specific rows to compare between source and target]

## Rollback Procedures

### Full Rollback
[Complete rollback script to reverse the migration]

### Partial Rollback (per-table)
[Rollback scripts for individual tables if a single table fails]

### Application Rollback
[Steps to revert application connection strings and code changes]

### Backup and Restore
[Backup commands to run before migration; restore commands for recovery]

## Downtime Estimate

| Phase | Estimated Duration | Can Run Before Maintenance Window |
|-------|-------------------|----------------------------------|
| Pre-create schema | [N min] | Yes |
| Export data from source | [N min] | Yes (if acceptable staleness) |
| Transfer data | [N min] | Depends on strategy |
| Import data to target | [N min] | No (requires write lock) |
| Create indexes | [N min] | After import |
| Run validation | [N min] | After import |
| Application switchover | [N min] | Final step |
| **Total maintenance window** | **[N hours N min]** | -- |
| **Total with buffer (20%)** | **[N hours N min]** | -- |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Data type precision loss | [L/M/H] | [L/M/H] | [Mitigation] |
| Trigger behavior difference | [L/M/H] | [L/M/H] | [Mitigation] |
| Application query incompatibility | [L/M/H] | [L/M/H] | [Mitigation] |
| Downtime exceeds estimate | [L/M/H] | [L/M/H] | [Mitigation] |
| Rollback needed after partial migration | [L/M/H] | [L/M/H] | [Mitigation] |
| Connection pooler incompatibility | [L/M/H] | [L/M/H] | [Mitigation] |

## Pre-Migration Checklist

- [ ] Source database credentials verified and tested
- [ ] Target database provisioned and accessible
- [ ] Target database version confirmed compatible
- [ ] Network connectivity between source and target verified
- [ ] Sufficient disk space on export machine (2x data size recommended)
- [ ] Sufficient disk space on target (3x data size for import + index building)
- [ ] Pre-migration backup of source database completed
- [ ] Pre-migration backup of target database completed (if not empty)
- [ ] All team members notified of maintenance window
- [ ] Application deployment pipeline ready for connection string update
- [ ] Monitoring and alerting configured for target database
- [ ] Rollback procedure reviewed and tested on staging
- [ ] Migration scripts tested on staging environment with production-like data
- [ ] Application tested against target database on staging
- [ ] DNS TTL lowered (if using DNS-based switchover)

## Step-by-Step Execution Guide

### Before Maintenance Window (can be done in advance)

1. [ ] Run pre-migration backup of source database
2. [ ] Execute schema DDL scripts on target (tables, indexes, types, enums)
3. [ ] Verify schema created correctly (run index and constraint verification queries)
4. [ ] Test application connectivity to target database (read-only)

### During Maintenance Window

5. [ ] Announce maintenance window start
6. [ ] Set application to maintenance mode / read-only mode
7. [ ] Verify no active writes to source database
8. [ ] Export data from source database
9. [ ] Transform data (if transformations needed)
10. [ ] Disable foreign key checks and triggers on target
11. [ ] Import data to target database
12. [ ] Re-enable foreign key checks and triggers on target
13. [ ] Reset sequences / auto-increment values
14. [ ] Run validation: row counts
15. [ ] Run validation: checksums on critical tables
16. [ ] Run validation: foreign key integrity
17. [ ] Run validation: sample data spot-checks
18. [ ] If validation passes: update application connection string to target
19. [ ] If validation fails: execute rollback procedure, restore source
20. [ ] Deploy application with new connection string
21. [ ] Verify application is functioning correctly
22. [ ] Monitor error rates and query performance for 30 minutes
23. [ ] Announce maintenance window end

### After Maintenance Window

24. [ ] Monitor target database performance for 24 hours
25. [ ] Compare query performance (slow query log) against baseline
26. [ ] Verify all scheduled jobs and background workers are functioning
27. [ ] Keep source database running (read-only) for 7 days as safety net
28. [ ] After 7 days with no issues: decommission source database
29. [ ] Update documentation with new connection details
30. [ ] Archive migration scripts and plan for audit trail

## Post-Migration Verification

- [ ] All tables present in target with correct schema
- [ ] Row counts match between source and target for all tables
- [ ] Checksums match for critical tables
- [ ] All indexes present and functional
- [ ] All foreign keys present and valid (or documented as application-level)
- [ ] All triggers present and functional (or documented as moved to application)
- [ ] All stored procedures present and functional (or documented as moved to application)
- [ ] All views present and returning correct results
- [ ] Application login and authentication working
- [ ] Application CRUD operations working
- [ ] Application search functionality working
- [ ] Background jobs executing successfully
- [ ] API response times within acceptable range
- [ ] No increase in error rates
- [ ] Monitoring dashboards updated to track target database

## Application Changes Required

[List all application-level changes needed to work with the new database]

| Change | File/Service | Description | Priority |
|--------|-------------|-------------|----------|
| Connection string | .env / config | Update DATABASE_URL to target | Critical |
| ORM dialect | db/config | Change dialect from X to Y | Critical |
| Query syntax | [list files] | Rewrite provider-specific queries | High |
| Trigger logic | [list files] | Move trigger logic to application middleware | High |
| Stored proc calls | [list files] | Replace CALL/SELECT with application functions | High |
| Type handling | [list files] | Update type mappings (e.g., boolean handling) | Medium |
```
