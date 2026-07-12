from src.agents.execution.execution_feedback import (
    ExecutionFeedback,
)

from src.agents.execution.execution_state import (
    ExecutionState,
)

from src.agents.execution.execution_status import (
    ExecutionStatus,
)


class PlanEvaluator:
    """
    Evaluates execution state and generates feedback.
    """

    def evaluate(
        self,
        state: ExecutionState,
    ) -> ExecutionFeedback:
        """
        Analyze execution result.
        """

        if (
            state.status
            == ExecutionStatus.COMPLETED
        ):
            return ExecutionFeedback(
                success=True,
                message=(
                    "Execution completed successfully"
                ),
            )

        if (
            state.status
            == ExecutionStatus.FAILED
        ):
            return ExecutionFeedback(
                success=False,
                message=(
                    "Execution failed"
                ),
                issues=[
                    "Execution status is failed"
                ],
                recommendations=[
                    "Review execution strategy"
                ],
            )

        return ExecutionFeedback(
            success=False,
            message=(
                "Execution incomplete"
            ),
            issues=[
                "Execution not finished"
            ],
        )