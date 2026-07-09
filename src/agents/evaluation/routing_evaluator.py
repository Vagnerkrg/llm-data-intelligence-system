from dataclasses import dataclass
from datetime import datetime



@dataclass
class RoutingEvaluation:
    """
    Represents a routing decision evaluation.
    """

    question: str

    selected_tool: str | None

    confidence: float

    success: bool

    timestamp: datetime