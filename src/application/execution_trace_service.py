"""Application service for public execution trace queries."""

from __future__ import annotations

from typing import Any, Optional

from src.agents.runtime.agent_runtime import AgentRuntime
from src.api.schemas import (
    ExecutionErrorTraceResponse,
    ExecutionEventResponse,
    ExecutionMetricResponse,
    ExecutionResponse,
    ExecutionStateResponse,
    ExecutionTraceResponse,
    ExecutionStatus,
)
from src.observability.domain.models import (
    ExecutionTrace,
)


class ExecutionTraceApplicationService:
    """Application boundary for read-only execution observability."""

    def __init__(
        self,
        runtime: Optional[AgentRuntime] = None,
    ) -> None:
        self.runtime = runtime or AgentRuntime()

    def get_execution(
        self,
        execution_id: str,
    ) -> ExecutionResponse:
        """Return the public execution representation."""
        trace = self._get_trace(
            execution_id,
        )

        return self._map_execution(
            trace,
        )

    def get_trace(
        self,
        execution_id: str,
    ) -> ExecutionTraceResponse:
        """Return the complete public execution trace."""
        trace = self._get_trace(
            execution_id,
        )

        ordered_events = sorted(
            trace.events,
            key=lambda item: item.timestamp,
        )

        ordered_metrics = sorted(
            trace.metrics,
            key=lambda item: item.timestamp,
        )

        ordered_errors = sorted(
            trace.errors,
            key=lambda item: item.timestamp,
        )

        state = None

        if trace.state_history:
            latest_state = max(
                trace.state_history,
                key=lambda item: item.updated_at,
            )

            state = ExecutionStateResponse(
                execution_id=latest_state.execution_id,
                status=self._map_status(
                    latest_state.status,
                ),
                current_component=(latest_state.current_component),
                current_stage=(latest_state.current_stage),
                current_step=(latest_state.current_step),
                started_at=latest_state.started_at,
                updated_at=latest_state.updated_at,
                metadata=dict(
                    latest_state.metadata,
                ),
            )

        return ExecutionTraceResponse(
            execution_id=trace.execution_id,
            status=self._map_status(
                trace.status,
            ),
            started_at=trace.started_at,
            finished_at=trace.finished_at,
            duration_ms=trace.duration,
            state=state,
            events=[self._map_event(event) for event in ordered_events],
            metrics=[self._map_metric(metric) for metric in ordered_metrics],
            errors=[self._map_error(error) for error in ordered_errors],
        )

    def _get_trace(
        self,
        execution_id: str,
    ) -> ExecutionTrace:
        """Retrieve a trace through Observability."""
        observability = getattr(
            self.runtime,
            "observability",
            None,
        )

        if observability is None:
            raise LookupError(f"Execution '{execution_id}' not found.")

        trace_method = getattr(
            observability,
            "trace",
            None,
        )

        if not callable(trace_method):
            raise LookupError(f"Execution '{execution_id}' not found.")

        try:
            trace = trace_method(
                execution_id,
            )
        except KeyError as exc:
            raise LookupError(f"Execution '{execution_id}' not found.") from exc
        except Exception as exc:
            raise RuntimeError("Unable to retrieve execution trace.") from exc

        if trace is None:
            raise LookupError(f"Execution '{execution_id}' not found.")

        return trace

    def _map_execution(
        self,
        trace: ExecutionTrace,
    ) -> ExecutionResponse:
        """Map internal trace into the public execution response."""
        return ExecutionResponse(
            execution_id=trace.execution_id,
            status=self._map_status(
                trace.status,
            ),
            created_at=trace.started_at,
            started_at=trace.started_at,
            finished_at=trace.finished_at,
            duration_ms=trace.duration,
            correlation_id=self._correlation_id(
                trace,
            ),
            metadata={
                "correlation_id": self._correlation_id(
                    trace,
                ),
                "source": "observability",
                "values": dict(
                    trace.metadata,
                ),
            },
            result=None,
            error=(
                self._latest_error(
                    trace,
                )
                if trace.status.value == "failed"
                else None
            ),
        )

    @staticmethod
    def _correlation_id(
        trace: ExecutionTrace,
    ) -> str | None:
        """Return correlation ID without exposing internal context."""
        if trace.context is None:
            return None

        return trace.context.correlation_id

    @staticmethod
    def _map_status(
        status: Any,
    ) -> ExecutionStatus:
        """Map domain status to the public API enum."""
        value = str(
            getattr(
                status,
                "value",
                status,
            )
        ).lower()

        mapping = {
            "pending": ExecutionStatus.PENDING,
            "running": ExecutionStatus.RUNNING,
            "completed": ExecutionStatus.COMPLETED,
            "failed": ExecutionStatus.FAILED,
            "cancelled": ExecutionStatus.CANCELLED,
        }

        return mapping.get(
            value,
            ExecutionStatus.PENDING,
        )

    @staticmethod
    def _map_event(
        event: Any,
    ) -> ExecutionEventResponse:
        """Map an internal event to a public response."""
        return ExecutionEventResponse(
            event_id=event.event_id,
            execution_id=event.execution_id,
            event_type=str(
                getattr(
                    event.event_type,
                    "value",
                    event.event_type,
                )
            ),
            timestamp=event.timestamp,
            component=event.component,
            stage=event.stage,
            status=(
                ExecutionTraceApplicationService._map_status(
                    event.status,
                )
                if event.status is not None
                else None
            ),
            metadata=dict(
                event.metadata,
            ),
        )

    @staticmethod
    def _map_metric(
        metric: Any,
    ) -> ExecutionMetricResponse:
        """Map an internal metric to a public response."""
        return ExecutionMetricResponse(
            metric_name=metric.metric_name,
            value=metric.value,
            unit=metric.unit,
            timestamp=metric.timestamp,
            execution_id=metric.execution_id,
            component=metric.component,
            metric_type=str(
                getattr(
                    metric.metric_type,
                    "value",
                    metric.metric_type,
                )
            ),
            metadata=dict(
                metric.metadata,
            ),
        )

    @staticmethod
    def _map_error(
        error: Any,
    ) -> ExecutionErrorTraceResponse:
        """Map an internal error to a public response."""
        return ExecutionErrorTraceResponse(
            error_id=error.error_id,
            execution_id=error.execution_id,
            timestamp=error.timestamp,
            component=error.component,
            stage=error.stage,
            severity=str(
                getattr(
                    error.severity,
                    "value",
                    error.severity,
                )
            ),
            error_type=error.error_type,
            message=error.message,
            recoverable=error.recoverable,
            metadata=dict(
                error.metadata,
            ),
        )

    def _latest_error(
        self,
        trace: ExecutionTrace,
    ):
        """Return the latest error mapped to the public contract."""
        if not trace.errors:
            return None

        error = max(
            trace.errors,
            key=lambda item: item.timestamp,
        )

        return {
            "code": "EXECUTION_FAILED",
            "message": error.message,
            "details": {
                "error_type": error.error_type,
                "severity": str(
                    getattr(
                        error.severity,
                        "value",
                        error.severity,
                    )
                ),
            },
        }
