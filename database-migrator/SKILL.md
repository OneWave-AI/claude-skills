---
name: database-migrator
description: Migrates databases between providers (Postgres, MySQL, Supabase, PlanetScale, MongoDB). Reads source schema, generates migration scripts, handles data type mapping, foreign keys, indexes, triggers, stored procedures. Validates migration with row counts and checksums. Generates migration-plan.md with step-by-step execution guide, rollback procedures, estimated downtime.
tools: Read, Write, Bash, Glob, Grep, Agent
user_invocable: true
---

# Database Migrator

Move schemas, data, and logic between database providers. This is a cross-provider migration engine, not a schema designer: it handles data type incompatibilities, provider-specific SQL dialects, foreign key ordering, sequence and auto-increment translation, trigger rewrites, and stored procedure conversion. It validates with row counts and checksums and produces an auditable migration-plan.md.

## Contents

- references/schema-discovery.md -- Extraction queries for relational, MongoDB, Supabase, and PlanetScale sources.
- references/type-mapping.md -- Data type maps (PG/MySQL/Mongo) and SQL function translation.
- references/script-generation.md -- DDL, sequence, trigger, procedure, and view translation.
- references/data-migration.md -- Export, transform, and import commands per provider.
- references/validation.md -- Row count, checksum, FK integrity, index, and spot-check queries.
- references/rollback-and-downtime.md -- Rollback scripts, backup/restore, downtime estimation.
- references/migration-plan-template.md -- Full migration-plan.md output template.
- references/edge-cases.md -- Large tables, lossy mappings, document flattening, multi-schema, quality checklist.

## Supported Paths and Complexity

Supported source/target pairs: PostgreSQL, MySQL, Supabase (Postgres), PlanetScale (MySQL), and MongoDB, in any direction.

- Low: Same underlying engine (e.g., Postgres to Supabase). Mostly connection and permission changes.
- Medium: Same paradigm, different dialect (e.g., Postgres to MySQL). Requires type mapping and dialect translation.
- Medium-High: Different dialect plus provider constraints (e.g., PlanetScale has no database-level foreign keys).
- High: Paradigm shift (e.g., relational to document). Requires schema redesign, not just translation.

## When to Use

- Moving a production database from one provider to another.
- Migrating between self-hosted and managed services.
- Replicating a schema across providers for multi-cloud or disaster recovery.
- Consolidating multiple databases into a single provider.
- Translating a complete data model between relational and MongoDB.
- Producing a validated, auditable migration plan before executing in production.

## When NOT to Use

- Designing a new schema from scratch (use database-schema-designer).
- Migrating application code between frameworks (use full-codebase-migrator).
- Changing a few columns or adding one table (write the ALTER statements directly).
- Real-time replication or CDC -- this skill generates point-in-time scripts, not streaming pipelines.

## Workflow

Follow these steps precisely when this skill is invoked.

1. Gather migration parameters. Establish: source provider and version; target provider and version; connection method (live or dump file); schema scope (which schemas/tables); data migration (schema only or schema + data, full or partial); downtime tolerance; data volume; application dependencies; and output location (default to current directory). If the user already supplied these, skip the questions and proceed.

2. Discover the source schema. Extract tables, columns, types, defaults, constraints, indexes, foreign keys, triggers, procedures, functions, views, sequences, enums, and row counts. For MongoDB, scan collections to infer schema. For Supabase, also extract RLS policies, extensions, and publications. See references/schema-discovery.md.

3. Map data types. Translate every source type to the best target type and flag lossy or precision-changing conversions. Translate provider-specific SQL functions. See references/type-mapping.md.

4. Generate schema scripts. Resolve table creation order by topological sort (defer cyclic foreign keys). Generate DDL, translate sequences/auto-increment, rewrite triggers and stored procedures, and translate views. See references/script-generation.md.

5. Generate data migration scripts. Produce export, transform, and import commands for the source and target providers. See references/data-migration.md.

6. Generate the validation plan. Produce row count, checksum, foreign key integrity, index, trigger/procedure, and sample data spot-check queries for source and target. See references/validation.md.

7. Generate the rollback plan and downtime estimate. Produce reverse-order DROP scripts, backup/restore commands, application rollback steps, and a phased downtime estimate with reduction strategies. See references/rollback-and-downtime.md.

8. Generate migration-plan.md. Assemble the executive summary, scope, schema inventory, type mapping, incompatibilities, scripts, validation, rollback, downtime, risk assessment, checklists, step-by-step execution guide, and required application changes. Use the template in references/migration-plan-template.md.

9. Handle edge cases. Account for extremely large tables, lossy mappings, MongoDB document flattening, PlanetScale foreign key workarounds, Supabase specifics, and multi-schema migrations. Verify the plan against the quality checklist. See references/edge-cases.md.
