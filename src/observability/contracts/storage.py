"""Persistence contracts for the Observability Layer."""

from __future__ import annotations

from typing import List, Optional, Protocol

from src.observability.domain.models import (
    ExecutionError,
    ExecutionEvent,
    ExecutionMetric,
    ExecutionTrace,
)


class TraceRepository(Protocol):
    """Repository contract for execution traces."""

    def save(
        self,
        trace: ExecutionTrace,
    ) -> ExecutionTrace:
        """Persist an execution trace."""
        ...

    def get(
        self,
        execution_id: str,
    ) -> Optional[ExecutionTrace]:
        """Retrieve a trace by execution ID."""
        ...

    def list(
        self,
        *,
        limit: Optional[int] = None,
    ) -> List[ExecutionTrace]:
        """List stored traces."""
        ...

    def delete(
        self,
        execution_id: str,
    ) -> bool:
        """Delete a trace."""
        ...


class EventRepository(Protocol):
    """Repository contract for execution events."""

    def save(
        self,
        event: ExecutionEvent,
    ) -> ExecutionEvent:
        """Persist an event."""
        ...

    def get_by_execution_id(
        self,
        execution_id: str,
    ) -> List[ExecutionEvent]:
        """Retrieve events for an execution."""
        ...

    def delete_by_execution_id(
        self,
        execution_id: str,
    ) -> int:
        """Delete events for an execution."""
        ...


class MetricsRepository(Protocol):
    """Repository contract for execution metrics."""

    def save(
        self,
        metric: ExecutionMetric,
    ) -> ExecutionMetric:
        """Persist a metric."""
        ...

    def get_by_execution_id(
        self,
        execution_id: str,
    ) -> List[ExecutionMetric]:
        """Retrieve metrics for an execution."""
        ...

    def delete_by_execution_id(
        self,
        execution_id: str,
    ) -> int:
        """Delete metrics for an execution."""
        ...


class ErrorRepository(Protocol):
    """Repository contract for execution errors."""

    def save(
        self,
        error: ExecutionError,
    ) -> ExecutionError:
        """Persist an error."""
        ...

    def get_by_execution_id(
        self,
        execution_id: str,
    ) -> List[ExecutionError]:
        """Retrieve errors for an execution."""
        ...

    def delete_by_execution_id(
        self,
        execution_id: str,
    ) -> int:
        """Delete errors for an execution."""
        ...


class ObservabilityRepository(Protocol):
    """
    Aggregate persistence contract for Observability.

    This contract represents the storage boundary consumed by
    application services.
    """

    def save_trace(
        self,
        trace: ExecutionTrace,
    ) -> ExecutionTrace:
        """Persist the complete trace."""
        ...

    def get_trace(
        self,
        execution_id: str,
    ) -> Optional[ExecutionTrace]:
        """Retrieve the complete trace."""
        ...

    def list_traces(
        self,
        *,
        limit: Optional[int] = None,
    ) -> List[ExecutionTrace]:
        """Retrieve execution history."""
        ...

    def exists(
        self,
        execution_id: str,
    ) -> bool:
        """Check whether an execution exists."""
        ...

    def delete_trace(
        self,
        execution_id: str,
    ) -> bool:
        """Delete a complete execution trace."""
        ...
