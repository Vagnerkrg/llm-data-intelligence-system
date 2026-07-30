from typing import List

from src.cognitive.evaluation.strategies.weighted_strategy import (
    WeightedStrategy
)

from src.cognitive.evaluation.strategies.normalized_strategy import (
    NormalizedStrategy
)


class CompositeStrategy:
    """
    Estratégia composta que combina múltiplas
    estratégias de avaliação cognitiva.
    """

    def __init__(self):

        self.weighted_strategy = WeightedStrategy()
        self.normalized_strategy = NormalizedStrategy()


    def evaluate(self, evaluations: List) -> float:
        """
        Executa avaliação composta:

        1. Calcula score ponderado
        2. Normaliza resultado
        """

        weighted_score = (
            self.weighted_strategy.evaluate(
                evaluations
            )
        )

        return self.normalized_strategy.evaluate(
            weighted_score
        )