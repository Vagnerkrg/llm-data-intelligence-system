from dataclasses import dataclass
from datetime import datetime


@dataclass
class RoutingFeedback:
    """
    Represents post-routing evaluation feedback.

    Stores the result of analyzing whether
    a routing decision was effective.
    """


    question: str

    selected_tool: str | None

    successful: bool

    confidence: float

    comment: str

    timestamp: datetime