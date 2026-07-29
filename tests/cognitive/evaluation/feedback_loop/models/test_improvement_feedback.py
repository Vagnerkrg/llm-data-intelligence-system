from datetime import datetime

from src.cognitive.evaluation.feedback_loop.models.improvement_feedback import (
    ImprovementFeedback,
)


def test_improvement_feedback_creation():

    improvement = ImprovementFeedback(
        improvement_id="imp-001",
        feedback_id="fb-001",
        action="adjust_reasoning_strategy",
        expected_result="increase_decision_quality",
        created_at=datetime.now(),
    )

    assert improvement.action == "adjust_reasoning_strategy"


def test_improvement_feedback_matches_feedback():

    improvement = ImprovementFeedback(
        improvement_id="imp-001",
        feedback_id="fb-001",
        action="optimize",
        expected_result="better_result",
        created_at=datetime.now(),
    )

    assert improvement.matches_feedback("fb-001")
    assert not improvement.matches_feedback("fb-002")