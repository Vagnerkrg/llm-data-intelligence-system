from datetime import datetime

from src.cognitive.evaluation.feedback_loop.models.improvement_feedback import (
    ImprovementFeedback,
)
from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)
from src.cognitive.evaluation.feedback_loop.protocols.learning_integration_protocol import (
    LearningIntegrationProtocol,
)


class FakeLearningIntegration(LearningIntegrationProtocol):

    def store_learning_feedback(
        self,
        feedback: LearningFeedback,
    ) -> bool:

        return True

    def create_improvement_feedback(
        self,
        feedback: LearningFeedback,
    ) -> ImprovementFeedback:

        return ImprovementFeedback(
            improvement_id="imp-test",
            feedback_id=feedback.feedback_id,
            action="optimize_reasoning",
            expected_result="better_decision",
            created_at=datetime.now(),
        )


def test_learning_feedback_storage():

    service = FakeLearningIntegration()

    feedback = LearningFeedback(
        feedback_id="fb-001",
        source="evaluation",
        signal="low_quality",
        impact="high",
        created_at=datetime.now(),
    )

    assert service.store_learning_feedback(feedback)


def test_create_improvement_feedback():

    service = FakeLearningIntegration()

    feedback = LearningFeedback(
        feedback_id="fb-001",
        source="evaluation",
        signal="low_quality",
        impact="high",
        created_at=datetime.now(),
    )

    improvement = service.create_improvement_feedback(feedback)

    assert isinstance(
        improvement,
        ImprovementFeedback,
    )

    assert improvement.feedback_id == "fb-001"