from src.intelligence.execution.metrics import (
    ExecutionMetricsStore,
)

from src.intelligence.execution.models import (
    ExecutionMetric,
)


def test_execution_metric_creation():

    metric = ExecutionMetric(
        metric_name="execution_time_ms",
        metric_value=150,
        category="performance",
    )

    assert metric.metric_name == "execution_time_ms"
    assert metric.metric_value == 150
    assert metric.category == "performance"



def test_execution_metrics_store_add_and_get():

    store = ExecutionMetricsStore()

    metric = ExecutionMetric(
        metric_name="tools_used",
        metric_value=2,
    )

    store.add(
        execution_id="exec-001",
        metric=metric,
    )

    result = store.get_by_execution(
        "exec-001"
    )

    assert len(result) == 1
    assert result[0].execution_id == "exec-001"
    assert result[0].metric.metric_name == "tools_used"



def test_execution_metrics_store_get_all():

    store = ExecutionMetricsStore()

    store.add(
        execution_id="exec-001",
        metric=ExecutionMetric(
            metric_name="steps_count",
            metric_value=3,
        ),
    )

    store.add(
        execution_id="exec-002",
        metric=ExecutionMetric(
            metric_name="steps_count",
            metric_value=5,
        ),
    )

    result = store.get_all()

    assert len(result) == 2