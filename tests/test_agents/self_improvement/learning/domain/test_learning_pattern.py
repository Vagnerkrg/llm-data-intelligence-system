from src.agents.self_improvement.learning.domain import LearningPattern


def test_learning_pattern_creation():

    pattern = LearningPattern(
        name="execution_optimization",
        frequency=3
    )

    assert pattern.name == "execution_optimization"
    assert pattern.frequency == 3