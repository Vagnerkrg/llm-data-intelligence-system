from src.agents.self_improvement.evaluation.domain.evaluation_context import (
    EvaluationContext,
)

from src.agents.self_improvement.evaluation.domain.evaluation_result import (
    EvaluationResult,
)

from src.agents.self_improvement.evaluation.services.evaluation_engine import (
    EvaluationEngine,
)


def test_evaluation_engine_generates_result():

    context = EvaluationContext(
        execution_id="exec-001",
        goal="Analyze customer dataset",
        expected_result="Analysis report",
        actual_result="Analysis report",
    )

    engine = EvaluationEngine()

    result = engine.evaluate(context)

    assert isinstance(result, EvaluationResult)

    assert result.score >= 0

    assert result.evaluation_id is not None


def test_evaluation_engine_generates_learning_signals():

    context = EvaluationContext(
        execution_id="exec-002",
        goal="Complex analysis",
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

    engine = EvaluationEngine()

    result = engine.evaluate(context)

    assert isinstance(result, EvaluationResult)

    assert len(result.signals) > 0