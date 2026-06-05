# Schema Templates

Reference templates for generating SQL and NoSQL schemas. Replace bracketed placeholders with domain-specific values.

## SQL Schema Output

```sql
-- [Entity Name] Table
-- Purpose: [Description]

CREATE TABLE [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  [field_name] [TYPE] [CONSTRAINTS],
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_[table]_[field] ON [table]([field]);
CREATE INDEX idx_[table]_[field1]_[field2] ON [table]([field1], [field2]);

-- Foreign Keys
ALTER TABLE [child_table]
  ADD CONSTRAINT fk_[constraint_name]
  FOREIGN KEY ([foreign_key_field])
  REFERENCES [parent_table](id)
  ON DELETE CASCADE;
```

## NoSQL Schema Output (MongoDB example)

```javascript
// [Collection Name]
// Purpose: [Description]

{
  _id: ObjectId,
  [field_name]: [type],

  // Embedded document
  [embedded_object]: {
    field1: type,
    field2: type
  },

  // Reference
  [related_id]: ObjectId,  // Ref to [other_collection]

  created_at: ISODate,
  updated_at: ISODate
}

// Indexes
db.[collection].createIndex({ field: 1 })
db.[collection].createIndex({ field1: 1, field2: -1 })
db.[collection].createIndex({ field: "text" })  // Text search
```

## Entity Relationship Diagram (text format)

```
+---------------------+
|      users          |
+---------------------+
| id (PK)             |
| email (UNIQUE)      |
| name                |
| created_at          |
+----------+----------+
           |
           | 1:N
           |
+----------v----------+
|      posts          |
+---------------------+
| id (PK)             |
| user_id (FK)        |
| title               |
| content             |
| created_at          |
+----------+----------+
           |
           | N:M (via post_tags)
           |
+----------v----------+
|       tags          |
+---------------------+
| id (PK)             |
| name (UNIQUE)       |
+---------------------+
```

## Migration Scripts

```sql
-- Migration: create_users_table
-- Date: 2024-01-15

BEGIN;

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

COMMIT;
```

```sql
-- Rollback
BEGIN;
DROP TABLE users;
COMMIT;
```
