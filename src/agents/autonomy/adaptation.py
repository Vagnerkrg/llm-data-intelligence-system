from dataclasses import dataclass, field


@dataclass(slots=True)
class AdaptationStrategy:
    """
    Represents a possible behavioral adaptation strategy.

    Defines a proposed improvement based on learning signals,
    including expected effects and confidence level.
    """

    strategy_id: str
    learning_signal_id: str

    trigger: str

    action: str

    expected_effect: str

    confidence: float = 0.0

    metadata: dict[str, str] = field(
        default_factory=dict
    )