from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationDecision:
    """
    Represents a cognitive action decision.
    """

    action: str

    priority: str

    target: str