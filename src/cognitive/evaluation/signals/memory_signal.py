from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MemorySignal:
    """
    Sinal utilizado para comunicação
    com a camada de memória cognitiva.
    """

    action: str

    content: str

    importance: float = 0.0

    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value