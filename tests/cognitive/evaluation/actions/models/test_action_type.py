from src.cognitive.evaluation.actions.models.action_type import (
    ActionType,
)


def test_action_type_contains_expected_values():

    assert ActionType.ACCEPT.value == "accept"

    assert ActionType.IMPROVE.value == "improve"

    assert ActionType.RETRY.value == "retry"

    assert ActionType.REPLAN.value == "replan"

    assert ActionType.ESCALATE.value == "escalate"

    assert ActionType.ABORT.value == "abort"