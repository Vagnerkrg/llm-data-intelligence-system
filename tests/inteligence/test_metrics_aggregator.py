from src.intelligence.execution.metrics_aggregator import (
    MetricsAggregator,
)


def test_metrics_aggregator_add_and_get_metrics():

    aggregator = MetricsAggregator()

    aggregator.add_metric(
        execution_id="exec-001",
        metric_name="execution_time_ms",
        metric_value=150,
    )

    metrics = aggregator.get_metrics("exec-001")

    assert len(metrics) == 1
    assert metrics[0]["metric_name"] == "execution_time_ms"
    assert metrics[0]["metric_value"] == 150


def test_metrics_aggregator_analysis():

    aggregator = MetricsAggregator()

    aggregator.add_metric(
        execution_id="exec-001",
        metric_name="execution_time_ms",
        metric_value=100,
    )

    aggregator.add_metric(
        execution_id="exec-001",
        metric_name="steps_count",
        metric_value=200,
    )

    summary = aggregator.analyze("exec-001")

    assert summary["execution_id"] == "exec-001"
    assert summary["total_metrics"] == 2
    assert summary["numeric_metrics"] == 2
    assert summary["average_value"] == 150
    assert summary["min_value"] == 100
    assert summary["max_value"] == 200
    assert summary["status"] == "healthy"


def test_metrics_aggregator_without_data():

    aggregator = MetricsAggregator()

    summary = aggregator.analyze("unknown-execution")

    assert summary["execution_id"] == "unknown-execution"
    assert summary["total_metrics"] == 0
    assert summary["status"] == "no_data"