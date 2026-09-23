# Other Engines

Differences from the PostgreSQL defaults in [postgres.md](postgres.md). Apply the same workflow; change the types and index features.

## MySQL 8.x (InnoDB)

- Character set `utf8mb4` with a `utf8mb4_0900_ai_ci` (or `_bin`) collation; plain `utf8` is a 3-byte alias that cannot store all of Unicode.
- Primary keys: `BIGINT UNSIGNED AUTO_INCREMENT`. InnoDB clusters rows by primary key, so random UUIDv4 keys fragment the table; if UUIDs are needed, store UUIDv7 (or `UUID_TO_BIN(UUID(), 1)`) in `BINARY(16)`.
- Timestamps: `DATETIME(6)` stored in UTC (set by the app), or `TIMESTAMP`, which is limited to 2038.
- `CHECK` constraints are enforced from 8.0.16; older versions parse and ignore them.
- No partial indexes. Use a generated column plus an index, or a composite index that includes the filter column.
- Functional indexes (8.0.13+): `CREATE INDEX idx_users_email_lower ON users ((lower(email)));`
- InnoDB creates an index for each foreign key automatically if none exists.
- `ENUM` is common but altering it rewrites the table on older versions; a lookup table is easier to evolve.
- Online DDL: prefer `ALGORITHM=INSTANT` or `INPLACE, LOCK=NONE` where supported; use gh-ost or pt-online-schema-change for large tables otherwise.
- No row-level security; enforce tenancy in the app or with views.

## SQLite

- Declare tables `STRICT` so column types are enforced.
- Foreign keys are off by default: run `PRAGMA foreign_keys = ON;` on every connection.
- `INTEGER PRIMARY KEY` is an alias for the rowid and the fastest key.
- Store timestamps as ISO 8601 `TEXT` in UTC or as Unix epoch `INTEGER`; pick one and be consistent.
- Partial and expression indexes are supported.
- `ALTER TABLE` is limited (no dropping constraints); many changes need the create-copy-rename pattern.
- Use WAL mode (`PRAGMA journal_mode = WAL;`) for concurrent readers.

## MongoDB

- Design from access patterns: list the queries, then shape documents so each common query reads one document or one index range.
- Embed when data is read together, owned by the parent, and bounded (order line items). Reference when data is shared, updated independently, or grows without limit (comments on a popular post).
- Documents are capped at 16 MB; unbounded arrays are the usual way to hit it.
- Enforce shape with `$jsonSchema` validators on the collection (see [schema-templates.md](schema-templates.md)).
- Compound index order follows the ESR rule: equality fields, then sort fields, then range fields.
- Multi-document transactions exist but cost more; a schema that needs them for common writes is often better modeled with embedding.
- Denormalized copies (a user's name on each post) need an update path; document which copies are allowed to go stale.
