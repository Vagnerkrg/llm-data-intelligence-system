from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.services.cognitive_evaluation_adapter import (
    CognitiveEvaluationAdapter,
)
from src.agents.runtime.execution_context import ExecutionContext


def test_should_adapt_execution_context_to_evaluation_context():
    adapter = CognitiveEvaluationAdapter()

    execution_context = ExecutionContext(
        question="Analyze customer data"
    )

    execution_context.status = "completed"

    result = adapter.adapt(execution_context)

    assert isinstance(result, EvaluationContext)

    assert result.execution_result is not None


def test_should_preserve_execution_status():
    adapter = CognitiveEvaluationAdapter()

    execution_context = ExecutionContext(
        question="Test execution"
    )

    execution_context.status = "completed"

    result = adapter.adapt(execution_context)

    assert result.execution_result["execution_status"] == (
        "completed"
    )


def test_should_adapt_reasoning_information():
    adapter = CognitiveEvaluationAdapter()

    execution_context = ExecutionContext(
        question="Analyze products"
    )

    execution_context.reasoning = {
        "completeness": 1.0,
        "confidence": 0.9,
        "strategy": 1.0,
        "conclusion_quality": 0.8,
    }

    result = adapter.adapt(execution_context)

    assert result.reasoning_information == {
        "completeness": 1.0,
        "confidence": 0.9,
        "strategy": 1.0,
        "conclusion_quality": 0.8,
    }


def test_should_adapt_memory_context():
    adapter = CognitiveEvaluationAdapter()

    execution_context = ExecutionContext(
        question="Use previous customer information"
    )

    execution_context.memory_context = {
        "memory_usage": 1.0,
        "relevance_score": 0.9,
        "retrieved_context_quality": 0.8,
        "memory_contribution": 0.7,
    }

    result = adapter.adapt(execution_context)

    assert result.memory_information == {
        "memory_usage": 1.0,
        "relevance_score": 0.9,
        "retrieved_context_quality": 0.8,
        "memory_contribution": 0.7,
    }


def test_should_preserve_execution_question_in_metadata():
    adapter = CognitiveEvaluationAdapter()

    execution_context = ExecutionContext(
        question="How many customers exist?"
    )

    result = adapter.adapt(execution_context)

    assert result.metadata["question"] == (
        "How many customers exist?"
    )


def test_should_adapt_completed_steps():
    adapter = CognitiveEvaluationAdapter()

    execution_context = ExecutionContext(
        question="Execute analysis"
    )

    execution_context.results = [
        {"result": "step 1"},
        {"result": "step 2"},
    ]

    result = adapter.adapt(execution_context)

    assert result.execution_result["completed_steps"] == 2.0


def test_should_return_valid_evaluation_context_when_information_is_missing():
    adapter = CognitiveEvaluationAdapter()

    execution_context = ExecutionContext(
        question="Simple question"
    )

    result = adapter.adapt(execution_context)

    assert isinstance(result, EvaluationContext)

    assert result.execution_result is not None


def test_should_adapt_cognitive_improvement_information():
    adapter = CognitiveEvaluationAdapter()

    execution_context = ExecutionContext(
        question="Improve execution"
    )

    execution_context.cognitive_improvement = {
        "improvement_score": 0.8,
        "improvements": [
            "better planning",
        ],
    }

    result = adapter.adapt(execution_context)

    assert result.improvement_information == {
        "improvement_score": 0.8,
        "improvements": [
            "better planning",
        ],
    }