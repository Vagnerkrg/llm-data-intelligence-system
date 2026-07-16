from dataclasses import dataclass, field


@dataclass
class ExecutionPerformanceReport:
    """
    Represents the performance analysis of an execution.
    """

    execution_id: str

    duration_ms: float | int | None = None

    efficiency_score: float = 0.0

    status: str = "unknown"

    issues: list[str] = field(
        default_factory=list
    )