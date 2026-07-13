from src.agents.decision.decision_engine import DecisionEngine
from src.agents.decision.decision_integration import DecisionIntegration
from src.agents.decision.decision_context import DecisionContext
from src.agents.decision.decision_alternative import DecisionAlternative
from src.agents.decision.decision_strategy import DecisionStrategy


def test_decision_integration_executes_flow():

    integration = DecisionIntegration(
        engine=DecisionEngine()
    )

    context = DecisionContext(
        request_id="req-002",
        objective="Select best strategy",
    )

    alternatives = [
        DecisionAlternative(
            name="Strategy B",
            description="Alternative approach",
            expected_outcome="Better result",
            confidence=0.8,
        )
    ]

    result = integration.evaluate(
        context,
        DecisionStrategy(),
        alternatives,
    )

    assert result.decision_id == "req-002"