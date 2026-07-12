from dataclasses import dataclass, field
from typing import Any, Dict, List

from src.agents.execution.execution_status import (
    ExecutionStatus,
)

from src.agents.execution.execution_event import (
    ExecutionEvent,
)

from src.agents.execution.execution_metrics import (
    ExecutionMetrics,
)


@dataclass
class ExecutionState:
    """
    Represents the current lifecycle state
    of an execution.
    """

    execution_id: str

    status: ExecutionStatus = (
        ExecutionStatus.PENDING
    )

    current_step_id: str | None = None

    events: List[ExecutionEvent] = field(
        default_factory=list
    )

    metrics: ExecutionMetrics = field(
        default_factory=ExecutionMetrics
    )

    results: List[Any] = field(
        default_factory=list
    )

    metadata: Dict[str, Any] = field(
        default_factory=dict
    )