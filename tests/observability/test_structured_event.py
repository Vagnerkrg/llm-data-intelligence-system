"""Tests for the structured event system."""

from datetime import timedelta

import pytest

from src.observability.domain.enums import (
    EventType,
    ExecutionStatus,
)
from src.observability.services.event_emitter import (
    EventEmissionError,
    EventEmitter,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)
from src.observability.services.structured_event import (
    StructuredEventService,
)
from tests.observability.test_execution_trace import BASE_TIME


@pytest.fixture
def trace_service() -> ExecutionTraceService:
    """Create a fresh trace service."""
    return ExecutionTraceService()


@pytest.fixture
def event_service(
    trace_service: ExecutionTraceService,
) -> StructuredEventService:
    """Create a structured event service."""
    return StructuredEventService(
        trace_service=trace_service,
    )


def test_emit_event_into_execution_trace(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_event",
    )

    event = event_service.emit(
        execution_id="exec_event",
        event_type=EventType.REASONING_STARTED,
        component="reasoning",
        stage="reasoning",
        timestamp=BASE_TIME,
        metadata={
            "strategy": "analytical",
        },
    )

    assert event.execution_id == "exec_event"
    assert event.event_type == EventType.REASONING_STARTED
    assert event.component == "reasoning"
    assert event.stage == "reasoning"
    assert event.metadata["strategy"] == "analytical"


def test_emit_lifecycle_event(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_lifecycle",
    )

    event = event_service.emit_lifecycle(
        execution_id="exec_lifecycle",
        event_type=EventType.EXECUTION_STARTED,
        status=ExecutionStatus.RUNNING,
        timestamp=BASE_TIME,
    )

    assert event.component == "execution"
    assert event.stage == "lifecycle"
    assert event.status == ExecutionStatus.RUNNING


def test_emit_domain_specific_events(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_domains",
    )

    reasoning = event_service.emit_reasoning(
        "exec_domains",
        EventType.REASONING_COMPLETED,
    )

    planning = event_service.emit_planning(
        "exec_domains",
        EventType.PLANNING_COMPLETED,
    )

    tool = event_service.emit_tool(
        "exec_domains",
        EventType.TOOL_CALL_COMPLETED,
    )

    memory = event_service.emit_memory(
        "exec_domains",
        EventType.MEMORY_RETRIEVAL_COMPLETED,
    )

    knowledge = event_service.emit_knowledge(
        "exec_domains",
        EventType.KNOWLEDGE_ACCESSED,
    )

    cognitive = event_service.emit_cognitive(
        "exec_domains",
        EventType.COGNITIVE_EVALUATION_COMPLETED,
    )

    assert reasoning.component == "reasoning"
    assert planning.component == "planning"
    assert tool.component == "tool"
    assert memory.component == "memory"
    assert knowledge.component == "knowledge"
    assert cognitive.component == "cognitive"


def test_events_are_queryable_by_execution_id(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_query",
    )

    event_service.emit(
        "exec_query",
        EventType.REASONING_STARTED,
        "reasoning",
    )

    event_service.emit(
        "exec_query",
        EventType.REASONING_COMPLETED,
        "reasoning",
    )

    events = event_service.get_events(
        "exec_query",
    )

    assert len(events) == 2
    assert all(event.execution_id == "exec_query" for event in events)


def test_events_are_ordered_by_timestamp(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_order",
    )

    event_service.emit(
        "exec_order",
        EventType.STEP_COMPLETED,
        "execution",
        timestamp=BASE_TIME + timedelta(seconds=5),
    )

    event_service.emit(
        "exec_order",
        EventType.STEP_STARTED,
        "execution",
        timestamp=BASE_TIME + timedelta(seconds=1),
    )

    event_service.emit(
        "exec_order",
        EventType.EXECUTION_STARTED,
        "execution",
        timestamp=BASE_TIME,
    )

    events = event_service.get_events(
        "exec_order",
    )

    timestamps = [event.timestamp for event in events]

    assert timestamps == sorted(timestamps)


def test_duplicate_events_are_controlled(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_duplicate",
    )

    event_service.emit(
        "exec_duplicate",
        EventType.TOOL_CALL_STARTED,
        "tool",
        deduplication_key="tool-call-001",
    )

    with pytest.raises(ValueError):
        event_service.emit(
            "exec_duplicate",
            EventType.TOOL_CALL_STARTED,
            "tool",
            deduplication_key="tool-call-001",
        )

    assert (
        event_service.count(
            "exec_duplicate",
        )
        == 1
    )


def test_deduplication_is_isolated_per_execution(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_first",
    )

    trace_service.create_trace(
        execution_id="exec_second",
    )

    event_service.emit(
        "exec_first",
        EventType.TOOL_CALL_STARTED,
        "tool",
        deduplication_key="tool-001",
    )

    event = event_service.emit(
        "exec_second",
        EventType.TOOL_CALL_STARTED,
        "tool",
        deduplication_key="tool-001",
    )

    assert event.execution_id == "exec_second"


def test_event_is_immutable_after_emission(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_immutable",
    )

    event = event_service.emit(
        "exec_immutable",
        EventType.REASONING_COMPLETED,
        "reasoning",
    )

    with pytest.raises(Exception):
        event.component = "changed"


def test_event_metadata_is_copied(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_metadata",
    )

    metadata = {
        "value": "original",
    }

    event_service.emit(
        "exec_metadata",
        EventType.REASONING_COMPLETED,
        "reasoning",
        metadata=metadata,
    )

    metadata["value"] = "mutated"

    events = event_service.get_events(
        "exec_metadata",
    )

    assert events[0].metadata["value"] == "original"


def test_unknown_execution_is_rejected(
    event_service: StructuredEventService,
) -> None:
    with pytest.raises(KeyError):
        event_service.emit(
            "exec_unknown",
            EventType.REASONING_STARTED,
            "reasoning",
        )


def test_event_emitter_raises_structured_error(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    emitter = EventEmitter(
        service=event_service,
    )

    with pytest.raises(EventEmissionError):
        emitter.emit(
            execution_id="exec_unknown",
            event_type=EventType.REASONING_STARTED,
            component="reasoning",
        )


def test_event_emitter_can_fail_safely(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    emitter = EventEmitter(
        service=event_service,
    )

    result = emitter.try_emit(
        execution_id="exec_unknown",
        event_type=EventType.REASONING_STARTED,
        component="reasoning",
    )

    assert result is None


def test_error_event_is_supported(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_error_event",
    )

    event = event_service.emit_error(
        "exec_error_event",
        metadata={
            "error_type": "ToolExecutionError",
        },
        timestamp=BASE_TIME,
    )

    assert event.event_type == EventType.ERROR_OCCURRED
    assert event.component == "system"
    assert event.stage == "error"


def test_cognitive_catalog_events_are_supported(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_cognitive_catalog",
    )

    events = [
        event_service.emit_cognitive(
            "exec_cognitive_catalog",
            EventType.COGNITIVE_EVALUATION_STARTED,
        ),
        event_service.emit_cognitive(
            "exec_cognitive_catalog",
            EventType.LEARNING_SIGNAL_GENERATED,
        ),
        event_service.emit_cognitive(
            "exec_cognitive_catalog",
            EventType.LEARNING_OUTCOME_CREATED,
        ),
        event_service.emit_cognitive(
            "exec_cognitive_catalog",
            EventType.EVOLUTION_DECISION_CREATED,
        ),
        event_service.emit_cognitive(
            "exec_cognitive_catalog",
            EventType.ADAPTATION_APPLIED,
        ),
    ]

    assert len(events) == 5


def test_events_remain_isolated_between_executions(
    trace_service: ExecutionTraceService,
    event_service: StructuredEventService,
) -> None:
    trace_service.create_trace(
        execution_id="exec_a",
    )

    trace_service.create_trace(
        execution_id="exec_b",
    )

    event_service.emit(
        "exec_a",
        EventType.REASONING_COMPLETED,
        "reasoning",
    )

    event_service.emit(
        "exec_b",
        EventType.PLANNING_COMPLETED,
        "planning",
    )

    first = event_service.get_events(
        "exec_a",
    )

    second = event_service.get_events(
        "exec_b",
    )

    assert len(first) == 1
    assert len(second) == 1
    assert first[0].event_type != second[0].event_type
