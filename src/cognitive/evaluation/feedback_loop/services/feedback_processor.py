from datetime import datetime

from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)


class FeedbackProcessor:
    """
    Serviço responsável por transformar
    sinais de avaliação em feedback estruturado.
    """

    def process(
        self,
        feedback_id: str,
        source: str,
        signal: str,
        impact: str,
    ) -> LearningFeedback:

        return LearningFeedback(
            feedback_id=feedback_id,
            source=source,
            signal=signal,
            impact=impact,
            created_at=datetime.now(),
        )
