from dataclasses import dataclass, field


@dataclass(slots=True)
class LearningSignal:
    """
    Represents knowledge extracted from an agent experience.

    Stores patterns, impact and confidence information
    that can be used to improve future behavior.
    """

    signal_id: str
    reflection_id: str

    source: str

    pattern: str

    impact: str

    confidence: float = 0.0

    metadata: dict[str, str] = field(
        default_factory=dict
    )