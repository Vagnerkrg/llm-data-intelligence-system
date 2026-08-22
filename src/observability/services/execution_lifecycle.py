"""Execution lifecycle service."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from src.observability.domain.enums import ExecutionStatus
from src.observability.domain.models import (
    ExecutionError,
    ExecutionEvent,
    ExecutionMetric,
    ExecutionTrace,
    ObservabilityContext,
)


class ExecutionLifecycleService:
    """Coordinate execution lifecycle operations."""

    def create(
        self,
        execution_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> ExecutionTrace:
        """Create a new pending execution trace."""
        if execution_id is None:
            trace = ExecutionTrace()
        else:
            trace = ExecutionTrace(
                execution_id=execution_id,
            )

        trace.attach_context(
            ObservabilityContext(
                execution_id=trace.execution_id,
                correlation_id=correlation_id,
            )
        )

        return trace

    def start(
        self,
        trace: ExecutionTrace,
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Start an execution."""
        return trace.start(timestamp=timestamp)

    def complete(
        self,
        trace: ExecutionTrace,
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Complete an execution."""
        return trace.complete(timestamp=timestamp)

    def fail(
        self,
        trace: ExecutionTrace,
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Fail an execution."""
        return trace.fail(timestamp=timestamp)

    def cancel(
        self,
        trace: ExecutionTrace,
        timestamp: Optional[datetime] = None,
    ) -> ExecutionTrace:
        """Cancel an execution."""
        return trace.cancel(timestamp=timestamp)

    def add_event(
        self,
        trace: ExecutionTrace,
        event: ExecutionEvent,
    ) -> ExecutionTrace:
        """Add an event to an execution trace."""
        return trace.add_event(event)

    def add_metric(
        self,
        trace: ExecutionTrace,
        metric: ExecutionMetric,
    ) -> ExecutionTrace:
        """Add a metric to an execution trace."""
        return trace.add_metric(metric)

    def add_error(
        self,
        trace: ExecutionTrace,
        error: ExecutionError,
    ) -> ExecutionTrace:
        """Add an error to an execution trace."""
        return trace.add_error(error)

    def is_terminal(
        self,
        trace: ExecutionTrace,
    ) -> bool:
        """Return whether execution reached a terminal state."""
        return trace.status in {
            ExecutionStatus.COMPLETED,
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        }
