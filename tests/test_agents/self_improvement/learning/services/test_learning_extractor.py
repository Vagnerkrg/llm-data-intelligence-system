from src.agents.self_improvement.learning.services import LearningExtractor


def test_learning_extractor_initialization():

    extractor = LearningExtractor()

    assert extractor is not None