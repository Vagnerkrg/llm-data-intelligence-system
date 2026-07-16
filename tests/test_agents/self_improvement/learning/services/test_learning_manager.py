from src.agents.self_improvement.learning.services import LearningManager


def test_learning_manager_initialization():

    manager = LearningManager()

    assert manager is not None