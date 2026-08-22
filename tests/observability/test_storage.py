"""Tests for Observability persistence."""

from datetime import timedelta

import pytest

from src.observability.domain.enums import (
    ErrorSeverity,
    EventType,
    MetricType,
)
from src.observability.domain.models import (
    ExecutionError,
    ExecutionEvent,
    ExecutionMetric,
    ExecutionTrace,
)
from src.observability.infrastructure.storage.sqlite_repositories import (
    SQLiteObservabilityRepository,
)
from src.observability.infrastructure.storage.sqlite_store import (
    SQLiteObservabilityStore,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)
from src.observability.services.metrics import (
    MetricsService,
)
from src.observability.services.structured_event import (
    StructuredEventService,
)


@pytest.fixture
def repository() -> SQLiteObservabilityRepository:
    """Create an isolated in-memory repository."""
    store = SQLiteObservabilityStore(
        database_path=":memory:",
    )

    return SQLiteObservabilityRepository(
        store=store,
    )


@pytest.fixture
def trace_service(
    repository: SQLiteObservabilityRepository,
) -> ExecutionTraceService:
    """Create a trace service backed by SQLite."""
    return ExecutionTraceService(
        repository=repository,
    )


def test_create_trace_is_persisted(
    trace_service: ExecutionTraceService,
    repository: SQLiteObservabilityRepository,
) -> None:
    trace = trace_service.create_trace(
        execution_id="exec_storage_001",
    )

    persisted = repository.get_trace(
        trace.execution_id,
    )

    assert persisted is not None
    assert persisted.execution_id == trace.execution_id
    assert persisted.status.value == "pending"


def test_lifecycle_survives_reconstruction(
    trace_service: ExecutionTraceService,
) -> None:
    execution_id = "exec_storage_002"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.start(
        execution_id,
    )

    trace_service.complete(
        execution_id,
    )

    reconstructed = trace_service.reconstruct(
        execution_id,
    )

    assert reconstructed.status.value == "completed"
    assert reconstructed.started_at is not None
    assert reconstructed.finished_at is not None
    assert reconstructed.duration is not None


def test_event_is_persisted(
    trace_service: ExecutionTraceService,
    repository: SQLiteObservabilityRepository,
) -> None:
    execution_id = "exec_event_storage"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        stage="reasoning",
        metadata={
            "confidence": 0.91,
        },
    )

    events = repository.events.get_by_execution_id(
        execution_id,
    )

    assert len(events) == 1
    assert events[0].event_type == EventType.REASONING_COMPLETED
    assert events[0].metadata["confidence"] == 0.91


def test_metric_is_persisted(
    trace_service: ExecutionTraceService,
    repository: SQLiteObservabilityRepository,
) -> None:
    execution_id = "exec_metric_storage"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.record_metric(
        execution_id=execution_id,
        metric_name="evaluation_score",
        value=0.92,
        unit="score",
        component="evaluation",
        metric_type=MetricType.SCORE,
    )

    metrics = repository.metrics.get_by_execution_id(
        execution_id,
    )

    assert len(metrics) == 1
    assert metrics[0].value == 0.92
    assert metrics[0].metric_type == MetricType.SCORE


def test_error_is_persisted(
    trace_service: ExecutionTraceService,
    repository: SQLiteObservabilityRepository,
) -> None:
    execution_id = "exec_error_storage"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.record_error(
        execution_id=execution_id,
        component="runtime",
        error_type="RuntimeError",
        message="test error",
        severity=ErrorSeverity.ERROR,
    )

    errors = repository.errors.get_by_execution_id(
        execution_id,
    )

    assert len(errors) == 1
    assert errors[0].error_type == "RuntimeError"
    assert errors[0].message == "test error"


def test_complete_trace_is_reconstructed(
    trace_service: ExecutionTraceService,
) -> None:
    execution_id = "exec_complete_trace"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.start(
        execution_id,
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
    )

    trace_service.record_metric(
        execution_id=execution_id,
        metric_name="reasoning_duration_ms",
        value=100,
        unit="ms",
        component="reasoning",
        metric_type=MetricType.DURATION,
    )

    trace_service.record_error(
        execution_id=execution_id,
        component="reasoning",
        error_type="TestWarning",
        message="warning",
        severity=ErrorSeverity.WARNING,
    )

    trace_service.complete(
        execution_id,
    )

    trace = trace_service.get_trace(
        execution_id,
    )

    assert len(trace.events) >= 2
    assert len(trace.metrics) == 1
    assert len(trace.errors) == 1
    assert trace.status.value == "completed"


def test_execution_isolation(
    trace_service: ExecutionTraceService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_a",
    )

    trace_service.create_trace(
        execution_id="exec_b",
    )

    trace_service.record_event(
        execution_id="exec_a",
        event_type=EventType.EXECUTION_STARTED,
        component="execution",
    )

    trace_a = trace_service.get_trace(
        "exec_a",
    )

    trace_b = trace_service.get_trace(
        "exec_b",
    )

    assert len(trace_a.events) == 1
    assert len(trace_b.events) == 0


def test_event_order_is_preserved(
    trace_service: ExecutionTraceService,
) -> None:
    execution_id = "exec_order"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.start(
        execution_id,
    )

    trace = trace_service.get_trace(
        execution_id,
    )

    first = trace.started_at

    second = first + timedelta(
        seconds=2,
    )

    third = first + timedelta(
        seconds=1,
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        timestamp=second,
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_STARTED,
        component="reasoning",
        timestamp=third,
    )

    events = trace_service.reconstruct(
        execution_id,
    ).events

    assert events[0].timestamp <= events[1].timestamp


def test_duplicate_event_id_is_ignored(
    repository: SQLiteObservabilityRepository,
) -> None:
    trace = ExecutionTrace(
        execution_id="exec_duplicate",
    )

    repository.save_trace(
        trace,
    )

    event = ExecutionEvent(
        event_id="evt_duplicate",
        execution_id="exec_duplicate",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
    )

    repository.events.save(
        event,
    )

    repository.events.save(
        event,
    )

    events = repository.events.get_by_execution_id(
        "exec_duplicate",
    )

    assert len(events) == 1


def test_duplicate_error_id_is_ignored(
    repository: SQLiteObservabilityRepository,
) -> None:
    trace = ExecutionTrace(
        execution_id="exec_error_duplicate",
    )

    repository.save_trace(
        trace,
    )

    error = ExecutionError(
        error_id="err_duplicate",
        execution_id="exec_error_duplicate",
        component="runtime",
        severity=ErrorSeverity.ERROR,
        error_type="RuntimeError",
        message="duplicate",
    )

    repository.errors.save(
        error,
    )

    repository.errors.save(
        error,
    )

    errors = repository.errors.get_by_execution_id(
        "exec_error_duplicate",
    )

    assert len(errors) == 1


def test_history_is_queryable(
    trace_service: ExecutionTraceService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_history_a",
    )

    trace_service.start(
        "exec_history_a",
    )

    trace_service.complete(
        "exec_history_a",
    )

    trace_service.create_trace(
        execution_id="exec_history_b",
    )

    history = trace_service.list_history()

    ids = {trace.execution_id for trace in history}

    assert {
        "exec_history_a",
        "exec_history_b",
    }.issubset(ids)


def test_history_limit_is_respected(
    trace_service: ExecutionTraceService,
) -> None:
    for index in range(3):
        trace_service.create_trace(
            execution_id=f"exec_limit_{index}",
        )

    history = trace_service.list_history(
        limit=2,
    )

    assert len(history) == 2


def test_invalid_history_limit_is_rejected(
    trace_service: ExecutionTraceService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_limit_error",
    )

    with pytest.raises(ValueError):
        trace_service.list_history(
            limit=0,
        )


def test_deletion_removes_complete_trace(
    trace_service: ExecutionTraceService,
) -> None:
    execution_id = "exec_delete"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
    )

    trace_service.record_metric(
        execution_id=execution_id,
        metric_name="test_metric",
        value=1,
        unit="count",
        component="test",
    )

    trace_service.record_error(
        execution_id=execution_id,
        component="test",
        error_type="TestError",
        message="delete me",
        severity=ErrorSeverity.ERROR,
    )

    assert trace_service.delete(
        execution_id,
    )

    assert not trace_service.exists(
        execution_id,
    )


def test_metrics_service_can_use_persistent_trace_service(
    trace_service: ExecutionTraceService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_metrics_di",
    )

    metrics = MetricsService(
        trace_service=trace_service,
    )

    metrics.increment(
        execution_id="exec_metrics_di",
        metric_name="executions_total",
        component="execution",
    )

    restored = trace_service.get_trace(
        "exec_metrics_di",
    )

    assert len(restored.metrics) == 1


def test_structured_event_service_can_use_persistent_trace_service(
    trace_service: ExecutionTraceService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_events_di",
    )

    service = StructuredEventService(
        trace_service=trace_service,
    )

    service.emit(
        execution_id="exec_events_di",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
    )

    restored = trace_service.get_trace(
        "exec_events_di",
    )

    assert len(restored.events) == 1


def test_repository_backend_is_replaceable() -> None:
    class FakeRepository:
        def __init__(self):
            self.traces = {}

        def save_trace(self, trace):
            self.traces[trace.execution_id] = trace.model_copy(
                deep=True,
            )
            return trace

        def get_trace(self, execution_id):
            trace = self.traces.get(execution_id)

            return (
                trace.model_copy(
                    deep=True,
                )
                if trace is not None
                else None
            )

        def list_traces(self, *, limit=None):
            values = list(self.traces.values())

            return values[:limit] if limit else values

        def exists(self, execution_id):
            return execution_id in self.traces

        def delete_trace(self, execution_id):
            return (
                self.traces.pop(
                    execution_id,
                    None,
                )
                is not None
            )

    repository = FakeRepository()

    service = ExecutionTraceService(
        repository=repository,
    )

    trace = service.create_trace(
        execution_id="exec_replaceable",
    )

    assert repository.get_trace(trace.execution_id) is not None
