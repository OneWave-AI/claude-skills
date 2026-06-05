# data-pipeline-spec.md Template

Generate a comprehensive `data-pipeline-spec.md` for every pipeline as the final output. It is the living specification the team uses to understand, operate, and maintain the pipeline. Reference all implementation files and incorporate the design decisions made during the process. The spec must contain these sections.

```markdown
# Data Pipeline Specification: [Pipeline Name]

## Overview
- **Pipeline Name**: [name]
- **Version**: [version]
- **Owner**: [team/person]
- **Created**: [date]
- **Last Updated**: [date]
- **Status**: [draft/active/deprecated]

## Purpose
[2-3 sentences describing what this pipeline does and why it exists.]

## Architecture
[Describe the chosen architecture pattern and why it was selected.]

### Data Flow Diagram
[ASCII or mermaid diagram showing the end-to-end data flow.]

## Data Sources
### [Source 1 Name]
- **Type**: [database/api/file/stream]
- **Connection**: [connection details, redacted secrets]
- **Tables/Endpoints**: [list of tables or API endpoints]
- **Extraction Strategy**: [full/incremental/cdc]
- **Volume**: [estimated rows/day, total size]
- **Schema**: [key columns, data types, primary keys]

## Destination
- **Type**: [warehouse/lake/database]
- **Target Tables**: [list]
- **Schema Design**: [star/snowflake/OBT/vault]
- **Partitioning**: [strategy]
- **Clustering**: [fields]

## Transformations
### [Transform 1 Name]
- **Input**: [source tables]
- **Output**: [target table]
- **Logic**: [description of business rules]
- **SQL/Code**: [reference to implementation file]

## Data Quality Checks
### Pre-Transform Checks
| Check | Column | Severity | Threshold |
|-------|--------|----------|-----------|
| not_null | id | critical | 0% null |

### Post-Transform Checks
| Check | Column | Severity | Threshold |
|-------|--------|----------|-----------|

## Scheduling
- **Frequency**: [cron expression and human-readable]
- **Timezone**: [timezone]
- **Dependencies**: [upstream pipelines]
- **SLA**: [maximum acceptable completion time]

## Error Handling
- **Retry Policy**: [attempts, backoff strategy]
- **Dead Letter Queue**: [where failed records go]
- **Alerting**: [channels and severity thresholds]
- **Manual Recovery**: [steps for manual intervention]

## Monitoring
- **Metrics**: [list of tracked metrics]
- **Dashboards**: [links to monitoring dashboards]
- **Alert Rules**: [conditions and channels]

## Operational Runbook
### Starting the Pipeline
[Steps to start/restart]

### Stopping the Pipeline
[Steps to gracefully stop]

### Backfilling
[Steps to backfill historical data]

### Common Issues and Resolutions
| Issue | Symptoms | Resolution |
|-------|----------|------------|
| [issue] | [symptoms] | [steps] |

## Change Log
| Date | Version | Change | Author |
|------|---------|--------|--------|
| [date] | 1.0.0 | Initial pipeline | [author] |
```
