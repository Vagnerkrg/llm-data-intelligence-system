from src.agents.self_improvement.learning.services import LearningRepository


def test_learning_repository_storage():

    repository = LearningRepository()

    repository.save("learning_rule")

    assert repository.count() == 1