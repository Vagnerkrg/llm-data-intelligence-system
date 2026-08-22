from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any


@dataclass
class ConsolidatedKnowledge:
    """
    Representa um conhecimento consolidado
    extraído de experiências anteriores.
    """

    knowledge_id: str

    content: str

    source_pattern: str

    confidence: float

    metadata: Dict[str, Any] = field(default_factory=dict)

    usage_count: int = 0

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def id(self) -> str:
        """
        Compatibilidade com consumidores
        que utilizam o identificador como 'id'.
        """

        return self.knowledge_id

    def increase_usage(self) -> None:
        """
        Incrementa o número de utilizações
        deste conhecimento.
        """

        self.usage_count += 1

    def update_confidence(self, confidence: float) -> None:
        """
        Atualiza nível de confiança
        do conhecimento.
        """

        self.confidence = confidence

    def add_metadata(self, key: str, value: Any) -> None:
        """
        Adiciona informação complementar.
        """

        self.metadata[key] = value

    def is_reliable(self, threshold: float = 0.7) -> bool:
        """
        Verifica se o conhecimento possui
        confiança suficiente.
        """

        return self.confidence >= threshold
