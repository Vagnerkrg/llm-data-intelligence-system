from src.agents.self_improvement.adaptation.services.adaptation_executor import (
    AdaptationExecutor,
)

from src.agents.self_improvement.adaptation.domain.adaptation_action import (
    AdaptationAction,
)

from src.agents.self_improvement.adaptation.domain.adaptation_type import (
    AdaptationType,
)


def test_adaptation_executor_executes_action():

    executor = AdaptationExecutor()

    action = AdaptationAction(
        adaptation_type=AdaptationType.STRATEGY,
        target="planner",
        description="Optimize execution strategy",
    )

    result = executor.execute(action)

    assert result.success is True
    assert result.action == action