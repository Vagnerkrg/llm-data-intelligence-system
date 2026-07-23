from src.cognitive.evaluation.actions.models.action import (
    Action,
)

from src.cognitive.evaluation.actions.models.action_type import (
    ActionType,
)


def test_action_terminal():

    action = Action(ActionType.ACCEPT)

    assert action.is_terminal()


def test_action_retry():

    action = Action(ActionType.RETRY)

    assert action.requires_retry()


def test_action_not_terminal():

    action = Action(ActionType.IMPROVE)

    assert not action.is_terminal()