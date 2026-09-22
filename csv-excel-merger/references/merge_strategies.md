# Merge Strategies

Reference for the `csv-excel-merger` skill: column matching, key normalization, conflict resolution, and deduplication.

## Column matching

Map columns onto one unified schema, in order of confidence:

1. **Exact** - `email` = `email`
2. **Normalized** - lowercase, trim, collapse spaces/hyphens/underscores: `E-Mail Address` -> `email_address`
3. **Known variant** - from the table below
4. **Fuzzy** - `difflib.get_close_matches(name, unified, cutoff=0.8)`; always confirm fuzzy matches with the user

| Unified      | Common variants                                      |
|--------------|------------------------------------------------------|
| `first_name` | `firstname`, `First Name`, `fname`, `given_name`     |
| `last_name`  | `lastname`, `Last Name`, `lname`, `surname`          |
| `full_name`  | `name`, `contact_name`, `Full Name`                  |
| `email`      | `e-mail`, `email_address`, `Email Address`, `mail`   |
| `phone`      | `phone_number`, `mobile`, `cell`, `tel`              |
| `company`    | `organization`, `org`, `account`, `company_name`     |
| `title`      | `job_title`, `position`, `role`                      |
| `created_at` | `date_added`, `signup_date`, `created`               |

If one file has `full_name` and another has `first_name` + `last_name`, split or join explicitly and say which you did.

## Key normalization

Apply before dedupe or join, to the key columns only:

```python
df["email"] = df["email"].str.strip().str.lower()
df["phone"] = df["phone"].str.replace(r"\D", "", regex=True).str[-10:]  # US numbers; adjust per country
df["company_key"] = (df["company"].str.lower()
                     .str.replace(r"[^\w\s]", "", regex=True)
                     .str.replace(r"\b(inc|llc|ltd|corp|co)\b", "", regex=True)
                     .str.strip())
```

Keep the original columns for output and use the normalized columns only for matching.

When no single column is unique, use a compound key: `subset=["email", "company_key"]`.

## Conflict resolution

When the same key appears in several files with different values:

| Strategy | When | How |
|----------|------|-----|
| Keep last | Sources are ordered by recency | Sort by recency, `drop_duplicates(keep="last")` |
| Keep first | First source is the system of record | `drop_duplicates(keep="first")` |
| Most complete | Sources are equally trusted | Sort by non-null count, keep the top row |
| Combine fields | Sources hold complementary fields | `groupby(key).first()` takes the first non-null per column |
| Flag for review | Values matter (money, legal names) | Write conflicting rows to `conflicts_review.csv` |

```python
# Most complete row wins
combined["_filled"] = combined.replace("", pd.NA).notna().sum(axis=1)
best = (combined.sort_values("_filled", kind="stable")
        .drop_duplicates(subset=["email"], keep="last")
        .drop(columns="_filled"))

# Combine complementary fields (first non-null per column, in source order)
combined_fields = combined.replace("", pd.NA).groupby("email", sort=False).first().reset_index()

# Collect real conflicts for review: keys where a column has more than one distinct value
conflicts = (combined.replace("", pd.NA).groupby("email")["phone"]
             .nunique().loc[lambda s: s > 1])
```

## Deduplication options

- **keep="first" / keep="last"** - exact key matches
- **keep=False** - drop every copy (for finding records that appear only once)
- **Fuzzy duplicates** - same person, different spelling: compare normalized name + company, or use a library such as `rapidfuzz`, and send matches for review rather than auto-merging

Always keep a `source_file` column so each surviving row can be traced to its origin.
