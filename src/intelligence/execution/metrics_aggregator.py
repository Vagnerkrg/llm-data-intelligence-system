from collections import defaultdict
from statistics import mean


class MetricsAggregator:
    """
    Aggregates execution metrics and produces intelligence summaries.

    Responsible for transforming raw execution metrics into
    higher-level observability information.
    """

    def __init__(self):
        self._metrics = defaultdict(list)

    def add_metric(
        self,
        execution_id: str,
        metric_name: str,
        metric_value,
    ):
        """
        Add a metric to an execution context.
        """

        self._metrics[execution_id].append(
            {
                "metric_name": metric_name,
                "metric_value": metric_value,
            }
        )

    def get_metrics(self, execution_id: str):
        """
        Retrieve all metrics from an execution.
        """

        return self._metrics.get(execution_id, [])

    def analyze(self, execution_id: str):
        """
        Generate an execution metrics summary.
        """

        metrics = self.get_metrics(execution_id)

        if not metrics:
            return {
                "execution_id": execution_id,
                "total_metrics": 0,
                "status": "no_data",
            }

        values = [
            metric["metric_value"]
            for metric in metrics
            if isinstance(metric["metric_value"], (int, float))
        ]

        summary = {
            "execution_id": execution_id,
            "total_metrics": len(metrics),
            "numeric_metrics": len(values),
        }

        if values:
            summary.update(
                {
                    "average_value": mean(values),
                    "min_value": min(values),
                    "max_value": max(values),
                }
            )

        summary["status"] = self._evaluate_status(summary)

        return summary

    def _evaluate_status(self, summary):
        """
        Basic health evaluation.

        This is intentionally simple now.
        Future versions can introduce adaptive thresholds.
        """

        average = summary.get("average_value")

        if average is None:
            return "unknown"

        if average < 500:
            return "healthy"

        if average < 2000:
            return "attention"

        return "critical"