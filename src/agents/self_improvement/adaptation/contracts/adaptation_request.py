from dataclasses import dataclass

from ..domain.adaptation_context import AdaptationContext


@dataclass
class AdaptationRequest:
    """
    Request received by the adaptation capability.
    """

    context: AdaptationContext

    target: str