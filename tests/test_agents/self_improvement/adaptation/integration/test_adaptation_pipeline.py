from src.agents.self_improvement.adaptation.services.adaptation_engine import (
    AdaptationEngine,
)

from src.agents.self_improvement.adaptation.contracts.adaptation_request import (
    AdaptationRequest,
)

from src.agents.self_improvement.adaptation.domain.adaptation_context import (
    AdaptationContext,
)


def test_adaptation_pipeline():

    engine = AdaptationEngine()

    request = AdaptationRequest(
        context=AdaptationContext(
            source="learning_signal",
            reason="optimize tool selection",
            confidence=0.85,
        ),
        target="tool_selector",
    )

    response = engine.adapt(request)

    assert response.result.action.description == (
        "optimize tool selection"
    )