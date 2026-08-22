from datetime import datetime

from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)

from src.cognitive.evaluation.feedback_loop.models.feedback_cycle import (
    FeedbackCycleStatus,
)

from src.cognitive.evaluation.feedback_loop.services.feedback_loop_engine import (
    FeedbackLoopEngine,
)


def test_feedback_loop_engine_process():

    engine = FeedbackLoopEngine()

    feedback = LearningFeedback(
        feedback_id="feedback-001",
        source="evaluation",
        signal="low_quality",
        impact="high",
        created_at=datetime.now(),
    )

    cycle = engine.process_feedback(feedback)

    assert cycle.evaluation_id == "feedback-001"
    assert cycle.status == FeedbackCycleStatus.CREATED


def test_feedback_loop_engine_complete():

    engine = FeedbackLoopEngine()

    feedback = LearningFeedback(
        feedback_id="feedback-001",
        source="evaluation",
        signal="low_quality",
        impact="high",
        created_at=datetime.now(),
    )

    cycle = engine.process_feedback(feedback)

    result = engine.complete_cycle(cycle)

    assert result.status == FeedbackCycleStatus.APPLIED
