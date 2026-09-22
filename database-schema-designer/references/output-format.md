# Output Format

Structure the deliverable in this order. Omit sections that do not apply (for example, scaling notes for a small internal tool).

````markdown
# [Domain] schema - [Engine and version]

## Assumptions
- [Volumes, tenancy model, anything inferred rather than stated]

## ERD
```mermaid
erDiagram
  ...
```

## DDL
```sql
-- Full CREATE statements: tables, constraints, indexes, triggers, RLS
```

## Query-to-index map
| Query | Served by |
|---|---|

## Design decisions
- [Key type, why]
- [Each deliberate denormalization, and the query it serves]
- [ON DELETE choices that are not obvious]

## Migrations
```sql
-- up
```
```sql
-- down (mark destructive steps)
```

## Verification
- [What was run: DDL applied to Postgres 18, EXPLAIN results for key queries]
- [Or: "Not executed; reviewed by hand"]

## Later, if needed
- [Partitioning trigger point, read replicas, archival, caching]
````

If the user uses an ORM, add the equivalent model definitions (Prisma schema, Drizzle tables, Django models) after the DDL, or deliver those instead of raw SQL when that is what the project uses.
