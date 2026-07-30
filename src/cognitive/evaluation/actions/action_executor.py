from .models.action import Action
from .models.action_result import ActionResult


class ActionExecutor:
    """
    Executes a selected action.

    Future versions will integrate
    Runtime, Planner, Memory and
    Self Improvement.
    """

    def execute(
        self,
        action: Action,
    ) -> ActionResult:

        result = ActionResult(

            action=action,

            message=f"{action.action_type.value} executed",

        )

        result.mark_executed()

        return result