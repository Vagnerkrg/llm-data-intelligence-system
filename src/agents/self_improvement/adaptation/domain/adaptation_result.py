from dataclasses import dataclass

from .adaptation_action import AdaptationAction


@dataclass
class AdaptationResult:
    """
    Result generated after applying an adaptation.
    """

    success: bool

    action: AdaptationAction

    message: str