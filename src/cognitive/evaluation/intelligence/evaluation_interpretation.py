from dataclasses import dataclass, field


@dataclass(frozen=True)
class EvaluationInterpretation:
    """
    Cognitive interpretation of evaluation results.
    """

    severity: str

    requires_improvement: bool

    areas: list[str] = field(
        default_factory=list
    )