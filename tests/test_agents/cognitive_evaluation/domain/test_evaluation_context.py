from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)


def test_should_create_evaluation_context():
    context = EvaluationContext(
        execution_result="execution result",
        reasoning_information="reasoning information",
        planning_information="planning information",
        memory_information="memory information",
        improvement_information="improvement information",
    )

    assert context.execution_result == "execution result"
    assert context.reasoning_information == "reasoning information"
    assert context.planning_information == "planning information"
    assert context.memory_information == "memory information"
    assert context.improvement_information == "improvement information"
    assert context.metadata == {}


def test_should_use_default_values():
    context = EvaluationContext()

    assert context.execution_result is None
    assert context.reasoning_information is None
    assert context.planning_information is None
    assert context.memory_information is None
    assert context.improvement_information is None
    assert context.metadata == {}


def test_should_serialize_context():
    context = EvaluationContext(
        execution_result={"success": True},
        reasoning_information={"confidence": 0.9},
        planning_information={"steps": 3},
        memory_information={"relevant": True},
        improvement_information={"suggestions": 2},
        metadata={"agent_id": "agent-001"},
    )

    data = context.to_dict()

    assert data == {
        "execution_result": {"success": True},
        "reasoning_information": {"confidence": 0.9},
        "planning_information": {"steps": 3},
        "memory_information": {"relevant": True},
        "improvement_information": {"suggestions": 2},
        "metadata": {"agent_id": "agent-001"},
    }
