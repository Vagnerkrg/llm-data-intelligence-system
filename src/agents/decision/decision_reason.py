from dataclasses import dataclass, field


@dataclass(slots=True)
class DecisionReason:
    """
    Represents the justification behind a cognitive decision.

    DecisionReason provides explainability by storing why
    a specific strategy was selected.
    """

    justification: str
    confidence: float
    evidence: list[str] = field(default_factory=list)