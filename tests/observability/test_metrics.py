"""Tests for observability metrics collection."""

import math

import pytest

from src.observability.domain.enums import (
    EventType,
    MetricName,
    MetricType,
)
from src.observability.domain.models import (
    ExecutionEvent,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)
from src.observability.services.metrics import (
    MetricsService,
)
from src.observability.services.metrics_collector import (
    MetricsCollector,
)


@pytest.fixture
def trace_service() -> ExecutionTraceService:
    """Create a fresh trace service."""
    return ExecutionTraceService()


@pytest.fixture
def metrics_service(
    trace_service: ExecutionTraceService,
) -> MetricsService:
    """Create a metrics service."""
    return MetricsService(
        trace_service=trace_service,
    )


@pytest.fixture
def collector(
    metrics_service: MetricsService,
) -> MetricsCollector:
    """Create a metrics collector."""
    return MetricsCollector(
        metrics_service=metrics_service,
    )


@pytest.fixture
def execution_id(
    trace_service: ExecutionTraceService,
) -> str:
    """Create a test execution."""
    trace = trace_service.create_trace(
        execution_id="exec_metrics",
    )

    return trace.execution_id


def test_metric_catalog_contains_required_metrics() -> None:
    assert MetricName.EXECUTIONS_TOTAL.value == "executions_total"
    assert MetricName.EXECUTION_DURATION_MS.value == "execution_duration_ms"
    assert MetricName.REASONING_DURATION_MS.value == "reasoning_duration_ms"
    assert MetricName.TOOL_CALLS_TOTAL.value == "tool_calls_total"
    assert MetricName.EVALUATION_SCORE.value == "evaluation_score"
    assert MetricName.SUCCESS_RATE.value == "success_rate"


def test_record_metric(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    metric = metrics_service.record(
        execution_id=execution_id,
        metric_name=MetricName.REASONING_DURATION_MS,
        value=125.5,
        unit="ms",
        component="reasoning",
        metric_type=MetricType.DURATION,
    )

    assert metric.execution_id == execution_id
    assert metric.metric_name == (MetricName.REASONING_DURATION_MS.value)
    assert metric.value == 125.5
    assert metric.unit == "ms"
    assert metric.metric_type == MetricType.DURATION


def test_record_metric_is_associated_with_trace(
    metrics_service: MetricsService,
    trace_service: ExecutionTraceService,
    execution_id: str,
) -> None:
    metrics_service.record(
        execution_id=execution_id,
        metric_name=MetricName.EXECUTIONS_TOTAL,
        value=1,
        unit="count",
        component="execution",
        metric_type=MetricType.COUNT,
    )

    trace = trace_service.get_trace(
        execution_id,
    )

    assert len(trace.metrics) == 1
    assert trace.metrics[0].execution_id == execution_id


def test_increment_counter(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    metrics_service.increment(
        execution_id,
        MetricName.TOOL_CALLS_TOTAL,
        "tool",
    )

    metrics_service.increment(
        execution_id,
        MetricName.TOOL_CALLS_TOTAL,
        "tool",
        amount=2,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.TOOL_CALLS_TOTAL,
        )
        == 3.0
    )


def test_negative_counter_increment_is_rejected(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    with pytest.raises(ValueError):
        metrics_service.increment(
            execution_id,
            MetricName.TOOL_CALLS_TOTAL,
            "tool",
            amount=-1,
        )


def test_duration_cannot_be_negative(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    with pytest.raises(ValueError):
        metrics_service.observe_duration(
            execution_id,
            MetricName.REASONING_DURATION_MS,
            -1,
            "reasoning",
        )


def test_rate_must_be_between_zero_and_one(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    with pytest.raises(ValueError):
        metrics_service.observe_rate(
            execution_id,
            MetricName.SUCCESS_RATE,
            1.5,
            "system",
        )


def test_invalid_nan_value_is_rejected(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    with pytest.raises(ValueError):
        metrics_service.record(
            execution_id,
            MetricName.EVALUATION_SCORE,
            math.nan,
            "score",
            "evaluation",
        )


def test_invalid_infinite_value_is_rejected(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    with pytest.raises(ValueError):
        metrics_service.record(
            execution_id,
            MetricName.EVALUATION_SCORE,
            math.inf,
            "score",
            "evaluation",
        )


def test_aggregate_metrics(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    for value in (10, 20, 30):
        metrics_service.record(
            execution_id,
            MetricName.REASONING_DURATION_MS,
            value,
            "ms",
            "reasoning",
            metric_type=MetricType.DURATION,
        )

    result = metrics_service.aggregate(
        execution_id,
        MetricName.REASONING_DURATION_MS,
    )

    assert result["count"] == 3.0
    assert result["sum"] == 60.0
    assert result["min"] == 10.0
    assert result["max"] == 30.0
    assert result["avg"] == 20.0


def test_empty_aggregate_returns_zeroes(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    result = metrics_service.aggregate(
        execution_id,
        MetricName.ERRORS_TOTAL,
    )

    assert result == {
        "count": 0,
        "sum": 0.0,
        "min": 0.0,
        "max": 0.0,
        "avg": 0.0,
    }


def test_aggregate_all_metrics(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    metrics_service.increment(
        execution_id,
        MetricName.EXECUTIONS_TOTAL,
        "execution",
    )

    metrics_service.observe_duration(
        execution_id,
        MetricName.EXECUTION_DURATION_MS,
        100,
        "execution",
    )

    result = metrics_service.aggregate_all(
        execution_id,
    )

    assert "executions_total" in result
    assert "execution_duration_ms" in result


def test_execution_result_success(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    metrics_service.record_execution_result(
        execution_id,
        successful=True,
        duration_ms=250,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.EXECUTIONS_TOTAL,
        )
        == 1
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.EXECUTIONS_SUCCESSFUL,
        )
        == 1
    )

    assert (
        metrics_service.success_rate(
            execution_id,
        )
        == 1.0
    )

    assert (
        metrics_service.failure_rate(
            execution_id,
        )
        == 0.0
    )


def test_execution_result_failure(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    metrics_service.record_execution_result(
        execution_id,
        successful=False,
        duration_ms=500,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.EXECUTIONS_FAILED,
        )
        == 1
    )

    assert (
        metrics_service.failure_rate(
            execution_id,
        )
        == 1.0
    )


def test_collector_reasoning_metric(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_reasoning_duration(
        execution_id,
        duration_ms=75,
    )

    assert (
        metrics_service.average_metric(
            execution_id,
            MetricName.REASONING_DURATION_MS,
        )
        == 75
    )


def test_collector_planning_metric(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_planning_duration(
        execution_id,
        duration_ms=45,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.PLANNING_DURATION_MS,
        )
        == 45
    )


def test_collector_tool_success(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_tool_call(
        execution_id,
        successful=True,
        duration_ms=30,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.TOOL_CALLS_TOTAL,
        )
        == 1
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.TOOL_CALLS_SUCCESSFUL,
        )
        == 1
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.TOOL_CALLS_FAILED,
        )
        == 0
    )


def test_collector_tool_failure(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_tool_call(
        execution_id,
        successful=False,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.TOOL_CALLS_FAILED,
        )
        == 1
    )


def test_collector_memory_retrieval(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_memory_retrieval(
        execution_id,
        duration_ms=20,
        memories_retrieved=4,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.MEMORY_RETRIEVALS_TOTAL,
        )
        == 1
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.MEMORIES_RETRIEVED,
        )
        == 4
    )


def test_collector_knowledge_access(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_knowledge_access(
        execution_id,
        updated=True,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.KNOWLEDGE_ACCESSES_TOTAL,
        )
        == 1
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.KNOWLEDGE_UPDATES_TOTAL,
        )
        == 1
    )


def test_collector_evaluation(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_evaluation(
        execution_id,
        score=0.91,
        duration_ms=120,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.EVALUATIONS_TOTAL,
        )
        == 1
    )

    assert (
        metrics_service.average_metric(
            execution_id,
            MetricName.EVALUATION_SCORE,
        )
        == 0.91
    )


def test_collector_learning(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_learning(
        execution_id,
        signal_generated=True,
        outcome_created=True,
        duration_ms=50,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.LEARNING_SIGNALS_TOTAL,
        )
        == 1
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.LEARNING_OUTCOMES_TOTAL,
        )
        == 1
    )


def test_collector_evolution(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_evolution(
        execution_id,
        decision_created=True,
        adaptation_applied=True,
        duration_ms=80,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.EVOLUTION_DECISIONS_TOTAL,
        )
        == 1
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.ADAPTATIONS_APPLIED_TOTAL,
        )
        == 1
    )


def test_collector_error(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_error(
        execution_id,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.ERRORS_TOTAL,
        )
        == 1
    )


def test_collector_consumes_structured_event(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    event = ExecutionEvent(
        execution_id=execution_id,
        event_type=EventType.TOOL_CALL_COMPLETED,
        component="tool",
        metadata={
            "duration_ms": 55,
        },
    )

    collector.collect_from_event(
        event,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.TOOL_CALLS_TOTAL,
        )
        == 1
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.TOOL_CALLS_SUCCESSFUL,
        )
        == 1
    )


def test_collector_consumes_failed_event(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    event = ExecutionEvent(
        execution_id=execution_id,
        event_type=EventType.ERROR_OCCURRED,
        component="system",
    )

    collector.collect_from_event(
        event,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.ERRORS_TOTAL,
        )
        == 1
    )


def test_metrics_are_isolated_per_execution(
    metrics_service: MetricsService,
    trace_service: ExecutionTraceService,
) -> None:
    first = trace_service.create_trace(
        execution_id="exec_first",
    )

    second = trace_service.create_trace(
        execution_id="exec_second",
    )

    metrics_service.increment(
        first.execution_id,
        MetricName.EXECUTIONS_TOTAL,
        "execution",
    )

    assert (
        metrics_service.total_metric_count(
            first.execution_id,
        )
        == 1
    )

    assert (
        metrics_service.total_metric_count(
            second.execution_id,
        )
        == 0
    )


def test_metric_context_is_preserved(
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    metric = metrics_service.record(
        execution_id,
        MetricName.EVALUATION_SCORE,
        0.88,
        "score",
        "evaluation",
        metadata={
            "model": "evaluation-v1",
            "source": "cognitive",
        },
    )

    assert metric.metadata["model"] == "evaluation-v1"
    assert metric.metadata["source"] == "cognitive"


def test_missing_optional_duration_is_supported(
    collector: MetricsCollector,
    metrics_service: MetricsService,
    execution_id: str,
) -> None:
    collector.collect_tool_call(
        execution_id,
        successful=True,
        duration_ms=None,
    )

    assert (
        metrics_service.count_metric(
            execution_id,
            MetricName.TOOL_CALLS_TOTAL,
        )
        == 1
    )
