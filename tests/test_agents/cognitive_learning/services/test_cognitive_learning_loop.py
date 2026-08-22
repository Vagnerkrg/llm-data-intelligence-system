from src.agents.autonomous_evolution.domain.evolution_context import (
    EvolutionContext,
)
from src.agents.autonomous_evolution.domain.evolution_decision import (
    EvolutionDecision,
)
from src.agents.autonomous_evolution.domain.evolution_status import (
    EvolutionStatus,
)
from src.agents.autonomous_evolution.domain.optimization_signal import (
    OptimizationSignal,
)
from src.agents.cognitive_evaluation.domain.evaluation_context import (
    EvaluationContext,
)
from src.agents.cognitive_evaluation.domain.evaluation_result import (
    EvaluationResult,
)
from src.agents.cognitive_learning.integration.learning_evolution_bridge import (
    LearningEvolutionResult,
)
from src.agents.cognitive_learning.services.cognitive_learning_loop import (
    CognitiveLearningLoop,
)


class FakeEvaluator:
    def __init__(self, score: float = 0.9) -> None:
        self.score = score

    def evaluate(self, context):
        return EvaluationResult(
            overall_score=self.score,
            status="completed",
            metadata={},
        )


class FakeKnowledgeIntegrator:
    def integrate_many(self, outcomes):
        return []


class FakeMemoryBridge:
    def store_many(self, outcomes):
        return []


class FakeOptimizer:
    def optimize(self, context):
        return [
            OptimizationSignal(
                signal_type="strategy_preference",
                target="execution_strategy",
                direction="reinforce",
                strength=0.9,
                confidence=0.9,
                reason="Effective strategy.",
                supporting_patterns=["effective_execution_pattern"],
            )
        ]


class FakeEvolutionBridge:
    def evaluate(
        self,
        *,
        learning_outcomes,
        learning_signals,
        optimization_signals,
    ):
        return LearningEvolutionResult(
            context=EvolutionContext(
                learning_information=[
                    {
                        "score": 0.9,
                        "confidence": 0.9,
                    }
                ]
            ),
            decision=EvolutionDecision(
                should_evolve=True,
                confidence=0.9,
                status=EvolutionStatus.PROPOSED,
                reason="Learning supports evolution.",
            ),
            learning_evidence_count=(len(learning_outcomes) + len(learning_signals)),
            optimization_signal_count=len(optimization_signals),
        )


class FailingOptimizer:
    def optimize(self, context):
        raise RuntimeError("optimization failed")


def _evaluation_context():
    return EvaluationContext()


def test_runs_complete_cognitive_learning_loop():
    loop = CognitiveLearningLoop(
        cognitive_evaluator=FakeEvaluator(),
        knowledge_integrator=FakeKnowledgeIntegrator(),
        memory_bridge=FakeMemoryBridge(),
        experience_optimizer=FakeOptimizer(),
        evolution_bridge=FakeEvolutionBridge(),
    )

    result = loop.run(
        _evaluation_context(),
        execution_history=[
            {
                "score": 0.9,
                "confidence": 0.9,
                "strategy": "stable",
            },
            {
                "score": 0.9,
                "confidence": 0.9,
                "strategy": "stable",
            },
        ],
    )

    assert result.success
    assert result.evaluation_result is not None
    assert result.learning_experiences
    assert result.learning_outcomes
    assert result.evolution_result is not None
    assert result.evolution_result.should_evolve
    assert result.failed_stage is None


def test_preserves_intermediate_learning_state():
    loop = CognitiveLearningLoop(
        cognitive_evaluator=FakeEvaluator(),
        knowledge_integrator=FakeKnowledgeIntegrator(),
        experience_optimizer=FakeOptimizer(),
        evolution_bridge=FakeEvolutionBridge(),
    )

    result = loop.run(_evaluation_context())

    assert result.evaluation_result is not None
    assert len(result.learning_experiences) == 1
    assert len(result.learning_outcomes) == 1
    assert result.memory_results == []


def test_memory_stage_is_optional():
    loop = CognitiveLearningLoop(
        cognitive_evaluator=FakeEvaluator(),
        knowledge_integrator=FakeKnowledgeIntegrator(),
        experience_optimizer=FakeOptimizer(),
        evolution_bridge=FakeEvolutionBridge(),
    )

    result = loop.run(_evaluation_context())

    assert result.success
    assert result.memory_results == []


def test_isolates_component_failure():
    loop = CognitiveLearningLoop(
        cognitive_evaluator=FakeEvaluator(),
        knowledge_integrator=FakeKnowledgeIntegrator(),
        experience_optimizer=FailingOptimizer(),
        evolution_bridge=FakeEvolutionBridge(),
    )

    result = loop.run(_evaluation_context())

    assert not result.success
    assert result.failed_stage == "optimization"
    assert result.error == "optimization failed"
    assert result.learning_experiences
    assert result.learning_outcomes


def test_dependency_injection_preserves_components():
    evaluator = FakeEvaluator()
    knowledge = FakeKnowledgeIntegrator()
    optimizer = FakeOptimizer()
    evolution = FakeEvolutionBridge()

    loop = CognitiveLearningLoop(
        cognitive_evaluator=evaluator,
        knowledge_integrator=knowledge,
        experience_optimizer=optimizer,
        evolution_bridge=evolution,
    )

    assert loop.cognitive_evaluator is evaluator
    assert loop.knowledge_integrator is knowledge
    assert loop.experience_optimizer is optimizer
    assert loop.evolution_bridge is evolution


def test_deterministic_learning_state_for_same_inputs():
    first_loop = CognitiveLearningLoop(
        cognitive_evaluator=FakeEvaluator(),
        knowledge_integrator=FakeKnowledgeIntegrator(),
        experience_optimizer=FakeOptimizer(),
        evolution_bridge=FakeEvolutionBridge(),
    )

    second_loop = CognitiveLearningLoop(
        cognitive_evaluator=FakeEvaluator(),
        knowledge_integrator=FakeKnowledgeIntegrator(),
        experience_optimizer=FakeOptimizer(),
        evolution_bridge=FakeEvolutionBridge(),
    )

    first = first_loop.run(_evaluation_context())

    second = second_loop.run(_evaluation_context())

    assert [item.signal_type for item in first.learning_experiences] == [
        item.signal_type for item in second.learning_experiences
    ]

    assert [item.learned_pattern for item in first.learning_outcomes] == [
        item.learned_pattern for item in second.learning_outcomes
    ]

    assert first.evolution_result.should_evolve == (
        second.evolution_result.should_evolve
    )
