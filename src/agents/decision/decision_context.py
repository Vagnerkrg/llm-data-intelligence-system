from dataclasses import dataclass, field


@dataclass(slots=True)
class DecisionContext:
    """
    Represents the cognitive context where a decision is made.

    Supports both the new cognitive model (goal)
    and legacy decision execution contracts.
    """

    goal: str | None = None

    request_id: str | None = None
    objective: str | None = None

    constraints: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    available_tools: list[str] = field(default_factory=list)

    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """
        Maintains compatibility between objective and goal.
        """

        if self.goal is None and self.objective:
            self.goal = self.objective

        if self.objective is None and self.goal:
            self.objective = self.goal