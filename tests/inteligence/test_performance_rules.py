from src.intelligence.execution.performance.rules import (
    PerformanceRule,
    DEFAULT_PERFORMANCE_RULES,
    evaluate_rule,
)


def test_performance_rule_dataclass_creation():
    """
    Should create a performance rule.
    """

    rule = PerformanceRule(
        metric_name="execution_time_ms",
        threshold=1000,
        operator=">",
        severity="warning",
        message="Slow execution",
    )

    assert rule.metric_name == "execution_time_ms"
    assert rule.threshold == 1000
    assert rule.operator == ">"
    assert rule.severity == "warning"


def test_default_performance_rules_exist():
    """
    Should provide default performance rules.
    """

    assert len(DEFAULT_PERFORMANCE_RULES) == 3


def test_evaluate_greater_than_rule():
    """
    Should evaluate greater than operator.
    """

    rule = PerformanceRule(
        metric_name="execution_time_ms",
        threshold=1000,
        operator=">",
        severity="warning",
        message="Slow execution",
    )

    assert evaluate_rule(
        rule,
        1500,
    ) is True


def test_evaluate_greater_than_rule_false():
    """
    Should not trigger when value is below threshold.
    """

    rule = PerformanceRule(
        metric_name="execution_time_ms",
        threshold=1000,
        operator=">",
        severity="warning",
        message="Slow execution",
    )

    assert evaluate_rule(
        rule,
        500,
    ) is False


def test_evaluate_greater_equal_rule():
    """
    Should evaluate greater or equal operator.
    """

    rule = PerformanceRule(
        metric_name="error_count",
        threshold=1,
        operator=">=",
        severity="warning",
        message="Execution contains errors.",
    )

    assert evaluate_rule(
        rule,
        1,
    ) is True


def test_evaluate_unknown_operator_returns_false():
    """
    Should return false for unsupported operators.
    """

    rule = PerformanceRule(
        metric_name="execution_time_ms",
        threshold=1000,
        operator="==",
        severity="warning",
        message="Invalid operator",
    )

    assert evaluate_rule(
        rule,
        1000,
    ) is False