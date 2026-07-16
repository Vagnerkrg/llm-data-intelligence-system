from typing import Iterable

from .events import ExecutionEvent
from .models import ExecutionMetric
from .metrics import ExecutionMetricsStore


class ExecutionMetricsCollector:
    """
    Collects execution events and transforms them into metrics.

    Responsible for converting execution telemetry
    into structured metrics stored in ExecutionMetricsStore.
    """

    def __init__(
        self,
        store: ExecutionMetricsStore,
    ):
        self.store = store


    def collect(
        self,
        event: ExecutionEvent,
    ) -> list[ExecutionMetric]:

        metrics = self._extract_metrics(event)

        for metric in metrics:
            self.store.add(
                execution_id=event.execution_id,
                metric=metric,
            )

        return metrics


    def collect_many(
        self,
        events: Iterable[ExecutionEvent],
    ) -> list[ExecutionMetric]:

        collected = []

        for event in events:
            collected.extend(
                self.collect(event)
            )

        return collected


    def _extract_metrics(
        self,
        event: ExecutionEvent,
    ) -> list[ExecutionMetric]:

        metrics = []


        if hasattr(event, "duration_ms"):

            metrics.append(
                ExecutionMetric(
                    metric_name="duration_ms",
                    metric_value=event.duration_ms,
                    category="performance",
                )
            )


        if hasattr(event, "tools_used"):

            metrics.append(
                ExecutionMetric(
                    metric_name="tools_used",
                    metric_value=event.tools_used,
                    category="execution",
                )
            )


        if hasattr(event, "steps_count"):

            metrics.append(
                ExecutionMetric(
                    metric_name="steps_count",
                    metric_value=event.steps_count,
                    category="execution",
                )
            )


        return metrics