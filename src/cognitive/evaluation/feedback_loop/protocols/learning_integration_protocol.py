from abc import ABC, abstractmethod

from src.cognitive.evaluation.feedback_loop.models.improvement_feedback import (
    ImprovementFeedback,
)
from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)


class LearningIntegrationProtocol(ABC):
    """
    Contrato responsável pela integração
    entre feedback e sistemas de aprendizado.
    """

    @abstractmethod
    def store_learning_feedback(
        self,
        feedback: LearningFeedback,
    ) -> bool:
        """
        Persiste um sinal de aprendizado.
        """
        pass

    @abstractmethod
    def create_improvement_feedback(
        self,
        feedback: LearningFeedback,
    ) -> ImprovementFeedback:
        """
        Cria uma ação de melhoria baseada no feedback.
        """
        pass
