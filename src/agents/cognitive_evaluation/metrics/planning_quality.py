from typing import Any

from ..domain.evaluation_context import EvaluationContext
from ..domain.evaluation_metric import EvaluationMetric


class PlanningQualityMetric:
    """
    Evaluates the quality of an agent's execution plan.

    The metric considers:

    - execution steps
    - step consistency
    - dependency resolution
    - plan completeness
    """

    metric_name = "planning_quality"
    metric_category = "planning"

    def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationMetric:
        """
        Evaluate planning quality from an evaluation context.
        """

        information = context.planning_information

        if not information:
            return EvaluationMetric(
                name=self.metric_name,
                category=self.metric_category,
                score=0.0,
                description="Planning information is unavailable.",
            )

        if not isinstance(information, dict):
            return EvaluationMetric(
                name=self.metric_name,
                category=self.metric_category,
                score=0.0,
                description="Invalid planning information.",
            )

        factors = [
            self._normalize_value(information.get("execution_steps")),
            self._normalize_value(information.get("step_consistency")),
            self._normalize_value(information.get("dependency_resolution")),
            self._normalize_value(information.get("plan_completeness")),
        ]

        available = [factor for factor in factors if factor is not None]

        score = sum(available) / len(available) if available else 0.0

        return EvaluationMetric(
            name=self.metric_name,
            category=self.metric_category,
            score=score,
            metadata={
                "factors_evaluated": len(available),
                "factors_available": len(factors),
            },
            description="Planning quality evaluated.",
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
