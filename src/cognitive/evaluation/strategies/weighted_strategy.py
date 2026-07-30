from typing import List

from src.cognitive.evaluation.models.capability_evaluation import (
    CapabilityEvaluation
)


class WeightedStrategy:
    """
    Estratégia que calcula avaliação agregada
    considerando pesos das capacidades.
    """

    def evaluate(
        self,
        evaluations: List[CapabilityEvaluation]
    ) -> float:
        """
        Calcula score ponderado.

        Formula:
        sum(score * weight) / sum(weights)
        """

        if not evaluations:
            return 0.0

        total_weight = sum(
            evaluation.weight
            for evaluation in evaluations
        )

        if total_weight == 0:
            return 0.0

        weighted_sum = sum(
            evaluation.score * evaluation.weight
            for evaluation in evaluations
        )

        return weighted_sum / total_weight