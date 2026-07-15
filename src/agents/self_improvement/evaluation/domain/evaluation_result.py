from dataclasses import dataclass, field

from .evaluation_finding import EvaluationFinding
from .learning_signal import LearningSignal


@dataclass(frozen=True)
class EvaluationResult:
    """
    Final result produced by Self Evaluation.
    """

    evaluation_id: str

    score: float

    quality_level: str

    findings: list[EvaluationFinding] = field(
        default_factory=list
    )

    signals: list[LearningSignal] = field(
        default_factory=list
    )