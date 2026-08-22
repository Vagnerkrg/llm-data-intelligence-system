from src.agents.autonomous_evolution.domain import (
    EvolutionContext,
    EvolutionDecision,
    EvolutionResult,
    ExperienceOptimizationContext,
)


def test_autonomous_evolution_domain_accepts_generic_external_information() -> None:
    evaluation = object()
    memory = object()
    learning = object()
    knowledge = object()

    context = EvolutionContext(
        evaluation_information=evaluation,
        memory_information=memory,
        learning_information=learning,
        knowledge_information=knowledge,
    )

    assert context.evaluation_information is evaluation
    assert context.memory_information is memory
    assert context.learning_information is learning
    assert context.knowledge_information is knowledge


def test_experience_optimization_context_is_independent_from_runtime() -> None:
    context = ExperienceOptimizationContext(
        execution_history=[{"score": 0.90}],
        cognitive_evaluations=[{"overall_score": 0.85}],
    )

    assert context.execution_history[0]["score"] == 0.90
    assert context.cognitive_evaluations[0]["overall_score"] == 0.85


def test_domain_objects_do_not_execute_external_behavior() -> None:
    decision = EvolutionDecision()
    result = EvolutionResult()

    assert decision.should_evolve is False
    assert result.success is False
