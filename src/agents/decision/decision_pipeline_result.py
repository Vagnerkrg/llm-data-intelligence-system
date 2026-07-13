from dataclasses import dataclass


@dataclass(slots=True)
class DecisionPipelineResult:
    """
    Represents the final output of the Decision Intelligence Pipeline.

    Contains the selected decision information,
    confidence level and explanation.
    """

    decision_id: str
    confidence: float
    explanation: str