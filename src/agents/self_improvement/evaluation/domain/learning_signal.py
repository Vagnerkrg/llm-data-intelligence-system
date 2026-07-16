from dataclasses import dataclass


@dataclass(frozen=True)
class LearningSignal:
    """
    Represents a future improvement signal.

    This object prepares the integration
    with the Learning capability.
    """

    signal_type: str

    pattern: str

    confidence: float

    impact: str

    recommendation: str