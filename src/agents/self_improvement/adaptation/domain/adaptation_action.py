from dataclasses import dataclass

from .adaptation_type import AdaptationType


@dataclass
class AdaptationAction:
    """
    Represents an action that changes future agent behavior.
    """

    adaptation_type: AdaptationType

    target: str

    description: str

    priority: str = "medium"