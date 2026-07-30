from src.cognitive.evaluation.actions.action_engine import (
    ActionEngine,
)

from src.cognitive.evaluation.models.evaluation_result import (
    EvaluationResult,
)


def test_action_engine():

    engine = ActionEngine()

    result = engine.execute(

        EvaluationResult(

            score=0.95,

            passed=True,

            evaluator="unit",

        )

    )

    assert result.executed

    assert result.action.action_type.value == "accept"