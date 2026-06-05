# Rollback Plan and Downtime Estimation

## Rollback Plan

Every migration must have a tested rollback plan. Generate rollback scripts for each phase.

### Schema Rollback

Generate DROP statements in reverse topological order:

```sql
-- =============================================================================
-- ROLLBACK SCRIPT: Drop all migrated objects
-- Execute in this exact order (reverse dependency order)
-- =============================================================================

-- Drop views first (they depend on tables)
DROP VIEW IF EXISTS [target_schema].[view_name] CASCADE;

-- Drop triggers
DROP TRIGGER IF EXISTS [trigger_name] ON [target_schema].[table_name];

-- Drop functions and procedures
DROP FUNCTION IF EXISTS [target_schema].[function_name]([arg_types]);
DROP PROCEDURE IF EXISTS [target_schema].[procedure_name]([arg_types]);

-- Drop tables in reverse topological order (children before parents)
DROP TABLE IF EXISTS [target_schema].[child_table] CASCADE;
DROP TABLE IF EXISTS [target_schema].[parent_table] CASCADE;

-- Drop sequences (PostgreSQL)
DROP SEQUENCE IF EXISTS [target_schema].[sequence_name];

-- Drop custom types (PostgreSQL)
DROP TYPE IF EXISTS [target_schema].[type_name];

-- Drop schema if it was created for the migration
DROP SCHEMA IF EXISTS [target_schema];
```

### Data Rollback

If the migration replaces an existing database (not a fresh target):

1. Pre-migration backup: Generate a backup command to run BEFORE the migration starts.
2. Restore from backup: Document the restore procedure.

```bash
# Pre-migration backup (PostgreSQL)
pg_dump --format=custom --file=pre_migration_backup_$(date +%Y%m%d_%H%M%S).dump [dbname]

# Restore from backup (PostgreSQL)
pg_restore --clean --if-exists --dbname=[dbname] pre_migration_backup_[timestamp].dump

# Pre-migration backup (MySQL)
mysqldump --single-transaction --routines --triggers --events [dbname] > pre_migration_backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup (MySQL)
mysql [dbname] < pre_migration_backup_[timestamp].sql

# Pre-migration backup (MongoDB)
mongodump --db=[dbname] --out=pre_migration_backup_$(date +%Y%m%d_%H%M%S)/

# Restore from backup (MongoDB)
mongorestore --db=[dbname] --drop pre_migration_backup_[timestamp]/[dbname]/
```

### Application Rollback

Document application changes needed if the migration is rolled back:
- Connection string changes to revert
- ORM/query changes to revert
- Environment variable changes to revert
- DNS / connection pooler changes to revert

## Downtime Estimation

Calculate estimated downtime based on data volume and migration method.

### Downtime Factors

| Factor | Impact on Downtime |
|--------|-------------------|
| Schema DDL execution | Seconds to low minutes (negligible for most schemas) |
| Data export from source | Dependent on data volume and disk I/O |
| Data transfer (network) | Dependent on data volume and network bandwidth |
| Data import to target | Dependent on data volume, indexes, and constraints |
| Index creation | Can be significant for large tables (minutes to hours) |
| Validation queries | Minutes for row counts; longer for checksums on large tables |
| Application switchover | Seconds (connection string change) to minutes (DNS propagation) |

### Estimation Formula

```
Estimated downtime =
    Schema DDL:           ~1 minute per 100 tables
  + Data export:          ~1 minute per GB (SSD) or ~3 minutes per GB (HDD)
  + Data transfer:        data_size_gb / (network_bandwidth_mbps / 8 / 1024)
  + Data import:          ~2 minutes per GB (without indexes) or ~5 minutes per GB (with indexes)
  + Index creation:       ~1 minute per index per million rows
  + Constraint validation: ~30 seconds per foreign key per million rows
  + Validation:           ~2 minutes per 10 tables
  + Application switch:   ~5 minutes (conservative)
  + Buffer (20%):         total * 0.2
```

### Downtime Reduction Strategies

Document these options in the migration plan:

1. Pre-create schema: Create all tables, indexes, and constraints before the maintenance window. Only data load happens during downtime.
2. Create indexes after load: Load data without indexes, then create indexes. Faster overall but indexes are built from scratch.
3. Parallel table loads: Load independent tables simultaneously (tables with no FK dependencies between them).
4. Disable constraints during load: Turn off FK checks and unique checks during bulk load. Re-enable after.
5. Use native replication for zero-downtime: For same-engine migrations (e.g., Postgres to Supabase), use logical replication to sync in real-time, then cut over.
6. Dual-write period: Application writes to both old and new database during transition. Complex but eliminates downtime.
