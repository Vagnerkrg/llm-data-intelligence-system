from typing import Any

from ..domain.evaluation_metric import EvaluationMetric
from ..domain.evaluation_context import EvaluationContext


class ReasoningQualityMetric:
    """
    Evaluates the quality of an agent's reasoning process.

    The metric considers:

    - reasoning completeness
    - confidence level
    - strategy definition
    - conclusion quality

    The calculation is deterministic and independent
    from the runtime layer.
    """

    metric_name = "reasoning_quality"
    metric_category = "reasoning"

    def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationMetric:
        """
        Evaluate reasoning quality from an evaluation context.
        """

        information = context.reasoning_information

        if not information:
            return EvaluationMetric(
                name=self.metric_name,
                category=self.metric_category,
                score=0.0,
                description="Reasoning information is unavailable.",
            )

        if not isinstance(information, dict):
            return EvaluationMetric(
                name=self.metric_name,
                category=self.metric_category,
                score=0.0,
                description="Invalid reasoning information.",
            )

        factors = [
            self._normalize_value(
                information.get("completeness")
            ),
            self._normalize_value(
                information.get("confidence")
            ),
            self._normalize_value(
                information.get("strategy")
            ),
            self._normalize_value(
                information.get("conclusion_quality")
            ),
        ]

        available = [
            factor for factor in factors
            if factor is not None
        ]

        score = (
            sum(available) / len(available)
            if available
            else 0.0
        )

        return EvaluationMetric(
            name=self.metric_name,
            category=self.metric_category,
            score=score,
            metadata={
                "factors_evaluated": len(available),
                "factors_available": len(factors),
            },
            description="Reasoning quality evaluated.",
        )

    @staticmethod
    def _normalize_value(value: Any) -> float | None:
        """
        Normalize a metric component to the [0.0, 1.0] range.
        """

        if value is None:
            return None

        if isinstance(value, bool):
            return float(value)

        if isinstance(value, (int, float)):
            return max(0.0, min(1.0, float(value)))

        return None