# Data Type and Function Mapping

The core translation layer. Map every source type to the best target type, and translate provider-specific SQL functions.

## PostgreSQL to MySQL Type Map

| PostgreSQL Type | MySQL Type | Notes |
|----------------|-----------|-------|
| SMALLINT | SMALLINT | Direct |
| INTEGER | INT | Direct |
| BIGINT | BIGINT | Direct |
| SERIAL | INT AUTO_INCREMENT | Remove DEFAULT nextval() |
| BIGSERIAL | BIGINT AUTO_INCREMENT | Remove DEFAULT nextval() |
| NUMERIC(p,s) | DECIMAL(p,s) | Direct |
| REAL | FLOAT | Direct |
| DOUBLE PRECISION | DOUBLE | Direct |
| MONEY | DECIMAL(19,4) | Loses currency formatting |
| BOOLEAN | TINYINT(1) | TRUE/FALSE to 1/0 |
| CHAR(n) | CHAR(n) | Direct |
| VARCHAR(n) | VARCHAR(n) | Direct |
| TEXT | LONGTEXT | MySQL TEXT is 65KB; LONGTEXT is 4GB |
| BYTEA | LONGBLOB | Binary data |
| DATE | DATE | Direct |
| TIME | TIME | Direct |
| TIMESTAMP | DATETIME(6) | MySQL TIMESTAMP has 2038 limit |
| TIMESTAMP WITH TIME ZONE | DATETIME(6) | Store timezone separately or use UTC |
| INTERVAL | VARCHAR(255) | No native interval in MySQL |
| UUID | CHAR(36) or BINARY(16) | CHAR(36) for readability, BINARY(16) for performance |
| JSON | JSON | Direct (MySQL 5.7+) |
| JSONB | JSON | Loses binary optimization; add generated columns for indexed paths |
| ARRAY | JSON | No native arrays in MySQL |
| HSTORE | JSON | Key-value to JSON object |
| INET | VARCHAR(45) | IPv4 and IPv6 |
| CIDR | VARCHAR(45) | Network address |
| MACADDR | VARCHAR(17) | MAC address string |
| POINT | POINT | Spatial type (requires spatial index changes) |
| GEOMETRY | GEOMETRY | Spatial type |
| TSVECTOR | FULLTEXT INDEX | Use FULLTEXT index on relevant columns |
| ENUM('a','b') | ENUM('a','b') | Direct (but MySQL ENUM has different behavior) |
| INT4RANGE | VARCHAR(255) | No native range types in MySQL |
| BIT(n) | BIT(n) | Direct |
| XML | LONGTEXT | No native XML in MySQL |

## MySQL to PostgreSQL Type Map

| MySQL Type | PostgreSQL Type | Notes |
|-----------|----------------|-------|
| TINYINT | SMALLINT | Direct |
| TINYINT(1) | BOOLEAN | If used as boolean |
| SMALLINT | SMALLINT | Direct |
| MEDIUMINT | INTEGER | No MEDIUMINT in Postgres |
| INT | INTEGER | Direct |
| BIGINT | BIGINT | Direct |
| INT AUTO_INCREMENT | SERIAL or GENERATED ALWAYS AS IDENTITY | Prefer IDENTITY for new schemas |
| FLOAT | REAL | Direct |
| DOUBLE | DOUBLE PRECISION | Direct |
| DECIMAL(p,s) | NUMERIC(p,s) | Direct |
| BIT(n) | BIT(n) | Direct |
| CHAR(n) | CHAR(n) | Direct |
| VARCHAR(n) | VARCHAR(n) | Direct |
| TINYTEXT | TEXT | Postgres TEXT has no size limit |
| TEXT | TEXT | Direct |
| MEDIUMTEXT | TEXT | Direct |
| LONGTEXT | TEXT | Direct |
| TINYBLOB | BYTEA | Direct |
| BLOB | BYTEA | Direct |
| MEDIUMBLOB | BYTEA | Direct |
| LONGBLOB | BYTEA | Direct |
| DATE | DATE | Direct |
| TIME | TIME | Direct |
| DATETIME | TIMESTAMP | Direct |
| TIMESTAMP | TIMESTAMP WITH TIME ZONE | MySQL TIMESTAMP is UTC-converted |
| YEAR | SMALLINT | No YEAR type in Postgres |
| ENUM('a','b') | VARCHAR + CHECK or CREATE TYPE | Prefer CREATE TYPE for Postgres enums |
| SET('a','b') | TEXT[] or VARCHAR + CHECK | Use array type |
| JSON | JSONB | Prefer JSONB for indexing |
| GEOMETRY | GEOMETRY (PostGIS) | Requires PostGIS extension |
| POINT | POINT | Native or PostGIS |
| BINARY(n) | BYTEA | Direct |
| VARBINARY(n) | BYTEA | Direct |

## Relational to MongoDB Type Map

| SQL Type | MongoDB (BSON) Type | Notes |
|---------|-------------------|-------|
| INTEGER / INT | NumberInt (int32) | Direct |
| BIGINT | NumberLong (int64) | Direct |
| SERIAL / AUTO_INCREMENT | ObjectId or NumberLong | ObjectId preferred for _id |
| NUMERIC / DECIMAL | NumberDecimal (Decimal128) | Direct |
| FLOAT / REAL | Double | Direct |
| BOOLEAN | Boolean | Direct |
| CHAR / VARCHAR / TEXT | String | Direct |
| DATE | Date | Direct |
| TIMESTAMP | Date | MongoDB Date is millisecond precision |
| BYTEA / BLOB | BinData | Direct |
| UUID | String or BinData(4) | BinData(4) is more compact |
| JSON / JSONB | Object | Native -- embed directly |
| ARRAY | Array | Native -- embed directly |
| ENUM | String + validation | Use JSON Schema validator |

## MongoDB to Relational Type Map

| MongoDB (BSON) Type | PostgreSQL Type | MySQL Type | Notes |
|-------------------|----------------|-----------|-------|
| ObjectId | CHAR(24) or UUID | CHAR(24) or BINARY(12) | Convert to hex string or generate new UUID |
| String | TEXT or VARCHAR | VARCHAR(n) or TEXT | Inspect max lengths in sample data |
| NumberInt (int32) | INTEGER | INT | Direct |
| NumberLong (int64) | BIGINT | BIGINT | Direct |
| Double | DOUBLE PRECISION | DOUBLE | Direct |
| NumberDecimal | NUMERIC | DECIMAL | Direct |
| Boolean | BOOLEAN | TINYINT(1) | Direct |
| Date | TIMESTAMP WITH TIME ZONE | DATETIME(3) | Direct |
| BinData | BYTEA | LONGBLOB | Direct |
| Array | JSONB or junction table | JSON or junction table | Simple arrays: JSONB/JSON; relational arrays: junction table |
| Embedded Object | JSONB or separate table | JSON or separate table | Decide based on query patterns |
| Null | NULL | NULL | Nullable columns |
| Regex | TEXT | VARCHAR | Store pattern as string |
| Timestamp (BSON) | TIMESTAMP | TIMESTAMP | Internal MongoDB type -- convert to standard timestamp |

## Common SQL Function Mapping

| PostgreSQL | MySQL | Notes |
|-----------|-------|-------|
| NOW() | NOW() | Direct |
| CURRENT_TIMESTAMP | CURRENT_TIMESTAMP | Direct |
| string_agg(col, ',') | GROUP_CONCAT(col SEPARATOR ',') | Different syntax |
| COALESCE(a, b) | COALESCE(a, b) or IFNULL(a, b) | Direct |
| CONCAT_WS(',', a, b) | CONCAT_WS(',', a, b) | Direct |
| SUBSTRING(s FROM n FOR m) | SUBSTRING(s, n, m) | Different syntax |
| EXTRACT(EPOCH FROM ts) | UNIX_TIMESTAMP(ts) | Different function |
| TO_CHAR(ts, 'YYYY-MM-DD') | DATE_FORMAT(ts, '%Y-%m-%d') | Different format codes |
| INTERVAL '1 day' | INTERVAL 1 DAY | Different syntax |
| GENERATE_SERIES(1, 10) | Recursive CTE or sequence table | No direct equivalent |
| ARRAY_AGG(col) | JSON_ARRAYAGG(col) | MySQL 5.7+ |
| UNNEST(array_col) | JSON_TABLE(...) | MySQL 8.0+ |
| ANY(array) | IN (...) or JSON_CONTAINS | Different approach |
| ILIKE | LIKE (case-insensitive collation) | Set collation or use LOWER() |
| SIMILAR TO | REGEXP | Different regex engine |
| ~ (regex match) | REGEXP | Direct equivalent |
| gen_random_uuid() | UUID() | Direct equivalent |
| RETURNING id | LAST_INSERT_ID() | Different approach |
| ON CONFLICT DO UPDATE | INSERT ... ON DUPLICATE KEY UPDATE | Different syntax |
| LIMIT n OFFSET m | LIMIT m, n or LIMIT n OFFSET m | MySQL supports both |
| BOOLEAN true/false | 1/0 | Literal translation |
| ::type (cast) | CAST(x AS type) | Postgres shorthand |
