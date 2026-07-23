from dataclasses import dataclass


@dataclass
class CapabilityEvaluation:
    """
    Representa a avaliação de uma capacidade cognitiva.

    Exemplos:
    - reasoning
    - planning
    - memory
    - tools
    """

    capability: str

    score: float

    weight: float = 1.0

    description: str = ""

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight