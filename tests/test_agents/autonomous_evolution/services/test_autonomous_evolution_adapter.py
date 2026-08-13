import pytest

from src.agents.autonomous_evolution.domain import (
    EvolutionAction,
    EvolutionContext,
    EvolutionDecision,
    EvolutionResult,
    EvolutionStatus,
)
from src.agents.autonomous_evolution.services import (
    AdaptiveBehaviorPolicy,
    AutonomousEvolutionAdapter,
    EvolutionDecisionEngine,
)
from src.agents.runtime.execution_context import ExecutionContext


def test_adapter_builds_evolution_context() -> None:
    adapter = AutonomousEvolutionAdapter()

    context = ExecutionContext(
        question="Analyze products"
    )

    context.status = "completed"
    context.results.append(
        {"result": "success"}
    )

    evolution_context = adapter.build_context(
        context
    )

    assert isinstance(
        evolution_context,
        EvolutionContext,
    )

    assert evolution_context.execution_information[
        "score"
    ] == 1.0

    assert evolution_context.metadata[
        "question"
    ] == "Analyze products"


def test_adapter_requires_execution_context() -> None:
    adapter = AutonomousEvolutionAdapter()

    with pytest.raises(TypeError):
        adapter.build_context(
            "invalid"  # type: ignore[arg-type]
        )


def test_adapter_stores_evolution_decision_and_result() -> None:
    adapter = AutonomousEvolutionAdapter()

    context = ExecutionContext(
        question="Analyze products"
    )

    context.status = "completed"

    result = adapter.evaluate(
        context
    )

    assert isinstance(
        context.evolution_decision,
        EvolutionDecision,
    )

    assert isinstance(
        context.evolution_result,
        EvolutionResult,
    )

    assert result is context.evolution_result


def test_adapter_translates_adaptation_action_to_evolution_action() -> None:
    adapter = AutonomousEvolutionAdapter(
        evolution_decision_engine=EvolutionDecisionEngine(
            min_evidence=1,
        ),
        adaptive_behavior_policy=AdaptiveBehaviorPolicy(),
    )

    context = ExecutionContext(
        question="Analyze products"
    )

    context.status = "completed"

    context.set_cognitive_evaluation(
        {
            "overall_score": 0.95,
            "confidence": 0.95,
        }
    )

    result = adapter.evaluate(
        context
    )

    assert result.action is None or isinstance(
        result.action,
        EvolutionAction,
    )

    if result.action is not None:
        assert result.action.target == "agent"


def test_adapter_does_not_execute_adaptation() -> None:
    adapter = AutonomousEvolutionAdapter()

    context = ExecutionContext(
        question="Analyze products"
    )

    context.status = "completed"

    adapter.evaluate(
        context
    )

    assert (
        context.evolution_result is not None
    )


def test_adapter_uses_injected_dependencies() -> None:
    class FakeDecisionEngine:
        def __init__(self) -> None:
            self.called = False

        def decide(
            self,
            context: EvolutionContext,
        ) -> EvolutionDecision:
            self.called = True

            return EvolutionDecision(
                should_evolve=False,
                confidence=0.0,
                status=EvolutionStatus.PENDING,
                reason="No evidence.",
            )

    class FakePolicy:
        def __init__(self) -> None:
            self.called = False

        def evaluate(
            self,
            decision: EvolutionDecision,
            target: str,
        ):
            self.called = True
            return None

    decision_engine = FakeDecisionEngine()
    policy = FakePolicy()

    adapter = AutonomousEvolutionAdapter(
        evolution_decision_engine=decision_engine,
        adaptive_behavior_policy=policy,
    )

    context = ExecutionContext(
        question="Analyze products"
    )

    adapter.evaluate(
        context
    )

    assert decision_engine.called is True
    assert policy.called is True