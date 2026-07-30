from src.cognitive.evaluation.actions.action_selector import (
    ActionSelector,
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult,
)


def build(score):

    return EvaluationResult(

        score=score,

        passed=score >= 0.5,

        evaluator="unit",

    )


def test_selector_accept():

    selector = ActionSelector()

    action = selector.select(

        build(0.95)

    )

    assert action.action_type.value == "accept"


def test_selector_abort():

    selector = ActionSelector()

    action = selector.select(

        build(0.02)

    )

    assert action.action_type.value == "abort"