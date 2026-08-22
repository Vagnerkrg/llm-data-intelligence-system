from datetime import datetime

from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)


def test_learning_feedback_creation():

    feedback = LearningFeedback(
        feedback_id="fb-001",
        source="evaluation_engine",
        signal="decision_quality_low",
        impact="high",
        created_at=datetime.now(),
    )

    assert feedback.signal == "decision_quality_low"


def test_learning_feedback_high_impact():

    feedback = LearningFeedback(
        feedback_id="fb-001",
        source="evaluation_engine",
        signal="quality_issue",
        impact="HIGH",
        created_at=datetime.now(),
    )

    assert feedback.is_high_impact()
