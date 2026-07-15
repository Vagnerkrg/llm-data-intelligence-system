from src.intelligence.execution.models import ExecutionMetric

from src.intelligence.execution.performance.analyzer import (
    PerformanceAnalyzer,
    PerformanceInsight,
)


def test_performance_analyzer_detects_warning():
    """
    Should detect warning when execution time
    exceeds configured threshold.
    """

    analyzer = PerformanceAnalyzer()

    metrics = [
        ExecutionMetric(
            metric_name="execution_time_ms",
            metric_value=1500,
        )
    ]

    insights = analyzer.analyze(metrics)

    assert len(insights) == 1

    insight = insights[0]

    assert isinstance(
        insight,
        PerformanceInsight,
    )

    assert insight.metric_name == "execution_time_ms"
    assert insight.value == 1500
    assert insight.severity == "warning"


def test_performance_analyzer_detects_critical():
    """
    Should detect critical performance issue.
    """

    analyzer = PerformanceAnalyzer()

    metrics = [
        ExecutionMetric(
            metric_name="execution_time_ms",
            metric_value=6000,
        )
    ]

    insights = analyzer.analyze(metrics)

    assert len(insights) == 1

    assert insights[0].severity == "critical"


def test_performance_analyzer_ignores_normal_execution():
    """
    Should not generate insights for healthy metrics.
    """

    analyzer = PerformanceAnalyzer()

    metrics = [
        ExecutionMetric(
            metric_name="execution_time_ms",
            metric_value=200,
        )
    ]

    insights = analyzer.analyze(metrics)

    assert insights == []


def test_performance_analyzer_detects_error_metric():
    """
    Should detect execution errors.
    """

    analyzer = PerformanceAnalyzer()

    metrics = [
        ExecutionMetric(
            metric_name="error_count",
            metric_value=2,
        )
    ]

    insights = analyzer.analyze(metrics)

    assert len(insights) == 1

    insight = insights[0]

    assert insight.metric_name == "error_count"
    assert insight.severity == "warning"


def test_performance_analyzer_multiple_insights():
    """
    Should generate multiple insights
    from different metrics.
    """

    analyzer = PerformanceAnalyzer()

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

    insights = analyzer.analyze(metrics)

    assert len(insights) == 2

    metric_names = {
        insight.metric_name
        for insight in insights
    }

    assert "execution_time_ms" in metric_names
    assert "error_count" in metric_names