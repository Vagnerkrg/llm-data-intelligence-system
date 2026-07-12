from src.agents.execution.execution_feedback import (
    ExecutionFeedback,
)


def test_execution_feedback_default_values():
    """
    Validate default feedback structure.
    """

    feedback = ExecutionFeedback(
        success=True,
        message="Execution completed successfully",
    )

    assert feedback.success is True

    assert (
        feedback.message
        == "Execution completed successfully"
    )

    assert feedback.issues == []

    assert feedback.recommendations == []

    assert feedback.metadata == {}


def test_execution_feedback_with_issues():
    """
    Validate feedback containing problems.
    """

    feedback = ExecutionFeedback(
        success=False,
        message="Execution failed",
        issues=[
            "Tool timeout",
            "Missing data",
        ],
        recommendations=[
            "Retry execution",
            "Use alternative tool",
        ],
    )

    assert feedback.success is False

    assert len(feedback.issues) == 2

    assert (
        feedback.issues[0]
        == "Tool timeout"
    )

    assert len(feedback.recommendations) == 2

    assert (
        feedback.recommendations[0]
        == "Retry execution"
    )


def test_execution_feedback_metadata():
    """
    Validate metadata storage.
    """

    feedback = ExecutionFeedback(
        success=True,
        message="Completed",
        metadata={
            "execution_id": "exec_001",
            "duration": 4.5,
        },
    )

    assert (
        feedback.metadata["execution_id"]
        == "exec_001"
    )

    assert (
        feedback.metadata["duration"]
        == 4.5
    )


def test_execution_feedback_independent_lists():
    """
    Validate that list fields are independent.
    """

    first = ExecutionFeedback(
        success=True,
        message="First",
    )

    second = ExecutionFeedback(
        success=True,
        message="Second",
    )

    first.issues.append(
        "Problem detected"
    )

    assert second.issues == []