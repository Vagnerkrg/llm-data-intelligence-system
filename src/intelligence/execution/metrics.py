from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ExecutionMetric:
    """
    Represents a metric generated during execution.
    """

    metric_name: str
    metric_value: float | int
    execution_id: str | None = None
    category: str | None = None

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class ExecutionMetricRecord:
    """
    Represents a metric stored for an execution.
    """

    execution_id: str
    metric: ExecutionMetric


class ExecutionMetricsStore:
    """
    In-memory storage for execution metrics.
    """

    def __init__(self):
        self._metrics: list[ExecutionMetricRecord] = []


    def add(
        self,
        execution_id: str,
        metric: ExecutionMetric,
    ) -> None:
        """
        Stores a metric associated with an execution.
        """

        metric.execution_id = execution_id

        record = ExecutionMetricRecord(
            execution_id=execution_id,
            metric=metric,
        )

        self._metrics.append(record)


    def get_by_execution(
        self,
        execution_id: str,
    ) -> list[ExecutionMetricRecord]:
        """
        Retrieves metrics from an execution.
        """

        return [
            record
            for record in self._metrics
            if record.execution_id == execution_id
        ]


    def get_all(
        self,
    ) -> list[ExecutionMetricRecord]:
        """
        Returns all stored metrics.
        """

        return list(
            self._metrics
        )