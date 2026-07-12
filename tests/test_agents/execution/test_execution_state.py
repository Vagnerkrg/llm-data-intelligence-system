from src.agents.execution.execution_state import (
    ExecutionState,
)

from src.agents.execution.execution_status import (
    ExecutionStatus,
)

from src.agents.execution.execution_event import (
    ExecutionEvent,
    ExecutionEventType,
)

from src.agents.execution.execution_metrics import (
    ExecutionMetrics,
)


def test_execution_state_default_values():
    """
    Validate default execution state creation.
    """

    state = ExecutionState(
        execution_id="exec_001"
    )

    assert state.execution_id == "exec_001"

    assert (
        state.status
        == ExecutionStatus.PENDING
    )

    assert state.current_step_id is None

    assert state.events == []

    assert isinstance(
        state.metrics,
        ExecutionMetrics
    )

    assert state.results == []

    assert state.metadata == {}


def test_execution_state_with_events():
    """
    Validate event storage inside execution state.
    """

    event = ExecutionEvent(
        event_type=ExecutionEventType.STEP_STARTED,
        message="Step started",
    )

    state = ExecutionState(
        execution_id="exec_002",
        events=[event],
    )

    assert len(state.events) == 1

    assert (
        state.events[0].event_type
        == ExecutionEventType.STEP_STARTED
    )


def test_execution_state_with_metrics():
    """
    Validate metrics integration.
    """

    metrics = ExecutionMetrics(
        total_steps=3,
        completed_steps=1,
    )

    state = ExecutionState(
        execution_id="exec_003",
        metrics=metrics,
    )

    assert (
        state.metrics.total_steps
        == 3
    )

    assert (
        state.metrics.completed_steps
        == 1
    )


def test_execution_state_custom_metadata():
    """
    Validate metadata support.
    """

    state = ExecutionState(
        execution_id="exec_004",
        current_step_id="step_01",
        metadata={
            "agent": "analytics_agent",
        },
    )

    assert (
        state.current_step_id
        == "step_01"
    )

    assert (
        state.metadata["agent"]
        == "analytics_agent"
    )