from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class EvaluationContext:
    """
    Contexto utilizado durante uma avaliação cognitiva.

    Armazena informações sobre o agente,
    execução avaliada e metadados.
    """

    agent_id: str
    execution_id: Optional[str] = None

    input_data: Any = None
    output_data: Any = None

    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_metadata(self, key: str, value: Any) -> None:
        self.metadata[key] = value

    def get_metadata(self, key: str, default=None):
        return self.metadata.get(key, default)