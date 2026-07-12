from src.agents.execution.execution_feedback_loop import (
    ExecutionFeedbackLoop,
)

from src.agents.execution.execution_state import (
    ExecutionState,
)

from src.agents.execution.execution_status import (
    ExecutionStatus,
)

from src.agents.evaluation.plan_evaluator import (
    PlanEvaluator,
)


def test_feedback_loop_default_evaluator():
    """
    Validate default evaluator creation.
    """

    loop = ExecutionFeedbackLoop()

    assert isinstance(
        loop.evaluator,
        PlanEvaluator,
    )


def test_feedback_loop_success_flow():
    """
    Validate successful evaluation flow.
    """

    loop = ExecutionFeedbackLoop()

    state = ExecutionState(
        execution_id="exec_001",
        status=ExecutionStatus.COMPLETED,
    )

    feedback = loop.evaluate(
        state
    )

    assert feedback.success is True

    assert (
        feedback.message
        == "Execution completed successfully"
    )


def test_feedback_loop_failure_flow():
    """
    Validate failed evaluation flow.
    """

    loop = ExecutionFeedbackLoop()

    state = ExecutionState(
        execution_id="exec_002",
        status=ExecutionStatus.FAILED,
    )

    feedback = loop.evaluate(
        state
    )

    assert feedback.success is False

    assert (
        "Execution status is failed"
        in feedback.issues
    )


def test_feedback_loop_custom_evaluator():
    """
    Validate evaluator injection.
    """

    class CustomEvaluator:

        def evaluate(self, state):
            return "custom_feedback"


    loop = ExecutionFeedbackLoop(
        evaluator=CustomEvaluator()
    )

    result = loop.evaluate(
        ExecutionState(
            execution_id="exec_003"
        )
    )

    assert (
        result
        == "custom_feedback"
    )