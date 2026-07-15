from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationFinding:
    """
    Represents an observation identified
    during self evaluation.
    """

    category: str

    severity: str

    description: str