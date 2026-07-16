from src.intelligence.execution.observability import (
    ExecutionObservability,
)


def test_execution_observability_record_metric():

    observability = ExecutionObservability()

    metric = observability.record_metric(
        execution_id="exec-001",
        metric_name="execution_time_ms",
        metric_value=150,
        category="performance",
    )

    assert metric.execution_id == "exec-001"
    assert metric.metric_name == "execution_time_ms"
    assert metric.metric_value == 150


def test_execution_observability_get_metrics():

    observability = ExecutionObservability()

    observability.record_metric(
        execution_id="exec-001",
        metric_name="steps",
        metric_value=5,
    )

    metrics = observability.get_execution_metrics(
        "exec-001"
    )

    assert len(metrics) == 1
    assert metrics[0].metric_name == "steps"


def test_execution_observability_analysis():

    observability = ExecutionObservability()

    observability.record_metric(
        execution_id="exec-001",
        metric_name="execution_time_ms",
        metric_value=100,
    )

    observability.record_metric(
        execution_id="exec-001",
        metric_name="tool_calls",
        metric_value=20,
    )

    result = observability.analyze_execution(
        "exec-001"
    )

    assert result["execution_id"] == "exec-001"
    assert result["total_metrics"] == 2
    assert result["status"] == "healthy"