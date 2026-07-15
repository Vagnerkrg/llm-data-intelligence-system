from src.agents.self_improvement.adaptation.domain.adaptation_type import (
    AdaptationType,
)

from src.agents.self_improvement.adaptation.domain.adaptation_context import (
    AdaptationContext,
)

from src.agents.self_improvement.adaptation.domain.adaptation_action import (
    AdaptationAction,
)

from src.agents.self_improvement.adaptation.domain.adaptation_result import (
    AdaptationResult,
)


def test_adaptation_domain_models():

    context = AdaptationContext(
        source="evaluation",
        reason="slow execution",
        confidence=0.9,
    )

    action = AdaptationAction(
        adaptation_type=AdaptationType.BEHAVIOR,
        target="planner",
        description="change strategy",
    )

    result = AdaptationResult(
        success=True,
        action=action,
        message="approved",
    )

    assert context.confidence == 0.9
    assert action.target == "planner"
    assert result.success is True