from src.agents.self_improvement.adaptation.contracts.adaptation_request import (
    AdaptationRequest,
)

from src.agents.self_improvement.adaptation.domain.adaptation_context import (
    AdaptationContext,
)

from src.agents.self_improvement.adaptation.services.adaptation_manager import (
    AdaptationManager,
)


def test_adaptation_manager_runs_pipeline():

    manager = AdaptationManager()

    request = AdaptationRequest(
        context=AdaptationContext(
            source="evaluation",
            reason="optimize planner",
            confidence=0.90,
        ),
        target="planner",
    )

    response = manager.adapt(request)

    assert response.result.success is True
    assert response.result.action is not None
    assert response.result.message == "Adaptation approved."