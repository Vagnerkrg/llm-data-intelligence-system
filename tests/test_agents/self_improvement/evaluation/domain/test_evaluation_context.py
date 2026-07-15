from src.agents.self_improvement.evaluation.domain.evaluation_context import (
    EvaluationContext,
)


def test_evaluation_context_creation():

    context = EvaluationContext(
        execution_id="exec-001",
        goal="Analyze customer data",
        expected_result="Report",
        actual_result="Generated report",
    )

    assert context.execution_id == "exec-001"
    assert context.goal == "Analyze customer data"
    assert context.expected_result == "Report"
    assert context.actual_result == "Generated report"


def test_evaluation_context_default_values():

    context = EvaluationContext(
        execution_id="exec-002",
        goal="Test",
        expected_result=True,
        actual_result=True,
    )

    assert context.execution_metrics == {}
    assert context.decisions == []
    assert context.tools_used == []