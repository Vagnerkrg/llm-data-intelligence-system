from src.cognitive.evaluation.evaluators.reflection_evaluator import (
    ReflectionEvaluator
)

from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)


def test_reflection_evaluator_creation():

    evaluator = ReflectionEvaluator()

    assert evaluator is not None



def test_reflection_evaluator_with_reflection():

    evaluator = ReflectionEvaluator()

    context = EvaluationContext(
        agent_id="agent-001",
        metadata={
            "reflection": "analysis completed"
        }
    )


    result = evaluator.evaluate(
        context
    )


    assert result.score == 1.0
    assert result.passed is True



def test_reflection_evaluator_without_reflection():

    evaluator = ReflectionEvaluator()

    context = EvaluationContext(
        agent_id="agent-001"
    )


    result = evaluator.evaluate(
        context
    )


    assert result.score == 0.0
    assert result.passed is False