# Schema Translation and Script Generation

With the full schema extracted and type mapping established, generate the migration scripts.

## Table Creation Order

Foreign keys create dependencies between tables. Tables must be created in topological order (dependencies first):

1. Build a directed graph where an edge from table A to table B means A has a foreign key referencing B.
2. Perform a topological sort on this graph.
3. If cycles exist (mutual foreign keys), break the cycle by deferring one foreign key constraint to be added after all tables are created.

Table creation order algorithm:
```
1. Find all tables with zero foreign key dependencies -- these go first.
2. Remove those tables from the graph.
3. Repeat until all tables are placed.
4. If the graph is not empty after exhaustion, cycles exist.
   For each cycle: create all tables without the cyclic FK, then ALTER TABLE to add it.
```

## DDL Script Generation

For each table, generate the target-dialect CREATE TABLE statement. The script must include:

1. Table definition with all columns, mapped types, defaults, and NOT NULL constraints
2. Primary key definition (inline or as constraint)
3. Unique constraints
4. Check constraints (translated to target dialect)
5. Foreign key constraints (respecting creation order above)
6. Indexes (translated to target syntax)
7. Comments on tables and columns (if supported by target)

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

## Sequence and Auto-Increment Translation

PostgreSQL to MySQL:
- Replace `SERIAL` / `BIGSERIAL` with `AUTO_INCREMENT`
- Replace `GENERATED ALWAYS AS IDENTITY` with `AUTO_INCREMENT`
- Remove all `CREATE SEQUENCE` statements
- Remove all `DEFAULT nextval('sequence_name')` and use `AUTO_INCREMENT` on the column
- After data load, set `AUTO_INCREMENT` value: `ALTER TABLE t AUTO_INCREMENT = [max_id + 1];`

MySQL to PostgreSQL:
- Replace `AUTO_INCREMENT` with `GENERATED ALWAYS AS IDENTITY` (preferred) or `SERIAL`
- After data load, reset sequence: `SELECT setval('table_column_seq', (SELECT MAX(column) FROM table));`

Relational to MongoDB:
- Remove auto-increment entirely; use ObjectId for `_id` unless the application requires numeric IDs
- If numeric IDs are required, document a counter collection pattern:
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

## Trigger Translation

Triggers are the most provider-specific feature. Each translation requires careful rewriting.

PostgreSQL triggers to MySQL:
- PostgreSQL uses trigger functions (PL/pgSQL); MySQL uses inline trigger bodies
- Replace `NEW.column` / `OLD.column` syntax (same in both, but function wrapper differs)
- Replace `RETURN NEW;` / `RETURN OLD;` (not needed in MySQL)
- Replace `TG_OP` with separate triggers per operation
- Replace `RAISE EXCEPTION` with `SIGNAL SQLSTATE`

MySQL triggers to PostgreSQL:
- Wrap trigger body in a PL/pgSQL function
- Add `RETURN NEW;` or `RETURN NULL;` as appropriate
- Replace `SIGNAL SQLSTATE` with `RAISE EXCEPTION`

Relational triggers to MongoDB:
- Document that MongoDB does not have database-level triggers
- Recommend alternatives:
  - MongoDB Change Streams (for event-driven processing)
  - Application-level middleware (Mongoose pre/post hooks)
  - Atlas Triggers (if using MongoDB Atlas)

PlanetScale target:
- PlanetScale does not support triggers
- Document all trigger logic that must move to the application layer
- Generate application-level middleware code or ORM hooks as replacements

## Stored Procedure and Function Translation

PostgreSQL to MySQL:
- Replace `CREATE OR REPLACE FUNCTION` with `CREATE PROCEDURE` or `CREATE FUNCTION`
- Replace PL/pgSQL syntax with MySQL procedural SQL
- Replace `RETURNS TABLE(...)` with result set from SELECT
- Replace `$$` delimiters with `DELIMITER //` ... `//` pattern
- Replace `RAISE NOTICE` with `SELECT` for debug output
- Replace `RAISE EXCEPTION` with `SIGNAL SQLSTATE`
- Replace `PERFORM` with `DO` or `SELECT ... INTO @dummy`
- Replace `RETURNING` clause (not available in MySQL; use `LAST_INSERT_ID()`)

MySQL to PostgreSQL:
- Replace `DELIMITER` pattern with `$$` delimiters
- Replace `SIGNAL SQLSTATE` with `RAISE EXCEPTION`
- Replace `LAST_INSERT_ID()` with `RETURNING` clause or `currval()`
- Replace `GROUP_CONCAT` with `string_agg`
- Replace `IFNULL` with `COALESCE`
- Replace `IF()` function with `CASE WHEN`

Relational to MongoDB:
- Stored procedures do not exist in MongoDB
- Translate to:
  - Aggregation pipelines (for data processing logic)
  - Application-level service functions
  - MongoDB Atlas Functions (if using Atlas)

PlanetScale target:
- PlanetScale does not support stored procedures
- All procedural logic must move to the application layer

## View Translation

Views are generally straightforward to translate but may contain provider-specific SQL:

1. Extract the view definition SQL.
2. Translate any provider-specific functions (see references/type-mapping.md function mapping).
3. Translate data types in CAST expressions.
4. Adjust JOIN syntax if needed.
5. For materialized views (PostgreSQL), note that MySQL does not support them natively -- recommend creating a table with a refresh procedure instead.
