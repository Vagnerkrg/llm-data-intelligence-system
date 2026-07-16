from dataclasses import dataclass

from ..domain.adaptation_context import AdaptationContext


@dataclass
class AdaptationRequest:
    """
    Contract representing an adaptation request.
    """

    context: AdaptationContext
    target: str