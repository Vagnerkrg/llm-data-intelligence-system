from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)

from src.cognitive.evaluation.feedback_loop.runtime.runtime_feedback_context import (
    RuntimeFeedbackContext,
)


class CognitiveFeedbackHandler:
    """
    Responsável por transformar eventos
    de execução em feedback cognitivo.
    """

    def handle(
        self,
        context: RuntimeFeedbackContext,
    ) -> LearningFeedback:

        return LearningFeedback(
            feedback_id=context.execution_id,
            source=context.capability,
            signal=context.signal,
            impact=context.impact,
            created_at=context.created_at,
        )
