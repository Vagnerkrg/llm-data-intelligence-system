from abc import ABC, abstractmethod


class EvaluationEngine(ABC):
    """
    Contrato principal da Cognitive Evaluation Engine.
    """

    @abstractmethod
    def evaluate(self, context):
        """
        Executa o processo de avaliação cognitiva.
        """

        pass