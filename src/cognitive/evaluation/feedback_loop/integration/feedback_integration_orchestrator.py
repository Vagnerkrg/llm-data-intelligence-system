from src.cognitive.evaluation.feedback_loop.integration.learning_memory_adapter import (
    LearningMemoryAdapter,
)

from src.cognitive.evaluation.feedback_loop.integration.cognitive_improvement_adapter import (
    CognitiveImprovementAdapter,
)

from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)

from src.cognitive.evaluation.feedback_loop.models.improvement_feedback import (
    ImprovementFeedback,
)


class FeedbackIntegrationOrchestrator:
    """
    Orquestra a integração completa:

    Feedback Loop
          |
          +--> Memory
          |
          +--> Improvement
    """

    def __init__(self):

        self.memory_adapter = LearningMemoryAdapter()
        self.improvement_adapter = CognitiveImprovementAdapter()


    def integrate_feedback(
        self,
        feedback: LearningFeedback,
    ) -> bool:

        return self.memory_adapter.store_feedback(
            feedback
        )


    def integrate_improvement(
        self,
        improvement: ImprovementFeedback,
    ) -> bool:

        return self.improvement_adapter.send_improvement(
            improvement
        )