from src.intelligence.execution.models import ExecutionMetric

from src.intelligence.execution.performance.evaluator import (
    PerformanceRuleEvaluator,
)


def test_performance_rule_evaluator_detects_warning():
    """
    Should detect warning based on performance rules.
    """

    evaluator = PerformanceRuleEvaluator()

    metrics = [
        ExecutionMetric(
            metric_name="execution_time_ms",
            metric_value=1500,
        )
    ]

    insights = evaluator.evaluate(
        metrics
    )

    assert len(insights) == 1

    insight = insights[0]

    assert insight.metric_name == "execution_time_ms"
    assert insight.value == 1500
    assert insight.severity == "warning"


def test_performance_rule_evaluator_detects_critical():
    """
    Should detect critical performance issues.
    """

    evaluator = PerformanceRuleEvaluator()

    metrics = [
        ExecutionMetric(
            metric_name="execution_time_ms",
            metric_value=6000,
        )
    ]

    insights = evaluator.evaluate(
        metrics
    )

    assert len(insights) == 1

    assert insights[0].severity == "critical"


def test_performance_rule_evaluator_detects_error():
    """
    Should detect execution errors.
    """

    evaluator = PerformanceRuleEvaluator()

    metrics = [
        ExecutionMetric(
            metric_name="error_count",
            metric_value=2,
        )
    ]

    insights = evaluator.evaluate(
        metrics
    )

    assert len(insights) == 1

    insight = insights[0]

    assert insight.metric_name == "error_count"
    assert insight.severity == "warning"


def test_performance_rule_evaluator_ignores_unknown_metrics():
    """
    Should ignore metrics without matching rules.
    """

    evaluator = PerformanceRuleEvaluator()

    metrics = [
        ExecutionMetric(
            metric_name="memory_usage",
            metric_value=500,
        )
    ]

    insights = evaluator.evaluate(
        metrics
    )

    assert insights == []


def test_performance_rule_evaluator_multiple_metrics():
    """
    Should generate insights from multiple metrics.
    """

    evaluator = PerformanceRuleEvaluator()

    metrics = [
        ExecutionMetric(
            metric_name="execution_time_ms",
            metric_value=6000,
        ),
        ExecutionMetric(
            metric_name="error_count",
            metric_value=3,
        ),
    ]

    insights = evaluator.evaluate(
        metrics
    )

    assert len(insights) == 2

    metric_names = {
        insight.metric_name
        for insight in insights
    }

    assert "execution_time_ms" in metric_names
    assert "error_count" in metric_names