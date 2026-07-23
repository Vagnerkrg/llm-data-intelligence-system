from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ImprovementSignal:
    """
    Sinal gerado quando uma capacidade precisa evoluir.
    """

    capability: str

    score: float

    reason: str

    priority: str = "medium"

    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value