from dataclasses import dataclass, field


@dataclass(slots=True)
class DecisionContext:
    """
    Represents the cognitive context where a decision is made.

    Contains the goal, constraints, available capabilities,
    tools and additional contextual information.
    """

    goal: str
    constraints: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    available_tools: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)