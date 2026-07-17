from src.agents.cognitive_improvement.domain.improvement_context import (
    ImprovementContext,
)

from src.agents.cognitive_improvement.domain.improvement_status import (
    ImprovementStatus,
)

from src.agents.cognitive_improvement.services.cycle_executor import (
    CycleExecutor,
)


def test_should_create_cycle_executor():

    executor = CycleExecutor()

    assert executor is not None



def test_should_execute_cognitive_cycle():

    executor = CycleExecutor()

    context = ImprovementContext(
        experience={
            "execution": "completed"
        },
        objective="Improve agent performance"
    )

    result = executor.execute(
        context
    )

    assert result is not None

    assert result.status == ImprovementStatus.COMPLETED



def test_should_preserve_cognitive_cycle_outputs():

    executor = CycleExecutor()

    context = ImprovementContext(
        experience={
            "execution": "completed"
        },
        objective="Improve agent performance"
    )


    result = executor.execute(
        context
    )


    assert result is not None

    assert result.status == ImprovementStatus.COMPLETED

    assert len(result.knowledge) > 0

    assert len(result.adaptations) > 0

    assert "evaluation" in result.metadata

    assert "reflection" in result.metadata

    assert "learning" in result.metadata