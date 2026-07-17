from src.agents.cognitive_improvement.domain.improvement_context import (
    ImprovementContext,
)

from src.agents.cognitive_improvement.domain.improvement_status import (
    ImprovementStatus,
)

from src.agents.cognitive_improvement.contracts.improvement_request import (
    ImprovementRequest,
)

from src.agents.cognitive_improvement.services.cognitive_improvement_engine import (
    CognitiveImprovementEngine,
)



def test_should_create_cognitive_improvement_engine():

    engine = CognitiveImprovementEngine()

    assert engine is not None



def test_should_execute_cognitive_improvement_cycle():

    engine = CognitiveImprovementEngine()

    context = ImprovementContext(
        experience={},
        objective="Improve agent execution"
    )

    request = ImprovementRequest(
        context=context
    )

    response = engine.execute(
        request
    )

    assert response is not None
    assert response.result is not None



def test_should_validate_improvement_result():

    engine = CognitiveImprovementEngine()

    context = ImprovementContext(
        experience={},
        objective="Improve agent execution"
    )

    request = ImprovementRequest(
        context=context
    )

    response = engine.execute(
        request
    )

    assert response.result is not None
    assert response.result.status == ImprovementStatus.COMPLETED