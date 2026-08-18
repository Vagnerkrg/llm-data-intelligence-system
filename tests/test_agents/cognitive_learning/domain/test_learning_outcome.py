from src.agents.cognitive_learning.domain import LearningOutcome


def test_learning_outcome_creation():
    outcome = LearningOutcome(
        experience_id="exp-1",
        learned_pattern="effective strategy",
        knowledge_candidate="strategy: effective strategy",
        confidence=0.9,
        recommendation="Prioritize this pattern.",
    )

    assert outcome.experience_id == "exp-1"
    assert outcome.learned_pattern == "effective strategy"
    assert outcome.confidence == 0.9
