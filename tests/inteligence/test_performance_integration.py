from src.intelligence.execution.models import ExecutionMetric

from src.intelligence.execution.performance.evaluator import (
    PerformanceRuleEvaluator,
)

from src.intelligence.execution.performance.analyzer import (
    PerformanceAnalyzer,
)


def test_performance_monitoring_flow():
    """
    Should evaluate metrics and generate performance insights.
    """

    metrics = [
        ExecutionMetric(
            metric_name="execution_time_ms",
            metric_value=6000,
        ),
        ExecutionMetric(
            metric_name="error_count",
            metric_value=2,
        ),
    ]

    evaluator = PerformanceRuleEvaluator()

    evaluation_results = evaluator.evaluate(
        metrics
    )

    analyzer = PerformanceAnalyzer()

    insights = analyzer.analyze(
        metrics
    )

    assert len(evaluation_results) == 2

    assert len(insights) == 2

    assert any(
        result.severity == "critical"
        for result in evaluation_results
    )

    assert any(
        insight.metric_name == "error_count"
        for insight in insights
    )