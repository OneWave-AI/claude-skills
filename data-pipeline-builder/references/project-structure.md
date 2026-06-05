# Project Structure and Architecture Patterns

## Project Structure

Organize all output files in this structure:

```
pipeline_name/
  README.md
  data-pipeline-spec.md
  config/
    pipeline_config.yaml
    connections.yaml.example
    .env.example
  src/
    extractors/
      __init__.py
      base_extractor.py
      [source_name]_extractor.py
    transformers/
      __init__.py
      base_transformer.py
      [transform_name]_transformer.py
    loaders/
      __init__.py
      base_loader.py
      [destination_name]_loader.py
    quality/
      __init__.py
      checks.py
      expectations.py
    utils/
      __init__.py
      logging_config.py
      retry.py
      metrics.py
  sql/
    staging/
      [table_name]_staging.sql
    transformations/
      [transform_name].sql
    quality_checks/
      [check_name].sql
  orchestration/
    dags/
      [pipeline_name]_dag.py
    schedules/
      schedule_config.yaml
  tests/
    unit/
      test_extractors.py
      test_transformers.py
      test_loaders.py
      test_quality.py
    integration/
      test_pipeline_e2e.py
    fixtures/
      sample_data/
  monitoring/
    alerts/
      alert_rules.yaml
    dashboards/
      pipeline_dashboard.json
  docker/
    Dockerfile
    docker-compose.yaml
  requirements.txt
  pyproject.toml
  Makefile
```

## Architecture Pattern Selection

Select the architecture pattern based on the gathered requirements.

### Batch ETL (Extract-Transform-Load)
- Best for: periodic bulk data movement with complex transformations.
- Typical stack: Airflow + Python/Spark + data warehouse.
- Use when: data freshness SLA >= 1 hour, complex business logic, multiple sources.

### Batch ELT (Extract-Load-Transform)
- Best for: loading raw data first, transforming in the warehouse.
- Typical stack: Airflow + Fivetran/Airbyte + dbt + data warehouse.
- Use when: warehouse has strong compute, transformations are SQL-expressible, schema evolution is frequent.

### Streaming ETL
- Best for: real-time or near-real-time data processing.
- Typical stack: Kafka/Kinesis + Flink/Spark Streaming + sink.
- Use when: data freshness SLA < 5 minutes, event-driven architecture.

### Micro-batch
- Best for: near-real-time with simpler infrastructure than full streaming.
- Typical stack: Airflow (short intervals) or Spark Structured Streaming.
- Use when: data freshness SLA 1-15 minutes, prefer batch simplicity.

### Hybrid (Lambda/Kappa)
- Best for: both real-time and batch requirements.
- Typical stack: streaming layer for speed + batch layer for accuracy.
- Use when: need both real-time dashboards and accurate historical reporting.

## Component Selection

For each pipeline, define these components:

1. Extractor: technology and approach for pulling data from each source.
2. Staging Layer: intermediate storage for raw extracted data.
3. Transformer: technology for applying business logic.
4. Loader: technology and approach for writing to the destination.
5. Orchestrator: scheduling and dependency management.
6. Monitor: observability, alerting, and data quality checks.
7. Error Handler: retry logic, dead letter queues, alerting on failures.
