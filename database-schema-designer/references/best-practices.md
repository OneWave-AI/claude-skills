# Schema Design Best Practices

## Naming Conventions

- Use snake_case for table and column names.
- Pluralize table names (users, posts).
- Use descriptive foreign key names (user_id, not uid).
- Prefix indexes (idx_table_column).
- Prefix constraints (fk_, uk_, ck_).

## Data Types

- Use appropriate types (INT vs BIGINT, VARCHAR vs TEXT).
- Consider storage size.
- Use ENUM for fixed sets of values.
- Use JSON/JSONB for flexible attributes.
- Use proper date/time types (TIMESTAMP vs DATETIME).

## Indexes

- Index foreign keys.
- Index columns in WHERE clauses.
- Add composite indexes for multi-column queries.
- Consider covering indexes.
- Monitor index usage and remove unused ones.

## Relationships

- Always use foreign keys in relational databases.
- Cascade deletes where appropriate.
- Consider soft deletes for audit trails.
- Use junction tables for many-to-many.

## Performance

- Denormalize for read-heavy workloads.
- Partition large tables.
- Use materialized views for complex queries.
- Consider read replicas.
- Plan for archival of old data.

## SQL Database Design

- Identify entities and their attributes.
- Define primary keys (prefer UUIDs for distributed systems).
- Establish relationships (1:1, 1:N, N:M).
- Normalize to 3NF (unless denormalization is needed for performance).
- Add appropriate indexes.
- Define foreign key constraints.
- Include timestamps (created_at, updated_at).
- Add soft delete flags if needed.
- Plan for data archival.

## NoSQL Database Design

- Design for access patterns (query-first approach).
- Decide embed vs reference per relationship.
- Plan for denormalization.
- Design indexes for common queries.
- Account for document size limits.
- Plan for eventual consistency.

## Output Quality Checklist

Ensure every schema:
- Follows normalization principles (unless deliberately denormalized).
- Includes all necessary constraints.
- Has appropriate indexes.
- Uses proper data types.
- Includes timestamps.
- Has clear relationships.
- Considers scalability.
- Includes migration scripts.
- Follows naming conventions.
- Is documented with comments.
- Considers performance implications.
- Includes rollback capability.
