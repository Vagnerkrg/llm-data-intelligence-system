from src.agents.self_improvement.learning.services import LearningValidator


def test_learning_validator_accepts_valid_learning():

    validator = LearningValidator()

    assert validator.validate(True)