from datetime import datetime

from src.agents.execution.execution_event import (
    ExecutionEvent,
    ExecutionEventType,
)


def test_execution_event_types():
    """
    Validate available execution event types.
    """

    assert (
        ExecutionEventType.EXECUTION_STARTED.value
        == "execution_started"
    )

    assert (
        ExecutionEventType.EXECUTION_COMPLETED.value
        == "execution_completed"
    )

    assert (
        ExecutionEventType.EXECUTION_FAILED.value
        == "execution_failed"
    )

    assert (
        ExecutionEventType.STEP_STARTED.value
        == "step_started"
    )

    assert (
        ExecutionEventType.STEP_COMPLETED.value
        == "step_completed"
    )

    assert (
        ExecutionEventType.STEP_FAILED.value
        == "step_failed"
    )

    assert (
        ExecutionEventType.TOOL_STARTED.value
        == "tool_started"
    )

    assert (
        ExecutionEventType.TOOL_COMPLETED.value
        == "tool_completed"
    )

    assert (
        ExecutionEventType.RETRY_REQUESTED.value
        == "retry_requested"
    )


def test_execution_event_creation():
    """
    Validate execution event object creation.
    """

    event = ExecutionEvent(
        event_type=ExecutionEventType.EXECUTION_STARTED,
        message="Execution started",
    )

    assert (
        event.event_type
        == ExecutionEventType.EXECUTION_STARTED
    )

    assert event.message == "Execution started"

    assert isinstance(
        event.timestamp,
        datetime
    )

    assert event.metadata == {}


def test_execution_event_metadata():
    """
    Validate custom metadata storage.
    """

    event = ExecutionEvent(
        event_type=ExecutionEventType.STEP_COMPLETED,
        message="Step completed",
        metadata={
            "step_id": "step_001",
            "tool": "analytics_tool",
        },
    )

    assert event.metadata["step_id"] == "step_001"

    assert event.metadata["tool"] == "analytics_tool"


def test_execution_event_enum_is_string_based():
    """
    Ensure event types are string enums.
    """

    assert isinstance(
        ExecutionEventType.EXECUTION_STARTED,
        str,
    )