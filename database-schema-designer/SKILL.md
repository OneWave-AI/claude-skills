---
name: database-schema-designer
description: Designs relational and document database schemas from requirements or an existing app - tables and collections, keys, relationships, constraints, indexes driven by real query patterns, ERDs, and reversible migration scripts - with PostgreSQL (including Supabase) as the default and MySQL, SQLite, and MongoDB supported. Use when the user wants to model data for a new app or feature, review or fix an existing schema, choose keys or indexes, plan multi-tenancy, normalize or denormalize, or write CREATE TABLE statements or migrations, even if they just describe their app and ask "how should I store this". For moving data between database providers, use database-migrator.
---

# Database Schema Designer

Design a schema that enforces the data's rules in the database and makes the app's real queries fast.

## Workflow

1. **Collect requirements.** Get from the conversation or codebase, and ask only for what blocks the design:
   - Engine and version (default: PostgreSQL 18; check `docker-compose.yml`, ORM config, or Supabase project if present)
   - Entities and how they relate, in plain language
   - The 5-10 most frequent or most important queries, including filters and sort order
   - Volume and growth (rows per table per year), read/write mix
   - Tenancy (single app, multi-tenant by organization), retention, audit, and compliance needs (PII, deletion requests)
   - ORM or migration tool in use (Prisma, Drizzle, Rails, Django, Alembic, Supabase migrations, plain SQL)

2. **Model entities and relationships.** List entities, attributes, and cardinality (1:1, 1:N, N:M). Normalize to 3NF by default; denormalize only for a named query that needs it, and say which.

3. **Choose keys and types** using [references/postgres.md](references/postgres.md) (or [references/other-engines.md](references/other-engines.md) for MySQL, SQLite, MongoDB). Defaults for Postgres: `bigint generated always as identity` or `uuid DEFAULT uuidv7()` primary keys, `text` over `varchar(n)`, `timestamptz` for every timestamp, `numeric` for money.

4. **Encode the rules as constraints.** `NOT NULL` wherever a value is required, `UNIQUE` for natural keys, `CHECK` for ranges and allowed values, foreign keys with a deliberate `ON DELETE` choice for each. Data rules that live only in app code get broken by the next script or admin fix.

5. **Derive indexes from the queries in step 1**, not from a checklist. For each query, name the index that serves it. Index every foreign key column you join or cascade on (Postgres does not do this automatically). Do not add an index a `UNIQUE` or primary key already provides.

6. **Write the deliverable**: DDL, ERD, index rationale, and migrations with rollback, using [references/schema-templates.md](references/schema-templates.md) and the layout in [references/output-format.md](references/output-format.md). Match the user's migration tool if they have one.

7. **Verify.** If a database is available (local Postgres, Docker `postgres:18`, a Supabase branch), run the DDL, insert a few rows, and `EXPLAIN` the key queries to confirm the planned indexes are used. Otherwise, walk each query from step 1 against the schema by hand. Then check the list below.

## Checks before delivering

- Every query from step 1 is served by a stated index or is explained as a scan that is fine at the expected size.
- Every foreign key has an explicit `ON DELETE` behavior and an index on the referencing column.
- No timestamp without time zone; no floating point for money; no `varchar(255)` by habit.
- `updated_at` actually updates: a `DEFAULT now()` only sets it on insert, so add a trigger or set it in the ORM.
- Uniqueness that should ignore case (emails, usernames) is enforced case-insensitively.
- Multi-tenant tables carry `tenant_id` (or `org_id`), include it in unique constraints and leading index columns, and have row-level security if the database is reachable from clients (always on Supabase).
- Migrations that touch large existing tables avoid long locks (see migration safety in [references/postgres.md](references/postgres.md)).
- Rollback scripts are real inverses, and destructive rollbacks (dropping a column with data) are called out.

## Worked example

Request: "Multi-tenant project tracker: orgs, users who can belong to several orgs, projects per org, tasks per project. The main screen lists a project's open tasks by due date."

- Entities: `orgs`, `users`, `org_members` (N:M between users and orgs with a `role`), `projects` (N:1 org), `tasks` (N:1 project, optional assignee).
- Key query: open tasks for one project ordered by due date, so a partial index `ON tasks (project_id, due_at) WHERE status <> 'done'`.
- Rules as constraints: `UNIQUE (org_id, user_id)` on `org_members`; `CHECK (role IN ('owner','admin','member'))`; `status` limited by `CHECK`; unique project name per org with `UNIQUE (org_id, name)`.
- Deletes: removing an org cascades to projects and tasks; deleting a user sets `tasks.assignee_id` to null instead of deleting tasks.
- Tenancy: `tasks` carries `org_id` so row-level security can check membership without a join through `projects`, and a composite foreign key `(project_id, org_id) -> projects (id, org_id)` keeps the two consistent.

The full DDL for this example is in [references/schema-templates.md](references/schema-templates.md).

## Failure modes

- Designing tables before knowing the queries, then indexing every column "just in case". Each index slows every write.
- Postgres `ENUM` types for values that will change. Adding a value is easy, but removing or renaming one is painful; a `CHECK` constraint or lookup table is easier to evolve.
- Soft deletes (`deleted_at`) added everywhere by default. They leak into every query and unique constraint. Use them where there is a real restore or audit need, and pair them with partial unique indexes.
- Polymorphic foreign keys (`commentable_type` + `commentable_id`) that the database cannot enforce. Prefer separate nullable FKs with a `CHECK` that exactly one is set, or separate tables.
- Storing structured, queried fields inside `jsonb`. JSON is for sparse or truly variable attributes; anything you filter, join, or constrain on deserves a column.
