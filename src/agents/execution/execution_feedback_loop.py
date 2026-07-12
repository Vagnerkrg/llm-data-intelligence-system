from src.agents.execution.execution_feedback import (
    ExecutionFeedback,
)

from src.agents.execution.execution_state import (
    ExecutionState,
)

from src.agents.evaluation.plan_evaluator import (
    PlanEvaluator,
)


class ExecutionFeedbackLoop:
    """
    Coordinates execution evaluation feedback flow.
    """

    def __init__(
        self,
        evaluator=None,
    ):
        self.evaluator = (
            evaluator
            if evaluator
            else PlanEvaluator()
        )

    def evaluate(
        self,
        state: ExecutionState,
    ) -> ExecutionFeedback:
        """
        Evaluate execution state and return feedback.
        """

        return self.evaluator.evaluate(
            state
        )