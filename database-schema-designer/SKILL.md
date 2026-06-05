---
name: database-schema-designer
description: Design optimized database schemas for SQL and NoSQL databases including tables, relationships, indexes, and constraints. Creates ERD diagrams, migration scripts, and data modeling best practices. Use when users need database design, schema optimization, or data architecture planning.
---

# Database Schema Designer

Design optimized, scalable database schemas with proper relationships and indexes.

## Contents

- `references/schema-templates.md` — SQL/NoSQL schema templates, ASCII ERD, and migration script templates.
- `references/output-format.md` — labeled section structure for the final deliverable.
- `references/best-practices.md` — naming, data types, indexes, relationships, SQL/NoSQL design rules, and the output quality checklist.

## Workflow

1. Gather requirements. Determine the database engine (PostgreSQL, MySQL, MongoDB, etc.), application domain, main entities, most common queries, expected data volume and growth, performance requirements, and any compliance constraints.

2. Design the schema. Apply the engine-appropriate rules in `references/best-practices.md` (SQL Database Design or NoSQL Database Design).

3. Generate the complete schema. Produce CREATE TABLE statements or collection documents using the templates in `references/schema-templates.md`.

4. Create the entity relationship diagram in text format following the ERD template in `references/schema-templates.md`.

5. Provide migration scripts with both up and down (rollback) paths, per the migration template in `references/schema-templates.md`.

6. Format the complete output using the labeled sections in `references/output-format.md`.

7. Verify the result against the output quality checklist in `references/best-practices.md`.

## Example Triggers

- "Design a database schema for an e-commerce platform"
- "Create SQL tables for a blog system"
- "Help me design a MongoDB schema for a social network"
- "Optimize this database schema for performance"
- "Generate migration scripts for my schema"

Generate production-ready, optimized database schemas that scale.
