from src.cognitive.evaluation.metrics.execution_metrics import ExecutionMetrics


def test_execution_metrics_creation():

    metrics = ExecutionMetrics(
        execution_id="exec-001",
        success=True,
        duration=1.5
    )

    assert metrics.execution_id == "exec-001"
    assert metrics.success is True
    assert metrics.duration == 1.5


def test_execution_metrics_failure():

    metrics = ExecutionMetrics(
        execution_id="exec-002",
        success=False,
        duration=3.0
    )

    assert metrics.success is False


def test_execution_metrics_duration():

    metrics = ExecutionMetrics(
        execution_id="exec-003",
        success=True,
        duration=0.5
    )

    assert metrics.duration >= 0