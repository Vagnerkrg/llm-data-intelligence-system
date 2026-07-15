from src.agents.self_improvement.adaptation.domain.adaptation_action import (
    AdaptationAction,
)

from src.agents.self_improvement.adaptation.domain.adaptation_type import (
    AdaptationType,
)

from src.agents.self_improvement.adaptation.services.adaptation_validator import (
    AdaptationValidator,
)


def test_validator_accepts_valid_action():

    validator = AdaptationValidator()

    action = AdaptationAction(
        adaptation_type=AdaptationType.STRATEGY,
        target="planner",
        description="Optimize execution strategy",
    )

    assert validator.validate(action) is True


def test_validator_rejects_missing_target():

    validator = AdaptationValidator()

    action = AdaptationAction(
        adaptation_type=AdaptationType.STRATEGY,
        target="",
        description="Optimize execution strategy",
    )

    assert validator.validate(action) is False