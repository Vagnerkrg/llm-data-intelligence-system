from src.agents.cognitive_improvement.domain.improvement_result import (
    ImprovementResult,
)

from src.agents.cognitive_improvement.domain.improvement_status import (
    ImprovementStatus,
)

from src.agents.cognitive_improvement.services.improvement_validator import (
    ImprovementValidator,
)


def test_should_validate_completed_improvement():

    validator = ImprovementValidator()

    result = ImprovementResult(
        status=ImprovementStatus.COMPLETED
    )

    assert validator.validate(
        result
    ) is True