from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
import uuid


class ExecutionEventType(str, Enum):
    """
    Defines execution lifecycle events.
    """

    STARTED = "started"
    STEP_STARTED = "step_started"
    STEP_COMPLETED = "step_completed"
    STEP_FAILED = "step_failed"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class ExecutionEvent:
    """
    Represents an atomic event generated during execution.
    """

    execution_id: str
    event_type: ExecutionEventType
    component: str
    payload: dict[str, Any] = field(default_factory=dict)

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )