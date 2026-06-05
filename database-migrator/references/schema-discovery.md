# Source Schema Discovery

Extract everything from the source database. This is the foundation of the entire migration.

## Relational Databases (Postgres, MySQL, Supabase, PlanetScale)

Extract the following using information_schema queries or provider-specific catalog queries.

### Tables and Columns

PostgreSQL / Supabase:
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

MySQL / PlanetScale:
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

### Primary Keys

PostgreSQL / Supabase:
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

MySQL / PlanetScale:
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

### Foreign Keys

PostgreSQL / Supabase:
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

MySQL / PlanetScale:
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

### Indexes

PostgreSQL / Supabase:
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

MySQL / PlanetScale:
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

### Check Constraints

PostgreSQL / Supabase:
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

MySQL 8.0+:
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

### Triggers

PostgreSQL / Supabase:
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

MySQL / PlanetScale:
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

### Stored Procedures and Functions

PostgreSQL / Supabase:
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

MySQL / PlanetScale:
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

### Views

PostgreSQL / Supabase:
```sql
SELECT
    table_schema,
    table_name AS view_name,
    view_definition
FROM information_schema.views
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;
```

MySQL / PlanetScale:
```sql
SELECT
    TABLE_SCHEMA,
    TABLE_NAME AS VIEW_NAME,
    VIEW_DEFINITION
FROM information_schema.VIEWS
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_SCHEMA, TABLE_NAME;
```

### Sequences (PostgreSQL / Supabase only)
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

### Enums (PostgreSQL / Supabase only)
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

### Row Counts

PostgreSQL / Supabase (fast estimate):
```sql
SELECT
    schemaname,
    relname AS table_name,
    n_live_tup AS estimated_row_count
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;
```

MySQL / PlanetScale:
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

## MongoDB

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
- Validators: `db.getCollectionInfos()` for JSON Schema validators
- Capped collections: Size and max document limits
- Sharding config: `sh.status()` if sharded
- Aggregation pipelines saved as views: `db.system.views.find()`

## Supabase-Specific Extraction

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

## PlanetScale-Specific Considerations

PlanetScale does not support:
- Foreign key constraints at the database level (enforced at application level)
- Stored procedures
- Triggers
- Events

When PlanetScale is the target, flag all of these for application-level handling. When PlanetScale is the source, note that foreign key relationships must be inferred from naming conventions and application code.
