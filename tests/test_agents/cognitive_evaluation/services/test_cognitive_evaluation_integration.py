from src.agents.cognitive_evaluation.domain.evaluation_result import (
    EvaluationResult,
)
from src.agents.cognitive_evaluation.services.cognitive_evaluation_adapter import (
    CognitiveEvaluationAdapter,
)
from src.agents.cognitive_evaluation.services.cognitive_evaluator import (
    CognitiveEvaluator,
)
from src.agents.runtime.agent_runtime import AgentRuntime


def test_should_evaluate_completed_agent_execution():
    runtime = AgentRuntime()

    execution_context = runtime.execute("Quantos clientes existem?")

    adapter = CognitiveEvaluationAdapter()

    evaluation_context = adapter.adapt(execution_context)

    evaluator = CognitiveEvaluator()

    result = evaluator.evaluate(evaluation_context)

    assert isinstance(
        result,
        EvaluationResult,
    )

    assert result.status == "completed"

    assert len(result.metrics) == 5

    assert 0.0 <= result.overall_score <= 1.0


def test_should_produce_deterministic_cognitive_evaluation():
    runtime = AgentRuntime()

    execution_context = runtime.execute("Analise os dados dos clientes.")

    adapter = CognitiveEvaluationAdapter()

    evaluator = CognitiveEvaluator()

    first_context = adapter.adapt(execution_context)

    second_context = adapter.adapt(execution_context)

    first_result = evaluator.evaluate(first_context)

    second_result = evaluator.evaluate(second_context)

    assert first_result.overall_score == second_result.overall_score

    assert [metric.score for metric in first_result.metrics] == [
        metric.score for metric in second_result.metrics
    ]
