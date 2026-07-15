from src.agents.self_improvement.adaptation.services.adaptation_engine import (
    AdaptationEngine,
)

from src.agents.self_improvement.adaptation.contracts.adaptation_request import (
    AdaptationRequest,
)

from src.agents.self_improvement.adaptation.domain.adaptation_context import (
    AdaptationContext,
)


def test_adaptation_engine_creates_response():

    engine = AdaptationEngine()

    request = AdaptationRequest(
        context=AdaptationContext(
            source="evaluation",
            reason="improve execution",
            confidence=0.9,
        ),
        target="planner",
    )

    response = engine.adapt(request)

    assert response.result.success is True
    assert response.result.action.target == "planner"