from src.cognitive.evaluation.actions.models.action import (
    Action,
)

from src.cognitive.evaluation.actions.models.action_result import (
    ActionResult,
)

from src.cognitive.evaluation.actions.models.action_type import (
    ActionType,
)


def test_action_result_execution():

    result = ActionResult(

        action=Action(ActionType.ACCEPT)

    )

    assert not result.executed

    result.mark_executed()

    assert result.executed

    assert result.succeeded()