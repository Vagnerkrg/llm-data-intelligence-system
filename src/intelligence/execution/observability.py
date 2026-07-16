from src.intelligence.execution.metrics import (
    ExecutionMetric,
    ExecutionMetricsStore,
)

from src.intelligence.execution.metrics_aggregator import (
    MetricsAggregator,
)


class ExecutionObservability:
    """
    Coordinates execution metrics collection,
    storage and analysis.

    This layer connects execution events
    with intelligence insights.
    """

    def __init__(self):
        self.store = ExecutionMetricsStore()
        self.aggregator = MetricsAggregator()


    def record_metric(
        self,
        execution_id: str,
        metric_name: str,
        metric_value,
        category: str | None = None,
    ):
        """
        Record an execution metric.
        """

        metric = ExecutionMetric(
            execution_id=execution_id,
            metric_name=metric_name,
            metric_value=metric_value,
            category=category,
        )


        self.store.add(
            execution_id=execution_id,
            metric=metric,
        )


        self.aggregator.add_metric(
            execution_id=execution_id,
            metric_name=metric_name,
            metric_value=metric_value,
        )


        return metric


    def get_execution_metrics(
        self,
        execution_id: str,
    ):
        """
        Retrieve stored metrics.
        """

        records = self.store.get_by_execution(
            execution_id
        )

        return [
            record.metric
            for record in records
        ]


    def analyze_execution(
        self,
        execution_id: str,
    ):
        """
        Generate execution intelligence summary.
        """

        return self.aggregator.analyze(
            execution_id
        )