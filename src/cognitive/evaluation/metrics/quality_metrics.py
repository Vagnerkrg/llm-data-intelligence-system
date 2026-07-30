from dataclasses import dataclass


@dataclass
class QualityMetrics:
    """
    Métricas de qualidade das avaliações cognitivas.
    """

    evaluator: str

    quality_score: float

    threshold: float = 0.80


    def is_high_quality(self) -> bool:
        return self.quality_score >= self.threshold