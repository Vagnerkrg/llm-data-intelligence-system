from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict


@dataclass
class ExecutionMetrics:
    """
    Represents execution lifecycle metrics.
    """

    started_at: datetime | None = None

    completed_at: datetime | None = None

    total_steps: int = 0

    completed_steps: int = 0

    failed_steps: int = 0

    retry_count: int = 0

    tool_calls: int = 0

    metadata: Dict[str, object] = field(
        default_factory=dict
    )

    @property
    def duration_seconds(self) -> float | None:
        """
        Calculate execution duration.
        """

        if not self.started_at or not self.completed_at:
            return None

        return (
            self.completed_at - self.started_at
        ).total_seconds()