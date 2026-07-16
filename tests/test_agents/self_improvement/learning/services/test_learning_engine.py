from src.agents.self_improvement.learning.services import LearningEngine


def test_learning_engine_initialization():

    engine = LearningEngine()

    assert engine is not None