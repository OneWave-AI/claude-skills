# Data Quality Check Pattern

Composable, configurable data quality checks for validating pipeline data at every stage. Generate checks tailored to the specific data being processed.

```python
"""Data quality check module for validating pipeline data at every stage."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional

import structlog

logger = structlog.get_logger(__name__)


class CheckSeverity(Enum):
    """Severity level for quality check failures."""

    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"


class CheckStatus(Enum):
    """Result status of a quality check."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class QualityCheckResult:
    """Result of a single data quality check."""

    check_name: str
    status: CheckStatus
    severity: CheckSeverity
    message: str
    checked_at: datetime
    records_checked: int
    records_failed: int = 0
    failed_examples: list[dict[str, Any]] = field(default_factory=list)
    metadata: Optional[dict[str, Any]] = None

    @property
    def failure_rate(self) -> float:
        """Calculate the percentage of records that failed the check."""
        if self.records_checked == 0:
            return 0.0
        return self.records_failed / self.records_checked * 100


@dataclass
class QualitySuiteResult:
    """Aggregate result of running a full quality check suite."""

    suite_name: str
    results: list[QualityCheckResult]
    executed_at: datetime
    duration_seconds: float

    @property
    def passed(self) -> bool:
        """Return True if no ERROR or CRITICAL checks failed."""
        return not any(
            r.status == CheckStatus.FAILED
            and r.severity in (CheckSeverity.ERROR, CheckSeverity.CRITICAL)
            for r in self.results
        )

    @property
    def summary(self) -> dict[str, int]:
        """Return count of checks by status."""
        counts: dict[str, int] = {"passed": 0, "failed": 0, "skipped": 0}
        for r in self.results:
            counts[r.status.value] += 1
        return counts


class QualityCheck:
    """A single configurable data quality check.

    Checks are composable and can be combined into suites.
    Each check is a function that takes data and returns a boolean.
    """

    def __init__(
        self,
        name: str,
        description: str,
        check_fn: Callable[[list[dict[str, Any]]], tuple[bool, list[dict[str, Any]]]],
        severity: CheckSeverity = CheckSeverity.ERROR,
    ) -> None:
        self.name = name
        self.description = description
        self.check_fn = check_fn
        self.severity = severity

    def run(self, data: list[dict[str, Any]]) -> QualityCheckResult:
        """Execute the quality check against the provided data.

        Args:
            data: List of records to check.

        Returns:
            QualityCheckResult with pass/fail status and details.
        """
        log = logger.bind(check=self.name)
        try:
            passed, failed_records = self.check_fn(data)
            status = CheckStatus.PASSED if passed else CheckStatus.FAILED
            log.info("check_completed", status=status.value, failures=len(failed_records))
            return QualityCheckResult(
                check_name=self.name,
                status=status,
                severity=self.severity,
                message=self.description,
                checked_at=datetime.utcnow(),
                records_checked=len(data),
                records_failed=len(failed_records),
                failed_examples=failed_records[:10],
            )
        except Exception as exc:
            log.error("check_error", error=str(exc))
            return QualityCheckResult(
                check_name=self.name,
                status=CheckStatus.FAILED,
                severity=self.severity,
                message=f"Check raised exception: {exc}",
                checked_at=datetime.utcnow(),
                records_checked=len(data),
                records_failed=len(data),
            )


# -- Built-in Quality Checks ---------------------------------------------------

def not_null_check(column: str) -> QualityCheck:
    """Create a check that ensures a column has no null values."""

    def _check(data: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
        failed = [row for row in data if row.get(column) is None]
        return len(failed) == 0, failed

    return QualityCheck(
        name=f"not_null_{column}",
        description=f"Column '{column}' must not contain null values",
        check_fn=_check,
        severity=CheckSeverity.ERROR,
    )


def unique_check(column: str) -> QualityCheck:
    """Create a check that ensures a column has unique values."""

    def _check(data: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
        seen: dict[Any, int] = {}
        duplicates: list[dict[str, Any]] = []
        for row in data:
            val = row.get(column)
            if val in seen:
                duplicates.append(row)
            seen[val] = seen.get(val, 0) + 1
        return len(duplicates) == 0, duplicates

    return QualityCheck(
        name=f"unique_{column}",
        description=f"Column '{column}' must contain unique values",
        check_fn=_check,
        severity=CheckSeverity.ERROR,
    )


def range_check(
    column: str,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
) -> QualityCheck:
    """Create a check that ensures a numeric column falls within a range."""

    def _check(data: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
        failed = []
        for row in data:
            val = row.get(column)
            if val is None:
                continue
            if min_value is not None and val < min_value:
                failed.append(row)
            elif max_value is not None and val > max_value:
                failed.append(row)
        return len(failed) == 0, failed

    bounds = []
    if min_value is not None:
        bounds.append(f">= {min_value}")
    if max_value is not None:
        bounds.append(f"<= {max_value}")
    desc = f"Column '{column}' must be {' and '.join(bounds)}"

    return QualityCheck(
        name=f"range_{column}",
        description=desc,
        check_fn=_check,
        severity=CheckSeverity.ERROR,
    )


def freshness_check(
    timestamp_column: str,
    max_age_hours: int,
) -> QualityCheck:
    """Create a check that ensures data is not older than a threshold."""

    def _check(data: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
        if not data:
            return True, []
        now = datetime.utcnow()
        stale = []
        for row in data:
            ts = row.get(timestamp_column)
            if ts is None:
                continue
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts)
            age = (now - ts).total_seconds() / 3600
            if age > max_age_hours:
                stale.append(row)
        return len(stale) == 0, stale

    return QualityCheck(
        name=f"freshness_{timestamp_column}",
        description=f"Column '{timestamp_column}' must not be older than {max_age_hours} hours",
        check_fn=_check,
        severity=CheckSeverity.CRITICAL,
    )


def row_count_check(
    min_rows: int = 1,
    max_rows: Optional[int] = None,
) -> QualityCheck:
    """Create a check that ensures the dataset has an expected row count."""

    def _check(data: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
        count = len(data)
        if count < min_rows:
            return False, []
        if max_rows is not None and count > max_rows:
            return False, []
        return True, []

    desc = f"Row count must be >= {min_rows}"
    if max_rows is not None:
        desc += f" and <= {max_rows}"

    return QualityCheck(
        name="row_count",
        description=desc,
        check_fn=_check,
        severity=CheckSeverity.CRITICAL,
    )


def referential_integrity_check(
    column: str,
    reference_values: set[Any],
) -> QualityCheck:
    """Create a check that ensures all values in a column exist in a reference set."""

    def _check(data: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
        orphans = [row for row in data if row.get(column) not in reference_values]
        return len(orphans) == 0, orphans

    return QualityCheck(
        name=f"referential_integrity_{column}",
        description=f"All values in '{column}' must exist in the reference set",
        check_fn=_check,
        severity=CheckSeverity.ERROR,
    )


def schema_check(
    expected_columns: list[str],
) -> QualityCheck:
    """Create a check that ensures all expected columns are present."""

    def _check(data: list[dict[str, Any]]) -> tuple[bool, list[dict[str, Any]]]:
        if not data:
            return True, []
        actual_columns = set(data[0].keys())
        missing = set(expected_columns) - actual_columns
        if missing:
            return False, [{"missing_columns": list(missing)}]
        return True, []

    return QualityCheck(
        name="schema_check",
        description=f"Data must contain columns: {', '.join(expected_columns)}",
        check_fn=_check,
        severity=CheckSeverity.CRITICAL,
    )
```
