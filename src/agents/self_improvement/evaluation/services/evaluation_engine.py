from uuid import uuid4

from ..domain.evaluation_context import EvaluationContext
from ..domain.evaluation_result import EvaluationResult

from .quality_analyzer import QualityAnalyzer
from .signal_generator import SignalGenerator


class EvaluationEngine:
    """
    Main orchestration service for Self Evaluation.
    """

    def __init__(self) -> None:
        self._quality_analyzer = QualityAnalyzer()
        self._signal_generator = SignalGenerator()

    def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationResult:

        findings = self._quality_analyzer.analyze(
            context
        )

        signals = self._signal_generator.generate(
            findings
        )

        score = max(
            0.0,
            1.0 - (len(findings) * 0.1)
        )

        quality_level = (
            "high"
            if score >= 0.8
            else "medium"
        )

        return EvaluationResult(
            evaluation_id=str(uuid4()),
            score=score,
            quality_level=quality_level,
            findings=findings,
            signals=signals,
        )