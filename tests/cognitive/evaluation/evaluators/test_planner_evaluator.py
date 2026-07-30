from src.cognitive.evaluation.evaluators.planner_evaluator import (
    PlannerEvaluator
)

from src.cognitive.evaluation.models.evaluation_context import (
    EvaluationContext
)


def test_planner_evaluator_creation():

    evaluator = PlannerEvaluator()

    assert evaluator is not None


def test_planner_evaluator_with_plan():

    evaluator = PlannerEvaluator()

    context = EvaluationContext(
        agent_id="agent-001",
        metadata={
            "plan": [
                "load data",
                "analyze",
                "report"
            ]
        }
    )

    result = evaluator.evaluate(
        context
    )

    assert result.passed is True
    assert result.score == 1.0


def test_planner_evaluator_without_plan():

    evaluator = PlannerEvaluator()

    context = EvaluationContext(
        agent_id="agent-001"
    )

    result = evaluator.evaluate(
        context
    )

    assert result.passed is False
    assert result.score == 0.0