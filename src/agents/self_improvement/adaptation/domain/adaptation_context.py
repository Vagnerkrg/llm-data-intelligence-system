from dataclasses import dataclass, field


@dataclass
class AdaptationContext:
    """
    Context used to decide and apply an adaptation.
    """

    source: str

    reason: str

    confidence: float

    metadata: dict = field(default_factory=dict)