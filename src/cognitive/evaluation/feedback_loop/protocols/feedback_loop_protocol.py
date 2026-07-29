from abc import ABC, abstractmethod

from src.cognitive.evaluation.feedback_loop.models.feedback_cycle import (
    FeedbackCycle,
)
from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)


class FeedbackLoopProtocol(ABC):
    """
    Contrato responsável pelo processamento
    do ciclo de feedback cognitivo.
    """

    @abstractmethod
    def process_feedback(
        self,
        feedback: LearningFeedback,
    ) -> FeedbackCycle:
        """
        Processa um feedback e gera um ciclo cognitivo.
        """
        pass

    @abstractmethod
    def complete_cycle(
        self,
        cycle: FeedbackCycle,
    ) -> FeedbackCycle:
        """
        Finaliza o ciclo de aprendizado.
        """
        pass