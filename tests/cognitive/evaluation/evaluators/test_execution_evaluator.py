from src.cognitive.evaluation.evaluators.execution_evaluator import (
    ExecutionEvaluator
)

from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)


def test_execution_evaluator_creation():

    evaluator = ExecutionEvaluator()

    assert evaluator is not None


def test_execution_evaluator_success():

    evaluator = ExecutionEvaluator()

    context = EvaluationContext(
        agent_id="agent-001",
        execution_id="exec-001",
        output_data={
            "result": "ok"
        }
    )

    result = evaluator.evaluate(
        context
    )

    assert result.passed is True
    assert result.score == 1.0


def test_execution_evaluator_failure():

    evaluator = ExecutionEvaluator()

    context = EvaluationContext(
        agent_id="agent-001",
        execution_id="exec-002",
        output_data=None
    )

    result = evaluator.evaluate(
        context
    )

    assert result.passed is False
    assert result.score == 0.0