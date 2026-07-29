from datetime import datetime

from src.cognitive.evaluation.feedback_loop.models.feedback_cycle import (
    FeedbackCycle,
    FeedbackCycleStatus,
)


def test_feedback_cycle_creation():

    cycle = FeedbackCycle(
        cycle_id="cycle-001",
        evaluation_id="eval-001",
        status=FeedbackCycleStatus.CREATED,
        created_at=datetime.now(),
    )

    assert cycle.cycle_id == "cycle-001"
    assert cycle.status == FeedbackCycleStatus.CREATED


def test_feedback_cycle_status_transition():

    cycle = FeedbackCycle(
        cycle_id="cycle-001",
        evaluation_id="eval-001",
        status=FeedbackCycleStatus.CREATED,
        created_at=datetime.now(),
    )

    cycle.mark_processed()

    assert cycle.status == FeedbackCycleStatus.PROCESSED

    cycle.mark_learned()

    assert cycle.status == FeedbackCycleStatus.LEARNED