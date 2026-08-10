from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.domain.evaluation_result import (
    EvaluationResult,
)
from src.agents.cognitive_evaluation.services.cognitive_evaluator import (
    CognitiveEvaluator,
)


def test_should_evaluate_all_cognitive_metrics():
    evaluator = CognitiveEvaluator()

    context = EvaluationContext(
        execution_result={
            "execution_status": "completed",
            "completed_steps": 1.0,
            "failed_steps": 0.0,
            "execution_efficiency": 1.0,
        },
        reasoning_information={
            "completeness": 1.0,
            "confidence": 1.0,
            "strategy": 1.0,
            "conclusion_quality": 1.0,
        },
        planning_information={
            "execution_steps": 1.0,
            "step_consistency": 1.0,
            "dependency_resolution": 1.0,
            "plan_completeness": 1.0,
        },
        memory_information={
            "memory_usage": 1.0,
            "relevance_score": 1.0,
            "retrieved_context_quality": 1.0,
            "memory_contribution": 1.0,
        },
    )

    result = evaluator.evaluate(context)

    assert isinstance(result, EvaluationResult)
    assert result.status == "completed"
    assert len(result.metrics) == 5
    assert result.overall_score == 1.0


def test_should_return_zero_when_all_information_is_missing():
    evaluator = CognitiveEvaluator()

    context = EvaluationContext()

    result = evaluator.evaluate(context)

    assert isinstance(result, EvaluationResult)
    assert result.status == "completed"
    assert result.overall_score == 0.0
    assert len(result.metrics) == 5


def test_should_include_individual_metric_breakdown():
    evaluator = CognitiveEvaluator()

    context = EvaluationContext(
        reasoning_information={
            "completeness": 1.0,
        }
    )

    result = evaluator.evaluate(context)

    metric_names = [
        metric.name
        for metric in result.metrics
    ]

    assert "reasoning_quality" in metric_names
    assert "planning_quality" in metric_names
    assert "execution_quality" in metric_names
    assert "memory_effectiveness" in metric_names
    assert "cognitive_score" in metric_names


def test_should_produce_deterministic_evaluation():
    evaluator = CognitiveEvaluator()

    context = EvaluationContext(
        reasoning_information={
            "completeness": 0.8,
            "confidence": 0.7,
        },
        planning_information={
            "execution_steps": 0.9,
            "plan_completeness": 0.8,
        },
    )

    first_result = evaluator.evaluate(context)
    second_result = evaluator.evaluate(context)

    assert (
        first_result.overall_score
        == second_result.overall_score
    )

    assert [
        metric.score
        for metric in first_result.metrics
    ] == [
        metric.score
        for metric in second_result.metrics
    ]