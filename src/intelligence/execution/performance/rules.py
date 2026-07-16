from dataclasses import dataclass


@dataclass
class PerformanceRule:
    """
    Represents a performance evaluation rule.
    """

    metric_name: str
    threshold: float
    operator: str
    severity: str
    message: str


DEFAULT_PERFORMANCE_RULES = [
    PerformanceRule(
        metric_name="execution_time_ms",
        threshold=1000,
        operator=">",
        severity="warning",
        message="Execution time exceeded expected threshold.",
    ),
    PerformanceRule(
        metric_name="execution_time_ms",
        threshold=5000,
        operator=">",
        severity="critical",
        message="Execution time reached critical threshold.",
    ),
    PerformanceRule(
        metric_name="error_count",
        threshold=1,
        operator=">=",
        severity="warning",
        message="Execution contains errors.",
    ),
]


def evaluate_rule(
    rule: PerformanceRule,
    value: float,
) -> bool:
    """
    Evaluate metric value against rule.
    """

    if rule.operator == ">":
        return value > rule.threshold

    if rule.operator == ">=":
        return value >= rule.threshold

    if rule.operator == "<":
        return value < rule.threshold

    if rule.operator == "<=":
        return value <= rule.threshold

    return False