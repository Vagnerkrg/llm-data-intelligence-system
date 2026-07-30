from src.cognitive.evaluation.feedback.models.feedback_result import (
    FeedbackResult,
)

from src.cognitive.evaluation.feedback.models.feedback_type import (
    FeedbackType,
)


def test_feedback_result_creation():

    result = FeedbackResult(

        feedback_id="feedback-001",

        feedback_type=FeedbackType.SUCCESS,

        message="Everything is correct.",

        confidence=0.95,

        recommendation="Continue.",

        source="CES",

    )

    assert result.feedback_id == "feedback-001"

    assert result.feedback_type == FeedbackType.SUCCESS

    assert result.confidence == 0.95

    assert result.metadata == {}