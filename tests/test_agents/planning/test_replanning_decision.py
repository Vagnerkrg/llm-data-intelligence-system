from src.agents.planning.replanning_decision import (
    ReplanningDecisionEngine,
)

from src.agents.execution.execution_feedback import (
    ExecutionFeedback,
)


def test_replanning_decision_on_failure():
    """
    Validate replanning request after failure.
    """

    engine = ReplanningDecisionEngine()

    feedback = ExecutionFeedback(
        success=False,
        message="Execution failed",
        issues=[
            "Tool timeout"
        ],
    )

    decision = engine.decide(
        feedback
    )

    assert decision.should_replan is True

    assert (
        decision.reason
        == "Execution failure detected"
    )

    assert (
        "Tool timeout"
        in decision.issues
    )


def test_replanning_decision_on_success():
    """
    Validate no replanning after success.
    """

    engine = ReplanningDecisionEngine()

    feedback = ExecutionFeedback(
        success=True,
        message="Completed",
    )

    decision = engine.decide(
        feedback
    )

    assert decision.should_replan is False

    assert (
        decision.reason
        == "Execution completed successfully"
    )


def test_replanning_decision_preserves_multiple_issues():
    """
    Validate issue propagation.
    """

    engine = ReplanningDecisionEngine()

    feedback = ExecutionFeedback(
        success=False,
        message="Failed",
        issues=[
            "Timeout",
            "Invalid response",
        ],
    )

    decision = engine.decide(
        feedback
    )

    assert len(decision.issues) == 2


def test_replanning_decision_default_issue_list():
    """
    Validate decision default structure.
    """

    engine = ReplanningDecisionEngine()

    feedback = ExecutionFeedback(
        success=True,
        message="OK",
    )

    decision = engine.decide(
        feedback
    )

    assert decision.issues == []