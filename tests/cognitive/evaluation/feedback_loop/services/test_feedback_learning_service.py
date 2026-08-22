from datetime import datetime

from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)

from src.cognitive.evaluation.feedback_loop.services.feedback_learning_service import (
    FeedbackLearningService,
)


def test_store_learning_feedback():

    service = FeedbackLearningService()

    feedback = LearningFeedback(
        feedback_id="fb-001",
        source="evaluation",
        signal="improvement_needed",
        impact="medium",
        created_at=datetime.now(),
    )

    result = service.store_learning_feedback(feedback)

    assert result is True
    assert len(service.learning_store) == 1


def test_create_improvement_feedback():

    service = FeedbackLearningService()

    feedback = LearningFeedback(
        feedback_id="fb-001",
        source="evaluation",
        signal="memory_issue",
        impact="high",
        created_at=datetime.now(),
    )

    improvement = service.create_improvement_feedback(feedback)

    assert improvement.feedback_id == "fb-001"
    assert improvement.action == "analyze_and_improve"
