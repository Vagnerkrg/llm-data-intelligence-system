"""Metrics collection and aggregation service."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Dict, List, Optional, Union

from src.observability.domain.enums import MetricName, MetricType
from src.observability.domain.models import ExecutionMetric
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


MetricNameValue = Union[MetricName, str]


class MetricsService:
    """Collect, validate and aggregate execution metrics."""

    def __init__(
        self,
        trace_service: Optional[ExecutionTraceService] = None,
    ) -> None:
        self.trace_service = trace_service or ExecutionTraceService()

    def record(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
        value: float,
        unit: str,
        component: str,
        *,
        metric_type: MetricType = MetricType.VALUE,
        timestamp: Optional[datetime] = None,
        metadata: Optional[dict] = None,
    ) -> ExecutionMetric:
        """Record a validated execution metric."""

        normalized_value = self._validate_value(value)
        normalized_name = self._normalize_name(metric_name)

        metric = ExecutionMetric(
            metric_name=normalized_name,
            value=normalized_value,
            unit=unit,
            timestamp=self._normalize_timestamp(timestamp),
            execution_id=execution_id,
            component=component,
            metric_type=metric_type,
            metadata=deepcopy(metadata or {}),
        )

        self.trace_service.record_metric(
            execution_id=execution_id,
            metric_name=metric.metric_name,
            value=metric.value,
            unit=metric.unit,
            component=metric.component,
            metric_type=metric.metric_type,
            timestamp=metric.timestamp,
            metadata=metric.metadata,
        )

        return deepcopy(metric)

    def increment(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
        component: str,
        *,
        amount: float = 1,
        unit: str = "count",
        metadata: Optional[dict] = None,
    ) -> ExecutionMetric:
        """Increment a counter metric."""

        if amount <= 0:
            raise ValueError("Counter increment must be greater than zero.")

        return self.record(
            execution_id=execution_id,
            metric_name=metric_name,
            value=amount,
            unit=unit,
            component=component,
            metric_type=MetricType.COUNT,
            metadata=metadata,
        )

    def observe_duration(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
        duration_ms: float,
        component: str,
        *,
        metadata: Optional[dict] = None,
    ) -> ExecutionMetric:
        """Record a duration metric in milliseconds."""

        if duration_ms < 0:
            raise ValueError("Duration cannot be negative.")

        return self.record(
            execution_id=execution_id,
            metric_name=metric_name,
            value=duration_ms,
            unit="ms",
            component=component,
            metric_type=MetricType.DURATION,
            metadata=metadata,
        )

    def observe_score(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
        score: float,
        component: str,
        *,
        metadata: Optional[dict] = None,
    ) -> ExecutionMetric:
        """Record a cognitive score."""

        return self.record(
            execution_id=execution_id,
            metric_name=metric_name,
            value=score,
            unit="score",
            component=component,
            metric_type=MetricType.SCORE,
            metadata=metadata,
        )

    def observe_rate(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
        rate: float,
        component: str,
        *,
        metadata: Optional[dict] = None,
    ) -> ExecutionMetric:
        """Record a rate between zero and one."""

        if not 0 <= rate <= 1:
            raise ValueError("Rate must be between 0 and 1.")

        return self.record(
            execution_id=execution_id,
            metric_name=metric_name,
            value=rate,
            unit="ratio",
            component=component,
            metric_type=MetricType.RATE,
            metadata=metadata,
        )

    def get_metrics(
        self,
        execution_id: str,
    ) -> List[ExecutionMetric]:
        """Return metrics associated with an execution."""

        trace = self.trace_service.get_trace(
            execution_id,
        )

        return [deepcopy(metric) for metric in trace.metrics]

    def aggregate(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
    ) -> Dict[str, float]:
        """Aggregate values for one metric."""

        target = self._normalize_name(metric_name)

        metrics = [
            metric
            for metric in self.get_metrics(execution_id)
            if metric.metric_name == target
        ]

        if not metrics:
            return {
                "count": 0,
                "sum": 0.0,
                "min": 0.0,
                "max": 0.0,
                "avg": 0.0,
            }

        values = [metric.value for metric in metrics]

        return {
            "count": float(len(values)),
            "sum": float(sum(values)),
            "min": float(min(values)),
            "max": float(max(values)),
            "avg": float(sum(values) / len(values)),
        }

    def aggregate_all(
        self,
        execution_id: str,
    ) -> Dict[str, Dict[str, float]]:
        """Aggregate all metrics of an execution."""

        metrics = self.get_metrics(execution_id)

        names = sorted({metric.metric_name for metric in metrics})

        return {
            name: self.aggregate(
                execution_id,
                name,
            )
            for name in names
        }

    def success_rate(
        self,
        execution_id: str,
    ) -> float:
        """Calculate execution success rate."""

        total = self._counter_value(
            execution_id,
            MetricName.EXECUTIONS_TOTAL,
        )

        successful = self._counter_value(
            execution_id,
            MetricName.EXECUTIONS_SUCCESSFUL,
        )

        if total <= 0:
            return 0.0

        return successful / total

    def failure_rate(
        self,
        execution_id: str,
    ) -> float:
        """Calculate execution failure rate."""

        total = self._counter_value(
            execution_id,
            MetricName.EXECUTIONS_TOTAL,
        )

        failed = self._counter_value(
            execution_id,
            MetricName.EXECUTIONS_FAILED,
        )

        if total <= 0:
            return 0.0

        return failed / total

    def record_execution_result(
        self,
        execution_id: str,
        *,
        successful: bool,
        duration_ms: Optional[float] = None,
    ) -> List[ExecutionMetric]:
        """Record standard execution outcome metrics."""

        recorded: List[ExecutionMetric] = []

        recorded.append(
            self.increment(
                execution_id,
                MetricName.EXECUTIONS_TOTAL,
                "execution",
            )
        )

        if successful:
            recorded.append(
                self.increment(
                    execution_id,
                    MetricName.EXECUTIONS_SUCCESSFUL,
                    "execution",
                )
            )
        else:
            recorded.append(
                self.increment(
                    execution_id,
                    MetricName.EXECUTIONS_FAILED,
                    "execution",
                )
            )

        if duration_ms is not None:
            recorded.append(
                self.observe_duration(
                    execution_id,
                    MetricName.EXECUTION_DURATION_MS,
                    duration_ms,
                    "execution",
                )
            )

        recorded.append(
            self.observe_rate(
                execution_id,
                MetricName.SUCCESS_RATE,
                self.success_rate_after(successful),
                "system",
            )
        )

        recorded.append(
            self.observe_rate(
                execution_id,
                MetricName.FAILURE_RATE,
                self.failure_rate_after(successful),
                "system",
            )
        )

        return recorded

    def success_rate_after(
        self,
        successful: bool,
    ) -> float:
        """Return success rate for a single execution outcome."""
        return 1.0 if successful else 0.0

    def failure_rate_after(
        self,
        successful: bool,
    ) -> float:
        """Return failure rate for a single execution outcome."""
        return 0.0 if successful else 1.0

    def count_metric(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
    ) -> float:
        """Return the sum of a counter metric."""

        return self._counter_value(
            execution_id,
            metric_name,
        )

    def average_metric(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
    ) -> float:
        """Return average value of a metric."""

        return self.aggregate(
            execution_id,
            metric_name,
        )["avg"]

    def total_metric_count(
        self,
        execution_id: str,
    ) -> int:
        """Return total number of metric records."""

        return len(self.get_metrics(execution_id))

    def _counter_value(
        self,
        execution_id: str,
        metric_name: MetricNameValue,
    ) -> float:
        """Return sum for a counter metric."""

        target = self._normalize_name(metric_name)

        metrics = [
            metric.value
            for metric in self.get_metrics(execution_id)
            if metric.metric_name == target
        ]

        return float(sum(metrics))

    @staticmethod
    def _normalize_name(
        metric_name: MetricNameValue,
    ) -> str:
        """Normalize a catalog name."""

        if isinstance(metric_name, MetricName):
            return metric_name.value

        if not isinstance(metric_name, str):
            raise TypeError("metric_name must be a MetricName or string.")

        if not metric_name.strip():
            raise ValueError("metric_name cannot be empty.")

        return metric_name.strip()

    @staticmethod
    def _validate_value(
        value: float,
    ) -> float:
        """Validate metric values."""

        if isinstance(value, bool):
            raise TypeError("Metric value cannot be boolean.")

        try:
            numeric = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("Metric value must be numeric.") from exc

        if numeric != numeric:
            raise ValueError("Metric value cannot be NaN.")

        if numeric in {
            float("inf"),
            float("-inf"),
        }:
            raise ValueError("Metric value must be finite.")

        return numeric

    @staticmethod
    def _normalize_timestamp(
        timestamp: Optional[datetime],
    ) -> datetime:
        """Normalize timestamp to UTC."""

        value = timestamp or datetime.now(
            timezone.utc,
        )

        if value.tzinfo is None:
            return value.replace(
                tzinfo=timezone.utc,
            )

        return value.astimezone(
            timezone.utc,
        )
