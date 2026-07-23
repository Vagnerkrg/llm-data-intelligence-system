from dataclasses import dataclass


@dataclass
class ThresholdStrategy:
    """
    Estratégia baseada em limite mínimo de aprovação.
    """

    threshold: float = 0.7

    def evaluate(self, score: float) -> bool:
        """
        Retorna True quando o score
        atinge o limite definido.
        """

        return score >= self.threshold