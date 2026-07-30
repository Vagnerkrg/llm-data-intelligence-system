from dataclasses import dataclass


@dataclass
class CapabilityMetrics:
    """
    Métricas relacionadas a capacidades cognitivas.
    
    Exemplos:
    - reasoning
    - planning
    - memory
    - reflection
    """

    capability: str

    score: float

    weight: float = 1.0


    @property
    def weighted_score(self) -> float:
        return self.score * self.weight