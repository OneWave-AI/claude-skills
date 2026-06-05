# Python Implementation Patterns

Reference code patterns for pipeline implementation. Customize every generated file to the specific pipeline. Do not emit placeholder code that requires manual editing.

## Python Code Standards

1. Type hints everywhere -- every function signature must have full type annotations.
2. Docstrings -- every public function and class must have a docstring.
3. Logging -- use structured logging with correlation IDs for traceability.
4. Configuration -- no hardcoded values; make everything configurable via YAML or environment variables.
5. Error handling -- use explicit exception types, never bare `except:` clauses.
6. Idempotency -- make every pipeline step safely re-runnable.
7. Testability -- separate business logic from I/O for easy unit testing.

## Base Extractor Pattern

```python
"""Base extractor module providing the abstract interface for all data extractors."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Generator, Optional

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class ExtractionResult:
    """Container for extraction results with metadata."""

    data: list[dict[str, Any]]
    source_name: str
    extraction_timestamp: datetime
    record_count: int
    watermark_value: Optional[str] = None
    schema_hash: Optional[str] = None

    def __post_init__(self) -> None:
        if self.record_count != len(self.data):
            raise ValueError(
                f"Record count mismatch: declared {self.record_count}, "
                f"actual {len(self.data)}"
            )


class BaseExtractor(ABC):
    """Abstract base class for all data extractors.

    Subclasses must implement `connect`, `extract`, and `close` methods.
    The base class provides retry logic, logging, and watermark tracking.
    """

    def __init__(self, config: dict[str, Any], source_name: str) -> None:
        self.config = config
        self.source_name = source_name
        self._connected = False
        self._log = logger.bind(source=source_name)

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the data source."""
        ...

    @abstractmethod
    def extract(
        self,
        watermark: Optional[str] = None,
        batch_size: int = 10000,
    ) -> Generator[ExtractionResult, None, None]:
        """Extract data from the source, yielding batches.

        Args:
            watermark: Resume point for incremental extraction.
            batch_size: Number of records per batch.

        Yields:
            ExtractionResult for each batch of extracted data.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """Clean up connections and resources."""
        ...

    def __enter__(self) -> "BaseExtractor":
        self.connect()
        self._connected = True
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
        self._connected = False

    def validate_connection(self) -> bool:
        """Test that the source connection is alive and responsive."""
        try:
            self.connect()
            self.close()
            return True
        except Exception as exc:
            self._log.error("connection_validation_failed", error=str(exc))
            return False
```

## Base Transformer Pattern

```python
"""Base transformer module providing the abstract interface for all transformations."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class TransformationResult:
    """Container for transformation results with lineage metadata."""

    data: list[dict[str, Any]]
    transform_name: str
    input_record_count: int
    output_record_count: int
    transformation_timestamp: datetime
    dropped_records: int = 0
    error_records: list[dict[str, Any]] = field(default_factory=list)
    lineage: Optional[dict[str, Any]] = None

    @property
    def drop_rate(self) -> float:
        """Calculate the percentage of records dropped during transformation."""
        if self.input_record_count == 0:
            return 0.0
        return self.dropped_records / self.input_record_count * 100


class BaseTransformer(ABC):
    """Abstract base class for all data transformers.

    Subclasses must implement `transform` and `validate_output`.
    Provides standard logging, error collection, and lineage tracking.
    """

    def __init__(self, config: dict[str, Any], transform_name: str) -> None:
        self.config = config
        self.transform_name = transform_name
        self._log = logger.bind(transform=transform_name)

    @abstractmethod
    def transform(
        self,
        data: list[dict[str, Any]],
    ) -> TransformationResult:
        """Apply transformation logic to the input data.

        Args:
            data: List of records to transform.

        Returns:
            TransformationResult containing transformed data and metadata.
        """
        ...

    @abstractmethod
    def validate_output(
        self,
        result: TransformationResult,
    ) -> list[str]:
        """Validate the transformation output against business rules.

        Args:
            result: The transformation result to validate.

        Returns:
            List of validation error messages. Empty list means valid.
        """
        ...

    def _track_lineage(
        self,
        input_sources: list[str],
        output_fields: list[str],
        logic_description: str,
    ) -> dict[str, Any]:
        """Generate lineage metadata for the transformation."""
        return {
            "transform_name": self.transform_name,
            "input_sources": input_sources,
            "output_fields": output_fields,
            "logic": logic_description,
            "timestamp": datetime.utcnow().isoformat(),
        }
```

## Base Loader Pattern

```python
"""Base loader module providing the abstract interface for all data loaders."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional

import structlog

logger = structlog.get_logger(__name__)


class LoadStrategy(Enum):
    """Supported load strategies."""

    APPEND = "append"
    OVERWRITE = "overwrite"
    UPSERT = "upsert"
    MERGE = "merge"
    SCD_TYPE_2 = "scd_type_2"


@dataclass
class LoadResult:
    """Container for load operation results."""

    destination_name: str
    strategy: LoadStrategy
    records_loaded: int
    records_updated: int
    records_rejected: int
    load_timestamp: datetime
    duration_seconds: float
    partition_key: Optional[str] = None
    rejected_records: list[dict[str, Any]] = None

    def __post_init__(self) -> None:
        if self.rejected_records is None:
            self.rejected_records = []

    @property
    def success_rate(self) -> float:
        """Calculate the percentage of records successfully loaded."""
        total = self.records_loaded + self.records_rejected
        if total == 0:
            return 100.0
        return self.records_loaded / total * 100


class BaseLoader(ABC):
    """Abstract base class for all data loaders.

    Subclasses must implement `connect`, `load`, and `close` methods.
    The base class provides transaction management, retry logic, and metrics.
    """

    def __init__(
        self,
        config: dict[str, Any],
        destination_name: str,
        strategy: LoadStrategy = LoadStrategy.APPEND,
    ) -> None:
        self.config = config
        self.destination_name = destination_name
        self.strategy = strategy
        self._connected = False
        self._log = logger.bind(destination=destination_name, strategy=strategy.value)

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to the destination system."""
        ...

    @abstractmethod
    def load(
        self,
        data: list[dict[str, Any]],
        target_table: str,
    ) -> LoadResult:
        """Load data into the destination.

        Args:
            data: List of records to load.
            target_table: Target table or collection name.

        Returns:
            LoadResult with load operation metadata.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """Clean up connections and resources."""
        ...

    def __enter__(self) -> "BaseLoader":
        self.connect()
        self._connected = True
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
        self._connected = False

    @abstractmethod
    def create_table_if_not_exists(
        self,
        table_name: str,
        schema: dict[str, str],
    ) -> None:
        """Ensure the target table exists with the correct schema.

        Args:
            table_name: Name of the table to create.
            schema: Column name to data type mapping.
        """
        ...
```

## Retry and Error Handling Pattern

```python
"""Retry and error handling utilities for pipeline resilience."""

import functools
import time
from typing import Any, Callable, Optional, Type

import structlog

logger = structlog.get_logger(__name__)


class PipelineError(Exception):
    """Base exception for all pipeline errors."""

    def __init__(self, message: str, stage: str, details: Optional[dict] = None) -> None:
        super().__init__(message)
        self.stage = stage
        self.details = details or {}


class ExtractionError(PipelineError):
    """Raised when data extraction fails."""

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        super().__init__(message, stage="extraction", details=details)


class TransformationError(PipelineError):
    """Raised when data transformation fails."""

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        super().__init__(message, stage="transformation", details=details)


class LoadError(PipelineError):
    """Raised when data loading fails."""

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        super().__init__(message, stage="load", details=details)


class QualityCheckError(PipelineError):
    """Raised when a critical quality check fails."""

    def __init__(self, message: str, details: Optional[dict] = None) -> None:
        super().__init__(message, stage="quality_check", details=details)


def retry(
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay_seconds: float = 300.0,
    retryable_exceptions: tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """Decorator that retries a function with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts before giving up.
        delay_seconds: Initial delay between retries in seconds.
        backoff_factor: Multiplier applied to delay after each retry.
        max_delay_seconds: Maximum delay between retries.
        retryable_exceptions: Tuple of exception types that trigger a retry.

    Returns:
        Decorated function with retry logic.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            log = logger.bind(function=func.__name__)
            current_delay = delay_seconds
            last_exception: Optional[Exception] = None

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as exc:
                    last_exception = exc
                    if attempt == max_attempts:
                        log.error(
                            "max_retries_exceeded",
                            attempt=attempt,
                            error=str(exc),
                        )
                        raise
                    log.warning(
                        "retrying",
                        attempt=attempt,
                        max_attempts=max_attempts,
                        delay=current_delay,
                        error=str(exc),
                    )
                    time.sleep(current_delay)
                    current_delay = min(
                        current_delay * backoff_factor,
                        max_delay_seconds,
                    )

            raise last_exception  # Should not reach here, but safety net

        return wrapper

    return decorator
```
