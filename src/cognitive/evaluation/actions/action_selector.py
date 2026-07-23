from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult,
)

from .models.action import Action
from .models.action_type import ActionType


class ActionSelector:
    """
    Selects the most appropriate action
    from an evaluation result.
    """

    def select(
        self,
        result: EvaluationResult,
    ) -> Action:

        score = result.score

        if score >= 0.90:
            action = ActionType.ACCEPT

        elif score >= 0.75:
            action = ActionType.IMPROVE

        elif score >= 0.50:
            action = ActionType.RETRY

        elif score >= 0.30:
            action = ActionType.REPLAN

        elif score >= 0.10:
            action = ActionType.ESCALATE

        else:
            action = ActionType.ABORT

        return Action(

            action_type=action,

            priority=int(score * 100),

            reason=f"Evaluation score {score:.2f}",
        )