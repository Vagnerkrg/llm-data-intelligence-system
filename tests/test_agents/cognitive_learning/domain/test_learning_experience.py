from src.agents.cognitive_learning.domain import LearningExperience


def test_learning_experience_creation():
    experience = LearningExperience(
        experience_id="exp-1",
        source="cognitive_evaluation",
        signal_type="strategy",
        pattern="effective strategy",
        outcome="observed",
        confidence=0.9,
        impact="high",
    )

    assert experience.experience_id == "exp-1"
    assert experience.signal_type == "strategy"
    assert experience.confidence == 0.9
    assert experience.impact == "high"
