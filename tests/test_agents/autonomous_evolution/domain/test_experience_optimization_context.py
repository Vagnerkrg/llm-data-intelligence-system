from src.agents.autonomous_evolution.domain import (
    ExperienceOptimizationContext,
)


def test_context_creation() -> None:
    context = ExperienceOptimizationContext(
        execution_history=[
            {"score": 0.9},
            {"score": 0.8},
        ],
        cognitive_evaluations=[
            {"overall_score": 0.85},
        ],
        learning_outcomes=[
            {"result": "improvement"},
        ],
        evolution_decisions=[
            {"should_evolve": True},
        ],
    )

    assert len(context.execution_history) == 2
    assert len(context.cognitive_evaluations) == 1
    assert len(context.learning_outcomes) == 1
    assert len(context.evolution_decisions) == 1


def test_context_serialization() -> None:
    context = ExperienceOptimizationContext(
        execution_history=[
            {"score": 0.9},
        ],
        metadata={
            "source": "test",
        },
    )

    data = context.to_dict()

    assert data["execution_history"] == [
        {"score": 0.9},
    ]
    assert data["metadata"]["source"] == "test"