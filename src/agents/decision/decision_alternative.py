from dataclasses import dataclass, field


@dataclass(slots=True)
class DecisionAlternative:
    """
    Represents a possible option considered during decision making.

    An alternative describes a potential strategy before
    the final decision selection.
    """

    name: str
    description: str
    expected_outcome: str
    estimated_cost: float = 0.0
    confidence: float = 0.0
    metadata: dict[str, str] = field(default_factory=dict)