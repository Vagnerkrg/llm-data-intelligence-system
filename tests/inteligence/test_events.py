from src.intelligence.execution.events import (
    ExecutionEvent,
    ExecutionEventType,
)


def test_execution_event_creation():

    event = ExecutionEvent(
        execution_id="exec-001",
        event_type=ExecutionEventType.STARTED,
        component="agent_runtime",
    )

    assert event.execution_id == "exec-001"
    assert event.event_type == ExecutionEventType.STARTED
    assert event.component == "agent_runtime"
    assert event.event_id is not None
    assert event.timestamp is not None