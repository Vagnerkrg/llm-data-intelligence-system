from dataclasses import dataclass

from ..domain.adaptation_result import AdaptationResult


@dataclass
class AdaptationResponse:
    """
    Contract representing adaptation execution response.
    """

    result: AdaptationResult