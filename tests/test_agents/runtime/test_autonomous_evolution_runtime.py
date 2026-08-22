from src.agents.autonomous_evolution.domain import (
    EvolutionDecision,
    EvolutionResult,
)
from src.agents.runtime.agent_runtime import AgentRuntime


def test_agent_runtime_stores_autonomous_evolution_decision() -> None:
    runtime = AgentRuntime()

    context = runtime.execute("Analyze products")

    assert context.evolution_decision is not None

    assert isinstance(
        context.evolution_decision,
        EvolutionDecision,
    )


def test_agent_runtime_stores_autonomous_evolution_result() -> None:
    runtime = AgentRuntime()

    context = runtime.execute("Analyze products")

    assert context.evolution_result is not None

    assert isinstance(
        context.evolution_result,
        EvolutionResult,
    )


def test_agent_runtime_evolution_has_cognitive_evaluation_first() -> None:
    runtime = AgentRuntime()

    context = runtime.execute("Analyze products")

    assert context.cognitive_evaluation is not None
    assert context.evolution_decision is not None

    assert context.evolution_result.metadata["evidence_count"] >= 1


def test_agent_runtime_does_not_execute_adaptation() -> None:
    runtime = AgentRuntime()

    context = runtime.execute("Analyze products")

    assert (
        context.adaptation_action is None or context.adaptation_action.target == "agent"
    )


def test_agent_runtime_supports_evolution_dependency_injection() -> None:
    class FakeEvolutionAdapter:
        def __init__(self) -> None:
            self.called = False

        def evaluate(self, context):
            self.called = True
            return EvolutionResult(
                success=False,
            )

    adapter = FakeEvolutionAdapter()

    runtime = AgentRuntime(
        autonomous_evolution_adapter=adapter,
    )

    context = runtime.prepare("Analyze products")

    result = runtime.evaluate_evolution(context)

    assert adapter.called is True
    assert isinstance(
        result,
        EvolutionResult,
    )
