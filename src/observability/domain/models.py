"""Core observability domain entities."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import ConfigDict, Field, field_validator, model_validator

from .base import SerializableModel
from .enums import (
    ErrorSeverity,
    EventType,
    ExecutionStatus,
    MetricType,
)


def utc_now() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


def new_execution_id() -> str:
    """Generate an execution identifier."""
    return f"exec_{uuid4().hex}"


def new_event_id() -> str:
    """Generate an event identifier."""
    return f"evt_{uuid4().hex}"


def new_error_id() -> str:
    """Generate an error identifier."""
    return f"err_{uuid4().hex}"


class ObservabilityContext(SerializableModel):
    """Correlation context shared across observable operations."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    execution_id: str = Field(
        default_factory=new_execution_id,
        min_length=1,
    )

    correlation_id: Optional[str] = Field(
        default=None,
        min_length=1,
    )

    parent_execution_id: Optional[str] = Field(
        default=None,
        min_length=1,
    )

    trace_id: Optional[str] = Field(
        default=None,
        min_length=1,
    )

    span_id: Optional[str] = Field(
        default=None,
        min_length=1,
    )

    metadata: Dict[str, Any] = Field(default_factory=dict)


class ExecutionState(SerializableModel):
    """Observable snapshot of an execution state."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    execution_id: str = Field(min_length=1)
    status: ExecutionStatus = ExecutionStatus.PENDING

    current_component: Optional[str] = None
    current_stage: Optional[str] = None
    current_step: Optional[str] = None

    started_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=utc_now)

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("started_at", "updated_at")
    @classmethod
    def normalize_timestamp(
        cls,
        value: Optional[datetime],
    ) -> Optional[datetime]:
        """Normalize timestamps to UTC."""
        if value is None:
            return None

        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)


class ExecutionEvent(SerializableModel):
    """Immutable event emitted during execution."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    event_id: str = Field(
        default_factory=new_event_id,
        min_length=1,
    )

    execution_id: str = Field(min_length=1)

    event_type: EventType

    timestamp: datetime = Field(default_factory=utc_now)

    component: str = Field(min_length=1)

    stage: Optional[str] = None

    status: Optional[ExecutionStatus] = None

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def normalize_timestamp(
        cls,
        value: datetime,
    ) -> datetime:
        """Normalize timestamp to UTC."""
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)


class ExecutionMetric(SerializableModel):
    """Immutable execution measurement."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    metric_name: str = Field(min_length=1)

    value: float

    unit: str = Field(min_length=1)

    timestamp: datetime = Field(default_factory=utc_now)

    execution_id: str = Field(min_length=1)

    component: str = Field(min_length=1)

    metric_type: MetricType = MetricType.VALUE

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def normalize_timestamp(
        cls,
        value: datetime,
    ) -> datetime:
        """Normalize timestamp to UTC."""
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)


class ExecutionError(SerializableModel):
    """Immutable observable execution error."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    error_id: str = Field(
        default_factory=new_error_id,
        min_length=1,
    )

    execution_id: str = Field(min_length=1)

    timestamp: datetime = Field(default_factory=utc_now)

    component: str = Field(min_length=1)

    stage: Optional[str] = None

    severity: ErrorSeverity

    error_type: str = Field(min_length=1)

    message: str = Field(min_length=1)

    recoverable: bool = True

    metadata: Dict[str, Any] = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def normalize_timestamp(
        cls,
        value: datetime,
    ) -> datetime:
        """Normalize timestamp to UTC."""
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)


class ExecutionTrace(SerializableModel):
    """Complete observable representation of one execution."""

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    execution_id: str = Field(
        default_factory=new_execution_id,
        min_length=1,
    )

    status: ExecutionStatus = ExecutionStatus.PENDING

    started_at: Optional[datetime] = None

    finished_at: Optional[datetime] = None

    events: List[ExecutionEvent] = Field(
        default_factory=list,
    )

    metrics: List[ExecutionMetric] = Field(
        default_factory=list,
    )

    errors: List[ExecutionError] = Field(
        default_factory=list,
    )

    state: Optional[ExecutionState] = None

    state_history: List[ExecutionState] = Field(
        default_factory=list,
    )

    context: Optional[ObservabilityContext] = None

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
    )

    @property
    def duration(self) -> Optional[float]:
        """Return execution duration in seconds."""
        if self.started_at is None or self.finished_at is None:
            return None

        return (self.finished_at - self.started_at).total_seconds()

    @model_validator(mode="after")
    def validate_invariants(self) -> "ExecutionTrace":
        """Validate domain invariants."""

        if (
            self.started_at is not None
            and self.finished_at is not None
            and self.finished_at < self.started_at
        ):
            raise ValueError("finished_at cannot be earlier than started_at.")

        if self.state is not None:
            if self.state.execution_id != self.execution_id:
                raise ValueError(
                    "ExecutionState.execution_id must match "
                    "ExecutionTrace.execution_id."
                )

        if self.context is not None:
            if self.context.execution_id != self.execution_id:
                raise ValueError(
                    "ObservabilityContext.execution_id must match "
                    "ExecutionTrace.execution_id."
                )

        for state in self.state_history:
            if state.execution_id != self.execution_id:
                raise ValueError(
                    "ExecutionState.execution_id must match "
                    "ExecutionTrace.execution_id."
                )

        for event in self.events:
            if event.execution_id != self.execution_id:
                raise ValueError(
                    "ExecutionEvent.execution_id must match "
                    "ExecutionTrace.execution_id."
                )

        for metric in self.metrics:
            if metric.execution_id != self.execution_id:
                raise ValueError(
                    "ExecutionMetric.execution_id must match "
                    "ExecutionTrace.execution_id."
                )

        for error in self.errors:
            if error.execution_id != self.execution_id:
                raise ValueError(
                    "ExecutionError.execution_id must match "
                    "ExecutionTrace.execution_id."
                )

        return self

    def attach_context(
        self,
        context: ObservabilityContext,
    ) -> "ExecutionTrace":
        """Attach correlation context to the execution."""

        if context.execution_id != self.execution_id:
            raise ValueError("Context execution_id must match trace execution_id.")

        self.context = context

        return self

    def start(
        self,
        timestamp: Optional[datetime] = None,
    ) -> "ExecutionTrace":
        """Move execution from pending to running."""

        if self.status != ExecutionStatus.PENDING:
            raise ValueError("Only a pending execution can be started.")

        self.started_at = timestamp or utc_now()
        self.status = ExecutionStatus.RUNNING

        self._sync_state()

        return self

    def complete(
        self,
        timestamp: Optional[datetime] = None,
    ) -> "ExecutionTrace":
        """Move execution from running to completed."""

        if self.status != ExecutionStatus.RUNNING:
            raise ValueError("Only a running execution can be completed.")

        finished_at = timestamp or utc_now()

        if self.started_at is None:
            raise ValueError("A running execution must have started_at.")

        if finished_at < self.started_at:
            raise ValueError("finished_at cannot be earlier than started_at.")

        self.finished_at = finished_at
        self.status = ExecutionStatus.COMPLETED

        self._sync_state()

        return self

    def fail(
        self,
        timestamp: Optional[datetime] = None,
    ) -> "ExecutionTrace":
        """Move execution to failed."""

        if self.status not in {
            ExecutionStatus.PENDING,
            ExecutionStatus.RUNNING,
        }:
            raise ValueError("Only pending or running executions can fail.")

        now = timestamp or utc_now()

        if self.started_at is None:
            self.started_at = now

        if now < self.started_at:
            raise ValueError("finished_at cannot be earlier than started_at.")

        self.finished_at = now
        self.status = ExecutionStatus.FAILED

        self._sync_state()

        return self

    def cancel(
        self,
        timestamp: Optional[datetime] = None,
    ) -> "ExecutionTrace":
        """Move execution to cancelled."""

        if self.status != ExecutionStatus.RUNNING:
            raise ValueError("Only a running execution can be cancelled.")

        if self.started_at is None:
            raise ValueError("A running execution must have started_at.")

        now = timestamp or utc_now()

        if now < self.started_at:
            raise ValueError("finished_at cannot be earlier than started_at.")

        self.finished_at = now
        self.status = ExecutionStatus.CANCELLED

        self._sync_state()

        return self

    def add_state(
        self,
        state: ExecutionState,
    ) -> "ExecutionTrace":
        """Register an execution state snapshot."""

        if state.execution_id != self.execution_id:
            raise ValueError("State execution_id must match trace execution_id.")

        self.state = state
        self.state_history.append(state)

        self.state_history.sort(
            key=lambda item: item.updated_at,
        )

        return self

    def add_event(
        self,
        event: ExecutionEvent,
    ) -> "ExecutionTrace":
        """Add an event to the trace."""

        if event.execution_id != self.execution_id:
            raise ValueError("Event execution_id must match trace execution_id.")

        self.events.append(event)

        self.events.sort(
            key=lambda item: item.timestamp,
        )

        return self

    def add_metric(
        self,
        metric: ExecutionMetric,
    ) -> "ExecutionTrace":
        """Add a metric to the trace."""

        if metric.execution_id != self.execution_id:
            raise ValueError("Metric execution_id must match trace execution_id.")

        self.metrics.append(metric)

        return self

    def add_error(
        self,
        error: ExecutionError,
    ) -> "ExecutionTrace":
        """Add an error to the trace."""

        if error.execution_id != self.execution_id:
            raise ValueError("Error execution_id must match trace execution_id.")

        self.errors.append(error)

        self.errors.sort(
            key=lambda item: item.timestamp,
        )

        return self

    def snapshot(self) -> ExecutionState:
        """Return a copy of the current execution state."""

        self._sync_state()

        if self.state is None:
            raise RuntimeError("Execution state could not be created.")

        return self.state.model_copy(deep=True)

    def _sync_state(self) -> None:
        """Synchronize current state and register its history."""

        state = ExecutionState(
            execution_id=self.execution_id,
            status=self.status,
            started_at=self.started_at,
            updated_at=utc_now(),
            metadata=self.metadata.copy(),
        )

        self.state = state
        self.state_history.append(state)
