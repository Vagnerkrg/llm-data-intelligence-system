from dataclasses import dataclass

from src.intelligence.execution.models import ExecutionMetric

from .rules import (
    DEFAULT_PERFORMANCE_RULES,
    PerformanceRule,
    evaluate_rule,
)


@dataclass
class PerformanceEvaluationResult:
    """
    Represents the result of a performance rule evaluation.
    """

    metric_name: str
    value: float | int
    severity: str
    message: str


class PerformanceRuleEvaluator:
    """
    Evaluates execution metrics against performance rules.
    """

    SEVERITY_PRIORITY = {
        "critical": 2,
        "warning": 1,
        "info": 0,
    }

    def __init__(
        self,
        rules: list[PerformanceRule] | None = None,
    ):
        self.rules = (
            rules
            if rules is not None
            else DEFAULT_PERFORMANCE_RULES
        )

    def evaluate(
        self,
        metrics: list[ExecutionMetric],
    ) -> list[PerformanceEvaluationResult]:
        """
        Evaluate metrics and generate performance findings.
        """

        results: list[PerformanceEvaluationResult] = []

        for metric in metrics:

            matched_rules = []

            for rule in self.rules:

                if rule.metric_name != metric.metric_name:
                    continue

                if evaluate_rule(
                    rule,
                    metric.metric_value,
                ):
                    matched_rules.append(rule)

            if not matched_rules:
                continue

            selected_rule = max(
                matched_rules,
                key=lambda rule: self.SEVERITY_PRIORITY.get(
                    rule.severity,
                    0,
                ),
            )

            results.append(
                PerformanceEvaluationResult(
                    metric_name=metric.metric_name,
                    value=metric.metric_value,
                    severity=selected_rule.severity,
                    message=selected_rule.message,
                )
            )

        return results