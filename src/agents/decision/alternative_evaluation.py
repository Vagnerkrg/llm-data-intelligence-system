from dataclasses import dataclass, field


@dataclass(slots=True)
class AlternativeEvaluation:
    """
    Represents the evaluation of a decision alternative
    before the final decision selection.
    """

    alternative_id: str
    score: float
    confidence: float
    risk_level: str
    evaluation_reason: str

    metadata: dict[str, str] = field(
        default_factory=dict
    )