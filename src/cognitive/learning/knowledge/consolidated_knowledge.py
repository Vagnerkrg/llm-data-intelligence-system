from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any


@dataclass
class ConsolidatedKnowledge:
    """
    Representa uma unidade de conhecimento
    consolidada pelo sistema cognitivo.
    """

    knowledge_id: str
    content: str
    source_pattern: str
    confidence: float

    metadata: Dict[str, Any] = field(default_factory=dict)

    usage_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def reinforce(self, value: float = 0.05) -> None:
        """
        Reforça a confiança do conhecimento.
        """

        self.confidence = min(1.0, self.confidence + value)

    def register_usage(self) -> None:
        """
        Registra utilização do conhecimento.
        """

        self.usage_count += 1

    def is_valid(self) -> bool:
        """
        Verifica se o conhecimento possui
        confiança suficiente.
        """

        return self.confidence >= 0.7
