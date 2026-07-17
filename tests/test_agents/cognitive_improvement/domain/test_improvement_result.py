from src.agents.cognitive_improvement.domain.improvement_result import (
    ImprovementResult,
)
from src.agents.cognitive_improvement.domain.improvement_status import (
    ImprovementStatus,
)


def test_should_create_improvement_result():
    result = ImprovementResult(
        status=ImprovementStatus.PENDING
    )

    assert result is not None
    assert result.status == ImprovementStatus.PENDING