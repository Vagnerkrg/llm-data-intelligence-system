from src.agents.self_improvement.learning.services import LearningManager


def test_learning_pipeline():

    manager = LearningManager()

    result = manager.learn()

    assert result is not None