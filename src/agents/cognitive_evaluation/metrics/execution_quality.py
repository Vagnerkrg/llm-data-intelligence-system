from typing import Any

from ..domain.evaluation_context import EvaluationContext
from ..domain.evaluation_metric import EvaluationMetric


class ExecutionQualityMetric:
    """
    Evaluates the quality of agent execution.

    The metric considers:

    - execution status
    - completed steps
    - failed steps
    - execution efficiency
    """

    metric_name = "execution_quality"
    metric_category = "execution"

    def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationMetric:
        """
        Evaluate execution quality from an evaluation context.
        """

        information = context.execution_result

        if not information:
            return EvaluationMetric(
                name=self.metric_name,
                category=self.metric_category,
                score=0.0,
                description="Execution information is unavailable.",
            )

        if not isinstance(information, dict):
            return EvaluationMetric(
                name=self.metric_name,
                category=self.metric_category,
                score=0.0,
                description="Invalid execution information.",
            )

        status_score = self._status_score(information.get("execution_status"))

        completed_score = self._normalize_value(information.get("completed_steps"))

        failed_steps = information.get("failed_steps")

        failed_score = (
            1.0 - self._normalize_value(failed_steps)
            if self._normalize_value(failed_steps) is not None
            else None
        )

        efficiency_score = self._normalize_value(
            information.get("execution_efficiency")
        )

        factors = [
            status_score,
            completed_score,
            failed_score,
            efficiency_score,
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
            description="Execution quality evaluated.",
        )

    @staticmethod
    def _status_score(status: Any) -> float | None:
        """
        Convert execution status into a normalized score.
        """

        if status is None:
            return None

        if isinstance(status, bool):
            return float(status)

        if isinstance(status, (int, float)):
            return max(0.0, min(1.0, float(status)))

        if isinstance(status, str):
            normalized = status.strip().lower()

            if normalized in {
                "completed",
                "success",
                "successful",
                "succeeded",
            }:
                return 1.0

            if normalized in {
                "partial",
                "partially_completed",
                "in_progress",
            }:
                return 0.5

            if normalized in {
                "failed",
                "error",
                "cancelled",
                "canceled",
            }:
                return 0.0

        return None

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
