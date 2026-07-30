from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationRecommendation:
    """
    Represents an actionable recommendation
    generated from an evaluation decision.
    """

    strategy: str

    confidence: float

    rationale: str