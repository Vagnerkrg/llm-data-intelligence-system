from src.agents.execution.execution_status import ExecutionStatus


def test_execution_status_values():
    """
    Validate all available execution lifecycle states.
    """

    assert ExecutionStatus.PENDING.value == "pending"

    assert ExecutionStatus.RUNNING.value == "running"

    assert ExecutionStatus.COMPLETED.value == "completed"

    assert ExecutionStatus.FAILED.value == "failed"

    assert ExecutionStatus.CANCELLED.value == "cancelled"

    assert ExecutionStatus.PAUSED.value == "paused"


def test_execution_status_is_string_enum():
    """
    Ensure ExecutionStatus behaves as a string enum.
    """

    assert isinstance(
        ExecutionStatus.RUNNING,
        str
    )


def test_execution_status_members():
    """
    Validate expected amount of execution states.
    """

    assert len(ExecutionStatus) == 6