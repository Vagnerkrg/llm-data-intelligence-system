from src.agents.self_improvement.learning.domain import LearningExperience


def test_learning_experience_creation():

    experience = LearningExperience(
        description="Improved execution strategy",
        success=True
    )

    assert experience.description == "Improved execution strategy"
    assert experience.success is True