from src.agents.autonomous_evolution.domain import EvolutionContext


def test_evolution_context_creation() -> None:
    context = EvolutionContext(
        execution_information={"execution_id": "exec-001"},
        evaluation_information={"score": 0.8},
        learning_information={"signal": "improvement"},
        knowledge_information={"source": "knowledge-base"},
        memory_information={"history": []},
    )

    assert context.execution_information["execution_id"] == "exec-001"
    assert context.evaluation_information["score"] == 0.8
    assert context.learning_information["signal"] == "improvement"


def test_evolution_context_defaults_are_independent() -> None:
    first = EvolutionContext()
    second = EvolutionContext()

    first.metadata["source"] = "test"

    assert second.metadata == {}


def test_evolution_context_serialization() -> None:
    context = EvolutionContext(
        execution_information={"id": "exec-001"},
        metadata={"environment": "test"},
    )

    result = context.to_dict()

    assert result["execution_information"] == {"id": "exec-001"}
    assert result["metadata"] == {"environment": "test"}