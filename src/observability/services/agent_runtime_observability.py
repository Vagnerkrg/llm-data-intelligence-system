"""Observability integration facade for Agent Runtime."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from src.observability.domain.enums import (
    ErrorSeverity,
    EventType,
    ExecutionStatus,
)
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)
from src.observability.services.metrics import (
    MetricsService,
)
from src.observability.services.metrics_collector import (
    MetricsCollector,
)
from src.observability.services.structured_event import (
    StructuredEventService,
)


class AgentRuntimeObservability:
    """Safe integration boundary between Agent Runtime and Observability."""

    def __init__(
        self,
        *,
        enabled: bool = True,
        trace_service: Optional[ExecutionTraceService] = None,
        event_service: Optional[StructuredEventService] = None,
        metrics_service: Optional[MetricsService] = None,
        metrics_collector: Optional[MetricsCollector] = None,
    ) -> None:
        self.enabled = enabled

        if not enabled:
            self.trace_service = None
            self.event_service = None
            self.metrics_service = None
            self.metrics_collector = None
            return

        resolved_trace_service = trace_service or ExecutionTraceService()

        resolved_event_service = event_service or StructuredEventService(
            trace_service=resolved_trace_service,
        )

        resolved_metrics_service = metrics_service or MetricsService(
            trace_service=resolved_trace_service,
        )

        resolved_metrics_collector = metrics_collector or MetricsCollector(
            metrics_service=resolved_metrics_service,
        )

        self.trace_service = resolved_trace_service
        self.event_service = resolved_event_service
        self.metrics_service = resolved_metrics_service
        self.metrics_collector = resolved_metrics_collector

    def start_execution(
        self,
        *,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Create and start an observable execution."""
        if not self.enabled:
            return None

        try:
            trace = self.trace_service.create_trace(
                correlation_id=correlation_id,
                metadata=metadata,
            )

            self.trace_service.start(
                trace.execution_id,
            )

            return trace.execution_id

        except Exception:
            return None

    def attach_to_context(
        self,
        context: Any,
        execution_id: Optional[str],
    ) -> None:
        """Propagate execution ID into runtime context."""
        if not self.enabled or not execution_id:
            return

        try:
            if hasattr(context, "set_execution_id"):
                context.set_execution_id(
                    execution_id,
                )
            else:
                context.execution_id = execution_id
                context.metadata["execution_id"] = execution_id
        except Exception:
            return

    def reasoning_started(
        self,
        execution_id: Optional[str],
    ) -> None:
        """Register reasoning start."""
        self._emit(
            execution_id,
            EventType.REASONING_STARTED,
            component="reasoning",
            stage="reasoning",
        )

    def reasoning_completed(
        self,
        execution_id: Optional[str],
    ) -> None:
        """Register reasoning completion."""
        self._emit(
            execution_id,
            EventType.REASONING_COMPLETED,
            component="reasoning",
            stage="reasoning",
        )

    def reasoning_failed(
        self,
        execution_id: Optional[str],
        error: Exception,
    ) -> None:
        """Register reasoning failure."""
        self._record_failure(
            execution_id,
            component="reasoning",
            stage="reasoning",
            error=error,
            event_type=EventType.REASONING_FAILED,
        )

    def planning_started(
        self,
        execution_id: Optional[str],
    ) -> None:
        """Register planning start."""
        self._emit(
            execution_id,
            EventType.PLANNING_STARTED,
            component="planning",
            stage="planning",
        )

    def planning_completed(
        self,
        execution_id: Optional[str],
    ) -> None:
        """Register planning completion."""
        self._emit(
            execution_id,
            EventType.PLANNING_COMPLETED,
            component="planning",
            stage="planning",
        )

    def planning_failed(
        self,
        execution_id: Optional[str],
        error: Exception,
    ) -> None:
        """Register planning failure."""
        self._record_failure(
            execution_id,
            component="planning",
            stage="planning",
            error=error,
            event_type=EventType.PLANNING_FAILED,
        )

    def execution_started(
        self,
        execution_id: Optional[str],
    ) -> None:
        """Register execution-stage start."""
        self._emit(
            execution_id,
            EventType.EXECUTION_STAGE_STARTED,
            component="execution",
            stage="execution",
        )

    def execution_completed(
        self,
        execution_id: Optional[str],
        duration_ms: Optional[float] = None,
    ) -> None:
        """Finalize execution and register completion."""
        if not self.enabled or not execution_id:
            return

        try:
            self.trace_service.complete(
                execution_id,
            )

            metadata = self._duration_metadata(
                duration_ms,
            )

            self._emit(
                execution_id,
                EventType.EXECUTION_COMPLETED,
                component="execution",
                stage="lifecycle",
                status=ExecutionStatus.COMPLETED,
                metadata=metadata,
            )

            if duration_ms is not None:
                self.metrics_collector.collect_execution_completed(
                    execution_id,
                    duration_ms,
                )

        except Exception:
            return

    def execution_failed(
        self,
        execution_id: Optional[str],
        error: Exception,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Register execution-stage failure."""
        metadata = self._duration_metadata(
            duration_ms,
        )

        self._record_failure(
            execution_id,
            component="execution",
            stage="execution",
            error=error,
            event_type=EventType.EXECUTION_STAGE_FAILED,
            metadata=metadata,
        )

    def step_started(
        self,
        execution_id: Optional[str],
        *,
        step: Optional[str] = None,
    ) -> None:
        """Register an execution step start."""
        metadata: Dict[str, Any] = {}

        if step:
            metadata["step"] = step

        self._emit(
            execution_id,
            EventType.STEP_STARTED,
            component="execution",
            stage="execution",
            metadata=metadata,
        )

    def step_completed(
        self,
        execution_id: Optional[str],
        *,
        step: Optional[str] = None,
    ) -> None:
        """Register an execution step completion."""
        metadata: Dict[str, Any] = {}

        if step:
            metadata["step"] = step

        self._emit(
            execution_id,
            EventType.STEP_COMPLETED,
            component="execution",
            stage="execution",
            metadata=metadata,
        )

    def step_failed(
        self,
        execution_id: Optional[str],
        error: Exception,
        *,
        step: Optional[str] = None,
    ) -> None:
        """Register an execution step failure."""
        metadata: Dict[str, Any] = {}

        if step:
            metadata["step"] = step

        self._record_failure(
            execution_id,
            component="execution",
            stage="execution",
            error=error,
            event_type=EventType.STEP_FAILED,
            metadata=metadata,
        )

    def tool_started(
        self,
        execution_id: Optional[str],
        *,
        tool: Optional[str] = None,
    ) -> None:
        """Register tool call start."""
        metadata: Dict[str, Any] = {}

        if tool:
            metadata["tool"] = tool

        self._emit(
            execution_id,
            EventType.TOOL_CALL_STARTED,
            component="tool",
            stage="tool_call",
            metadata=metadata,
        )

    def tool_completed(
        self,
        execution_id: Optional[str],
        *,
        tool: Optional[str] = None,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Register tool call completion."""
        metadata = self._duration_metadata(
            duration_ms,
        )

        if tool:
            metadata["tool"] = tool

        self._emit(
            execution_id,
            EventType.TOOL_CALL_COMPLETED,
            component="tool",
            stage="tool_call",
            metadata=metadata,
        )

    def tool_failed(
        self,
        execution_id: Optional[str],
        error: Exception,
        *,
        tool: Optional[str] = None,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Register tool call failure."""
        metadata = self._duration_metadata(
            duration_ms,
        )

        if tool:
            metadata["tool"] = tool

        self._record_failure(
            execution_id,
            component="tool",
            stage="tool_call",
            error=error,
            event_type=EventType.TOOL_CALL_FAILED,
            metadata=metadata,
        )

    def record_state(
        self,
        execution_id: Optional[str],
        *,
        status: ExecutionStatus,
        component: Optional[str] = None,
        stage: Optional[str] = None,
        step: Optional[str] = None,
    ) -> None:
        """Register a runtime state change."""
        if not self.enabled or not execution_id:
            return

        try:
            self.trace_service.update_state(
                execution_id,
                status=status,
                component=component,
                stage=stage,
                step=step,
            )

            self._emit(
                execution_id,
                EventType.EXECUTION_STATE_CHANGED,
                component=component or "runtime",
                stage=stage or "lifecycle",
                status=status,
                metadata=({"step": step} if step else {}),
            )

        except Exception:
            return

    def cognitive_evaluation_started(
        self,
        execution_id: Optional[str],
    ) -> None:
        """Register cognitive evaluation start."""
        self._emit(
            execution_id,
            EventType.COGNITIVE_EVALUATION_STARTED,
            component="evaluation",
            stage="evaluation",
        )

    def cognitive_evaluation_completed(
        self,
        execution_id: Optional[str],
        *,
        score: Optional[float] = None,
    ) -> None:
        """Register cognitive evaluation completion."""
        metadata: Dict[str, Any] = {}

        if score is not None:
            metadata["score"] = score

        self._emit(
            execution_id,
            EventType.COGNITIVE_EVALUATION_COMPLETED,
            component="evaluation",
            stage="evaluation",
            metadata=metadata,
        )

    def learning_completed(
        self,
        execution_id: Optional[str],
        *,
        signals: int = 0,
        outcomes: int = 0,
    ) -> None:
        """Register learning completion."""
        self._emit(
            execution_id,
            EventType.LEARNING_COMPLETED,
            component="learning",
            stage="learning",
            metadata={
                "signals": signals,
                "outcomes": outcomes,
            },
        )

    def evolution_completed(
        self,
        execution_id: Optional[str],
        *,
        decision_created: bool = False,
        adaptation_applied: bool = False,
    ) -> None:
        """Register evolution completion."""
        self._emit(
            execution_id,
            EventType.EVOLUTION_COMPLETED,
            component="evolution",
            stage="evolution",
            metadata={
                "decision_created": decision_created,
                "adaptation_applied": adaptation_applied,
            },
        )

    def error(
        self,
        execution_id: Optional[str],
        error: Exception,
        *,
        component: str = "runtime",
        stage: str = "runtime",
    ) -> None:
        """Register a non-fatal observability error."""
        self._record_failure(
            execution_id,
            component=component,
            stage=stage,
            error=error,
            event_type=EventType.ERROR_OCCURRED,
        )

    def complete_execution(
        self,
        execution_id: Optional[str],
        *,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Backward-compatible alias for execution_completed."""
        self.execution_completed(
            execution_id,
            duration_ms=duration_ms,
        )

    def fail_execution(
        self,
        execution_id: Optional[str],
        error: Exception,
        *,
        duration_ms: Optional[float] = None,
    ) -> None:
        """Finalize a failed execution."""
        if not self.enabled or not execution_id:
            return

        try:
            self.trace_service.record_error(
                execution_id,
                component="runtime",
                error_type=type(error).__name__,
                message=str(error),
                severity=ErrorSeverity.ERROR,
                stage="runtime",
            )

            self.trace_service.fail(
                execution_id,
            )

            metadata = self._duration_metadata(
                duration_ms,
            )

            self._emit(
                execution_id,
                EventType.EXECUTION_FAILED,
                component="execution",
                stage="lifecycle",
                status=ExecutionStatus.FAILED,
                metadata=metadata,
            )

            self.metrics_collector.collect_execution_failed(
                execution_id,
                duration_ms,
            )

        except Exception:
            return

    def trace(
        self,
        execution_id: Optional[str],
    ):
        """Return the current execution trace."""
        if not self.enabled or not execution_id:
            return None

        try:
            return self.trace_service.get_trace(
                execution_id,
            )
        except Exception:
            return None

    def _emit(
        self,
        execution_id: Optional[str],
        event_type: EventType,
        *,
        component: str,
        stage: str,
        status: Optional[ExecutionStatus] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Emit safely without affecting runtime."""
        if not self.enabled or not execution_id:
            return

        try:
            self.event_service.emit(
                execution_id=execution_id,
                event_type=event_type,
                component=component,
                stage=stage,
                status=status,
                metadata=metadata,
            )
        except Exception:
            return

    def _record_failure(
        self,
        execution_id: Optional[str],
        *,
        component: str,
        stage: str,
        error: Exception,
        event_type: EventType,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Record an error and event without breaking runtime."""
        if not self.enabled or not execution_id:
            return

        try:
            self.trace_service.record_error(
                execution_id=execution_id,
                component=component,
                error_type=type(error).__name__,
                message=str(error),
                severity=ErrorSeverity.ERROR,
                stage=stage,
                metadata=metadata,
            )

            self._emit(
                execution_id,
                event_type,
                component=component,
                stage=stage,
                status=ExecutionStatus.FAILED,
                metadata=metadata,
            )

        except Exception:
            return

    @staticmethod
    def _duration_metadata(
        duration_ms: Optional[float],
    ) -> Dict[str, Any]:
        """Build duration metadata."""
        if duration_ms is None:
            return {}

        return {
            "duration_ms": duration_ms,
        }

    @staticmethod
    def now() -> datetime:
        """Return current UTC time."""
        return datetime.now(timezone.utc)
