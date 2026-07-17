from src.agents.cognitive_improvement.contracts.improvement_request import (
    ImprovementRequest,
)
from src.agents.cognitive_improvement.domain.improvement_context import (
    ImprovementContext,
)


def test_should_create_improvement_request():
    context = ImprovementContext(
        experience="test experience",
        objective="test objective",
    )

    request = ImprovementRequest(
        context=context
    )

    assert request is not None
    assert request.context == context