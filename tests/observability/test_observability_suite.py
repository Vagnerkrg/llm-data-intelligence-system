"""System-level observability test suite for V1.28."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest

from src.agents.runtime.agent_runtime import AgentRuntime
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
from src.observability.infrastructure.storage.sqlite_repositories import (
    SQLiteObservabilityRepository,
)
from src.observability.infrastructure.storage.sqlite_store import (
    SQLiteObservabilityStore,
)
from src.observability.services.agent_runtime_observability import (
    AgentRuntimeObservability,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


class BrokenEventService:
    """Event service that simulates an observability failure."""

    def emit(self, *args, **kwargs):
        raise RuntimeError("event backend unavailable")


class BrokenMetricsService:
    """Metrics service that simulates an observability failure."""

    def record(self, *args, **kwargs):
        raise RuntimeError("metrics backend unavailable")

    def increment(self, *args, **kwargs):
        raise RuntimeError("metrics backend unavailable")


class BrokenTraceService:
    """Trace service that simulates an observability failure."""

    def create_trace(self, *args, **kwargs):
        raise RuntimeError("trace backend unavailable")


@pytest.fixture
def repository() -> SQLiteObservabilityRepository:
    """Create an isolated SQLite repository."""
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
    """Create a trace service backed by the test repository."""
    return ExecutionTraceService(
        repository=repository,
    )


def test_domain_serialization_roundtrip() -> None:
    """Domain objects must survive serialization."""
    context = ObservabilityContext(
        execution_id="exec_serialization",
        correlation_id="corr-001",
        metadata={
            "source": "test",
        },
    )

    payload = context.to_json()
    restored = ObservabilityContext.from_json(payload)

    assert restored.execution_id == context.execution_id
    assert restored.correlation_id == context.correlation_id
    assert restored.metadata == context.metadata


def test_execution_trace_serialization_roundtrip() -> None:
    """ExecutionTrace must be serializable and reconstructable."""
    trace = ExecutionTrace(
        execution_id="exec_trace_roundtrip",
        metadata={
            "source": "test",
        },
    )

    payload = trace.to_json()
    restored = ExecutionTrace.from_json(payload)

    assert restored.execution_id == trace.execution_id
    assert restored.status == trace.status
    assert restored.metadata == trace.metadata


def test_execution_event_serialization_roundtrip() -> None:
    """ExecutionEvent serialization must preserve metadata."""
    event = ExecutionEvent(
        execution_id="exec_event_roundtrip",
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        stage="reasoning",
        metadata={
            "confidence": 0.91,
        },
    )

    restored = ExecutionEvent.from_json(event.to_json())

    assert restored.execution_id == event.execution_id
    assert restored.event_type == event.event_type
    assert restored.metadata == event.metadata


def test_execution_metric_serialization_roundtrip() -> None:
    """ExecutionMetric serialization must preserve metric semantics."""
    metric = ExecutionMetric(
        metric_name="evaluation_score",
        value=0.93,
        unit="score",
        timestamp=datetime.now(timezone.utc),
        execution_id="exec_metric_roundtrip",
        component="evaluation",
        metric_type=MetricType.SCORE,
        metadata={
            "model": "test",
        },
    )

    restored = ExecutionMetric.from_json(metric.to_json())

    assert restored.metric_name == metric.metric_name
    assert restored.value == metric.value
    assert restored.metric_type == metric.metric_type
    assert restored.metadata == metric.metadata


def test_execution_state_serialization_roundtrip() -> None:
    """ExecutionState must survive serialization."""
    state = ExecutionState(
        execution_id="exec_state_roundtrip",
        status=ExecutionStatus.RUNNING,
        current_component="reasoning",
        current_stage="reasoning",
        current_step="analyze",
        updated_at=datetime.now(timezone.utc),
        metadata={
            "source": "test",
        },
    )

    restored = ExecutionState.from_json(state.to_json())

    assert restored.execution_id == state.execution_id
    assert restored.status == state.status
    assert restored.current_component == state.current_component


def test_execution_error_serialization_roundtrip() -> None:
    """ExecutionError must preserve severity and message."""
    error = ExecutionError(
        execution_id="exec_error_roundtrip",
        component="runtime",
        stage="execution",
        severity=ErrorSeverity.ERROR,
        error_type="RuntimeError",
        message="test failure",
        recoverable=False,
        metadata={
            "source": "test",
        },
    )

    restored = ExecutionError.from_json(error.to_json())

    assert restored.execution_id == error.execution_id
    assert restored.severity == error.severity
    assert restored.message == error.message
    assert restored.recoverable == error.recoverable


def test_execution_lifecycle_is_complete(
    trace_service: ExecutionTraceService,
) -> None:
    """The trace lifecycle must produce a complete execution."""
    execution_id = "exec_lifecycle_suite"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.start(
        execution_id,
    )

    trace_service.update_state(
        execution_id,
        status=ExecutionStatus.RUNNING,
        component="reasoning",
        stage="reasoning",
    )

    trace_service.complete(
        execution_id,
    )

    trace = trace_service.reconstruct(execution_id)

    assert trace.status == ExecutionStatus.COMPLETED
    assert trace.started_at is not None
    assert trace.finished_at is not None
    assert trace.duration is not None
    assert trace.state_history


def test_execution_correlation_is_preserved(
    trace_service: ExecutionTraceService,
) -> None:
    """Correlation IDs must survive persistence and reconstruction."""
    execution_id = "exec_correlation_suite"

    trace = trace_service.create_trace(
        execution_id=execution_id,
        correlation_id="corr-suite-001",
        metadata={
            "request_id": "request-001",
        },
    )

    restored = trace_service.get_trace(execution_id)

    assert restored.context is not None
    assert restored.context.correlation_id == trace.context.correlation_id
    assert restored.metadata["request_id"] == "request-001"


def test_events_metrics_errors_share_execution_id(
    trace_service: ExecutionTraceService,
) -> None:
    """All observability records must remain correlated."""
    execution_id = "exec_correlation_records"

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
        metric_name="reasoning_duration_ms",
        value=120,
        unit="ms",
        component="reasoning",
    )

    trace_service.record_error(
        execution_id=execution_id,
        component="reasoning",
        error_type="TestWarning",
        message="warning",
        severity=ErrorSeverity.WARNING,
    )

    trace = trace_service.get_trace(execution_id)

    assert all(event.execution_id == execution_id for event in trace.events)

    assert all(metric.execution_id == execution_id for metric in trace.metrics)

    assert all(error.execution_id == execution_id for error in trace.errors)


def test_timeline_is_deterministically_sorted(
    trace_service: ExecutionTraceService,
) -> None:
    """Timeline ordering must depend on timestamps, not insertion order."""
    execution_id = "exec_deterministic_timeline"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    base = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        timestamp=base + timedelta(seconds=3),
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_STARTED,
        component="reasoning",
        timestamp=base + timedelta(seconds=1),
    )

    trace_service.record_event(
        execution_id=execution_id,
        event_type=EventType.PLANNING_STARTED,
        component="planning",
        timestamp=base + timedelta(seconds=2),
    )

    timeline = trace_service.timeline(execution_id)

    timestamps = [item["timestamp"] for item in timeline]

    assert timestamps == sorted(timestamps)


def test_incomplete_execution_can_be_recovered(
    trace_service: ExecutionTraceService,
) -> None:
    """Incomplete executions must become explicit failed traces."""
    execution_id = "exec_incomplete"

    trace_service.create_trace(
        execution_id=execution_id,
    )

    trace_service.start(
        execution_id,
    )

    recovered = trace_service.recover_incomplete(execution_id)

    assert recovered.status == ExecutionStatus.FAILED
    assert recovered.errors
    assert recovered.errors[-1].error_type == "IncompleteExecution"


def test_duplicate_events_do_not_corrupt_trace(
    repository: SQLiteObservabilityRepository,
) -> None:
    """Duplicate event IDs must be idempotent."""
    execution_id = "exec_duplicate_suite"

    repository.save_trace(
        ExecutionTrace(
            execution_id=execution_id,
        )
    )

    event = ExecutionEvent(
        event_id="evt-suite-001",
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
    )

    repository.events.save(event)
    repository.events.save(event)

    events = repository.events.get_by_execution_id(execution_id)

    assert len(events) == 1


def test_memory_storage_isolation(
    trace_service: ExecutionTraceService,
) -> None:
    """Two executions must never share observability records."""
    trace_service.create_trace(
        execution_id="exec_isolation_a",
    )

    trace_service.create_trace(
        execution_id="exec_isolation_b",
    )

    trace_service.record_event(
        execution_id="exec_isolation_a",
        event_type=EventType.MEMORY_RETRIEVAL_COMPLETED,
        component="memory",
    )

    trace_a = trace_service.get_trace("exec_isolation_a")

    trace_b = trace_service.get_trace("exec_isolation_b")

    assert len(trace_a.events) == 1
    assert len(trace_b.events) == 0


def test_agent_runtime_can_run_with_observability_disabled() -> None:
    """Disabling observability must not disable the runtime."""
    runtime = AgentRuntime(
        observability_enabled=False,
    )

    context = runtime.create_context("test query")

    assert context.execution_id is None


def test_broken_trace_backend_is_isolated() -> None:
    """Trace backend failure must not escape the observability boundary."""
    observability = AgentRuntimeObservability(
        trace_service=BrokenTraceService(),
    )

    execution_id = observability.start_execution()

    assert execution_id is None


def test_broken_event_backend_is_isolated() -> None:
    """Event backend failures must never propagate to callers."""
    trace_service = ExecutionTraceService()

    observability = AgentRuntimeObservability(
        trace_service=trace_service,
        event_service=BrokenEventService(),
    )

    execution_id = observability.start_execution()

    assert execution_id is not None

    observability.learning_signal_generated(
        execution_id,
        confidence=0.9,
        signal_type="test",
    )

    trace = observability.trace(execution_id)

    assert trace is not None


def test_broken_metrics_backend_is_isolated() -> None:
    """Metric backend failures must never propagate to callers."""
    trace_service = ExecutionTraceService()

    observability = AgentRuntimeObservability(
        trace_service=trace_service,
        metrics_service=BrokenMetricsService(),
    )

    execution_id = observability.start_execution()

    assert execution_id is not None

    observability.cognitive_evaluation_completed(
        execution_id,
        score=0.9,
    )

    trace = observability.trace(execution_id)

    assert trace is not None


def test_dependency_injection_reuses_shared_trace_service() -> None:
    """Injected repositories/services must be preserved."""
    trace_service = ExecutionTraceService()

    observability = AgentRuntimeObservability(
        trace_service=trace_service,
    )

    execution_id = observability.start_execution()

    assert observability.trace_service is trace_service
    assert trace_service.exists(execution_id)


def test_repository_dependency_injection_survives_roundtrip() -> None:
    """Repository DI must persist and recover the same execution."""
    store = SQLiteObservabilityStore(
        database_path=":memory:",
    )

    repository = SQLiteObservabilityRepository(
        store=store,
    )

    first_service = ExecutionTraceService(
        repository=repository,
    )

    execution_id = "exec_repository_di"

    first_service.create_trace(
        execution_id=execution_id,
    )

    first_service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
    )

    second_service = ExecutionTraceService(
        repository=repository,
    )

    restored = second_service.get_trace(execution_id)

    assert restored.execution_id == execution_id
    assert len(restored.events) == 1


def test_full_persistence_recovery_scenario(
    repository: SQLiteObservabilityRepository,
) -> None:
    """Critical scenario: execution → trace → events → metrics → errors → recovery."""
    execution_id = "exec_critical_scenario"

    service = ExecutionTraceService(
        repository=repository,
    )

    service.create_trace(
        execution_id=execution_id,
        correlation_id="critical-correlation",
    )

    service.start(
        execution_id,
    )

    service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_STARTED,
        component="reasoning",
        stage="reasoning",
    )

    service.record_event(
        execution_id=execution_id,
        event_type=EventType.REASONING_COMPLETED,
        component="reasoning",
        stage="reasoning",
    )

    service.record_metric(
        execution_id=execution_id,
        metric_name="reasoning_duration_ms",
        value=100,
        unit="ms",
        component="reasoning",
        metric_type=MetricType.DURATION,
    )

    service.record_error(
        execution_id=execution_id,
        component="reasoning",
        error_type="TestWarning",
        message="non-fatal warning",
        severity=ErrorSeverity.WARNING,
        recoverable=True,
    )

    service.complete(
        execution_id,
    )

    restored = service.reconstruct(execution_id)

    assert restored.status == ExecutionStatus.COMPLETED
    assert restored.context.correlation_id == "critical-correlation"

    assert len(restored.events) >= 3
    assert len(restored.metrics) == 1
    assert len(restored.errors) == 1

    assert all(record.execution_id == execution_id for record in restored.events)


def test_concurrent_execution_ids_remain_isolated() -> None:
    """
    Distinct executions created concurrently must remain isolated.

    The test uses an in-memory service because the purpose here is
    correlation/isolation rather than concurrent SQLite writes.
    """
    service = ExecutionTraceService()

    execution_ids = [f"exec_concurrent_{index}" for index in range(12)]

    def create_execution(
        execution_id: str,
    ) -> str:
        service.create_trace(
            execution_id=execution_id,
        )

        service.record_event(
            execution_id=execution_id,
            event_type=EventType.EXECUTION_STARTED,
            component="execution",
        )

        return execution_id

    with ThreadPoolExecutor(max_workers=4) as executor:
        created_ids = list(
            executor.map(
                create_execution,
                execution_ids,
            )
        )

    assert set(created_ids) == set(execution_ids)

    for execution_id in execution_ids:
        trace = service.get_trace(execution_id)

        assert len(trace.events) == 1

        assert all(event.execution_id == execution_id for event in trace.events)


def test_execution_remains_available_after_observability_event_failure() -> None:
    """
    A failed event emission must not make the execution unavailable.
    """
    trace_service = ExecutionTraceService()

    observability = AgentRuntimeObservability(
        trace_service=trace_service,
        event_service=BrokenEventService(),
    )

    execution_id = observability.start_execution()

    assert execution_id is not None

    observability.error(
        execution_id,
        RuntimeError("test"),
        component="runtime",
        stage="runtime",
    )

    trace = trace_service.get_trace(execution_id)

    assert trace.execution_id == execution_id


def test_execution_remains_available_after_metrics_failure() -> None:
    """
    A failed metric collection must not make the trace unusable.
    """
    trace_service = ExecutionTraceService()

    observability = AgentRuntimeObservability(
        trace_service=trace_service,
        metrics_service=BrokenMetricsService(),
    )

    execution_id = observability.start_execution()

    assert execution_id is not None

    observability.cognitive_evaluation_completed(
        execution_id,
        score=0.82,
    )

    trace = trace_service.get_trace(execution_id)

    assert trace.execution_id == execution_id
