# Validation Plan

Every migration must be validated. Generate validation queries for both source and target.

## Row Count Validation

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

## Data Checksum Validation

Generate checksum queries for critical tables. Compare a hash of key columns between source and target.

PostgreSQL (source or target):
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

MySQL (source or target):
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

MongoDB (source or target):
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

## Foreign Key Integrity Validation

For every foreign key in the target, verify referential integrity:

```sql
-- Verify no orphaned foreign keys
SELECT COUNT(*) AS orphaned_rows
FROM [child_table] c
LEFT JOIN [parent_table] p ON c.[fk_column] = p.[pk_column]
WHERE c.[fk_column] IS NOT NULL AND p.[pk_column] IS NULL;
```

Expected result: zero orphaned rows for every foreign key relationship.

## Index Verification

PostgreSQL / Supabase:
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = '[target_schema]'
ORDER BY tablename, indexname;
```

MySQL / PlanetScale:
```sql
SELECT TABLE_NAME, INDEX_NAME, COLUMN_NAME, NON_UNIQUE
FROM information_schema.STATISTICS
WHERE TABLE_SCHEMA = DATABASE()
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;
```

Compare the count and names against the expected index list from the migration scripts.

## Trigger and Procedure Verification

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

## Sample Data Spot-Check

For the 5 largest tables, generate queries that compare specific rows:

```sql
-- Pick 10 random IDs from source, then verify those exact rows exist in target with matching data
-- Source:
SELECT * FROM [table] WHERE id IN ([random_id_1], [random_id_2], ..., [random_id_10]) ORDER BY id;

-- Target:
SELECT * FROM [table] WHERE id IN ([random_id_1], [random_id_2], ..., [random_id_10]) ORDER BY id;
```
