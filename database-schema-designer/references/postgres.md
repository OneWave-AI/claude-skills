# PostgreSQL Design Reference

Current major version: PostgreSQL 18. Features marked (18) need 18 or later; say so when the user's version is older.

## Contents
- Naming
- Primary keys
- Data types
- Constraints
- Indexes
- Newer features worth using
- Multi-tenancy and row-level security
- Partitioning and scale
- Migration safety

## Naming

- `snake_case`, plural table names (`users`, `order_items`), singular column names.
- Foreign keys: `<referenced_singular>_id` (`user_id`, `org_id`).
- Name constraints and indexes so errors are readable: `users_email_key`, `tasks_project_id_fkey`, `idx_tasks_project_due_open`.
- Avoid reserved words as names (`user`, `order`, `group`).

## Primary keys

| Choice | Use when | Notes |
|---|---|---|
| `bigint GENERATED ALWAYS AS IDENTITY` | Internal IDs, single database | Smallest and fastest. Prefer identity over `serial`, which is legacy. |
| `uuid DEFAULT uuidv7()` (18) | IDs exposed in URLs, generated across services, merged datasets | Time-ordered, so inserts stay local in the B-tree index, unlike random UUIDv4. On 17 or earlier, generate UUIDv7 in the app or use `gen_random_uuid()`. |
| Natural key | Stable codes such as ISO country codes | Rarely; natural keys change more than people expect. |

UUIDv7 embeds the creation time; do not use it where exposing that time is a problem.

## Data types

| Data | Use | Avoid |
|---|---|---|
| Text | `text`, with a `CHECK (char_length(x) <= n)` if a limit matters | `varchar(255)` by habit; there is no performance gain |
| Timestamps | `timestamptz` | `timestamp` without time zone |
| Dates only | `date` | Strings |
| Money | `numeric(12,2)` or integer minor units (`amount_cents bigint`) | `real`, `double precision`, `money` |
| Booleans | `boolean NOT NULL DEFAULT false` | Nullable booleans (three states by accident) |
| Allowed values | `text` + `CHECK (status IN (...))`, or a lookup table | `ENUM` types for lists that will change |
| Flexible attributes | `jsonb` (never `json`) | JSON for fields you filter or join on |
| Case-insensitive text | Unique index on `lower(email)`, or `citext` | Relying on the app to lowercase |
| IP addresses | `inet` | Text |
| Ranges | `tstzrange`, `daterange` | Two columns with no overlap protection |

## Constraints

- `NOT NULL` on every column that must have a value. Nullable should be a decision.
- `UNIQUE` for natural keys; in multi-tenant tables, scope it: `UNIQUE (org_id, slug)`.
- `CHECK` for ranges and allowed values: `CHECK (quantity > 0)`.
- Foreign keys with an explicit `ON DELETE`:
  - `CASCADE` for owned children (an order's line items)
  - `SET NULL` for optional references (a task's assignee)
  - `RESTRICT` / `NO ACTION` (default) for anything whose loss should block the delete
- Exclusion constraints for no-overlap rules (bookings): `EXCLUDE USING gist (room_id WITH =, during WITH &&)` (needs the `btree_gist` extension).

## Indexes

- Postgres does not index foreign key columns automatically. Index the referencing column whenever you join on it or delete parent rows, or cascades and joins will scan.
- `PRIMARY KEY` and `UNIQUE` already create an index; do not add a duplicate.
- Composite index order: equality columns first, then range or sort columns. `(project_id, due_at)` serves `WHERE project_id = $1 ORDER BY due_at`.
- Partial indexes for hot subsets: `... WHERE status <> 'done'`, `... WHERE deleted_at IS NULL`. Also the way to make uniqueness ignore soft-deleted rows.
- Expression indexes must match the query expression: `ON users (lower(email))` serves `WHERE lower(email) = $1`.
- Covering indexes with `INCLUDE (col)` enable index-only scans for small, hot reads.
- `jsonb`: a GIN index (`USING gin (attrs jsonb_path_ops)`) for containment queries (`@>`).
- Full-text: a generated `tsvector` column with a GIN index; trigram (`pg_trgm`) GIN for `ILIKE '%term%'`.
- BRIN for huge append-only tables ordered by time (logs, events).
- Skip scan (18): a multicolumn B-tree index can now serve queries that omit the leading column, when that column has few distinct values. It helps, but an index whose leading column matches the filter is still faster.
- Check usage later with `pg_stat_user_indexes` (`idx_scan = 0` means unused) and drop what is not used.

## Newer features worth using

- `uuidv7()` (18) - time-ordered UUID primary keys, see above.
- Virtual generated columns (18) - `GENERATED ALWAYS AS (expr)` is now virtual by default (computed on read, no storage). Virtual columns cannot be indexed; add `STORED` when you need an index on the column or read it constantly.
- Temporal constraints (18) - `PRIMARY KEY (id, valid_period WITHOUT OVERLAPS)` and `UNIQUE (... WITHOUT OVERLAPS)` on range columns, and `FOREIGN KEY (..., PERIOD valid_period)`, for versioned or effective-dated records (prices, contracts, assignments). Needs the `btree_gist` extension when the key mixes scalar and range columns.
- `RETURNING OLD.*, NEW.*` (18) - read before and after values in one `UPDATE`, useful for audit logging without triggers.
- `NULLS NOT DISTINCT` (15) - `UNIQUE NULLS NOT DISTINCT (a, b)` treats nulls as equal, so only one row with `b IS NULL` is allowed.
- `MERGE` (15) - standard upsert-and-delete in one statement; `INSERT ... ON CONFLICT` remains the simple upsert.

## Multi-tenancy and row-level security

- Shared tables with a `tenant_id` / `org_id` column suit most SaaS apps. Put the tenant column first in composite indexes and inside unique constraints.
- Denormalize `org_id` onto child tables that policies must check, and keep it consistent with a composite foreign key to the parent: `FOREIGN KEY (project_id, org_id) REFERENCES projects (id, org_id)` (the parent needs `UNIQUE (id, org_id)`).
- Row-level security: `ALTER TABLE t ENABLE ROW LEVEL SECURITY;` plus policies per operation. On Supabase, every table in an exposed schema needs RLS enabled and policies, because clients query it directly with the anon or authenticated key. Index the columns policies filter on.
- Wrap per-row function calls in policies in a subselect (`(select auth.uid())`) so they are evaluated once per query instead of once per row.

## Partitioning and scale

- Partition only when a table is large (roughly 100M+ rows or hundreds of GB) and queries or retention align with the partition key, usually time. Declarative range partitioning by month is the common case; dropping an old partition is far cheaper than `DELETE`.
- Primary keys and unique constraints on partitioned tables must include the partition key.
- Before partitioning, check that the right indexes and `VACUUM`/autovacuum settings are in place; most "big table" problems are index problems.

## Migration safety

On tables with real traffic:

- `CREATE INDEX CONCURRENTLY` (and `DROP INDEX CONCURRENTLY`) to avoid blocking writes. It cannot run inside a transaction block, so put it in its own migration and disable the tool's wrapping transaction.
- Adding a column with a constant default is instant. Adding `NOT NULL` to an existing column scans the table under a lock. Instead: on 18, `ADD CONSTRAINT x NOT NULL col NOT VALID`, backfill, then `VALIDATE CONSTRAINT x`; on older versions, add `CHECK (col IS NOT NULL) NOT VALID`, backfill, validate, then `SET NOT NULL` (the validated check lets Postgres skip the scan).
- Add foreign keys as `NOT VALID`, then `VALIDATE CONSTRAINT` in a separate step so the validation does not block writes.
- Set `lock_timeout` (for example `SET lock_timeout = '5s'`) so a migration waiting on a lock fails instead of queueing all traffic behind it.
- Rename and type changes break running app versions. Use expand and contract: add the new column, dual-write, backfill, switch reads, then drop the old column in a later release.

## Final checklist

- Keys: every table has a primary key; the type is deliberate.
- Types: `timestamptz`, `text`, `numeric` or integer cents, `jsonb` only for variable attributes.
- Constraints: `NOT NULL`, `UNIQUE`, `CHECK`, and foreign keys with explicit `ON DELETE`.
- Indexes: one per key query, foreign keys indexed, no duplicates of PK or unique indexes.
- `updated_at` maintained by a trigger or the ORM.
- Tenancy and RLS in place where clients can reach the database.
- Migrations reversible and safe for the table sizes involved.
