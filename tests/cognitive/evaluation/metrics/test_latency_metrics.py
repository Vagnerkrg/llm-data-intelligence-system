from src.cognitive.evaluation.metrics.latency_metrics import LatencyMetrics


def test_latency_metrics_creation():

    metrics = LatencyMetrics(
        execution_id="exec-001",
        latency_ms=250
    )

    assert metrics.execution_id == "exec-001"
    assert metrics.latency_ms == 250


def test_latency_metrics_average():

    metrics = LatencyMetrics(
        execution_id="exec-002",
        latency_ms=500
    )

    assert metrics.latency_seconds == 0.5


def test_latency_metrics_positive():

    metrics = LatencyMetrics(
        execution_id="exec-003",
        latency_ms=100
    )

    assert metrics.latency_ms >= 0