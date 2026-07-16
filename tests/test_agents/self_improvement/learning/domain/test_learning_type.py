from src.agents.self_improvement.learning.domain import LearningType


def test_learning_type_values():
    assert LearningType.STRATEGY
    assert LearningType.PATTERN
    assert LearningType.RULE