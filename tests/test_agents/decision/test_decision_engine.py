from src.agents.decision.decision_engine import DecisionEngine
from src.agents.decision.decision_context import DecisionContext
from src.agents.decision.decision_alternative import DecisionAlternative
from src.agents.decision.decision_strategy import DecisionStrategy


def test_decision_engine_creates_decision():

    engine = DecisionEngine()

    context = DecisionContext(
        request_id="req-001",
        objective="Improve analysis performance",
    )

    alternatives = [
        DecisionAlternative(
            name="Strategy A",
            description="Optimize execution",
            expected_outcome="Higher performance",
            confidence=0.9,
        )
    ]

    strategy = DecisionStrategy()

    decision = engine.decide(
        context,
        strategy,
        alternatives,
    )

    assert decision.decision_id == "req-001"
    assert decision.status is not None