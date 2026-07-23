from abc import ABC, abstractmethod


class CapabilityEvaluator(ABC):
    """
    Contrato base para avaliadores de capacidades cognitivas.

    Exemplos:
    - reasoning
    - memory
    - planning
    - tools
    """


    @abstractmethod
    def evaluate(self, context):
        """
        Executa avaliação sobre um contexto cognitivo.
        """

        pass