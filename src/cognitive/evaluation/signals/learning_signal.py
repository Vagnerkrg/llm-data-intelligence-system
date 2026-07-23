from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class LearningSignal:
    """
    Representa um aprendizado identificado
    durante uma avaliação cognitiva.
    """

    source: str

    knowledge: str

    confidence: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value