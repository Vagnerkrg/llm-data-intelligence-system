from src.agents.cognitive_learning.domain import LearningExperience
from src.agents.cognitive_learning.services import LearningOutcomeEngine


def test_evaluate_learning_experience():
    engine = LearningOutcomeEngine()

    experiences = [
        LearningExperience(
            experience_id="exp-1",
            source="cognitive_evaluation",
            signal_type="strategy",
            pattern="effective strategy",
            outcome="observed",
            confidence=0.9,
            impact="high",
        )
    ]

    result = engine.evaluate(experiences)

    assert len(result) == 1
    assert result[0].experience_id == "exp-1"
    assert result[0].confidence == 0.9
    assert "strategy" in result[0].knowledge_candidate
    assert result[0].recommendation
