from src.agents.cognitive_improvement.domain.improvement_context import (
    ImprovementContext,
)


def test_should_create_improvement_context():
    context = ImprovementContext(
        experience="test experience",
        objective="test objective",
    )

    assert context is not None
    assert context.experience == "test experience"
    assert context.objective == "test objective"
    assert context.metadata == {}