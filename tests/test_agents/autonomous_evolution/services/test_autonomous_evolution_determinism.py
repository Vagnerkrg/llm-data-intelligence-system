from src.agents.autonomous_evolution.domain import (
    ExperienceOptimizationContext,
    EvolutionContext,
)
from src.agents.autonomous_evolution.services import (
    EvolutionDecisionEngine,
    ExperienceDrivenOptimizer,
)


def test_evolution_decision_is_deterministic() -> None:
    engine = EvolutionDecisionEngine()

    context = EvolutionContext(
        evaluation_information={
            "overall_score": 0.90,
            "confidence": 0.90,
        },
        learning_information={
            "score": 0.85,
            "confidence": 0.85,
        },
    )

    first = engine.decide(context)
    second = engine.decide(context)

    assert first.to_dict() == second.to_dict()


def test_experience_optimization_is_deterministic() -> None:
    optimizer = ExperienceDrivenOptimizer()

    context = ExperienceOptimizationContext(
        execution_history=[
            {
                "score": 0.90,
                "confidence": 0.90,
                "strategy": "direct_execution",
            },
            {
                "score": 0.85,
                "confidence": 0.85,
                "strategy": "direct_execution",
            },
            {
                "score": 0.88,
                "confidence": 0.90,
                "strategy": "direct_execution",
            },
        ]
    )

    first = [signal.to_dict() for signal in optimizer.optimize(context)]

    second = [signal.to_dict() for signal in optimizer.optimize(context)]

    assert first == second
