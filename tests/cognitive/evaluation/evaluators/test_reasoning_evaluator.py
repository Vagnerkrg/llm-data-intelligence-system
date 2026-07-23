from src.cognitive.evaluation.evaluators.reasoning_evaluator import (
    ReasoningEvaluator
)

from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)


def test_reasoning_evaluator_creation():

    evaluator = ReasoningEvaluator()

    assert evaluator is not None



def test_reasoning_evaluator_with_output():

    evaluator = ReasoningEvaluator()

    context = EvaluationContext(
        agent_id="agent-001",
        output_data="logical answer"
    )


    result = evaluator.evaluate(
        context
    )


    assert result.score == 1.0
    assert result.passed is True



def test_reasoning_evaluator_without_output():

    evaluator = ReasoningEvaluator()

    context = EvaluationContext(
        agent_id="agent-001"
    )


    result = evaluator.evaluate(
        context
    )


    assert result.score == 0.0
    assert result.passed is False