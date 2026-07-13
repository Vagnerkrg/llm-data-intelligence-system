from dataclasses import dataclass, field


@dataclass(slots=True)
class AutonomyContext:
    """
    Represents the operational context used by the agent
    to observe and improve its own behavior.

    Stores execution information, historical data,
    metrics and feedback required for autonomous reflection.
    """

    context_id: str
    execution_id: str

    goal: str | None = None
    current_state: str | None = None

    execution_history: list[str] = field(
        default_factory=list
    )

    metrics: dict[str, float] = field(
        default_factory=dict
    )

    feedback: list[str] = field(
        default_factory=list
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )