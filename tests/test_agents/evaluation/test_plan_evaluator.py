from src.agents.evaluation.plan_evaluator import (
    PlanEvaluator,
)

from src.agents.execution.execution_state import (
    ExecutionState,
)

from src.agents.execution.execution_status import (
    ExecutionStatus,
)


def test_plan_evaluator_success_execution():
    """
    Validate successful execution evaluation.
    """

    evaluator = PlanEvaluator()

    state = ExecutionState(
        execution_id="exec_001",
        status=ExecutionStatus.COMPLETED,
    )

    feedback = evaluator.evaluate(
        state
    )

    assert feedback.success is True

    assert (
        feedback.message
        == "Execution completed successfully"
    )


def test_plan_evaluator_failed_execution():
    """
    Validate failed execution evaluation.
    """

    evaluator = PlanEvaluator()

    state = ExecutionState(
        execution_id="exec_002",
        status=ExecutionStatus.FAILED,
    )

    feedback = evaluator.evaluate(
        state
    )

    assert feedback.success is False

    assert (
        "Execution status is failed"
        in feedback.issues
    )


def test_plan_evaluator_running_execution():
    """
    Validate incomplete execution evaluation.
    """

    evaluator = PlanEvaluator()

    state = ExecutionState(
        execution_id="exec_003",
        status=ExecutionStatus.RUNNING,
    )

    feedback = evaluator.evaluate(
        state
    )

    assert feedback.success is False

    assert (
        "Execution not finished"
        in feedback.issues
    )