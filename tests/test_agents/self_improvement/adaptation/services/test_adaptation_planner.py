from src.agents.self_improvement.adaptation.domain.adaptation_context import (
    AdaptationContext,
)

from src.agents.self_improvement.adaptation.services.adaptation_planner import (
    AdaptationPlanner,
)


def test_adaptation_planner_creates_action():

    planner = AdaptationPlanner()

    context = AdaptationContext(
        source="learning_signal",
        reason="optimize tool selection",
        confidence=0.85,
    )

    action = planner.plan(
        context,
        "tool_selector",
    )

    assert action is not None