"""Structured event service."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from src.observability.domain.enums import EventType, ExecutionStatus
from src.observability.domain.models import ExecutionEvent
from src.observability.services.execution_trace import (
    ExecutionTraceService,
)


class StructuredEventService:
    """Create, validate, correlate and retrieve structured events."""

    def __init__(
        self,
        trace_service: Optional[ExecutionTraceService] = None,
    ) -> None:
        self.trace_service = trace_service or ExecutionTraceService()

        self._deduplication_keys: Dict[
            str,
            Set[str],
        ] = {}

    def emit(
        self,
        execution_id: str,
        event_type: EventType,
        component: str,
        *,
        stage: Optional[str] = None,
        status: Optional[ExecutionStatus] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Validate and emit a structured event."""

        if not execution_id:
            raise ValueError("execution_id is required.")

        if not component:
            raise ValueError("component is required.")

        if deduplication_key is not None:
            if self._is_duplicate(
                execution_id,
                deduplication_key,
            ):
                raise ValueError(
                    f"Duplicate event detected for key '{deduplication_key}'."
                )

        event = ExecutionEvent(
            execution_id=execution_id,
            event_type=event_type,
            timestamp=self._normalize_timestamp(
                timestamp,
            ),
            component=component,
            stage=stage,
            status=status,
            metadata=deepcopy(
                metadata or {},
            ),
        )

        self.trace_service.get_trace(
            execution_id,
        )

        self.trace_service.record_event(
            execution_id=execution_id,
            event_type=event_type,
            component=component,
            stage=stage,
            status=status,
            timestamp=event.timestamp,
            metadata=event.metadata,
        )

        if deduplication_key is not None:
            self._register_deduplication_key(
                execution_id,
                deduplication_key,
            )

        return deepcopy(event)

    def emit_lifecycle(
        self,
        execution_id: str,
        event_type: EventType,
        *,
        status: Optional[ExecutionStatus] = None,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit an execution lifecycle event."""
        return self.emit(
            execution_id=execution_id,
            event_type=event_type,
            component="execution",
            stage="lifecycle",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def emit_reasoning(
        self,
        execution_id: str,
        event_type: EventType,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        status: Optional[ExecutionStatus] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit a reasoning event."""
        return self.emit(
            execution_id=execution_id,
            event_type=event_type,
            component="reasoning",
            stage="reasoning",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def emit_planning(
        self,
        execution_id: str,
        event_type: EventType,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        status: Optional[ExecutionStatus] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit a planning event."""
        return self.emit(
            execution_id=execution_id,
            event_type=event_type,
            component="planning",
            stage="planning",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def emit_execution(
        self,
        execution_id: str,
        event_type: EventType,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        status: Optional[ExecutionStatus] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit an execution-stage event."""
        return self.emit(
            execution_id=execution_id,
            event_type=event_type,
            component="execution",
            stage="execution",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def emit_tool(
        self,
        execution_id: str,
        event_type: EventType,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        status: Optional[ExecutionStatus] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit a tool-call event."""
        return self.emit(
            execution_id=execution_id,
            event_type=event_type,
            component="tool",
            stage="tool_call",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def emit_memory(
        self,
        execution_id: str,
        event_type: EventType,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        status: Optional[ExecutionStatus] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit a memory event."""
        return self.emit(
            execution_id=execution_id,
            event_type=event_type,
            component="memory",
            stage="memory",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def emit_knowledge(
        self,
        execution_id: str,
        event_type: EventType,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        status: Optional[ExecutionStatus] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit a knowledge event."""
        return self.emit(
            execution_id=execution_id,
            event_type=event_type,
            component="knowledge",
            stage="knowledge",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def emit_cognitive(
        self,
        execution_id: str,
        event_type: EventType,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        status: Optional[ExecutionStatus] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit a cognitive event."""
        return self.emit(
            execution_id=execution_id,
            event_type=event_type,
            component="cognitive",
            stage="cognitive",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def emit_error(
        self,
        execution_id: str,
        *,
        metadata: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None,
        status: Optional[ExecutionStatus] = ExecutionStatus.FAILED,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit an error event."""
        return self.emit(
            execution_id=execution_id,
            event_type=EventType.ERROR_OCCURRED,
            component="system",
            stage="error",
            status=status,
            metadata=metadata,
            timestamp=timestamp,
            deduplication_key=deduplication_key,
        )

    def get_events(
        self,
        execution_id: str,
    ) -> List[ExecutionEvent]:
        """Return events associated with an execution."""
        trace = self.trace_service.get_trace(
            execution_id,
        )

        return [deepcopy(event) for event in trace.events]

    def count(
        self,
        execution_id: str,
    ) -> int:
        """Return event count for an execution."""
        return len(
            self.get_events(
                execution_id,
            )
        )

    def has_duplicate(
        self,
        execution_id: str,
        deduplication_key: str,
    ) -> bool:
        """Check whether a deduplication key was registered."""
        return self._is_duplicate(
            execution_id,
            deduplication_key,
        )

    def _is_duplicate(
        self,
        execution_id: str,
        deduplication_key: str,
    ) -> bool:
        """Check deduplication state."""
        return deduplication_key in self._deduplication_keys.get(
            execution_id,
            set(),
        )

    def _register_deduplication_key(
        self,
        execution_id: str,
        deduplication_key: str,
    ) -> None:
        """Register a deduplication key."""
        self._deduplication_keys.setdefault(
            execution_id,
            set(),
        ).add(
            deduplication_key,
        )

    @staticmethod
    def _normalize_timestamp(
        timestamp: Optional[datetime],
    ) -> datetime:
        """Normalize timestamps to UTC."""
        value = timestamp or datetime.now(timezone.utc)

        if value.tzinfo is None:
            return value.replace(
                tzinfo=timezone.utc,
            )

        return value.astimezone(
            timezone.utc,
        )
