from ..domain.evaluation_finding import EvaluationFinding
from ..domain.learning_signal import LearningSignal


class SignalGenerator:
    """
    Generates learning signals from findings.
    """

    def generate(
        self,
        findings: list[EvaluationFinding],
    ) -> list[LearningSignal]:

        signals: list[LearningSignal] = []

        for finding in findings:
            signals.append(
                LearningSignal(
                    signal_type=finding.category,
                    pattern=finding.description,
                    confidence=0.7,
                    impact=finding.severity,
                    recommendation=(
                        "Review execution strategy."
                    ),
                )
            )

        return signals