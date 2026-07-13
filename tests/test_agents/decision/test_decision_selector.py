from src.agents.decision.decision_selector import DecisionSelector
from src.agents.decision.decision import Decision
from src.agents.decision.decision_alternative import DecisionAlternative
from src.agents.decision.alternative_evaluation import AlternativeEvaluation


def test_decision_selector_selects_best_alternative():

    alternatives = [
        DecisionAlternative(
            name="strategy_a",
            description="First strategy",
            expected_outcome="Good result",
            confidence=0.6
        ),
        DecisionAlternative(
            name="strategy_b",
            description="Second strategy",
            expected_outcome="Better result",
            confidence=0.9
        )
    ]

    evaluations = [
        AlternativeEvaluation(
            alternative_id="strategy_a",
            score=0.6,
            confidence=0.6,
            risk_level="medium",
            evaluation_reason="acceptable"
        ),
        AlternativeEvaluation(
            alternative_id="strategy_b",
            score=0.9,
            confidence=0.9,
            risk_level="low",
            evaluation_reason="best option"
        )
    ]

    selector = DecisionSelector()

    decision = selector.select(
        alternatives,
        evaluations
    )

    assert isinstance(decision, Decision)
    assert decision.strategy == "strategy_b"