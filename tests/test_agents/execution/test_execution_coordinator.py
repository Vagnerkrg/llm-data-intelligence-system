from src.agents.execution.execution_coordinator import (
    ExecutionCoordinator,
)

from src.agents.execution.execution_state import (
    ExecutionState,
)

from src.agents.execution.execution_status import (
    ExecutionStatus,
)

from src.agents.execution.execution_event import (
    ExecutionEventType,
)


def test_execution_coordinator_start_execution():
    """
    Validate execution start lifecycle transition.
    """

    coordinator = ExecutionCoordinator()

    state = ExecutionState(
        execution_id="exec_001"
    )

    result = coordinator.start_execution(
        state
    )

    assert (
        result.status
        == ExecutionStatus.RUNNING
    )

    assert len(result.events) == 1

    assert (
        result.events[0].event_type
        == ExecutionEventType.EXECUTION_STARTED
    )


def test_execution_coordinator_complete_execution():
    """
    Validate execution completion lifecycle transition.
    """

    coordinator = ExecutionCoordinator()

    state = ExecutionState(
        execution_id="exec_002",
        status=ExecutionStatus.RUNNING,
    )

    result = coordinator.complete_execution(
        state
    )

    assert (
        result.status
        == ExecutionStatus.COMPLETED
    )

    assert len(result.events) == 1

    assert (
        result.events[0].event_type
        == ExecutionEventType.EXECUTION_COMPLETED
    )


def test_execution_coordinator_fail_execution():
    """
    Validate execution failure lifecycle transition.
    """

    coordinator = ExecutionCoordinator()

    state = ExecutionState(
        execution_id="exec_003",
        status=ExecutionStatus.RUNNING,
    )

    result = coordinator.fail_execution(
        state,
        error="Tool execution failed",
    )

    assert (
        result.status
        == ExecutionStatus.FAILED
    )

    assert len(result.events) == 1

    assert (
        result.events[0].event_type
        == ExecutionEventType.EXECUTION_FAILED
    )

    assert (
        result.events[0].message
        == "Tool execution failed"
    )


def test_execution_coordinator_preserves_state_data():
    """
    Validate state information preservation.
    """

    coordinator = ExecutionCoordinator()

    state = ExecutionState(
        execution_id="exec_004",
        current_step_id="step_01",
        metadata={
            "agent": "analytics_agent",
        },
    )

    result = coordinator.start_execution(
        state
    )

    assert (
        result.execution_id
        == "exec_004"
    )

    assert (
        result.current_step_id
        == "step_01"
    )

    assert (
        result.metadata["agent"]
        == "analytics_agent"
    )