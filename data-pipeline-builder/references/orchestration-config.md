# Orchestration, Configuration, and Monitoring Patterns

Reference patterns for the Airflow DAG, pipeline configuration, and monitoring layers. Generate the DAG with all task dependencies wired up, and produce monitoring configuration with appropriate alert thresholds.

## Airflow DAG Pattern

```python
"""Airflow DAG template for orchestrating the data pipeline."""

from datetime import datetime, timedelta
from typing import Any

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.task_group import TaskGroup

# -- DAG Default Arguments ------------------------------------------------------

default_args: dict[str, Any] = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,
    "max_retry_delay": timedelta(minutes=60),
    "execution_timeout": timedelta(hours=2),
}

# -- DAG Definition -------------------------------------------------------------

with DAG(
    dag_id="PIPELINE_NAME",
    default_args=default_args,
    description="PIPELINE_DESCRIPTION",
    schedule="CRON_EXPRESSION",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=["data-pipeline", "PIPELINE_TAG"],
) as dag:

    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed")

    # -- Extraction Tasks -------------------------------------------------------
    with TaskGroup("extraction") as extraction_group:
        pass  # Generated extraction tasks go here

    # -- Quality Checks (Pre-Transform) -----------------------------------------
    with TaskGroup("pre_transform_quality") as pre_quality_group:
        pass  # Generated pre-transform quality checks go here

    # -- Transformation Tasks ---------------------------------------------------
    with TaskGroup("transformation") as transformation_group:
        pass  # Generated transformation tasks go here

    # -- Quality Checks (Post-Transform) ----------------------------------------
    with TaskGroup("post_transform_quality") as post_quality_group:
        pass  # Generated post-transform quality checks go here

    # -- Load Tasks -------------------------------------------------------------
    with TaskGroup("loading") as loading_group:
        pass  # Generated load tasks go here

    # -- Final Quality Checks ---------------------------------------------------
    with TaskGroup("final_quality") as final_quality_group:
        pass  # Generated final quality checks go here

    # -- DAG Dependencies -------------------------------------------------------
    (
        start
        >> extraction_group
        >> pre_quality_group
        >> transformation_group
        >> post_quality_group
        >> loading_group
        >> final_quality_group
        >> end
    )
```

## Pipeline Configuration Pattern

```yaml
# pipeline_config.yaml -- Central configuration for the data pipeline

pipeline:
  name: "PIPELINE_NAME"
  version: "1.0.0"
  description: "PIPELINE_DESCRIPTION"
  owner: "data-engineering"
  schedule: "0 6 * * *"  # Daily at 6 AM UTC
  timezone: "UTC"
  max_runtime_minutes: 120
  tags:
    - data-pipeline

sources:
  - name: "SOURCE_NAME"
    type: "postgres"  # postgres, mysql, api, s3, gcs, sftp, kafka
    connection:
      host: "${SOURCE_HOST}"
      port: 5432
      database: "${SOURCE_DB}"
      username: "${SOURCE_USER}"
      password: "${SOURCE_PASSWORD}"
    extraction:
      strategy: "incremental"  # full, incremental, cdc
      watermark_column: "updated_at"
      batch_size: 10000
      tables:
        - schema: "public"
          table: "TABLE_NAME"
          primary_key: "id"
          columns: "*"  # or list specific columns

destination:
  name: "DESTINATION_NAME"
  type: "bigquery"  # bigquery, snowflake, redshift, postgres, s3, gcs
  connection:
    project: "${GCP_PROJECT}"
    dataset: "${BQ_DATASET}"
    location: "US"
  loading:
    strategy: "upsert"  # append, overwrite, upsert, merge, scd_type_2
    partition_field: "created_date"
    cluster_fields:
      - "category"
      - "region"

transformations:
  - name: "TRANSFORM_NAME"
    type: "sql"  # sql, python, dbt
    description: "TRANSFORM_DESCRIPTION"
    input_tables:
      - "staging.SOURCE_TABLE"
    output_table: "analytics.TARGET_TABLE"
    sql_file: "sql/transformations/TRANSFORM_NAME.sql"

quality:
  pre_transform:
    - check: "not_null"
      column: "id"
      severity: "critical"
    - check: "row_count"
      min_rows: 1
      severity: "critical"
    - check: "freshness"
      column: "updated_at"
      max_age_hours: 48
      severity: "error"
  post_transform:
    - check: "unique"
      column: "id"
      severity: "error"
    - check: "not_null"
      columns:
        - "id"
        - "name"
        - "created_date"
      severity: "error"
    - check: "referential_integrity"
      column: "category_id"
      reference_table: "dim_category"
      reference_column: "id"
      severity: "warn"
  thresholds:
    max_failure_rate_percent: 1.0
    min_row_count_ratio: 0.9  # Must retain at least 90% of input rows

monitoring:
  alerts:
    channels:
      - type: "slack"
        webhook_url: "${SLACK_WEBHOOK_URL}"
        channel: "#data-pipeline-alerts"
      - type: "email"
        recipients:
          - "data-team@company.com"
    rules:
      - name: "pipeline_failure"
        condition: "pipeline_status == 'failed'"
        severity: "critical"
        channels: ["slack", "email"]
      - name: "quality_check_failure"
        condition: "quality_suite_passed == false"
        severity: "error"
        channels: ["slack"]
      - name: "slow_pipeline"
        condition: "duration_minutes > 90"
        severity: "warn"
        channels: ["slack"]
  metrics:
    - name: "records_processed"
      type: "counter"
    - name: "pipeline_duration_seconds"
      type: "histogram"
    - name: "quality_check_pass_rate"
      type: "gauge"
    - name: "extraction_lag_seconds"
      type: "gauge"
```

## Monitoring and Alerting Pattern

```python
"""Pipeline monitoring and alerting utilities."""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Protocol

import structlog

logger = structlog.get_logger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels."""

    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PipelineMetrics:
    """Collected metrics for a single pipeline run."""

    pipeline_name: str
    run_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "running"
    records_extracted: int = 0
    records_transformed: int = 0
    records_loaded: int = 0
    records_rejected: int = 0
    quality_checks_passed: int = 0
    quality_checks_failed: int = 0
    errors: list[dict[str, Any]] = field(default_factory=list)
    custom_metrics: dict[str, Any] = field(default_factory=dict)

    @property
    def duration_seconds(self) -> Optional[float]:
        """Calculate pipeline run duration in seconds."""
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds()

    def to_dict(self) -> dict[str, Any]:
        """Serialize metrics to a dictionary for reporting."""
        return {
            "pipeline_name": self.pipeline_name,
            "run_id": self.run_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "duration_seconds": self.duration_seconds,
            "records": {
                "extracted": self.records_extracted,
                "transformed": self.records_transformed,
                "loaded": self.records_loaded,
                "rejected": self.records_rejected,
            },
            "quality": {
                "passed": self.quality_checks_passed,
                "failed": self.quality_checks_failed,
            },
            "errors": self.errors,
            "custom_metrics": self.custom_metrics,
        }


class AlertChannel(Protocol):
    """Protocol for alert delivery channels."""

    def send(self, severity: AlertSeverity, title: str, message: str) -> bool:
        """Send an alert through this channel."""
        ...


class MetricsCollector:
    """Collects and exposes pipeline metrics."""

    def __init__(self, pipeline_name: str, run_id: str) -> None:
        self.metrics = PipelineMetrics(
            pipeline_name=pipeline_name,
            run_id=run_id,
            start_time=datetime.utcnow(),
        )
        self._log = logger.bind(pipeline=pipeline_name, run_id=run_id)
        self._timers: dict[str, float] = {}

    def start_timer(self, name: str) -> None:
        """Start a named timer."""
        self._timers[name] = time.monotonic()

    def stop_timer(self, name: str) -> float:
        """Stop a named timer and return elapsed seconds."""
        if name not in self._timers:
            return 0.0
        elapsed = time.monotonic() - self._timers.pop(name)
        self.metrics.custom_metrics[f"{name}_duration_seconds"] = elapsed
        return elapsed

    def record_extraction(self, count: int) -> None:
        """Record extracted record count."""
        self.metrics.records_extracted += count
        self._log.info("extraction_recorded", count=count, total=self.metrics.records_extracted)

    def record_transformation(self, input_count: int, output_count: int) -> None:
        """Record transformation counts."""
        self.metrics.records_transformed += output_count
        dropped = input_count - output_count
        self._log.info(
            "transformation_recorded",
            input=input_count,
            output=output_count,
            dropped=dropped,
        )

    def record_load(self, loaded: int, rejected: int = 0) -> None:
        """Record load counts."""
        self.metrics.records_loaded += loaded
        self.metrics.records_rejected += rejected
        self._log.info("load_recorded", loaded=loaded, rejected=rejected)

    def record_quality_check(self, passed: bool) -> None:
        """Record a quality check result."""
        if passed:
            self.metrics.quality_checks_passed += 1
        else:
            self.metrics.quality_checks_failed += 1

    def record_error(self, stage: str, error: str, details: Optional[dict] = None) -> None:
        """Record a pipeline error."""
        self.metrics.errors.append({
            "stage": stage,
            "error": error,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat(),
        })
        self._log.error("pipeline_error", stage=stage, error=error)

    def finalize(self, status: str = "success") -> PipelineMetrics:
        """Finalize metrics collection and return the result."""
        self.metrics.end_time = datetime.utcnow()
        self.metrics.status = status
        self._log.info(
            "pipeline_completed",
            status=status,
            duration=self.metrics.duration_seconds,
            records_loaded=self.metrics.records_loaded,
        )
        return self.metrics
```
