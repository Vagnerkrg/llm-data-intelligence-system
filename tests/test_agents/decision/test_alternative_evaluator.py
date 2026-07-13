from src.agents.decision.alternative_evaluator import AlternativeEvaluator
from src.agents.decision.decision_alternative import DecisionAlternative
from src.agents.decision.decision_context import DecisionContext
from src.agents.decision.alternative_evaluation import AlternativeEvaluation


def test_alternative_evaluator_evaluates_alternatives():

    context = DecisionContext(
        goal="Optimize workflow",
        available_tools=["python"]
    )

    alternatives = [
        DecisionAlternative(
            name="automation",
            description="Automate data workflow",
            expected_outcome="Reduce manual work",
            confidence=0.7
        )
    ]

    evaluator = AlternativeEvaluator()

    evaluations = evaluator.evaluate(
        alternatives,
        context
    )

    assert isinstance(evaluations, list)
    assert len(evaluations) > 0

    assert isinstance(
        evaluations[0],
        AlternativeEvaluation
    )