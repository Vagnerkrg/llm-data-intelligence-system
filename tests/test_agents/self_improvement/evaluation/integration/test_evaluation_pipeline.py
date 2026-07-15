from src.agents.self_improvement.evaluation.domain.evaluation_context import (
    EvaluationContext,
)

from src.agents.self_improvement.evaluation.domain.evaluation_result import (
    EvaluationResult,
)

from src.agents.self_improvement.evaluation.services.evaluation_engine import (
    EvaluationEngine,
)


def test_evaluation_pipeline_complete_flow():

    context = EvaluationContext(
        execution_id="exec-integration-001",
        goal="Analyze customer behavior",
        expected_result="Customer insights report",
        actual_result="Customer insights report",
        tools_used=[
            "analytics_tool",
            "rag_tool",
        ],
    )

    engine = EvaluationEngine()

    result = engine.evaluate(context)

    assert isinstance(result, EvaluationResult)

    assert result.evaluation_id is not None

    assert result.score >= 0

    assert result.findings == []


def test_evaluation_pipeline_generates_learning_feedback():

    context = EvaluationContext(
        execution_id="exec-integration-002",
        goal="Perform complex analysis",
        expected_result="Optimized analysis",
        actual_result="Optimized analysis",
        tools_used=[
            "tool_a",
            "tool_b",
            "tool_c",
            "tool_d",
            "tool_e",
            "tool_f",
        ],
    )

    engine = EvaluationEngine()

    result = engine.evaluate(context)

    assert isinstance(result, EvaluationResult)

    assert len(result.signals) > 0

    signal = result.signals[0]

    assert signal.signal_type is not None

    assert signal.pattern is not None