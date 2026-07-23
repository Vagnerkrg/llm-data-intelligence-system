from abc import ABC, abstractmethod


class EvaluationStrategy(ABC):
    """
    Contrato para estratégias de avaliação cognitiva.

    Permite diferentes formas de agregação:
    - weighted
    - threshold
    - normalized
    - composite
    """


    @abstractmethod
    def execute(self, evaluations):
        """
        Executa uma estratégia sobre avaliações.
        """

        pass