from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ReflectionSignal:
    """
    Representa uma reflexão gerada
    após uma execução.
    """

    execution_id: str

    observation: str

    outcome: str

    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value