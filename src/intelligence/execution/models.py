from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ExecutionStep:
    """
    Represents a step inside an execution lifecycle.
    """

    component: str
    action: str
    output_data: dict | None = None
    status: str = "pending"

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class ExecutionMetric:
    """
    Represents a metric generated during an execution.

    Metrics can exist independently or be associated
    with a specific execution lifecycle.
    """

    metric_name: str
    metric_value: float | int

    execution_id: str | None = None

    category: str | None = None

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass
class ExecutionRecord:
    """
    Represents an execution lifecycle record.
    """

    execution_id: str
    request: str

    status: str = "running"

    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    finished_at: datetime | None = None

    steps: list[ExecutionStep] = field(
        default_factory=list
    )

    metrics: list[ExecutionMetric] = field(
        default_factory=list
    )