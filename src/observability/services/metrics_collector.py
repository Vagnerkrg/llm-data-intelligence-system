"""High-level observability metrics collector."""

from __future__ import annotations

from typing import Optional

from src.observability.domain.enums import (
    EventType,
    MetricName,
)
from src.observability.domain.models import ExecutionEvent
from src.observability.services.metrics import MetricsService


class MetricsCollector:
    """Collect canonical metrics from execution signals."""

    def __init__(
        self,
        metrics_service: Optional[MetricsService] = None,
    ) -> None:
        self.metrics = metrics_service or MetricsService()

    def collect_execution_started(
        self,
        execution_id: str,
    ) -> None:
        """Record execution start."""
        self.metrics.increment(
            execution_id,
            MetricName.EXECUTIONS_TOTAL,
            "execution",
        )

    def collect_execution_completed(
        self,
        execution_id: str,
        duration_ms: float,
    ) -> None:
        """Record successful execution."""
        self.metrics.increment(
            execution_id,
            MetricName.EXECUTIONS_SUCCESSFUL,
            "execution",
        )

        self.metrics.observe_duration(
            execution_id,
            MetricName.EXECUTION_DURATION_MS,
            duration_ms,
            "execution",
        )

        self.metrics.observe_rate(
            execution_id,
            MetricName.SUCCESS_RATE,
            1.0,
            "system",
        )

    def collect_execution_failed(
        self,
        execution_id: str,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Record failed execution."""
        self.metrics.increment(
            execution_id,
            MetricName.EXECUTIONS_FAILED,
            "execution",
        )

        if duration_ms is not None:
            self.metrics.observe_duration(
                execution_id,
                MetricName.EXECUTION_DURATION_MS,
                duration_ms,
                "execution",
            )

        self.metrics.observe_rate(
            execution_id,
            MetricName.FAILURE_RATE,
            1.0,
            "system",
        )

    def collect_reasoning_duration(
        self,
        execution_id: str,
        duration_ms: float,
    ) -> None:
        """Record reasoning duration."""
        self.metrics.observe_duration(
            execution_id,
            MetricName.REASONING_DURATION_MS,
            duration_ms,
            "reasoning",
        )

    def collect_planning_duration(
        self,
        execution_id: str,
        duration_ms: float,
    ) -> None:
        """Record planning duration."""
        self.metrics.observe_duration(
            execution_id,
            MetricName.PLANNING_DURATION_MS,
            duration_ms,
            "planning",
        )

    def collect_tool_call(
        self,
        execution_id: str,
        *,
        successful: bool,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Record one tool call."""
        self.metrics.increment(
            execution_id,
            MetricName.TOOL_CALLS_TOTAL,
            "tool",
        )

        if successful:
            self.metrics.increment(
                execution_id,
                MetricName.TOOL_CALLS_SUCCESSFUL,
                "tool",
            )
        else:
            self.metrics.increment(
                execution_id,
                MetricName.TOOL_CALLS_FAILED,
                "tool",
            )

        if duration_ms is not None:
            self.metrics.observe_duration(
                execution_id,
                MetricName.TOOL_EXECUTION_DURATION_MS,
                duration_ms,
                "tool",
            )

    def collect_memory_retrieval(
        self,
        execution_id: str,
        *,
        duration_ms: float,
        memories_retrieved: int = 0,
    ) -> None:
        """Record memory retrieval metrics."""
        self.metrics.increment(
            execution_id,
            MetricName.MEMORY_RETRIEVALS_TOTAL,
            "memory",
        )

        self.metrics.observe_duration(
            execution_id,
            MetricName.MEMORY_RETRIEVAL_DURATION_MS,
            duration_ms,
            "memory",
        )

        if memories_retrieved:
            self.metrics.increment(
                execution_id,
                MetricName.MEMORIES_RETRIEVED,
                "memory",
                amount=memories_retrieved,
            )

    def collect_knowledge_access(
        self,
        execution_id: str,
        *,
        updated: bool = False,
    ) -> None:
        """Record knowledge access."""
        self.metrics.increment(
            execution_id,
            MetricName.KNOWLEDGE_ACCESSES_TOTAL,
            "knowledge",
        )

        if updated:
            self.metrics.increment(
                execution_id,
                MetricName.KNOWLEDGE_UPDATES_TOTAL,
                "knowledge",
            )

    def collect_evaluation(
        self,
        execution_id: str,
        *,
        score: float,
        duration_ms: float,
    ) -> None:
        """Record cognitive evaluation metrics."""
        self.metrics.increment(
            execution_id,
            MetricName.EVALUATIONS_TOTAL,
            "evaluation",
        )

        self.metrics.observe_score(
            execution_id,
            MetricName.EVALUATION_SCORE,
            score,
            "evaluation",
        )

        self.metrics.observe_duration(
            execution_id,
            MetricName.EVALUATION_DURATION_MS,
            duration_ms,
            "evaluation",
        )

    def collect_learning(
        self,
        execution_id: str,
        *,
        signal_generated: bool = False,
        outcome_created: bool = False,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Record learning metrics."""
        if signal_generated:
            self.metrics.increment(
                execution_id,
                MetricName.LEARNING_SIGNALS_TOTAL,
                "learning",
            )

        if outcome_created:
            self.metrics.increment(
                execution_id,
                MetricName.LEARNING_OUTCOMES_TOTAL,
                "learning",
            )

        if duration_ms is not None:
            self.metrics.observe_duration(
                execution_id,
                MetricName.LEARNING_DURATION_MS,
                duration_ms,
                "learning",
            )

    def collect_evolution(
        self,
        execution_id: str,
        *,
        decision_created: bool = False,
        adaptation_applied: bool = False,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Record evolution metrics."""
        if decision_created:
            self.metrics.increment(
                execution_id,
                MetricName.EVOLUTION_DECISIONS_TOTAL,
                "evolution",
            )

        if adaptation_applied:
            self.metrics.increment(
                execution_id,
                MetricName.ADAPTATIONS_APPLIED_TOTAL,
                "evolution",
            )

        if duration_ms is not None:
            self.metrics.observe_duration(
                execution_id,
                MetricName.EVOLUTION_DURATION_MS,
                duration_ms,
                "evolution",
            )

    def collect_error(
        self,
        execution_id: str,
    ) -> None:
        """Record an execution error."""
        self.metrics.increment(
            execution_id,
            MetricName.ERRORS_TOTAL,
            "system",
        )

    def collect_from_event(
        self,
        event: ExecutionEvent,
    ) -> None:
        """Translate a structured event into metrics."""

        if event.event_type == EventType.EXECUTION_STARTED:
            self.collect_execution_started(
                event.execution_id,
            )
            return

        if event.event_type == EventType.EXECUTION_COMPLETED:
            duration_ms = self._duration_from_metadata(
                event,
            )

            if duration_ms is not None:
                self.collect_execution_completed(
                    event.execution_id,
                    duration_ms,
                )

            return

        if event.event_type == EventType.EXECUTION_FAILED:
            duration_ms = self._duration_from_metadata(
                event,
            )

            self.collect_execution_failed(
                event.execution_id,
                duration_ms,
            )
            return

        if event.event_type == EventType.REASONING_COMPLETED:
            duration_ms = self._duration_from_metadata(
                event,
            )

            if duration_ms is not None:
                self.collect_reasoning_duration(
                    event.execution_id,
                    duration_ms,
                )

            return

        if event.event_type == EventType.PLANNING_COMPLETED:
            duration_ms = self._duration_from_metadata(
                event,
            )

            if duration_ms is not None:
                self.collect_planning_duration(
                    event.execution_id,
                    duration_ms,
                )

            return

        if event.event_type == EventType.TOOL_CALL_COMPLETED:
            self.collect_tool_call(
                event.execution_id,
                successful=True,
                duration_ms=self._duration_from_metadata(
                    event,
                ),
            )
            return

        if event.event_type == EventType.TOOL_CALL_FAILED:
            self.collect_tool_call(
                event.execution_id,
                successful=False,
                duration_ms=self._duration_from_metadata(
                    event,
                ),
            )
            return

        if event.event_type == EventType.MEMORY_RETRIEVAL_COMPLETED:
            self.collect_memory_retrieval(
                event.execution_id,
                duration_ms=self._duration_from_metadata(
                    event,
                )
                or 0.0,
                memories_retrieved=int(
                    event.metadata.get(
                        "memories_retrieved",
                        0,
                    )
                ),
            )
            return

        if event.event_type == EventType.KNOWLEDGE_ACCESSED:
            self.collect_knowledge_access(
                event.execution_id,
                updated=False,
            )
            return

        if event.event_type == EventType.KNOWLEDGE_UPDATED:
            self.collect_knowledge_access(
                event.execution_id,
                updated=True,
            )
            return

        if event.event_type == EventType.COGNITIVE_EVALUATION_COMPLETED:
            self.collect_evaluation(
                event.execution_id,
                score=float(
                    event.metadata.get(
                        "score",
                        0.0,
                    )
                ),
                duration_ms=self._duration_from_metadata(
                    event,
                )
                or 0.0,
            )
            return

        if event.event_type == EventType.LEARNING_SIGNAL_GENERATED:
            self.collect_learning(
                event.execution_id,
                signal_generated=True,
            )
            return

        if event.event_type == EventType.LEARNING_OUTCOME_CREATED:
            self.collect_learning(
                event.execution_id,
                outcome_created=True,
            )
            return

        if event.event_type == EventType.EVOLUTION_DECISION_CREATED:
            self.collect_evolution(
                event.execution_id,
                decision_created=True,
            )
            return

        if event.event_type == EventType.ADAPTATION_APPLIED:
            self.collect_evolution(
                event.execution_id,
                adaptation_applied=True,
            )
            return

        if event.event_type == EventType.ERROR_OCCURRED:
            self.collect_error(
                event.execution_id,
            )

    @staticmethod
    def _duration_from_metadata(
        event: ExecutionEvent,
    ) -> Optional[float]:
        """Extract duration metadata when present."""
        value = event.metadata.get(
            "duration_ms",
        )

        if value is None:
            return None

        return float(value)
