from datetime import datetime

from src.cognitive.evaluation.feedback_loop.models.feedback_cycle import (
    FeedbackCycle,
    FeedbackCycleStatus,
)
from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)
from src.cognitive.evaluation.feedback_loop.protocols.feedback_loop_protocol import (
    FeedbackLoopProtocol,
)


class FakeFeedbackLoop(FeedbackLoopProtocol):
    def process_feedback(
        self,
        feedback: LearningFeedback,
    ) -> FeedbackCycle:

        return FeedbackCycle(
            cycle_id="cycle-test",
            evaluation_id=feedback.feedback_id,
            status=FeedbackCycleStatus.CREATED,
            created_at=datetime.now(),
        )

    def complete_cycle(
        self,
        cycle: FeedbackCycle,
    ) -> FeedbackCycle:

        cycle.mark_applied()
        return cycle


def test_feedback_loop_protocol_process():

    service = FakeFeedbackLoop()

    feedback = LearningFeedback(
        feedback_id="feedback-001",
        source="evaluation",
        signal="quality_issue",
        impact="high",
        created_at=datetime.now(),
    )

    cycle = service.process_feedback(feedback)

    assert cycle.evaluation_id == "feedback-001"
    assert cycle.status == FeedbackCycleStatus.CREATED


def test_feedback_loop_protocol_complete():

    service = FakeFeedbackLoop()

    cycle = FeedbackCycle(
        cycle_id="cycle-001",
        evaluation_id="eval-001",
        status=FeedbackCycleStatus.CREATED,
        created_at=datetime.now(),
    )

    result = service.complete_cycle(cycle)

    assert result.status == FeedbackCycleStatus.APPLIED
