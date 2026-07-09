from dataclasses import dataclass


@dataclass
class RoutingResult:
    """
    Represents the result of a routing decision.
    """

    tool: str | None

    confidence: float

    reason: str