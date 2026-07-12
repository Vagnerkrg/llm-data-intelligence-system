from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any


class ExecutionEventType(str, Enum):
    """
    Types of events generated during execution lifecycle.
    """

    EXECUTION_STARTED = "execution_started"

    EXECUTION_COMPLETED = "execution_completed"

    EXECUTION_FAILED = "execution_failed"

    STEP_STARTED = "step_started"

    STEP_COMPLETED = "step_completed"

    STEP_FAILED = "step_failed"

    TOOL_STARTED = "tool_started"

    TOOL_COMPLETED = "tool_completed"

    RETRY_REQUESTED = "retry_requested"


@dataclass
class ExecutionEvent:
    """
    Represents an event generated during execution lifecycle.
    """

    event_type: ExecutionEventType

    message: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )