"""Tests for the execution trace service."""

from datetime import datetime, timedelta, timezone

import pytest

from src.observability.domain.enums import (
    ErrorSeverity,
    EventType,
    ExecutionStatus,
    MetricType,
)
from src.observability.domain.models import ExecutionError
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


BASE_TIME = datetime(
    2026,
    8,
    22,
    12,
    0,
    tzinfo=timezone.utc,
)


@pytest.fixture
def service() -> ExecutionTraceService:
    """Create a fresh execution trace service."""
    return ExecutionTraceService()


def test_create_trace_generates_unique_execution_id(
    service: ExecutionTraceService,
) -> None:
    first = service.create_trace()
    second = service.create_trace()

    assert first.execution_id != second.execution_id
    assert first.execution_id.startswith("exec_")
    assert second.execution_id.startswith("exec_")


def test_create_trace_preserves_correlation_context(
    service: ExecutionTraceService,
) -> None:
    trace = service.create_trace(
        execution_id="exec_001",
        correlation_id="corr_001",
        metadata={"source": "test"},
    )

    assert trace.execution_id == "exec_001"
    assert trace.context is not None
    assert trace.context.correlation_id == "corr_001"
    assert trace.metadata["source"] == "test"


def test_duplicate_execution_id_is_rejected(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_duplicate",
    )

    with pytest.raises(ValueError):
        service.create_trace(
            execution_id="exec_duplicate",
        )


def test_start_registers_lifecycle_event(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_start",
    )

    trace = service.start(
        "exec_start",
        timestamp=BASE_TIME,
    )

    assert trace.status == ExecutionStatus.RUNNING
    assert trace.started_at == BASE_TIME
    assert len(trace.events) == 1
    assert trace.events[0].event_type == EventType.EXECUTION_STARTED


def test_complete_registers_event_and_duration(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_complete",
    )

    service.start(
        "exec_complete",
        timestamp=BASE_TIME,
    )

    trace = service.complete(
        "exec_complete",
        timestamp=BASE_TIME + timedelta(seconds=10),
    )

    assert trace.status == ExecutionStatus.COMPLETED
    assert trace.duration == 10.0

    event_types = [event.event_type for event in trace.events]

    assert EventType.EXECUTION_STARTED in event_types
    assert EventType.EXECUTION_COMPLETED in event_types


def test_failure_records_error_and_finalizes_trace(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_failed",
    )

    service.start(
        "exec_failed",
        timestamp=BASE_TIME,
    )

    error = ExecutionError(
        execution_id="exec_failed",
        timestamp=BASE_TIME + timedelta(seconds=3),
        component="execution",
        stage="tool_call",
        severity=ErrorSeverity.ERROR,
        error_type="ToolExecutionError",
        message="Tool failed.",
    )

    trace = service.fail(
        "exec_failed",
        error=error,
        timestamp=BASE_TIME + timedelta(seconds=4),
    )

    assert trace.status == ExecutionStatus.FAILED
    assert len(trace.errors) == 1
    assert trace.errors[0].error_id == error.error_id
    assert trace.finished_at == BASE_TIME + timedelta(seconds=4)


def test_cancel_finalizes_execution(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_cancel",
    )

    service.start(
        "exec_cancel",
        timestamp=BASE_TIME,
    )

    trace = service.cancel(
        "exec_cancel",
        timestamp=BASE_TIME + timedelta(seconds=2),
    )

    assert trace.status == ExecutionStatus.CANCELLED
    assert trace.finished_at == BASE_TIME + timedelta(seconds=2)

    assert trace.events[-1].event_type == EventType.EXECUTION_CANCELLED


def test_state_changes_are_registered(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_state",
    )

    service.start(
        "exec_state",
        timestamp=BASE_TIME,
    )

    service.update_state(
        "exec_state",
        status=ExecutionStatus.RUNNING,
        component="reasoning",
        stage="reasoning",
        step="step_1",
        timestamp=BASE_TIME + timedelta(seconds=1),
    )

    service.update_state(
        "exec_state",
        status=ExecutionStatus.RUNNING,
        component="planning",
        stage="planning",
        step="step_2",
        timestamp=BASE_TIME + timedelta(seconds=2),
    )

    trace = service.get_trace(
        "exec_state",
    )

    assert len(trace.state_history) >= 3

    components = [
        state.current_component
        for state in trace.state_history
        if state.current_component is not None
    ]

    assert components == [
        "reasoning",
        "planning",
    ]


def test_event_registration_preserves_execution_correlation(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_event",
    )

    event = service.record_event(
        execution_id="exec_event",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        stage="reasoning",
        timestamp=BASE_TIME,
    )

    assert event.execution_id == "exec_event"

    trace = service.get_trace(
        "exec_event",
    )

    assert len(trace.events) == 1
    assert trace.events[0].execution_id == "exec_event"


def test_cognitive_events_are_associated_with_trace(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_cognitive",
    )

    service.record_event(
        execution_id="exec_cognitive",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        stage="reasoning",
        timestamp=BASE_TIME,
    )

    service.record_event(
        execution_id="exec_cognitive",
        event_type=EventType.PLAN_CREATED,
        component="planning",
        stage="planning",
        timestamp=BASE_TIME + timedelta(seconds=1),
    )

    service.record_event(
        execution_id="exec_cognitive",
        event_type=EventType.EVALUATION_COMPLETED,
        component="evaluation",
        stage="evaluation",
        timestamp=BASE_TIME + timedelta(seconds=2),
    )

    trace = service.get_trace(
        "exec_cognitive",
    )

    assert [event.event_type for event in trace.events] == [
        EventType.REASONING_COMPLETED,
        EventType.PLAN_CREATED,
        EventType.EVALUATION_COMPLETED,
    ]


def test_metrics_are_associated_with_execution(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_metric",
    )

    metric = service.record_metric(
        execution_id="exec_metric",
        metric_name="reasoning.duration",
        value=42.5,
        unit="ms",
        component="reasoning",
        metric_type=MetricType.DURATION,
        timestamp=BASE_TIME,
    )

    trace = service.get_trace(
        "exec_metric",
    )

    assert metric.execution_id == "exec_metric"
    assert len(trace.metrics) == 1
    assert trace.metrics[0].metric_name == "reasoning.duration"
    assert trace.metrics[0].value == 42.5


def test_errors_are_associated_with_execution(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_error",
    )

    error = service.record_error(
        execution_id="exec_error",
        component="execution",
        error_type="RuntimeError",
        message="Unexpected failure.",
        severity=ErrorSeverity.ERROR,
        timestamp=BASE_TIME,
    )

    trace = service.get_trace(
        "exec_error",
    )

    assert error.execution_id == "exec_error"
    assert len(trace.errors) == 1
    assert trace.errors[0].message == "Unexpected failure."


def test_events_are_reconstructed_chronologically(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_order",
    )

    service.record_event(
        execution_id="exec_order",
        event_type=EventType.STEP_COMPLETED,
        component="execution",
        timestamp=BASE_TIME + timedelta(seconds=5),
    )

    service.record_event(
        execution_id="exec_order",
        event_type=EventType.STEP_STARTED,
        component="execution",
        timestamp=BASE_TIME + timedelta(seconds=1),
    )

    service.record_event(
        execution_id="exec_order",
        event_type=EventType.EXECUTION_STARTED,
        component="runtime",
        timestamp=BASE_TIME,
    )

    trace = service.reconstruct(
        "exec_order",
    )

    timestamps = [event.timestamp for event in trace.events]

    assert timestamps == sorted(timestamps)


def test_timeline_contains_all_observable_records(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_timeline",
    )

    service.start(
        "exec_timeline",
        timestamp=BASE_TIME,
    )

    service.record_event(
        execution_id="exec_timeline",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        timestamp=BASE_TIME + timedelta(seconds=1),
    )

    service.record_metric(
        execution_id="exec_timeline",
        metric_name="reasoning.duration",
        value=10,
        unit="ms",
        component="reasoning",
        timestamp=BASE_TIME + timedelta(seconds=2),
    )

    service.record_error(
        execution_id="exec_timeline",
        component="evaluation",
        error_type="EvaluationWarning",
        message="Warning.",
        severity=ErrorSeverity.WARNING,
        timestamp=BASE_TIME + timedelta(seconds=3),
    )

    timeline = service.timeline(
        "exec_timeline",
    )

    assert {item["type"] for item in timeline} >= {
        "state",
        "event",
        "metric",
        "error",
    }

    timestamps = [item["timestamp"] for item in timeline]

    assert timestamps == sorted(timestamps)


def test_executions_are_isolated(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_first",
    )

    service.create_trace(
        execution_id="exec_second",
    )

    service.record_event(
        execution_id="exec_first",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        timestamp=BASE_TIME,
    )

    first_trace = service.get_trace(
        "exec_first",
    )

    second_trace = service.get_trace(
        "exec_second",
    )

    assert len(first_trace.events) == 1
    assert len(second_trace.events) == 0


def test_get_trace_returns_isolated_copy(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_copy",
    )

    service.record_event(
        execution_id="exec_copy",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        timestamp=BASE_TIME,
    )

    trace = service.get_trace(
        "exec_copy",
    )

    trace.metadata["mutated"] = True
    trace.events.clear()

    stored = service.get_trace(
        "exec_copy",
    )

    assert "mutated" not in stored.metadata
    assert len(stored.events) == 1


def test_incomplete_execution_can_be_recovered(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_incomplete",
    )

    service.start(
        "exec_incomplete",
        timestamp=BASE_TIME,
    )

    trace = service.recover_incomplete(
        "exec_incomplete",
        timestamp=BASE_TIME + timedelta(seconds=10),
    )

    assert trace.status == ExecutionStatus.FAILED
    assert len(trace.errors) == 1
    assert trace.errors[0].error_type == "IncompleteExecution"
    assert trace.events[-1].event_type == EventType.EXECUTION_FAILED


def test_recovering_completed_execution_does_not_change_trace(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_completed",
    )

    service.start(
        "exec_completed",
        timestamp=BASE_TIME,
    )

    service.complete(
        "exec_completed",
        timestamp=BASE_TIME + timedelta(seconds=1),
    )

    trace = service.recover_incomplete(
        "exec_completed",
    )

    assert trace.status == ExecutionStatus.COMPLETED
    assert trace.errors == []


def test_unknown_execution_is_rejected(
    service: ExecutionTraceService,
) -> None:
    with pytest.raises(KeyError):
        service.get_trace(
            "exec_unknown",
        )


def test_existing_data_survives_failed_recording(
    service: ExecutionTraceService,
) -> None:
    service.create_trace(
        execution_id="exec_safe",
    )

    service.record_event(
        execution_id="exec_safe",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        timestamp=BASE_TIME,
    )

    with pytest.raises(KeyError):
        service.record_event(
            execution_id="different_execution",
            event_type=EventType.REASONING_FAILED,
            component="reasoning",
        )

    trace = service.get_trace(
        "exec_safe",
    )

    assert len(trace.events) == 1
    assert trace.events[0].event_type == EventType.REASONING_COMPLETED


def test_service_count_and_exists(
    service: ExecutionTraceService,
) -> None:
    assert service.count() == 0
    assert service.exists("exec_001") is False

    service.create_trace(
        execution_id="exec_001",
    )

    assert service.count() == 1
    assert service.exists("exec_001") is True
