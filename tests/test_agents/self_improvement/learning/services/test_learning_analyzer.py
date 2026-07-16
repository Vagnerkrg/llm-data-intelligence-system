from src.agents.self_improvement.learning.services import LearningAnalyzer


def test_learning_analyzer_initialization():

    analyzer = LearningAnalyzer()

    assert analyzer is not None