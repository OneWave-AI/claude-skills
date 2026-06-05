# Data Migration Scripts

## Data Export from Source

PostgreSQL / Supabase:
```bash
# Full table export to CSV
pg_dump --data-only --format=plain --table=[schema].[table] --file=[table].sql [dbname]

# Or CSV format for cross-platform compatibility
psql -c "COPY [schema].[table] TO STDOUT WITH CSV HEADER" [dbname] > [table].csv
```

MySQL / PlanetScale:
```bash
# Full table export
mysqldump --no-create-info --tab=/tmp/export --fields-terminated-by=',' --fields-enclosed-by='"' --lines-terminated-by='\n' [dbname] [table]

# Or SELECT INTO OUTFILE
mysql -e "SELECT * INTO OUTFILE '/tmp/[table].csv' FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\n' FROM [table]" [dbname]
```

MongoDB:
```bash
# Export collection to JSON
mongoexport --db=[dbname] --collection=[collection] --out=[collection].json --jsonArray

# Or BSON for binary data preservation
mongodump --db=[dbname] --collection=[collection] --out=./dump/
```

## Data Transformation

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

## Data Import to Target

PostgreSQL / Supabase (target):
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

MySQL / PlanetScale (target):
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

MongoDB (target):
```bash
# Import from JSON
mongoimport --db=[dbname] --collection=[collection] --file=[collection].json --jsonArray

# Or from BSON dump
mongorestore --db=[dbname] --collection=[collection] ./dump/[dbname]/[collection].bson
```
