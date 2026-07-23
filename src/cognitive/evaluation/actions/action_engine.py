from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult,
)

from .action_executor import ActionExecutor
from .action_selector import ActionSelector

from .models.action_result import ActionResult


class ActionEngine:
    """
    Main orchestration service for
    Cognitive Actions.
    """

    def __init__(self):

        self.selector = ActionSelector()

        self.executor = ActionExecutor()

    def execute(
        self,
        evaluation: EvaluationResult,
    ) -> ActionResult:

        action = self.selector.select(
            evaluation
        )

        return self.executor.execute(
            action
        )