from src.agents.cognitive_improvement.contracts.improvement_response import (
    ImprovementResponse,
)
from src.agents.cognitive_improvement.domain.improvement_result import (
    ImprovementResult,
)
from src.agents.cognitive_improvement.domain.improvement_status import (
    ImprovementStatus,
)


def test_should_create_improvement_response():
    result = ImprovementResult(
        status=ImprovementStatus.PENDING
    )

    response = ImprovementResponse(
        result=result
    )

    assert response is not None
    assert response.result == result