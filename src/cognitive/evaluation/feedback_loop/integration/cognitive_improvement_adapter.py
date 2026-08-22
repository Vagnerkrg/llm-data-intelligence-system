from src.cognitive.evaluation.feedback_loop.models.improvement_feedback import (
    ImprovementFeedback,
)


class CognitiveImprovementAdapter:
    """
    Adapter responsável pela integração
    com Cognitive Improvement Engine.
    """

    def __init__(self):

        self.improvement_queue = []

    def send_improvement(
        self,
        improvement: ImprovementFeedback,
    ) -> bool:
        """
        Envia recomendação de melhoria
        para o ciclo cognitivo.
        """

        self.improvement_queue.append(improvement)

        return True

    def get_pending_improvements(self):

        return self.improvement_queue
