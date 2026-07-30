from src.cognitive.evaluation.actions.action_executor import (
    ActionExecutor,
)

from src.cognitive.evaluation.actions.models.action import (
    Action,
)

from src.cognitive.evaluation.actions.models.action_type import (
    ActionType,
)


def test_executor():

    executor = ActionExecutor()

    result = executor.execute(

        Action(ActionType.ACCEPT)

    )

    assert result.executed

    assert result.succeeded()