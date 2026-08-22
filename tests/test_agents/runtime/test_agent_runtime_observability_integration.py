"""Integration tests for AgentRuntime observability."""

from types import SimpleNamespace

from src.agents.runtime.agent_runtime import AgentRuntime
from src.observability.services.agent_runtime_observability import (
    AgentRuntimeObservability,
)


class FakeReasoningEngine:
    def reason(self, question):
        return SimpleNamespace(
            question=question,
            reasoning="reasoned",
        )


class FakeGoalBuilder:
    def build(self, reasoning):
        return SimpleNamespace(
            name="test goal",
            description="test goal",
        )


class FakePlanner:
    def create_plan(
        self,
        question,
        reasoning_result=None,
        goal=None,
    ):
        return SimpleNamespace(
            steps=[],
            next_step=lambda: None,
        )


class FakeExecutionEngine:
    def __init__(self, observability=None):
        self.observability = observability

    def execute(self, context):
        context.complete()
        return context


class FakeImprovementEngine:
    def execute(self, request):
        return SimpleNamespace(
            result={
                "status": "improved",
            }
        )


class FakeEvaluationAdapter:
    def adapt(self, context):
        return context


class FakeEvaluator:
    def evaluate(self, context):
        return SimpleNamespace(
            score=0.9,
            overall_score=0.9,
            confidence=0.95,
        )


class FakeLearningLoop:
    def run(
        self,
        context,
        learning_signals,
        execution_history,
    ):
        return SimpleNamespace(
            success=True,
            evaluation_result=SimpleNamespace(
                overall_score=0.9,
            ),
            learning_experiences=[
                {
                    "signal_type": "cognitive_evaluation",
                    "confidence": 0.9,
                }
            ],
            learning_outcomes=[
                {
                    "outcome_type": "improvement",
                    "confidence": 0.85,
                }
            ],
            knowledge_results=[
                {
                    "knowledge_id": "knowledge-001",
                    "confidence": 0.92,
                    "provenance": "test",
                }
            ],
            memory_results=[
                {
                    "relevance_score": 0.88,
                }
            ],
            optimization_signals=[
                {
                    "signal_type": "optimization",
                    "confidence": 0.8,
                }
            ],
            evolution_result={
                "adapted": True,
                "confidence": 0.87,
            },
            failed_stage=None,
            error=None,
        )


class FakeEvolutionAdapter:
    def evaluate(self, context):
        return SimpleNamespace(
            adapted=True,
            confidence=0.9,
        )


def build_runtime(
    observability,
) -> AgentRuntime:
    return AgentRuntime(
        execution_engine=FakeExecutionEngine(
            observability=observability,
        ),
        planner=FakePlanner(),
        reasoning_engine=FakeReasoningEngine(),
        goal_builder=FakeGoalBuilder(),
        cognitive_improvement_engine=FakeImprovementEngine(),
        cognitive_evaluation_adapter=FakeEvaluationAdapter(),
        cognitive_evaluator=FakeEvaluator(),
        cognitive_learning_loop=FakeLearningLoop(),
        autonomous_evolution_adapter=FakeEvolutionAdapter(),
        observability=observability,
    )


def test_runtime_execution_produces_trace() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    execution_id = result.execution_id

    trace = observability.trace(
        execution_id,
    )

    assert trace is not None
    assert trace.execution_id == execution_id
    assert trace.finished_at is not None


def test_runtime_propagates_execution_id() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    assert result.execution_id is not None
    assert result.metadata["execution_id"] == result.execution_id


def test_runtime_records_reasoning_and_planning() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    trace = observability.trace(
        result.execution_id,
    )

    event_types = [event.event_type for event in trace.events]

    assert any(event.value == "reasoning.started" for event in event_types)

    assert any(event.value == "reasoning.completed" for event in event_types)

    assert any(event.value == "planning.started" for event in event_types)

    assert any(event.value == "planning.completed" for event in event_types)


def test_runtime_records_cognitive_evaluation() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    trace = observability.trace(
        result.execution_id,
    )

    assert any(
        event.event_type.value == "cognitive.evaluation_completed"
        for event in trace.events
    )

    assert any(metric.metric_name == "evaluation_score" for metric in trace.metrics)


def test_runtime_records_learning_outputs() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    trace = observability.trace(
        result.execution_id,
    )

    event_types = [event.event_type.value for event in trace.events]

    assert "learning.signal_generated" in event_types

    assert "learning.outcome_created" in event_types

    assert "learning.completed" in event_types


def test_runtime_records_knowledge_and_memory() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    trace = observability.trace(
        result.execution_id,
    )

    event_types = [event.event_type.value for event in trace.events]

    assert "knowledge.accessed" in event_types

    assert "knowledge.updated" in event_types

    assert "memory.retrieval_completed" in event_types


def test_runtime_records_optimization_and_evolution() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    trace = observability.trace(
        result.execution_id,
    )

    event_types = [event.event_type.value for event in trace.events]

    assert "evolution.change_evaluated" in event_types

    assert "evolution.decision_created" in event_types

    assert "evolution.adaptation_applied" in event_types


def test_runtime_preserves_cognitive_provenance() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    trace = observability.trace(
        result.execution_id,
    )

    provenance_values = [event.metadata.get("provenance") for event in trace.events]

    assert "cognitive_learning_loop" in provenance_values

    assert "learning_knowledge_integrator" in provenance_values

    assert "learning_memory_bridge" in provenance_values


def test_runtime_preserves_confidence() -> None:
    observability = AgentRuntimeObservability()

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    trace = observability.trace(
        result.execution_id,
    )

    confidence_values = [
        event.metadata.get("confidence")
        for event in trace.events
        if event.metadata.get("confidence") is not None
    ]

    assert confidence_values


def test_disabled_observability_preserves_runtime() -> None:
    observability = AgentRuntimeObservability(
        enabled=False,
    )

    runtime = build_runtime(
        observability,
    )

    result = runtime.execute(
        "test query",
    )

    assert result.status == "completed"
    assert result.execution_id is None


def test_observability_failure_does_not_break_runtime() -> None:
    class BrokenObservability:
        def start_execution(self, **kwargs):
            raise RuntimeError("broken")

        def attach_to_context(
            self,
            context,
            execution_id,
        ):
            return None

    runtime = build_runtime(
        BrokenObservability(),
    )

    result = runtime.execute(
        "test query",
    )

    assert result is not None
    assert result.status == "completed"
