"""Structured event emitter."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from src.observability.domain.enums import (
    EventType,
    ExecutionStatus,
)
from src.observability.domain.models import ExecutionEvent

if TYPE_CHECKING:
    from .structured_event import StructuredEventService


class EventEmissionError(RuntimeError):
    """Raised when a structured event cannot be emitted."""


class EventEmitter:
    """Emit structured events through StructuredEventService."""

    def __init__(
        self,
        service: "StructuredEventService",
    ) -> None:
        self.service = service

    def emit(
        self,
        execution_id: str,
        event_type: EventType,
        component: str,
        *,
        stage: Optional[str] = None,
        status: Optional[ExecutionStatus] = None,
        metadata: Optional[dict] = None,
        deduplication_key: Optional[str] = None,
    ) -> ExecutionEvent:
        """Emit one validated structured event."""
        try:
            return self.service.emit(
                execution_id=execution_id,
                event_type=event_type,
                component=component,
                stage=stage,
                status=status,
                metadata=metadata,
                deduplication_key=deduplication_key,
            )
        except Exception as exc:
            raise EventEmissionError(
                f"Failed to emit event '{event_type.value}' "
                f"for execution '{execution_id}'."
            ) from exc

    def try_emit(
        self,
        execution_id: str,
        event_type: EventType,
        component: str,
        *,
        stage: Optional[str] = None,
        status: Optional[ExecutionStatus] = None,
        metadata: Optional[dict] = None,
        deduplication_key: Optional[str] = None,
    ) -> Optional[ExecutionEvent]:
        """Attempt emission without breaking caller flow."""
        try:
            return self.emit(
                execution_id=execution_id,
                event_type=event_type,
                component=component,
                stage=stage,
                status=status,
                metadata=metadata,
                deduplication_key=deduplication_key,
            )
        except EventEmissionError:
            return None
