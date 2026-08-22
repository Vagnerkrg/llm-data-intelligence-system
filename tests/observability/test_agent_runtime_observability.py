"""Unit tests for Agent Runtime observability integration."""

from src.observability.domain.enums import (
    EventType,
    ExecutionStatus,
    MetricName,
)
from src.observability.services.agent_runtime_observability import (
    AgentRuntimeObservability,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


def test_disabled_observability_does_not_create_trace() -> None:
    observability = AgentRuntimeObservability(
        enabled=False,
    )

    execution_id = observability.start_execution()

    assert execution_id is None
    assert (
        observability.trace(
            execution_id,
        )
        is None
    )


def test_start_execution_creates_execution_id() -> None:
    observability = AgentRuntimeObservability(
        enabled=True,
    )

    execution_id = observability.start_execution()

    assert execution_id is not None
    assert execution_id.startswith("exec_")


def test_execution_id_is_attached_to_context() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    class Context:
        metadata = {}

    context = Context()

    observability.attach_to_context(
        context,
        execution_id,
    )

    assert context.execution_id == execution_id
    assert context.metadata["execution_id"] == execution_id


def test_reasoning_lifecycle_is_recorded() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.reasoning_started(
        execution_id,
    )

    observability.reasoning_completed(
        execution_id,
    )

    events = observability.trace(
        execution_id,
    ).events

    assert [event.event_type for event in events] == [
        EventType.EXECUTION_STARTED,
        EventType.REASONING_STARTED,
        EventType.REASONING_COMPLETED,
    ]


def test_execution_completion_is_recorded() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.execution_completed(
        execution_id,
        duration_ms=100,
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.status == ExecutionStatus.COMPLETED
    assert trace.events[-1].event_type == EventType.EXECUTION_COMPLETED


def test_execution_failure_is_recorded() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.fail_execution(
        execution_id,
        RuntimeError("runtime failure"),
        duration_ms=50,
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.status == ExecutionStatus.FAILED
    assert len(trace.errors) == 1
    assert trace.events[-1].event_type == EventType.EXECUTION_FAILED


def test_observability_failure_does_not_propagate() -> None:
    class BrokenTraceService:
        def create_trace(self, **kwargs):
            raise RuntimeError("observability unavailable")

    observability = AgentRuntimeObservability(
        trace_service=BrokenTraceService(),
    )

    execution_id = observability.start_execution()

    assert execution_id is None


def test_injected_trace_service_is_reused() -> None:
    trace_service = ExecutionTraceService()

    observability = AgentRuntimeObservability(
        trace_service=trace_service,
    )

    execution_id = observability.start_execution()

    trace = trace_service.get_trace(
        execution_id,
    )

    assert trace.execution_id == execution_id


def test_evaluation_score_creates_metric() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.cognitive_evaluation_completed(
        execution_id,
        score=0.91,
    )

    trace = observability.trace(
        execution_id,
    )

    assert any(
        metric.metric_name == MetricName.EVALUATION_SCORE.value
        for metric in trace.metrics
    )


def test_learning_signal_is_observed() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.learning_signal_generated(
        execution_id,
        confidence=0.88,
        signal_type="cognitive_evaluation",
        provenance="learning_loop",
    )

    trace = observability.trace(
        execution_id,
    )

    event = trace.events[-1]

    assert event.event_type == EventType.LEARNING_SIGNAL_GENERATED
    assert event.metadata["confidence"] == 0.88
    assert event.metadata["provenance"] == "learning_loop"


def test_learning_outcome_is_observed() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.learning_outcome_created(
        execution_id,
        outcome_type="improvement",
        confidence=0.75,
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.events[-1].event_type == EventType.LEARNING_OUTCOME_CREATED


def test_knowledge_access_is_observed() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.knowledge_accessed(
        execution_id,
        result={"source": "knowledge"},
        provenance="learning_knowledge_integrator",
        confidence=0.93,
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.events[-1].event_type == EventType.KNOWLEDGE_ACCESSED
    assert trace.events[-1].metadata["confidence"] == 0.93


def test_knowledge_update_is_observed() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.knowledge_updated(
        execution_id,
        result={"updated": True},
        provenance="learning_knowledge_integrator",
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.events[-1].event_type == EventType.KNOWLEDGE_UPDATED


def test_memory_retrieval_is_observed() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.memory_retrieval_completed(
        execution_id,
        memories_retrieved=3,
        relevance_score=0.89,
        provenance="learning_memory_bridge",
    )

    trace = observability.trace(
        execution_id,
    )

    event = trace.events[-1]

    assert event.event_type == EventType.MEMORY_RETRIEVAL_COMPLETED
    assert event.metadata["memories_retrieved"] == 3
    assert event.metadata["relevance_score"] == 0.89


def test_optimization_signal_is_observed() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.optimization_signal_generated(
        execution_id,
        signal_type="experience_optimization",
        confidence=0.81,
        provenance="experience_driven_optimizer",
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.events[-1].event_type == EventType.EVOLUTION_CHANGE_EVALUATED


def test_evolution_decision_is_observed() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.evolution_decision_created(
        execution_id,
        decision={"action": "adapt"},
        confidence=0.84,
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.events[-1].event_type == EventType.EVOLUTION_DECISION_CREATED


def test_adaptation_is_observed() -> None:
    observability = AgentRuntimeObservability()

    execution_id = observability.start_execution()

    observability.adaptation_applied(
        execution_id,
        result={"adapted": True},
        provenance="autonomous_evolution_adapter",
    )

    trace = observability.trace(
        execution_id,
    )

    assert trace.events[-1].event_type == EventType.ADAPTATION_APPLIED
