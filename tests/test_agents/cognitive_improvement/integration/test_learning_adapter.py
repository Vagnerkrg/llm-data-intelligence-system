from src.agents.cognitive_improvement.integration.learning_adapter import (
    LearningAdapter,
)


def test_should_create_learning_adapter():
    adapter = LearningAdapter()

    assert adapter is not None