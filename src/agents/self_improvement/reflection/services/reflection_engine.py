"""Reflection engine."""

from ..contracts import ReflectionRequest
from ..domain import ReflectionSummary
from .hypothesis_builder import HypothesisBuilder
from .insight_generator import InsightGenerator
from .pattern_analyzer import PatternAnalyzer
from .reflection_validator import ReflectionValidator


class ReflectionEngine:
    """Core reflection engine."""

    def __init__(
        self,
        analyzer: PatternAnalyzer | None = None,
        hypothesis_builder: HypothesisBuilder | None = None,
        insight_generator: InsightGenerator | None = None,
        validator: ReflectionValidator | None = None,
    ) -> None:
        self._analyzer = analyzer or PatternAnalyzer()
        self._hypothesis_builder = (
            hypothesis_builder or HypothesisBuilder()
        )
        self._insight_generator = (
            insight_generator or InsightGenerator()
        )
        self._validator = validator or ReflectionValidator()

    def reflect(
        self,
        request: ReflectionRequest,
    ) -> ReflectionSummary:
        """Execute a reflection cycle."""

        findings = self._analyzer.analyze(request.context)

        hypotheses = self._hypothesis_builder.build(findings)

        insights = self._insight_generator.generate(hypotheses)

        summary = ReflectionSummary(
            findings=findings,
            hypotheses=hypotheses,
            insights=insights,
            conclusion="Reflection completed successfully.",
            confidence=1.0 if findings else 0.0,
        )

        if not self._validator.validate(summary):
            raise ValueError("Invalid reflection summary.")

        return summary