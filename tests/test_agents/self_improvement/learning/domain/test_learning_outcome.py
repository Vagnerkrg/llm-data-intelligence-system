from src.agents.self_improvement.learning.domain import LearningOutcome


def test_learning_outcome_creation():

    outcome = LearningOutcome(
        improvement="Better planning",
        confidence=0.9
    )

    assert outcome.improvement == "Better planning"
    assert outcome.confidence == 0.9