from src.cognitive.evaluation.feedback.models.feedback_type import (
    FeedbackType,
)


def test_feedback_type_contains_expected_values():

    assert FeedbackType.SUCCESS.value == "success"

    assert FeedbackType.IMPROVEMENT.value == "improvement"

    assert FeedbackType.OPTIMIZATION.value == "optimization"

    assert FeedbackType.LEARNING.value == "learning"

    assert FeedbackType.WARNING.value == "warning"

    assert FeedbackType.CRITICAL.value == "critical"