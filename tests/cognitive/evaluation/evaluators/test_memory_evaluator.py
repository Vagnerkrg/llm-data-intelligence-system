from src.cognitive.evaluation.evaluators.memory_evaluator import (
    MemoryEvaluator
)

from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)


def test_memory_evaluator_creation():

    evaluator = MemoryEvaluator()

    assert evaluator is not None


def test_memory_evaluator_with_memory():

    evaluator = MemoryEvaluator()

    context = EvaluationContext(
        agent_id="agent-001",
        metadata={
            "memory_context": {
                "previous": "customer analysis"
            }
        }
    )

    result = evaluator.evaluate(
        context
    )

    assert result.passed is True
    assert result.score == 1.0


def test_memory_evaluator_without_memory():

    evaluator = MemoryEvaluator()

    context = EvaluationContext(
        agent_id="agent-001"
    )

    result = evaluator.evaluate(
        context
    )

    assert result.passed is False
    assert result.score == 0.0