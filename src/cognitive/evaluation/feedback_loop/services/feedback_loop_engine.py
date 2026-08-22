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


class FeedbackLoopEngine(FeedbackLoopProtocol):
    """
    Engine responsável por executar
    o ciclo cognitivo de feedback.
    """

    def process_feedback(
        self,
        feedback: LearningFeedback,
    ) -> FeedbackCycle:

        return FeedbackCycle(
            cycle_id=f"cycle-{feedback.feedback_id}",
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
