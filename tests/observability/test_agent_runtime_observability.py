"""Unit tests for Agent Runtime observability integration."""

from src.observability.domain.enums import (
    EventType,
    ExecutionStatus,
)
from src.observability.services.agent_runtime_observability import (
    AgentRuntimeObservability,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


def test_disabled_observability_does_not_create_trace() -> None:
    observability = AgentRuntimeObservability(
        enabled=False,
    )

    execution_id = observability.start_execution()

    assert execution_id is None
    assert (
        observability.trace(
            execution_id,
        )
        is None
    )


def test_start_execution_creates_execution_id() -> None:
    observability = AgentRuntimeObservability(
        enabled=True,
    )

    execution_id = observability.start_execution()

    assert execution_id is not None
    assert execution_id.startswith("exec_")


def test_execution_id_is_attached_to_context() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    class Context:
        metadata = {}

    context = Context()

    observability.attach_to_context(
        context,
        execution_id,
    )

    assert context.execution_id == execution_id
    assert context.metadata["execution_id"] == execution_id


def test_reasoning_lifecycle_is_recorded() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.reasoning_started(
        execution_id,
    )

    observability.reasoning_completed(
        execution_id,
    )

    events = observability.trace(
        execution_id,
    ).events

    assert [event.event_type for event in events] == [
        EventType.EXECUTION_STARTED,
        EventType.REASONING_STARTED,
        EventType.REASONING_COMPLETED,
    ]


def test_execution_completion_is_recorded() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.execution_completed(
        execution_id,
        duration_ms=100,
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.status == ExecutionStatus.COMPLETED
    assert trace.events[-1].event_type == EventType.EXECUTION_COMPLETED


def test_execution_failure_is_recorded() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.fail_execution(
        execution_id,
        RuntimeError("runtime failure"),
        duration_ms=50,
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.status == ExecutionStatus.FAILED
    assert len(trace.errors) == 1
    assert trace.events[-1].event_type == EventType.EXECUTION_FAILED


def test_observability_failure_does_not_propagate() -> None:
    class BrokenTraceService:
        def create_trace(self, **kwargs):
            raise RuntimeError("observability unavailable")

    observability = AgentRuntimeObservability(
        trace_service=BrokenTraceService(),
    )

    execution_id = observability.start_execution()

    assert execution_id is None


def test_injected_trace_service_is_reused() -> None:
    trace_service = ExecutionTraceService()

    observability = AgentRuntimeObservability(
        trace_service=trace_service,
    )

    execution_id = observability.start_execution()

    trace = trace_service.get_trace(
        execution_id,
    )

    assert trace.execution_id == execution_id
