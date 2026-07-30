from src.cognitive.evaluation.feedback_loop.runtime.feedback_runtime import (
    FeedbackRuntime,
)

from src.cognitive.evaluation.feedback_loop.runtime.runtime_feedback_context import (
    RuntimeFeedbackContext,
)

from src.cognitive.evaluation.feedback_loop.services.feedback_learning_service import (
    FeedbackLearningService,
)


class CognitiveFeedbackPipeline:
    """
    Pipeline responsável pelo ciclo cognitivo completo.

    Fluxo:

    Evaluation
        |
        v
    Feedback Runtime
        |
        v
    Learning Feedback
        |
        v
    Improvement Cycle
    """

    def __init__(self):

        self.feedback_runtime = FeedbackRuntime()

        self.learning_service = FeedbackLearningService()


    def execute(
        self,
        context: RuntimeFeedbackContext,
    ):

        feedback_cycle = self.feedback_runtime.execute_feedback_cycle(
            context
        )

        learning_feedback = (
            self.learning_service.store_learning_feedback(
                feedback_cycle
            )
        )

        return {
            "feedback_cycle": feedback_cycle,
            "learning_feedback": learning_feedback,
        }