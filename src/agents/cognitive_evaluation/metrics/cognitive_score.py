from collections.abc import Iterable

from ..domain.evaluation_metric import EvaluationMetric


class CognitiveScoreCalculator:
    """
    Aggregates individual cognitive metrics into
    a consolidated cognitive score.

    The initial strategy uses an arithmetic mean
    and does not apply arbitrary weights.
    """

    metric_name = "cognitive_score"
    metric_category = "cognitive"

    def calculate(
        self,
        metrics: Iterable[EvaluationMetric],
    ) -> EvaluationMetric:
        """
        Calculate the consolidated cognitive score.
        """

        metrics_list = list(metrics)

        if not metrics_list:
            return EvaluationMetric(
                name=self.metric_name,
                category=self.metric_category,
                score=0.0,
                metadata={
                    "metrics_evaluated": 0,
                },
                description="No cognitive metrics available.",
            )

        invalid_metrics = [
            metric
            for metric in metrics_list
            if not isinstance(metric, EvaluationMetric)
        ]

        if invalid_metrics:
            raise TypeError(
                "All metrics must be EvaluationMetric instances."
            )

        score = sum(
            metric.score
            for metric in metrics_list
        ) / len(metrics_list)

        return EvaluationMetric(
            name=self.metric_name,
            category=self.metric_category,
            score=score,
            metadata={
                "metrics_evaluated": len(metrics_list),
                "metric_names": [
                    metric.name
                    for metric in metrics_list
                ],
            },
            description="Consolidated cognitive score calculated.",
        )