# Edge Cases and Quality Checklist

## Extremely Large Tables (100M+ rows)

For tables exceeding 100 million rows:

1. Chunked export: Export in batches of 1-10 million rows using `LIMIT/OFFSET` or range-based `WHERE id BETWEEN x AND y`.
2. Parallel import: Split data files and import in parallel using multiple connections.
3. Deferred index creation: Create the table without indexes, load data, then create indexes. This is significantly faster than loading into an indexed table.
4. Partitioned loading: If the target supports partitioning, create partitions first and load into each partition in parallel.
5. Progress tracking: Generate a progress script that reports rows loaded vs total rows.

## Schema Differences That Require Data Transformation

When a type mapping is not lossless:

1. Precision loss: Flag any column where the target type has less precision. Example: PostgreSQL NUMERIC(38,18) to MySQL DECIMAL(38,18) is lossless, but NUMERIC(100,50) exceeds MySQL's limit of DECIMAL(65,30).
2. Encoding issues: UTF-8 4-byte characters require `utf8mb4` in MySQL, not `utf8`.
3. Timezone handling: Document whether timestamps are stored as UTC or local time, and how the target handles timezone conversion.
4. NULL vs empty string: PostgreSQL distinguishes NULL from empty string; some applications may not.

## MongoDB Document Flattening (MongoDB to Relational)

When migrating from MongoDB to a relational database:

1. Top-level fields: Map directly to columns in a primary table.
2. Embedded objects: Two strategies:
   - Flatten: Prefix column names with the object path (e.g., `address.street` becomes `address_street`). Use when the object is always present and has a fixed schema.
   - Separate table: Create a related table with a foreign key. Use when the object is optional or has variable schema.
3. Embedded arrays: Always create a junction or child table. Each array element becomes a row.
4. Polymorphic documents: Documents in the same collection with different shapes. Options:
   - Single Table Inheritance: One wide table with nullable columns for each document shape.
   - Class Table Inheritance: Separate tables per document shape with a shared base table.
   - Discriminator column: Single table with a `type` column to distinguish shapes.
5. Nested arrays of objects: Requires recursive flattening into multiple tables with foreign keys at each level.

## PlanetScale Foreign Key Workarounds

Since PlanetScale does not support database-level foreign keys:

1. Document all relationships in the migration plan as application-level constraints.
2. Generate application-level validation code (e.g., Prisma schema with `@relation`, or custom middleware).
3. Generate orphan detection queries to run periodically:
   ```sql
   -- Check for orphaned child rows (run periodically)
   SELECT c.id, c.[fk_column]
   FROM [child_table] c
   LEFT JOIN [parent_table] p ON c.[fk_column] = p.id
   WHERE c.[fk_column] IS NOT NULL AND p.id IS NULL;
   ```
4. Document cascade delete logic that must be implemented in the application.

## Supabase-Specific Migration Considerations

When migrating to Supabase:

1. Row Level Security (RLS): Generate RLS policies based on the application's authorization model. Document that RLS must be enabled on all tables exposed via the Supabase API.
2. Realtime subscriptions: Identify tables that need realtime and add them to the Supabase publication.
3. Storage buckets: If the source database stores file references, map them to Supabase Storage.
4. Edge Functions: If stored procedures contain API-callable logic, recommend migrating to Supabase Edge Functions.
5. Auth integration: If the source has a users table, document how to integrate with Supabase Auth.

## Multi-Schema or Multi-Database Migration

When the source has multiple schemas or databases:

1. Map source schemas to target schemas (if the target supports multiple schemas).
2. Merge schemas: If the target is single-schema (e.g., PlanetScale), prefix table names with the schema name.
3. Cross-schema references: Identify and document all cross-schema foreign keys. These may need special handling.
4. Schema-level permissions: Document permission differences between source and target.

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
- [ ] The step-by-step execution guide is actionable -- a DBA can follow it without additional context
