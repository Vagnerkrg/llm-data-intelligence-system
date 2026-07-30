from src.cognitive.evaluation.feedback_loop.models.learning_feedback import (
    LearningFeedback,
)


class LearningMemoryAdapter:
    """
    Adapter responsável pela comunicação
    entre Feedback Loop e Learning Memory.
    """

    def __init__(self):

        self.memory_store = []

    def store_feedback(
        self,
        feedback: LearningFeedback,
    ) -> bool:
        """
        Armazena feedback como experiência
        de aprendizado.
        """

        self.memory_store.append(feedback)

        return True

    def retrieve_feedback(
        self,
        feedback_id: str,
    ) -> LearningFeedback | None:
        """
        Recupera feedback armazenado.
        """

        for feedback in self.memory_store:

            if feedback.feedback_id == feedback_id:
                return feedback

        return None