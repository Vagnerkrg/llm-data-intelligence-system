from dataclasses import dataclass

from src.intelligence.execution.models import ExecutionMetric

from .rules import (
    DEFAULT_PERFORMANCE_RULES,
    evaluate_rule,
)


@dataclass
class PerformanceInsight:
    """
    Represents a detected performance insight.
    """

    metric_name: str
    value: float
    severity: str
    message: str


class PerformanceAnalyzer:
    """
    Analyzes execution metrics and generates
    performance intelligence insights.
    """

    SEVERITY_PRIORITY = {
        "critical": 3,
        "warning": 2,
        "info": 1,
    }

    def __init__(
        self,
        rules=None,
    ):
        self.rules = (
            rules
            if rules is not None
            else DEFAULT_PERFORMANCE_RULES
        )

    def analyze(
        self,
        metrics: list[ExecutionMetric],
    ) -> list[PerformanceInsight]:
        """
        Analyze execution metrics.

        Returns only the highest severity
        insight per metric.
        """

        insights = []

        for metric in metrics:

            matching_insights = []

            for rule in self.rules:

                if rule.metric_name != metric.metric_name:
                    continue

                if evaluate_rule(
                    rule,
                    metric.metric_value,
                ):
                    matching_insights.append(
                        PerformanceInsight(
                            metric_name=metric.metric_name,
                            value=metric.metric_value,
                            severity=rule.severity,
                            message=rule.message,
                        )
                    )

            if matching_insights:

                best_insight = max(
                    matching_insights,
                    key=lambda insight:
                    self.SEVERITY_PRIORITY.get(
                        insight.severity,
                        0,
                    ),
                )

                insights.append(best_insight)

        return insights