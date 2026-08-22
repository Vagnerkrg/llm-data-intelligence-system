"""Execution trace service."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.observability.domain.enums import (
    ErrorSeverity,
    EventType,
    ExecutionStatus,
    MetricType,
)
from src.observability.domain.models import (
    ExecutionError,
    ExecutionEvent,
    ExecutionMetric,
    ExecutionState,
    ExecutionTrace,
)
from src.observability.services.execution_lifecycle import (
    ExecutionLifecycleService,
)


class ExecutionTraceService:
    """Create, manage and reconstruct execution traces.

    The service intentionally uses in-memory storage in V1.28.
    Durable persistence belongs to the Observability Storage issue.
    """

    def __init__(
        self,
        lifecycle_service: Optional[ExecutionLifecycleService] = None,
    ) -> None:
        self.lifecycle = lifecycle_service or ExecutionLifecycleService()

        self._traces: Dict[
            str,
            ExecutionTrace,
        ] = {}

    def create_trace(
        self,
        execution_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ExecutionTrace:
        """Create and register a new execution trace."""

        trace = self.lifecycle.create(
            execution_id=execution_id,
            correlation_id=correlation_id,
        )

        if metadata:
            trace.metadata.update(
                metadata,
            )

        self._register(trace)

        return self._copy_trace(trace)

    def start(
        self,
        execution_id: str,
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Start an execution and register its lifecycle event."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        self.lifecycle.start(
            trace,
            timestamp=timestamp,
        )

        self._record_lifecycle_event(
            trace=trace,
            event_type=EventType.EXECUTION_STARTED,
            timestamp=trace.started_at,
            status=trace.status,
            component="execution_trace_service",
            stage="lifecycle",
        )

        self._persist(trace)

        return self._copy_trace(trace)

    def complete(
        self,
        execution_id: str,
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Complete an execution and finalize its trace."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        self.lifecycle.complete(
            trace,
            timestamp=timestamp,
        )

        self._record_lifecycle_event(
            trace=trace,
            event_type=EventType.EXECUTION_COMPLETED,
            timestamp=trace.finished_at,
            status=trace.status,
            component="execution_trace_service",
            stage="lifecycle",
        )

        self._persist(trace)

        return self._copy_trace(trace)

    def fail(
        self,
        execution_id: str,
        error: Optional[ExecutionError] = None,
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Fail an execution and record its associated error."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        self.lifecycle.fail(
            trace,
            timestamp=timestamp,
        )

        if error is not None:
            self._validate_error(
                trace,
                error,
            )
            self.lifecycle.add_error(
                trace,
                error,
            )

        self._record_lifecycle_event(
            trace=trace,
            event_type=EventType.EXECUTION_FAILED,
            timestamp=trace.finished_at,
            status=trace.status,
            component="execution_trace_service",
            stage="lifecycle",
        )

        self._persist(trace)

        return self._copy_trace(trace)

    def cancel(
        self,
        execution_id: str,
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Cancel an execution."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        self.lifecycle.cancel(
            trace,
            timestamp=timestamp,
        )

        self._record_lifecycle_event(
            trace=trace,
            event_type=EventType.EXECUTION_CANCELLED,
            timestamp=trace.finished_at,
            status=trace.status,
            component="execution_trace_service",
            stage="lifecycle",
        )

        self._persist(trace)

        return self._copy_trace(trace)

    def update_state(
        self,
        execution_id: str,
        *,
        status: Optional[ExecutionStatus] = None,
        component: Optional[str] = None,
        stage: Optional[str] = None,
        step: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ExecutionTrace:
        """Register an explicit execution state change."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        state = ExecutionState(
            execution_id=trace.execution_id,
            status=status or trace.status,
            current_component=component,
            current_stage=stage,
            current_step=step,
            started_at=trace.started_at,
            updated_at=timestamp or datetime.now().astimezone(),
            metadata=metadata or {},
        )

        trace.add_state(state)

        self._persist(trace)

        return self._copy_trace(trace)

    def record_event(
        self,
        execution_id: str,
        event_type: EventType,
        component: str,
        *,
        stage: Optional[str] = None,
        status: Optional[ExecutionStatus] = None,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ExecutionEvent:
        """Record an event associated with an execution."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        event = ExecutionEvent(
            execution_id=trace.execution_id,
            event_type=event_type,
            timestamp=timestamp or datetime.now().astimezone(),
            component=component,
            stage=stage,
            status=status,
            metadata=metadata or {},
        )

        self.lifecycle.add_event(
            trace,
            event,
        )

        self._persist(trace)

        return deepcopy(event)

    def record_metric(
        self,
        execution_id: str,
        metric_name: str,
        value: float,
        unit: str,
        component: str,
        *,
        metric_type: MetricType = MetricType.VALUE,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ExecutionMetric:
        """Record a metric associated with an execution."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        metric = ExecutionMetric(
            metric_name=metric_name,
            value=value,
            unit=unit,
            timestamp=timestamp or datetime.now().astimezone(),
            execution_id=trace.execution_id,
            component=component,
            metric_type=metric_type,
            metadata=metadata or {},
        )

        self.lifecycle.add_metric(
            trace,
            metric,
        )

        self._persist(trace)

        return deepcopy(metric)

    def record_error(
        self,
        execution_id: str,
        component: str,
        error_type: str,
        message: str,
        severity: ErrorSeverity,
        *,
        stage: Optional[str] = None,
        recoverable: bool = True,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ExecutionError:
        """Record an error without changing lifecycle state."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        error = ExecutionError(
            execution_id=trace.execution_id,
            timestamp=timestamp or datetime.now().astimezone(),
            component=component,
            stage=stage,
            severity=severity,
            error_type=error_type,
            message=message,
            recoverable=recoverable,
            metadata=metadata or {},
        )

        self.lifecycle.add_error(
            trace,
            error,
        )

        self._persist(trace)

        return deepcopy(error)

    def get_trace(
        self,
        execution_id: str,
    ) -> ExecutionTrace:
        """Return an isolated copy of a trace."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        return self._copy_trace(trace)

    def reconstruct(
        self,
        execution_id: str,
    ) -> ExecutionTrace:
        """Reconstruct a chronologically ordered execution trace."""

        trace = self.get_trace(
            execution_id,
        )

        trace.events.sort(
            key=lambda item: item.timestamp,
        )

        trace.metrics.sort(
            key=lambda item: item.timestamp,
        )

        trace.errors.sort(
            key=lambda item: item.timestamp,
        )

        trace.state_history.sort(
            key=lambda item: item.updated_at,
        )

        return trace

    def timeline(
        self,
        execution_id: str,
    ) -> List[Dict[str, Any]]:
        """Return all observable records in chronological order."""

        trace = self.reconstruct(
            execution_id,
        )

        records: List[Dict[str, Any]] = []

        for state in trace.state_history:
            records.append(
                {
                    "type": "state",
                    "timestamp": state.updated_at,
                    "data": state,
                }
            )

        for event in trace.events:
            records.append(
                {
                    "type": "event",
                    "timestamp": event.timestamp,
                    "data": event,
                }
            )

        for metric in trace.metrics:
            records.append(
                {
                    "type": "metric",
                    "timestamp": metric.timestamp,
                    "data": metric,
                }
            )

        for error in trace.errors:
            records.append(
                {
                    "type": "error",
                    "timestamp": error.timestamp,
                    "data": error,
                }
            )

        records.sort(
            key=lambda item: item["timestamp"],
        )

        return records

    def recover_incomplete(
        self,
        execution_id: str,
        *,
        message: str = "Execution finalized after incomplete lifecycle.",
        component: str = "execution_trace_service",
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Finalize an incomplete execution as failed."""

        trace = self._get_mutable_trace(
            execution_id,
        )

        if trace.status in {
            ExecutionStatus.COMPLETED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        }:
            return self._copy_trace(trace)

        error = ExecutionError(
            execution_id=trace.execution_id,
            timestamp=timestamp or datetime.now().astimezone(),
            component=component,
            stage="lifecycle",
            severity=ErrorSeverity.ERROR,
            error_type="IncompleteExecution",
            message=message,
            recoverable=False,
        )

        trace.add_error(
            error,
        )

        self.lifecycle.fail(
            trace,
            timestamp=timestamp,
        )

        self._record_lifecycle_event(
            trace=trace,
            event_type=EventType.EXECUTION_FAILED,
            timestamp=trace.finished_at,
            status=trace.status,
            component=component,
            stage="recovery",
            metadata={
                "reason": "incomplete_execution",
            },
        )

        self._persist(trace)

        return self._copy_trace(trace)

    def exists(
        self,
        execution_id: str,
    ) -> bool:
        """Return whether an execution exists."""
        return execution_id in self._traces

    def count(self) -> int:
        """Return the number of registered executions."""
        return len(self._traces)

    def _record_lifecycle_event(
        self,
        *,
        trace: ExecutionTrace,
        event_type: EventType,
        timestamp: Optional[datetime],
        status: ExecutionStatus,
        component: str,
        stage: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Register a lifecycle event."""
        event = ExecutionEvent(
            execution_id=trace.execution_id,
            event_type=event_type,
            timestamp=timestamp or datetime.now().astimezone(),
            component=component,
            stage=stage,
            status=status,
            metadata=metadata or {},
        )

        trace.add_event(
            event,
        )

    def _register(
        self,
        trace: ExecutionTrace,
    ) -> None:
        """Register a new trace."""
        if trace.execution_id in self._traces:
            raise ValueError(f"Execution '{trace.execution_id}' already exists.")

        self._traces[trace.execution_id] = deepcopy(
            trace,
        )

    def _persist(
        self,
        trace: ExecutionTrace,
    ) -> None:
        """Store the current trace snapshot in memory."""
        self._traces[trace.execution_id] = deepcopy(
            trace,
        )

    def _get_mutable_trace(
        self,
        execution_id: str,
    ) -> ExecutionTrace:
        """Get an internal mutable trace."""
        if execution_id not in self._traces:
            raise KeyError(f"Execution '{execution_id}' not found.")

        return self._traces[execution_id]

    def _copy_trace(
        self,
        trace: ExecutionTrace,
    ) -> ExecutionTrace:
        """Return an isolated deep copy."""
        return deepcopy(trace)

    @staticmethod
    def _validate_error(
        trace: ExecutionTrace,
        error: ExecutionError,
    ) -> None:
        """Validate error correlation before recording."""
        if error.execution_id != trace.execution_id:
            raise ValueError("Error execution_id must match trace execution_id.")
