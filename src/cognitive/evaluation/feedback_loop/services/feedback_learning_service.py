from src.cognitive.evaluation.feedback_loop.models.improvement_feedback import (
    ImprovementFeedback,
)

from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)

from src.cognitive.evaluation.feedback_loop.protocols.learning_integration_protocol import (
    LearningIntegrationProtocol,
)


class FeedbackLearningService(LearningIntegrationProtocol):
    """
    Serviço responsável por integrar
    feedback recebido com aprendizado.
    """

    def __init__(self):

        self.learning_store = []

    def store_learning_feedback(
        self,
        feedback: LearningFeedback,
    ) -> bool:

        self.learning_store.append(feedback)

        return True

    def create_improvement_feedback(
        self,
        feedback: LearningFeedback,
    ) -> ImprovementFeedback:

        return ImprovementFeedback(
            improvement_id=f"improvement-{feedback.feedback_id}",
            feedback_id=feedback.feedback_id,
            action="analyze_and_improve",
            expected_result="increase cognitive capability",
            created_at=feedback.created_at,
        )
