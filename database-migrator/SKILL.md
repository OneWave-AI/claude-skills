---
name: database-migrator
description: Migrates databases between providers (Postgres, MySQL, Supabase, PlanetScale, MongoDB). Reads source schema, generates migration scripts, handles data type mapping, foreign keys, indexes, triggers, stored procedures. Validates migration with row counts and checksums. Generates migration-plan.md with step-by-step execution guide, rollback procedures, estimated downtime.
tools: Read, Write, Bash, Glob, Grep, Agent
user_invocable: true
---

# Database Migrator

A production-grade database migration system that moves schemas, data, and logic between database providers. This skill reads the full source database schema, analyzes every table, column, index, constraint, trigger, stored procedure, and view, then generates executable migration scripts for the target provider. It validates the migration with row counts and data checksums, and produces a comprehensive migration-plan.md with step-by-step instructions, rollback procedures, and estimated downtime.

This is not a schema designer. It is a cross-provider migration engine that handles the hard parts: data type incompatibilities, provider-specific SQL dialects, foreign key ordering, sequence/auto-increment translation, trigger rewrites, and stored procedure conversion.

## Supported Migration Paths

| Source Provider | Target Provider | Complexity |
|----------------|----------------|------------|
| PostgreSQL | MySQL | Medium |
| PostgreSQL | Supabase (Postgres) | Low |
| PostgreSQL | PlanetScale (MySQL) | Medium-High |
| PostgreSQL | MongoDB | High |
| MySQL | PostgreSQL | Medium |
| MySQL | Supabase (Postgres) | Medium |
| MySQL | PlanetScale (MySQL) | Low |
| MySQL | MongoDB | High |
| Supabase (Postgres) | PostgreSQL | Low |
| Supabase (Postgres) | MySQL | Medium |
| Supabase (Postgres) | PlanetScale (MySQL) | Medium-High |
| Supabase (Postgres) | MongoDB | High |
| PlanetScale (MySQL) | PostgreSQL | Medium |
| PlanetScale (MySQL) | Supabase (Postgres) | Medium |
| PlanetScale (MySQL) | MySQL | Low |
| PlanetScale (MySQL) | MongoDB | High |
| MongoDB | PostgreSQL | High |
| MongoDB | MySQL | High |
| MongoDB | Supabase (Postgres) | High |
| MongoDB | PlanetScale (MySQL) | High |

### Complexity Notes

- **Low**: Same underlying engine (e.g., Postgres to Supabase). Mostly connection string and permission changes.
- **Medium**: Same paradigm, different dialect (e.g., Postgres to MySQL). Requires data type mapping and SQL dialect translation.
- **Medium-High**: Different dialect plus provider constraints (e.g., PlanetScale has no foreign keys at the database level).
- **High**: Paradigm shift (e.g., relational to document or vice versa). Requires schema redesign, not just translation.

## When to Use

- You are moving a production database from one provider to another
- You are migrating from a self-hosted database to a managed service (or vice versa)
- You need to replicate a schema across providers for multi-cloud or disaster recovery
- You are consolidating multiple databases into a single provider
- You need to move from a relational database to MongoDB (or vice versa) with a complete data model translation
- You need a validated, auditable migration plan before executing anything in production

## When NOT to Use

- You are designing a new database schema from scratch (use database-schema-designer instead)
- You are migrating application code between frameworks (use full-codebase-migrator instead)
- You only need to change a few columns or add a table to an existing database (just write the ALTER statements directly)
- You need real-time replication or CDC (change data capture) -- this skill generates point-in-time migration scripts, not streaming pipelines

## Architecture

```
You (Commander)
 |
 |-- Phase 1: Source Schema Discovery
 |    |-- Connect to source (connection string or dump file)
 |    |-- Extract full schema: tables, columns, types, defaults, constraints
 |    |-- Extract indexes, foreign keys, unique constraints, check constraints
 |    |-- Extract triggers, stored procedures, functions, views
 |    |-- Extract sequences, enums, custom types
 |    |-- Extract row counts per table
 |    |-- Extract sample data for type inference (MongoDB)
 |
 |-- Phase 2: Schema Analysis and Mapping
 |    |-- Map source data types to target data types
 |    |-- Identify incompatible features (provider-specific)
 |    |-- Resolve foreign key creation order (topological sort)
 |    |-- Plan trigger and stored procedure conversion
 |    |-- Identify data that needs transformation
 |    |-- Flag potential data loss or precision changes
 |
 |-- Phase 3: Migration Script Generation
 |    |-- Generate DDL scripts (CREATE TABLE, INDEX, etc.)
 |    |-- Generate DML scripts (INSERT, data transformation)
 |    |-- Generate trigger and stored procedure translations
 |    |-- Generate validation queries (row counts, checksums)
 |    |-- Generate rollback scripts (DROP, reverse migration)
 |
 |-- Phase 4: Validation Plan
 |    |-- Row count comparison queries
 |    |-- Data checksum queries (MD5/SHA256 of key columns)
 |    |-- Foreign key integrity checks
 |    |-- Index existence verification
 |    |-- Trigger and procedure existence verification
 |    |-- Sample data spot-checks
 |
 |-- Phase 5: migration-plan.md Generation
 |    |-- Executive summary
 |    |-- Step-by-step execution guide
 |    |-- Rollback procedures
 |    |-- Estimated downtime
 |    |-- Risk assessment
 |    |-- Pre-migration checklist
 |    |-- Post-migration verification
```

## Execution Protocol

Follow these steps precisely when this skill is invoked.

### Step 0: Gather Migration Parameters

Before doing any analysis, establish these parameters with the user:

1. **Source provider and version** -- Which database engine and version? (e.g., PostgreSQL 15, MySQL 8.0, MongoDB 7.0)
2. **Target provider and version** -- Where is the data going? (e.g., Supabase, PlanetScale, self-hosted Postgres 16)
3. **Connection method** -- Will you connect live, or work from a schema dump file / migration files?
4. **Schema scope** -- All schemas/databases, or specific ones? Which tables to include/exclude?
5. **Data migration** -- Schema only, or schema + data? If data, full or partial (e.g., last 90 days)?
6. **Downtime tolerance** -- Zero-downtime required, or is a maintenance window acceptable? How long?
7. **Data volume** -- Approximate total size (GB) and largest table row count.
8. **Application dependencies** -- What applications connect to this database? Do they need code changes?
9. **Output location** -- Where to write migration scripts and migration-plan.md. Default to current directory.

If the user has already specified these in their prompt, skip the questions and proceed.

### Step 1: Source Schema Discovery

This is the foundation of the entire migration. Extract everything from the source database.

#### 1a. Schema Extraction -- Relational Databases (Postgres, MySQL, Supabase, PlanetScale)

Extract the following using information_schema queries or provider-specific catalog queries.

**Tables and Columns:**

For PostgreSQL / Supabase:
```sql
SELECT
    t.table_schema,
    t.table_name,
    c.column_name,
    c.ordinal_position,
    c.data_type,
    c.udt_name,
    c.character_maximum_length,
    c.numeric_precision,
    c.numeric_scale,
    c.is_nullable,
    c.column_default,
    c.is_identity,
    c.identity_generation,
    pgd.description AS column_comment
FROM information_schema.tables t
JOIN information_schema.columns c
    ON t.table_schema = c.table_schema AND t.table_name = c.table_name
LEFT JOIN pg_catalog.pg_statio_all_tables psat
    ON psat.schemaname = t.table_schema AND psat.relname = t.table_name
LEFT JOIN pg_catalog.pg_description pgd
    ON pgd.objoid = psat.relid AND pgd.objsubid = c.ordinal_position
WHERE t.table_schema NOT IN ('pg_catalog', 'information_schema')
    AND t.table_type = 'BASE TABLE'
ORDER BY t.table_schema, t.table_name, c.ordinal_position;
```

For MySQL / PlanetScale:
```sql
SELECT
    t.TABLE_SCHEMA,
    t.TABLE_NAME,
    c.COLUMN_NAME,
    c.ORDINAL_POSITION,
    c.DATA_TYPE,
    c.COLUMN_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.NUMERIC_PRECISION,
    c.NUMERIC_SCALE,
    c.IS_NULLABLE,
    c.COLUMN_DEFAULT,
    c.EXTRA,
    c.COLUMN_COMMENT
FROM information_schema.TABLES t
JOIN information_schema.COLUMNS c
    ON t.TABLE_SCHEMA = c.TABLE_SCHEMA AND t.TABLE_NAME = c.TABLE_NAME
WHERE t.TABLE_SCHEMA = DATABASE()
    AND t.TABLE_TYPE = 'BASE TABLE'
ORDER BY t.TABLE_SCHEMA, t.TABLE_NAME, c.ORDINAL_POSITION;
```

**Primary Keys:**

For PostgreSQL / Supabase:
```sql
SELECT
    tc.table_schema,
    tc.table_name,
    tc.constraint_name,
    kcu.column_name,
    kcu.ordinal_position
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
WHERE tc.constraint_type = 'PRIMARY KEY'
    AND tc.table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY tc.table_schema, tc.table_name, kcu.ordinal_position;
```

For MySQL / PlanetScale:
```sql
SELECT
    tc.TABLE_SCHEMA,
    tc.TABLE_NAME,
    tc.CONSTRAINT_NAME,
    kcu.COLUMN_NAME,
    kcu.ORDINAL_POSITION
FROM information_schema.TABLE_CONSTRAINTS tc
JOIN information_schema.KEY_COLUMN_USAGE kcu
    ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
    AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
    AND tc.TABLE_NAME = kcu.TABLE_NAME
WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY'
    AND tc.TABLE_SCHEMA = DATABASE()
ORDER BY tc.TABLE_SCHEMA, tc.TABLE_NAME, kcu.ORDINAL_POSITION;
```

**Foreign Keys:**

For PostgreSQL / Supabase:
```sql
SELECT
    tc.table_schema,
    tc.table_name,
    tc.constraint_name,
    kcu.column_name,
    ccu.table_schema AS foreign_table_schema,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    rc.update_rule,
    rc.delete_rule
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
    ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage ccu
    ON ccu.constraint_name = tc.constraint_name AND ccu.table_schema = tc.table_schema
JOIN information_schema.referential_constraints rc
    ON tc.constraint_name = rc.constraint_name AND tc.table_schema = rc.constraint_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY tc.table_schema, tc.table_name;
```

For MySQL / PlanetScale:
```sql
SELECT
    tc.TABLE_SCHEMA,
    tc.TABLE_NAME,
    tc.CONSTRAINT_NAME,
    kcu.COLUMN_NAME,
    kcu.REFERENCED_TABLE_SCHEMA,
    kcu.REFERENCED_TABLE_NAME,
    kcu.REFERENCED_COLUMN_NAME,
    rc.UPDATE_RULE,
    rc.DELETE_RULE
FROM information_schema.TABLE_CONSTRAINTS tc
JOIN information_schema.KEY_COLUMN_USAGE kcu
    ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
    AND tc.TABLE_SCHEMA = kcu.TABLE_SCHEMA
    AND tc.TABLE_NAME = kcu.TABLE_NAME
JOIN information_schema.REFERENTIAL_CONSTRAINTS rc
    ON tc.CONSTRAINT_NAME = rc.CONSTRAINT_NAME
    AND tc.TABLE_SCHEMA = rc.CONSTRAINT_SCHEMA
WHERE tc.CONSTRAINT_TYPE = 'FOREIGN KEY'
    AND tc.TABLE_SCHEMA = DATABASE()
ORDER BY tc.TABLE_SCHEMA, tc.TABLE_NAME;
```

**Indexes:**

For PostgreSQL / Supabase:
```sql
SELECT
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename, indexname;
```

For MySQL / PlanetScale:
```sql
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    INDEX_NAME,
    NON_UNIQUE,
    SEQ_IN_INDEX,
    COLUMN_NAME,
    INDEX_TYPE,
    SUB_PART,
    EXPRESSION
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;
```

**Check Constraints:**

For PostgreSQL / Supabase:
```sql
SELECT
    tc.table_schema,
    tc.table_name,
    tc.constraint_name,
    cc.check_clause
FROM information_schema.table_constraints tc
JOIN information_schema.check_constraints cc
    ON tc.constraint_name = cc.constraint_name AND tc.constraint_schema = cc.constraint_schema
WHERE tc.constraint_type = 'CHECK'
    AND tc.table_schema NOT IN ('pg_catalog', 'information_schema')
    AND cc.check_clause NOT LIKE '%IS NOT NULL%'
ORDER BY tc.table_schema, tc.table_name;
```

For MySQL 8.0+:
```sql
SELECT
    tc.TABLE_SCHEMA,
    tc.TABLE_NAME,
    tc.CONSTRAINT_NAME,
    cc.CHECK_CLAUSE
FROM information_schema.TABLE_CONSTRAINTS tc
JOIN information_schema.CHECK_CONSTRAINTS cc
    ON tc.CONSTRAINT_NAME = cc.CONSTRAINT_NAME AND tc.CONSTRAINT_SCHEMA = cc.CONSTRAINT_SCHEMA
WHERE tc.CONSTRAINT_TYPE = 'CHECK'
    AND tc.TABLE_SCHEMA = DATABASE()
ORDER BY tc.TABLE_SCHEMA, tc.TABLE_NAME;
```

**Triggers:**

For PostgreSQL / Supabase:
```sql
SELECT
    trigger_schema,
    trigger_name,
    event_manipulation,
    event_object_schema,
    event_object_table,
    action_statement,
    action_timing,
    action_orientation
FROM information_schema.triggers
WHERE trigger_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY trigger_schema, event_object_table, trigger_name;
```

For MySQL / PlanetScale:
```sql
SELECT
    TRIGGER_SCHEMA,
    TRIGGER_NAME,
    EVENT_MANIPULATION,
    EVENT_OBJECT_SCHEMA,
    EVENT_OBJECT_TABLE,
    ACTION_STATEMENT,
    ACTION_TIMING,
    ACTION_ORIENTATION
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = DATABASE()
ORDER BY TRIGGER_SCHEMA, EVENT_OBJECT_TABLE, TRIGGER_NAME;
```

**Stored Procedures and Functions:**

For PostgreSQL / Supabase:
```sql
SELECT
    n.nspname AS schema_name,
    p.proname AS function_name,
    pg_get_function_arguments(p.oid) AS arguments,
    pg_get_function_result(p.oid) AS return_type,
    CASE p.prokind
        WHEN 'f' THEN 'FUNCTION'
        WHEN 'p' THEN 'PROCEDURE'
        WHEN 'a' THEN 'AGGREGATE'
        WHEN 'w' THEN 'WINDOW'
    END AS kind,
    l.lanname AS language,
    pg_get_functiondef(p.oid) AS definition
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
JOIN pg_language l ON p.prolang = l.oid
WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY n.nspname, p.proname;
```

For MySQL / PlanetScale:
```sql
SELECT
    ROUTINE_SCHEMA,
    ROUTINE_NAME,
    ROUTINE_TYPE,
    DATA_TYPE,
    ROUTINE_DEFINITION,
    EXTERNAL_LANGUAGE
FROM information_schema.ROUTINES
WHERE ROUTINE_SCHEMA = DATABASE()
ORDER BY ROUTINE_SCHEMA, ROUTINE_NAME;
```

**Views:**

For PostgreSQL / Supabase:
```sql
SELECT
    table_schema,
    table_name AS view_name,
    view_definition
FROM information_schema.views
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;
```

For MySQL / PlanetScale:
```sql
SELECT
    TABLE_SCHEMA,
    TABLE_NAME AS VIEW_NAME,
    VIEW_DEFINITION
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_SCHEMA, TABLE_NAME;
```

**Sequences (PostgreSQL / Supabase only):**
```sql
SELECT
    schemaname,
    sequencename,
    data_type,
    start_value,
    min_value,
    max_value,
    increment_by,
    cycle,
    last_value
FROM pg_sequences
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, sequencename;
```

**Enums (PostgreSQL / Supabase only):**
```sql
SELECT
    n.nspname AS schema_name,
    t.typname AS enum_name,
    string_agg(e.enumlabel, ', ' ORDER BY e.enumsortorder) AS enum_values
FROM pg_type t
JOIN pg_enum e ON t.oid = e.enumtypid
JOIN pg_namespace n ON t.typnamespace = n.oid
WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
GROUP BY n.nspname, t.typname
ORDER BY n.nspname, t.typname;
```

**Row Counts:**

For PostgreSQL / Supabase (fast estimate):
```sql
SELECT
    schemaname,
    relname AS table_name,
    n_live_tup AS estimated_row_count
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

For MySQL / PlanetScale:
```sql
SELECT
    TABLE_SCHEMA,
    TABLE_NAME,
    TABLE_ROWS AS estimated_row_count,
    DATA_LENGTH,
    INDEX_LENGTH
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE()
    AND TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_ROWS DESC;
```

#### 1b. Schema Extraction -- MongoDB

MongoDB has no enforced schema, so discovery requires collection scanning:

```javascript
// List all collections
db.getCollectionNames().forEach(function(collName) {
    print("--- Collection: " + collName + " ---");

    // Row count
    print("Document count: " + db[collName].countDocuments({}));

    // Sample documents for schema inference
    var sample = db[collName].aggregate([{ $sample: { size: 100 } }]).toArray();

    // Infer schema from sample
    var schema = {};
    sample.forEach(function(doc) {
        function inferType(obj, prefix) {
            for (var key in obj) {
                var fullKey = prefix ? prefix + "." + key : key;
                var val = obj[key];
                var type = typeof val;
                if (val === null) type = "null";
                else if (Array.isArray(val)) type = "array";
                else if (val instanceof ObjectId) type = "ObjectId";
                else if (val instanceof Date) type = "Date";
                else if (val instanceof NumberDecimal) type = "Decimal128";
                else if (type === "object") {
                    inferType(val, fullKey);
                    type = "object";
                }
                if (!schema[fullKey]) schema[fullKey] = {};
                schema[fullKey][type] = (schema[fullKey][type] || 0) + 1;
            }
        }
        inferType(doc, "");
    });

    printjson(schema);

    // Indexes
    printjson(db[collName].getIndexes());
});
```

Also extract:
- **Validators**: `db.getCollectionInfos()` for JSON Schema validators
- **Capped collections**: Size and max document limits
- **Sharding config**: `sh.status()` if sharded
- **Aggregation pipelines saved as views**: `db.system.views.find()`

#### 1c. Supabase-Specific Extraction

When the source or target is Supabase, also extract:

```sql
-- Row Level Security policies
SELECT
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename, policyname;

-- RLS enabled tables
SELECT
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename;

-- Extensions
SELECT extname, extversion FROM pg_extension ORDER BY extname;

-- Publication/subscription (for realtime)
SELECT * FROM pg_publication;
SELECT * FROM pg_publication_tables;
```

#### 1d. PlanetScale-Specific Considerations

PlanetScale does not support:
- Foreign key constraints at the database level (enforced at application level)
- Stored procedures
- Triggers
- Events

When PlanetScale is the target, flag all of these for application-level handling. When PlanetScale is the source, note that foreign key relationships must be inferred from naming conventions and application code.

### Step 2: Data Type Mapping

This is the core translation layer. Map every source type to the best target type.

#### 2a. PostgreSQL to MySQL Type Map

| PostgreSQL Type | MySQL Type | Notes |
|----------------|-----------|-------|
| SMALLINT | SMALLINT | Direct |
| INTEGER | INT | Direct |
| BIGINT | BIGINT | Direct |
| SERIAL | INT AUTO_INCREMENT | Remove DEFAULT nextval() |
| BIGSERIAL | BIGINT AUTO_INCREMENT | Remove DEFAULT nextval() |
| NUMERIC(p,s) | DECIMAL(p,s) | Direct |
| REAL | FLOAT | Direct |
| DOUBLE PRECISION | DOUBLE | Direct |
| MONEY | DECIMAL(19,4) | Loses currency formatting |
| BOOLEAN | TINYINT(1) | TRUE/FALSE to 1/0 |
| CHAR(n) | CHAR(n) | Direct |
| VARCHAR(n) | VARCHAR(n) | Direct |
| TEXT | LONGTEXT | MySQL TEXT is 65KB; LONGTEXT is 4GB |
| BYTEA | LONGBLOB | Binary data |
| DATE | DATE | Direct |
| TIME | TIME | Direct |
| TIMESTAMP | DATETIME(6) | MySQL TIMESTAMP has 2038 limit |
| TIMESTAMP WITH TIME ZONE | DATETIME(6) | Store timezone separately or use UTC |
| INTERVAL | VARCHAR(255) | No native interval in MySQL |
| UUID | CHAR(36) or BINARY(16) | CHAR(36) for readability, BINARY(16) for performance |
| JSON | JSON | Direct (MySQL 5.7+) |
| JSONB | JSON | Loses binary optimization; add generated columns for indexed paths |
| ARRAY | JSON | No native arrays in MySQL |
| HSTORE | JSON | Key-value to JSON object |
| INET | VARCHAR(45) | IPv4 and IPv6 |
| CIDR | VARCHAR(45) | Network address |
| MACADDR | VARCHAR(17) | MAC address string |
| POINT | POINT | Spatial type (requires spatial index changes) |
| GEOMETRY | GEOMETRY | Spatial type |
| TSVECTOR | FULLTEXT INDEX | Use FULLTEXT index on relevant columns |
| ENUM('a','b') | ENUM('a','b') | Direct (but MySQL ENUM has different behavior) |
| INT4RANGE | VARCHAR(255) | No native range types in MySQL |
| BIT(n) | BIT(n) | Direct |
| XML | LONGTEXT | No native XML in MySQL |

#### 2b. MySQL to PostgreSQL Type Map

| MySQL Type | PostgreSQL Type | Notes |
|-----------|----------------|-------|
| TINYINT | SMALLINT | Direct |
| TINYINT(1) | BOOLEAN | If used as boolean |
| SMALLINT | SMALLINT | Direct |
| MEDIUMINT | INTEGER | No MEDIUMINT in Postgres |
| INT | INTEGER | Direct |
| BIGINT | BIGINT | Direct |
| INT AUTO_INCREMENT | SERIAL or GENERATED ALWAYS AS IDENTITY | Prefer IDENTITY for new schemas |
| FLOAT | REAL | Direct |
| DOUBLE | DOUBLE PRECISION | Direct |
| DECIMAL(p,s) | NUMERIC(p,s) | Direct |
| BIT(n) | BIT(n) | Direct |
| CHAR(n) | CHAR(n) | Direct |
| VARCHAR(n) | VARCHAR(n) | Direct |
| TINYTEXT | TEXT | Postgres TEXT has no size limit |
| TEXT | TEXT | Direct |
| MEDIUMTEXT | TEXT | Direct |
| LONGTEXT | TEXT | Direct |
| TINYBLOB | BYTEA | Direct |
| BLOB | BYTEA | Direct |
| MEDIUMBLOB | BYTEA | Direct |
| LONGBLOB | BYTEA | Direct |
| DATE | DATE | Direct |
| TIME | TIME | Direct |
| DATETIME | TIMESTAMP | Direct |
| TIMESTAMP | TIMESTAMP WITH TIME ZONE | MySQL TIMESTAMP is UTC-converted |
| YEAR | SMALLINT | No YEAR type in Postgres |
| ENUM('a','b') | VARCHAR + CHECK or CREATE TYPE | Prefer CREATE TYPE for Postgres enums |
| SET('a','b') | TEXT[] or VARCHAR + CHECK | Use array type |
| JSON | JSONB | Prefer JSONB for indexing |
| GEOMETRY | GEOMETRY (PostGIS) | Requires PostGIS extension |
| POINT | POINT | Native or PostGIS |
| BINARY(n) | BYTEA | Direct |
| VARBINARY(n) | BYTEA | Direct |

#### 2c. Relational to MongoDB Type Map

| SQL Type | MongoDB (BSON) Type | Notes |
|---------|-------------------|-------|
| INTEGER / INT | NumberInt (int32) | Direct |
| BIGINT | NumberLong (int64) | Direct |
| SERIAL / AUTO_INCREMENT | ObjectId or NumberLong | ObjectId preferred for _id |
| NUMERIC / DECIMAL | NumberDecimal (Decimal128) | Direct |
| FLOAT / REAL | Double | Direct |
| BOOLEAN | Boolean | Direct |
| CHAR / VARCHAR / TEXT | String | Direct |
| DATE | Date | Direct |
| TIMESTAMP | Date | MongoDB Date is millisecond precision |
| BYTEA / BLOB | BinData | Direct |
| UUID | String or BinData(4) | BinData(4) is more compact |
| JSON / JSONB | Object | Native -- embed directly |
| ARRAY | Array | Native -- embed directly |
| ENUM | String + validation | Use JSON Schema validator |

#### 2d. MongoDB to Relational Type Map

| MongoDB (BSON) Type | PostgreSQL Type | MySQL Type | Notes |
|-------------------|----------------|-----------|-------|
| ObjectId | CHAR(24) or UUID | CHAR(24) or BINARY(12) | Convert to hex string or generate new UUID |
| String | TEXT or VARCHAR | VARCHAR(n) or TEXT | Inspect max lengths in sample data |
| NumberInt (int32) | INTEGER | INT | Direct |
| NumberLong (int64) | BIGINT | BIGINT | Direct |
| Double | DOUBLE PRECISION | DOUBLE | Direct |
| NumberDecimal | NUMERIC | DECIMAL | Direct |
| Boolean | BOOLEAN | TINYINT(1) | Direct |
| Date | TIMESTAMP WITH TIME ZONE | DATETIME(3) | Direct |
| BinData | BYTEA | LONGBLOB | Direct |
| Array | JSONB or junction table | JSON or junction table | Simple arrays: JSONB/JSON; relational arrays: junction table |
| Embedded Object | JSONB or separate table | JSON or separate table | Decide based on query patterns |
| Null | NULL | NULL | Nullable columns |
| Regex | TEXT | VARCHAR | Store pattern as string |
| Timestamp (BSON) | TIMESTAMP | TIMESTAMP | Internal MongoDB type -- convert to standard timestamp |

### Step 3: Schema Translation and Script Generation

With the full schema extracted and type mapping established, generate the migration scripts.

#### 3a. Table Creation Order

Foreign keys create dependencies between tables. Tables must be created in topological order (dependencies first):

1. Build a directed graph where an edge from table A to table B means A has a foreign key referencing B.
2. Perform a topological sort on this graph.
3. If cycles exist (mutual foreign keys), break the cycle by deferring one foreign key constraint to be added after all tables are created.

```
Table creation order algorithm:
1. Find all tables with zero foreign key dependencies -- these go first.
2. Remove those tables from the graph.
3. Repeat until all tables are placed.
4. If the graph is not empty after exhaustion, cycles exist.
   For each cycle: create all tables without the cyclic FK, then ALTER TABLE to add it.
```

#### 3b. DDL Script Generation

For each table, generate the target-dialect CREATE TABLE statement. The script must include:

1. **Table definition** with all columns, types (mapped per Step 2), defaults, and NOT NULL constraints
2. **Primary key** definition (inline or as constraint)
3. **Unique constraints**
4. **Check constraints** (translated to target dialect)
5. **Foreign key constraints** (respecting creation order from 3a)
6. **Indexes** (translated to target syntax)
7. **Comments** on tables and columns (if supported by target)

Template for each table in the output:
```sql
-- =============================================================================
-- Table: [schema].[table_name]
-- Source: [source_provider] [schema].[table_name]
-- Rows (estimated): [N]
-- =============================================================================

CREATE TABLE [target_schema].[table_name] (
    [column definitions with mapped types]
);

-- Primary Key
ALTER TABLE [target_schema].[table_name]
    ADD CONSTRAINT pk_[table_name] PRIMARY KEY ([columns]);

-- Unique Constraints
ALTER TABLE [target_schema].[table_name]
    ADD CONSTRAINT uk_[table_name]_[columns] UNIQUE ([columns]);

-- Check Constraints
ALTER TABLE [target_schema].[table_name]
    ADD CONSTRAINT ck_[table_name]_[name] CHECK ([translated_expression]);

-- Foreign Keys (only if target supports them)
ALTER TABLE [target_schema].[table_name]
    ADD CONSTRAINT fk_[table_name]_[column]
    FOREIGN KEY ([column]) REFERENCES [target_schema].[referenced_table]([referenced_column])
    ON UPDATE [action] ON DELETE [action];

-- Indexes
CREATE INDEX idx_[table_name]_[columns] ON [target_schema].[table_name] ([columns]);
CREATE UNIQUE INDEX uidx_[table_name]_[columns] ON [target_schema].[table_name] ([columns]);

-- Comments
COMMENT ON TABLE [target_schema].[table_name] IS '[description]';
COMMENT ON COLUMN [target_schema].[table_name].[column] IS '[description]';
```

#### 3c. Sequence and Auto-Increment Translation

**PostgreSQL to MySQL:**
- Replace `SERIAL` / `BIGSERIAL` with `AUTO_INCREMENT`
- Replace `GENERATED ALWAYS AS IDENTITY` with `AUTO_INCREMENT`
- Remove all `CREATE SEQUENCE` statements
- Remove all `DEFAULT nextval('sequence_name')` and use `AUTO_INCREMENT` on the column
- After data load, set `AUTO_INCREMENT` value: `ALTER TABLE t AUTO_INCREMENT = [max_id + 1];`

**MySQL to PostgreSQL:**
- Replace `AUTO_INCREMENT` with `GENERATED ALWAYS AS IDENTITY` (preferred) or `SERIAL`
- After data load, reset sequence: `SELECT setval('table_column_seq', (SELECT MAX(column) FROM table));`

**Relational to MongoDB:**
- Remove auto-increment entirely; use ObjectId for `_id` unless the application requires numeric IDs
- If numeric IDs required, document a counter collection pattern:
```javascript
// Counter collection for auto-increment emulation
db.counters.insertOne({ _id: "table_name", seq: 0 });

// Get next ID
function getNextSequence(name) {
    var ret = db.counters.findOneAndUpdate(
        { _id: name },
        { $inc: { seq: 1 } },
        { returnDocument: "after" }
    );
    return ret.seq;
}
```

#### 3d. Trigger Translation

Triggers are the most provider-specific feature. Each translation requires careful rewriting.

**PostgreSQL triggers to MySQL:**
- PostgreSQL uses trigger functions (PL/pgSQL); MySQL uses inline trigger bodies
- Replace `NEW.column` / `OLD.column` syntax (same in both, but function wrapper differs)
- Replace `RETURN NEW;` / `RETURN OLD;` (not needed in MySQL)
- Replace `TG_OP` with separate triggers per operation
- Replace `RAISE EXCEPTION` with `SIGNAL SQLSTATE`

**MySQL triggers to PostgreSQL:**
- Wrap trigger body in a PL/pgSQL function
- Add `RETURN NEW;` or `RETURN NULL;` as appropriate
- Replace `SIGNAL SQLSTATE` with `RAISE EXCEPTION`

**Relational triggers to MongoDB:**
- Document that MongoDB does not have database-level triggers
- Recommend alternatives:
  - MongoDB Change Streams (for event-driven processing)
  - Application-level middleware (Mongoose pre/post hooks)
  - Atlas Triggers (if using MongoDB Atlas)

**PlanetScale target:**
- PlanetScale does not support triggers
- Document all trigger logic that must move to the application layer
- Generate application-level middleware code or ORM hooks as replacements

#### 3e. Stored Procedure and Function Translation

**PostgreSQL to MySQL:**
- Replace `CREATE OR REPLACE FUNCTION` with `CREATE PROCEDURE` or `CREATE FUNCTION`
- Replace PL/pgSQL syntax with MySQL procedural SQL
- Replace `RETURNS TABLE(...)` with result set from SELECT
- Replace `$$` delimiters with `DELIMITER //` ... `//` pattern
- Replace `RAISE NOTICE` with `SELECT` for debug output
- Replace `RAISE EXCEPTION` with `SIGNAL SQLSTATE`
- Replace `PERFORM` with `DO` or `SELECT ... INTO @dummy`
- Replace `RETURNING` clause (not available in MySQL; use `LAST_INSERT_ID()`)

**MySQL to PostgreSQL:**
- Replace `DELIMITER` pattern with `$$` delimiters
- Replace `SIGNAL SQLSTATE` with `RAISE EXCEPTION`
- Replace `LAST_INSERT_ID()` with `RETURNING` clause or `currval()`
- Replace `GROUP_CONCAT` with `string_agg`
- Replace `IFNULL` with `COALESCE`
- Replace `IF()` function with `CASE WHEN`

**Relational to MongoDB:**
- Stored procedures do not exist in MongoDB
- Translate to:
  - Aggregation pipelines (for data processing logic)
  - Application-level service functions
  - MongoDB Atlas Functions (if using Atlas)

**PlanetScale target:**
- PlanetScale does not support stored procedures
- All procedural logic must move to the application layer

#### 3f. View Translation

Views are generally straightforward to translate but may contain provider-specific SQL:

1. Extract the view definition SQL
2. Translate any provider-specific functions (see function mapping below)
3. Translate data types in CAST expressions
4. Adjust JOIN syntax if needed
5. For materialized views (PostgreSQL), note that MySQL does not support them natively -- recommend creating a table with a refresh procedure instead

#### 3g. Common SQL Function Mapping

| PostgreSQL | MySQL | Notes |
|-----------|-------|-------|
| NOW() | NOW() | Direct |
| CURRENT_TIMESTAMP | CURRENT_TIMESTAMP | Direct |
| string_agg(col, ',') | GROUP_CONCAT(col SEPARATOR ',') | Different syntax |
| COALESCE(a, b) | COALESCE(a, b) or IFNULL(a, b) | Direct |
| CONCAT_WS(',', a, b) | CONCAT_WS(',', a, b) | Direct |
| SUBSTRING(s FROM n FOR m) | SUBSTRING(s, n, m) | Different syntax |
| EXTRACT(EPOCH FROM ts) | UNIX_TIMESTAMP(ts) | Different function |
| TO_CHAR(ts, 'YYYY-MM-DD') | DATE_FORMAT(ts, '%Y-%m-%d') | Different format codes |
| INTERVAL '1 day' | INTERVAL 1 DAY | Different syntax |
| GENERATE_SERIES(1, 10) | Recursive CTE or sequence table | No direct equivalent |
| ARRAY_AGG(col) | JSON_ARRAYAGG(col) | MySQL 5.7+ |
| UNNEST(array_col) | JSON_TABLE(...) | MySQL 8.0+ |
| ANY(array) | IN (...) or JSON_CONTAINS | Different approach |
| ILIKE | LIKE (case-insensitive collation) | Set collation or use LOWER() |
| SIMILAR TO | REGEXP | Different regex engine |
| ~ (regex match) | REGEXP | Direct equivalent |
| gen_random_uuid() | UUID() | Direct equivalent |
| RETURNING id | LAST_INSERT_ID() | Different approach |
| ON CONFLICT DO UPDATE | INSERT ... ON DUPLICATE KEY UPDATE | Different syntax |
| LIMIT n OFFSET m | LIMIT m, n or LIMIT n OFFSET m | MySQL supports both |
| BOOLEAN true/false | 1/0 | Literal translation |
| ::type (cast) | CAST(x AS type) | Postgres shorthand |

### Step 4: Data Migration Scripts

#### 4a. Data Export from Source

For relational sources, generate export commands:

**PostgreSQL / Supabase:**
```bash
# Full table export to CSV
pg_dump --data-only --format=plain --table=[schema].[table] --file=[table].sql [dbname]

# Or CSV format for cross-platform compatibility
psql -c "COPY [schema].[table] TO STDOUT WITH CSV HEADER" [dbname] > [table].csv
```

**MySQL / PlanetScale:**
```bash
# Full table export
mysqldump --no-create-info --tab=/tmp/export --fields-terminated-by=',' --fields-enclosed-by='"' --lines-terminated-by='\n' [dbname] [table]

# Or SELECT INTO OUTFILE
mysql -e "SELECT * INTO OUTFILE '/tmp/[table].csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' FROM [table]" [dbname]
```

**MongoDB:**
```bash
# Export collection to JSON
mongoexport --db=[dbname] --collection=[collection] --out=[collection].json --jsonArray

# Or BSON for binary data preservation
mongodump --db=[dbname] --collection=[collection] --out=./dump/
```

#### 4b. Data Transformation

Generate transformation scripts for data that needs conversion:

```sql
-- Example: PostgreSQL boolean to MySQL tinyint
-- In the INSERT or LOAD DATA statement:
-- Replace TRUE with 1, FALSE with 0

-- Example: PostgreSQL array to MySQL JSON
-- Transform: '{1,2,3}' becomes '[1,2,3]'

-- Example: PostgreSQL UUID to MySQL CHAR(36)
-- No transformation needed if stored as text

-- Example: PostgreSQL TIMESTAMP WITH TIME ZONE to MySQL DATETIME
-- Convert to UTC before export:
SET timezone = 'UTC';
COPY (SELECT id, created_at AT TIME ZONE 'UTC' AS created_at FROM table) TO STDOUT WITH CSV HEADER;
```

#### 4c. Data Import to Target

**PostgreSQL / Supabase (target):**
```sql
-- Disable triggers during load
ALTER TABLE [table] DISABLE TRIGGER ALL;

-- Disable foreign key checks during load
SET session_replication_role = replica;

-- Load data
COPY [schema].[table] FROM '/path/to/[table].csv' WITH CSV HEADER;

-- Reset sequences after load
SELECT setval(pg_get_serial_sequence('[schema].[table]', '[id_column]'),
    (SELECT COALESCE(MAX([id_column]), 0) FROM [schema].[table]));

-- Re-enable triggers
ALTER TABLE [table] ENABLE TRIGGER ALL;

-- Re-enable foreign key checks
SET session_replication_role = DEFAULT;

-- Analyze tables for query planner
ANALYZE [schema].[table];
```

**MySQL / PlanetScale (target):**
```sql
-- Disable foreign key checks
SET FOREIGN_KEY_CHECKS = 0;
SET UNIQUE_CHECKS = 0;
SET AUTOCOMMIT = 0;

-- Load data
LOAD DATA INFILE '/path/to/[table].csv'
INTO TABLE [table]
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Reset auto_increment
ALTER TABLE [table] AUTO_INCREMENT = (SELECT MAX(id) + 1 FROM [table]);

-- Re-enable checks
SET FOREIGN_KEY_CHECKS = 1;
SET UNIQUE_CHECKS = 1;
COMMIT;

-- Analyze tables
ANALYZE TABLE [table];
```

**MongoDB (target):**
```bash
# Import from JSON
mongoimport --db=[dbname] --collection=[collection] --file=[collection].json --jsonArray

# Or from BSON dump
mongorestore --db=[dbname] --collection=[collection] ./dump/[dbname]/[collection].bson
```

### Step 5: Validation Plan

Every migration must be validated. Generate validation queries for both source and target.

#### 5a. Row Count Validation

Generate a query for each table that compares source and target row counts:

```sql
-- Source (run on source database)
SELECT '[table_name]' AS table_name, COUNT(*) AS row_count FROM [source_schema].[table_name]
UNION ALL
SELECT '[table_name_2]', COUNT(*) FROM [source_schema].[table_name_2]
-- ... repeat for all tables
ORDER BY table_name;

-- Target (run on target database)
SELECT '[table_name]' AS table_name, COUNT(*) AS row_count FROM [target_schema].[table_name]
UNION ALL
SELECT '[table_name_2]', COUNT(*) FROM [target_schema].[table_name_2]
-- ... repeat for all tables
ORDER BY table_name;
```

Expected result: every table has identical row counts.

#### 5b. Data Checksum Validation

Generate checksum queries for critical tables. Compare a hash of key columns between source and target:

**PostgreSQL (source or target):**
```sql
SELECT
    MD5(string_agg(
        COALESCE(id::text, 'NULL') || '|' ||
        COALESCE(name, 'NULL') || '|' ||
        COALESCE(email, 'NULL') || '|' ||
        COALESCE(created_at::text, 'NULL'),
        ',' ORDER BY id
    )) AS table_checksum
FROM [schema].[table];
```

**MySQL (source or target):**
```sql
SELECT
    MD5(GROUP_CONCAT(
        CONCAT_WS('|',
            COALESCE(id, 'NULL'),
            COALESCE(name, 'NULL'),
            COALESCE(email, 'NULL'),
            COALESCE(created_at, 'NULL')
        )
        ORDER BY id SEPARATOR ','
    )) AS table_checksum
FROM [table];
```

**MongoDB (source or target):**
```javascript
// Hash all documents in a collection
var hash = db[collection].aggregate([
    { $sort: { _id: 1 } },
    { $group: {
        _id: null,
        docs: { $push: { $concat: [
            { $toString: "$_id" }, "|",
            { $ifNull: ["$name", "NULL"] }, "|",
            { $ifNull: ["$email", "NULL"] }
        ]}}
    }},
    { $project: {
        checksum: { $function: {
            body: function(arr) { return hex_md5(arr.join(",")); },
            args: ["$docs"],
            lang: "js"
        }}
    }}
]);
```

Expected result: checksums match between source and target for every validated table.

#### 5c. Foreign Key Integrity Validation

For every foreign key in the target, verify referential integrity:

```sql
-- Verify no orphaned foreign keys
SELECT COUNT(*) AS orphaned_rows
FROM [child_table] c
LEFT JOIN [parent_table] p ON c.[fk_column] = p.[pk_column]
WHERE c.[fk_column] IS NOT NULL AND p.[pk_column] IS NULL;
```

Expected result: zero orphaned rows for every foreign key relationship.

#### 5d. Index Verification

Verify all indexes were created:

**PostgreSQL / Supabase:**
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = '[target_schema]'
ORDER BY tablename, indexname;
```

**MySQL / PlanetScale:**
```sql
SELECT TABLE_NAME, INDEX_NAME, COLUMN_NAME, NON_UNIQUE
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;
```

Compare the count and names against the expected index list from the migration scripts.

#### 5e. Trigger and Procedure Verification

Verify all triggers and procedures were created:

```sql
-- PostgreSQL: verify triggers
SELECT trigger_name, event_object_table, action_timing, event_manipulation
FROM information_schema.triggers
WHERE trigger_schema = '[target_schema]';

-- PostgreSQL: verify functions/procedures
SELECT routine_name, routine_type
FROM information_schema.routines
WHERE routine_schema = '[target_schema]';

-- MySQL: verify triggers
SELECT TRIGGER_NAME, EVENT_OBJECT_TABLE, ACTION_TIMING, EVENT_MANIPULATION
FROM information_schema.TRIGGERS
WHERE TRIGGER_SCHEMA = DATABASE();

-- MySQL: verify procedures
SELECT ROUTINE_NAME, ROUTINE_TYPE
FROM information_schema.ROUTINES
WHERE ROUTINE_SCHEMA = DATABASE();
```

#### 5f. Sample Data Spot-Check

For the 5 largest tables, generate queries that compare specific rows:

```sql
-- Pick 10 random IDs from source, then verify those exact rows exist in target with matching data
-- Source:
SELECT * FROM [table] WHERE id IN ([random_id_1], [random_id_2], ..., [random_id_10]) ORDER BY id;

-- Target:
SELECT * FROM [table] WHERE id IN ([random_id_1], [random_id_2], ..., [random_id_10]) ORDER BY id;
```

### Step 6: Rollback Plan

Every migration must have a tested rollback plan. Generate rollback scripts for each phase.

#### 6a. Schema Rollback

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

#### 6b. Data Rollback

If the migration replaces an existing database (not a fresh target):

1. **Pre-migration backup**: Generate a backup command to run BEFORE the migration starts
2. **Restore from backup**: Document the restore procedure

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

#### 6c. Application Rollback

Document application changes needed if the migration is rolled back:
- Connection string changes to revert
- ORM/query changes to revert
- Environment variable changes to revert
- DNS / connection pooler changes to revert

### Step 7: Downtime Estimation

Calculate estimated downtime based on data volume and migration method.

#### 7a. Downtime Factors

| Factor | Impact on Downtime |
|--------|-------------------|
| Schema DDL execution | Seconds to low minutes (negligible for most schemas) |
| Data export from source | Dependent on data volume and disk I/O |
| Data transfer (network) | Dependent on data volume and network bandwidth |
| Data import to target | Dependent on data volume, indexes, and constraints |
| Index creation | Can be significant for large tables (minutes to hours) |
| Validation queries | Minutes for row counts; longer for checksums on large tables |
| Application switchover | Seconds (connection string change) to minutes (DNS propagation) |

#### 7b. Estimation Formula

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

#### 7c. Downtime Reduction Strategies

Document these options in the migration plan:

1. **Pre-create schema**: Create all tables, indexes, and constraints before the maintenance window. Only data load happens during downtime.
2. **Create indexes after load**: Load data without indexes, then create indexes. Faster overall but indexes are built from scratch.
3. **Parallel table loads**: Load independent tables simultaneously (tables with no FK dependencies between them).
4. **Disable constraints during load**: Turn off FK checks, unique checks during bulk load. Re-enable after.
5. **Use native replication for zero-downtime**: For same-engine migrations (e.g., Postgres to Supabase), use logical replication to sync in real-time, then cut over.
6. **Dual-write period**: Application writes to both old and new database during transition. Complex but eliminates downtime.

### Step 8: Generate migration-plan.md

Write the final deliverable. The document structure:

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

## Handling Edge Cases

### Extremely Large Tables (100M+ rows)

For tables exceeding 100 million rows:

1. **Chunked export**: Export in batches of 1-10 million rows using `LIMIT/OFFSET` or range-based `WHERE id BETWEEN x AND y`.
2. **Parallel import**: Split data files and import in parallel using multiple connections.
3. **Deferred index creation**: Create the table without indexes, load data, then create indexes. This is significantly faster than loading into an indexed table.
4. **Partitioned loading**: If the target supports partitioning, create partitions first and load into each partition in parallel.
5. **Progress tracking**: Generate a progress script that reports rows loaded vs total rows.

### Schema Differences That Require Data Transformation

When a type mapping is not lossless:

1. **Precision loss**: Flag any column where the target type has less precision. Example: PostgreSQL NUMERIC(38,18) to MySQL DECIMAL(38,18) is lossless, but NUMERIC(100,50) exceeds MySQL's limit of DECIMAL(65,30).
2. **Encoding issues**: UTF-8 4-byte characters (emojis) require `utf8mb4` in MySQL, not `utf8`.
3. **Timezone handling**: Document whether timestamps are stored as UTC or local time, and how the target handles timezone conversion.
4. **NULL vs empty string**: PostgreSQL distinguishes NULL from empty string; some applications may not.

### MongoDB Document Flattening (MongoDB to Relational)

When migrating from MongoDB to a relational database:

1. **Top-level fields**: Map directly to columns in a primary table.
2. **Embedded objects**: Two strategies:
   - **Flatten**: Prefix column names with the object path (e.g., `address.street` becomes `address_street`). Use when the object is always present and has a fixed schema.
   - **Separate table**: Create a related table with a foreign key. Use when the object is optional or has variable schema.
3. **Embedded arrays**: Always create a junction or child table. Each array element becomes a row.
4. **Polymorphic documents**: Documents in the same collection with different shapes. Options:
   - Single Table Inheritance: One wide table with nullable columns for each document shape.
   - Class Table Inheritance: Separate tables per document shape with a shared base table.
   - Discriminator column: Single table with a `type` column to distinguish shapes.
5. **Nested arrays of objects**: Requires recursive flattening into multiple tables with foreign keys at each level.

### PlanetScale Foreign Key Workarounds

Since PlanetScale does not support database-level foreign keys:

1. **Document all relationships** in the migration plan as application-level constraints.
2. **Generate application-level validation code** (e.g., Prisma schema with `@relation`, or custom middleware).
3. **Generate orphan detection queries** to run periodically:
   ```sql
   -- Check for orphaned child rows (run periodically)
   SELECT c.id, c.[fk_column]
   FROM [child_table] c
   LEFT JOIN [parent_table] p ON c.[fk_column] = p.id
   WHERE c.[fk_column] IS NOT NULL AND p.id IS NULL;
   ```
4. **Document cascade delete logic** that must be implemented in the application.

### Supabase-Specific Migration Considerations

When migrating to Supabase:

1. **Row Level Security (RLS)**: Generate RLS policies based on the application's authorization model. Document that RLS must be enabled on all tables exposed via the Supabase API.
2. **Realtime subscriptions**: Identify tables that need realtime and add them to the Supabase publication.
3. **Storage buckets**: If the source database stores file references, map them to Supabase Storage.
4. **Edge Functions**: If stored procedures contain API-callable logic, recommend migrating to Supabase Edge Functions.
5. **Auth integration**: If the source has a users table, document how to integrate with Supabase Auth.

### Multi-Schema or Multi-Database Migration

When the source has multiple schemas or databases:

1. **Map source schemas to target schemas** (if the target supports multiple schemas).
2. **Merge schemas**: If the target is single-schema (e.g., PlanetScale), prefix table names with the schema name.
3. **Cross-schema references**: Identify and document all cross-schema foreign keys. These may need special handling.
4. **Schema-level permissions**: Document permission differences between source and target.

## Quality Checklist for the Migration Plan

Before delivering the plan, verify:

- [ ] Every source table is accounted for in the schema inventory
- [ ] Every column has a type mapping documented
- [ ] Every foreign key has a creation order assigned
- [ ] Every index is included in the DDL scripts
- [ ] Every trigger is translated or documented as needing application-level migration
- [ ] Every stored procedure is translated or documented as needing application-level migration
- [ ] Every view is translated
- [ ] Data type incompatibilities are flagged with workarounds
- [ ] Row count validation queries are generated for every table
- [ ] Checksum validation queries are generated for critical tables
- [ ] Rollback scripts are complete and tested
- [ ] Downtime estimate accounts for all phases
- [ ] Pre-migration and post-migration checklists are included
- [ ] Application changes are documented
- [ ] The step-by-step execution guide is actionable -- a DBA can follow it without additional context
