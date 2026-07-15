from src.agents.self_improvement.evaluation.domain.evaluation_context import (
    EvaluationContext,
)

from src.agents.self_improvement.evaluation.services.quality_analyzer import (
    QualityAnalyzer,
)


def test_quality_analyzer_detects_no_issues():

    context = EvaluationContext(
        execution_id="exec-001",
        goal="Analyze dataset",
        expected_result="Report",
        actual_result="Report",
    )

    analyzer = QualityAnalyzer()

    findings = analyzer.analyze(context)

    assert findings == []


def test_quality_analyzer_detects_execution_complexity():

    context = EvaluationContext(
        execution_id="exec-002",
        goal="Analyze dataset",
        expected_result="Report",
        actual_result="Report",
        tools_used=[
            "tool_a",
            "tool_b",
            "tool_c",
            "tool_d",
            "tool_e",
            "tool_f",
        ],
    )

    analyzer = QualityAnalyzer()

    findings = analyzer.analyze(context)

    assert len(findings) > 0