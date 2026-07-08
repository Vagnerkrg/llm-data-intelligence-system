from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntelligenceResponse:

    answer: str

    source: str | None = None

    confidence: float | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )