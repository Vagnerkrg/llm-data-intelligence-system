"""Unit tests for the observability domain."""

from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from src.observability.domain.enums import (
    ErrorSeverity,
    EventType,
    ExecutionStatus,
    MetricType,
)
from src.observability.domain.models import (
    ExecutionError,
    ExecutionEvent,
    ExecutionMetric,
    ExecutionState,
    ExecutionTrace,
    ObservabilityContext,
)
from src.observability.services.execution_lifecycle import (
    ExecutionLifecycleService,
)


def test_context_generates_execution_id() -> None:
    context = ObservabilityContext()

    assert context.execution_id.startswith("exec_")


def test_context_supports_correlation_id() -> None:
    context = ObservabilityContext(
        correlation_id="corr_001",
    )

    assert context.correlation_id == "corr_001"


def test_trace_starts_pending() -> None:
    trace = ExecutionTrace()

    assert trace.status == ExecutionStatus.PENDING
    assert trace.started_at is None
    assert trace.finished_at is None


def test_trace_start_transition() -> None:
    trace = ExecutionTrace()

    started_at = datetime(
        2026,
        8,
        21,
        12,
        0,
        tzinfo=timezone.utc,
    )

    trace.start(started_at)

    assert trace.status == ExecutionStatus.RUNNING
    assert trace.started_at == started_at
    assert trace.state is not None
    assert trace.state.status == ExecutionStatus.RUNNING


def test_trace_complete_transition() -> None:
    trace = ExecutionTrace()

    started_at = datetime(
        2026,
        8,
        21,
        12,
        0,
        tzinfo=timezone.utc,
    )

    finished_at = started_at + timedelta(seconds=12)

    trace.start(started_at)
    trace.complete(finished_at)

    assert trace.status == ExecutionStatus.COMPLETED
    assert trace.finished_at == finished_at
    assert trace.duration == 12.0


def test_trace_failure_transition() -> None:
    trace = ExecutionTrace()

    started_at = datetime(
        2026,
        8,
        21,
        12,
        0,
        tzinfo=timezone.utc,
    )

    trace.start(started_at)
    trace.fail(started_at + timedelta(seconds=5))

    assert trace.status == ExecutionStatus.FAILED
    assert trace.finished_at is not None


def test_trace_cancel_transition() -> None:
    trace = ExecutionTrace()

    started_at = datetime(
        2026,
        8,
        21,
        12,
        0,
        tzinfo=timezone.utc,
    )

    trace.start(started_at)
    trace.cancel(started_at + timedelta(seconds=5))

    assert trace.status == ExecutionStatus.CANCELLED


def test_invalid_lifecycle_transition_is_rejected() -> None:
    trace = ExecutionTrace()

    with pytest.raises(ValueError):
        trace.complete()


def test_invalid_timestamp_order_is_rejected() -> None:
    started_at = datetime(
        2026,
        8,
        21,
        12,
        0,
        tzinfo=timezone.utc,
    )

    finished_at = started_at - timedelta(seconds=1)

    with pytest.raises(ValidationError):
        ExecutionTrace(
            started_at=started_at,
            finished_at=finished_at,
        )


def test_trace_attaches_context() -> None:
    trace = ExecutionTrace(
        execution_id="exec_001",
    )

    context = ObservabilityContext(
        execution_id="exec_001",
        correlation_id="corr_001",
    )

    trace.attach_context(context)

    assert trace.context is not None
    assert trace.context.execution_id == "exec_001"
    assert trace.context.correlation_id == "corr_001"


def test_context_with_wrong_execution_id_is_rejected() -> None:
    trace = ExecutionTrace(
        execution_id="exec_001",
    )

    context = ObservabilityContext(
        execution_id="exec_002",
    )

    with pytest.raises(ValueError):
        trace.attach_context(context)


def test_event_creation() -> None:
    event = ExecutionEvent(
        execution_id="exec_001",
        event_type=EventType.EXECUTION_STARTED,
        component="agent_runtime",
    )

    assert event.execution_id == "exec_001"
    assert event.event_type == EventType.EXECUTION_STARTED


def test_event_execution_id_must_match_trace() -> None:
    trace = ExecutionTrace(
        execution_id="exec_001",
    )

    event = ExecutionEvent(
        execution_id="exec_002",
        event_type=EventType.STEP_STARTED,
        component="execution",
    )

    with pytest.raises(ValueError):
        trace.add_event(event)


def test_event_is_immutable() -> None:
    event = ExecutionEvent(
        execution_id="exec_001",
        event_type=EventType.EXECUTION_STARTED,
        component="runtime",
    )

    with pytest.raises(ValidationError):
        event.component = "changed"


def test_metric_creation() -> None:
    metric = ExecutionMetric(
        execution_id="exec_001",
        metric_name="execution.duration",
        value=125.5,
        unit="ms",
        component="agent_runtime",
        metric_type=MetricType.DURATION,
    )

    assert metric.metric_name == "execution.duration"
    assert metric.value == 125.5
    assert metric.metric_type == MetricType.DURATION


def test_metric_execution_id_must_match_trace() -> None:
    trace = ExecutionTrace(
        execution_id="exec_001",
    )

    metric = ExecutionMetric(
        execution_id="exec_002",
        metric_name="test.metric",
        value=1,
        unit="count",
        component="test",
    )

    with pytest.raises(ValueError):
        trace.add_metric(metric)


def test_error_creation() -> None:
    error = ExecutionError(
        execution_id="exec_001",
        component="execution",
        stage="tool_call",
        severity=ErrorSeverity.ERROR,
        error_type="ToolExecutionError",
        message="Tool execution failed.",
    )

    assert error.severity == ErrorSeverity.ERROR
    assert error.recoverable is True


def test_error_execution_id_must_match_trace() -> None:
    trace = ExecutionTrace(
        execution_id="exec_001",
    )

    error = ExecutionError(
        execution_id="exec_002",
        component="execution",
        severity=ErrorSeverity.ERROR,
        error_type="ToolExecutionError",
        message="Failure.",
    )

    with pytest.raises(ValueError):
        trace.add_error(error)


def test_state_execution_id_must_match_trace() -> None:
    with pytest.raises(ValidationError):
        ExecutionTrace(
            execution_id="exec_001",
            state=ExecutionState(
                execution_id="exec_002",
            ),
        )


def test_trace_round_trip_json_serialization() -> None:
    trace = ExecutionTrace(
        execution_id="exec_001",
    )

    trace.start(
        datetime(
            2026,
            8,
            21,
            12,
            0,
            tzinfo=timezone.utc,
        )
    )

    trace.add_event(
        ExecutionEvent(
            execution_id="exec_001",
            event_type=EventType.EXECUTION_STARTED,
            component="agent_runtime",
        )
    )

    trace.add_metric(
        ExecutionMetric(
            execution_id="exec_001",
            metric_name="execution.duration",
            value=10,
            unit="ms",
            component="agent_runtime",
        )
    )

    payload = trace.to_json()

    restored = ExecutionTrace.from_json(payload)

    assert restored.execution_id == trace.execution_id
    assert restored.status == trace.status
    assert len(restored.events) == 1
    assert len(restored.metrics) == 1


def test_trace_round_trip_dict_serialization() -> None:
    trace = ExecutionTrace(
        execution_id="exec_001",
    )

    payload = trace.to_dict()

    restored = ExecutionTrace.from_dict(payload)

    assert restored.execution_id == "exec_001"


def test_lifecycle_service_creates_correlated_trace() -> None:
    service = ExecutionLifecycleService()

    trace = service.create(
        execution_id="exec_service",
        correlation_id="corr_service",
    )

    assert trace.execution_id == "exec_service"
    assert trace.context is not None
    assert trace.context.execution_id == "exec_service"
    assert trace.context.correlation_id == "corr_service"


def test_lifecycle_service_terminal_state() -> None:
    service = ExecutionLifecycleService()

    trace = service.create(
        execution_id="exec_terminal",
    )

    assert service.is_terminal(trace) is False

    service.start(trace)
    service.complete(trace)

    assert service.is_terminal(trace) is True


def test_snapshot_reflects_current_status() -> None:
    trace = ExecutionTrace(
        execution_id="exec_snapshot",
    )

    trace.start()

    snapshot = trace.snapshot()

    assert snapshot.execution_id == "exec_snapshot"
    assert snapshot.status == ExecutionStatus.RUNNING
