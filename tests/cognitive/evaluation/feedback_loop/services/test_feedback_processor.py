from src.cognitive.evaluation.feedback_loop.services.feedback_processor import (
    FeedbackProcessor,
)


def test_feedback_processor_creation():

    processor = FeedbackProcessor()

    feedback = processor.process(
        feedback_id="fb-001",
        source="evaluation",
        signal="reasoning_failure",
        impact="high",
    )

    assert feedback.feedback_id == "fb-001"
    assert feedback.signal == "reasoning_failure"
    assert feedback.impact == "high"
