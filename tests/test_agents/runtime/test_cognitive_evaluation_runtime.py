from src.agents.runtime.agent_runtime import AgentRuntime
from src.agents.cognitive_evaluation.domain.evaluation_result import (
    EvaluationResult,
)


def test_agent_runtime_stores_cognitive_evaluation():
    runtime = AgentRuntime()

    context = runtime.execute(
        "How many products exist?"
    )

    assert context.cognitive_evaluation is not None

    assert isinstance(
        context.cognitive_evaluation,
        EvaluationResult,
    )


def test_agent_runtime_cognitive_evaluation_is_completed():
    runtime = AgentRuntime()

    context = runtime.execute(
        "Analyze products"
    )

    assert (
        context.cognitive_evaluation.status
        == "completed"
    )


def test_agent_runtime_cognitive_evaluation_contains_metrics():
    runtime = AgentRuntime()

    context = runtime.execute(
        "Analyze products"
    )

    metrics = context.cognitive_evaluation.metrics

    metric_names = [
        metric.name
        for metric in metrics
    ]

    assert "reasoning_quality" in metric_names
    assert "planning_quality" in metric_names
    assert "execution_quality" in metric_names
    assert "memory_effectiveness" in metric_names
    assert "cognitive_score" in metric_names


def test_agent_runtime_cognitive_evaluation_is_deterministic():
    runtime = AgentRuntime()

    first_context = runtime.execute(
        "Analyze products"
    )

    second_context = runtime.execute(
        "Analyze products"
    )

    assert (
        first_context.cognitive_evaluation.overall_score
        == second_context.cognitive_evaluation.overall_score
    )