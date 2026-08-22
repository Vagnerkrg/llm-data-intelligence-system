from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class LearningPattern:
    """
    Representa um padrão aprendido pelo sistema cognitivo.

    Um padrão representa uma informação extraída
    de experiências, feedbacks ou avaliações.
    """

    pattern_id: str
    description: str
    frequency: int
    confidence: float
    metadata: Dict[str, Any]

    created_at: datetime = datetime.now()

    def increase_frequency(self) -> None:
        """
        Incrementa a frequência de ocorrência do padrão.
        """
        self.frequency += 1

    def strengthen(self, value: float) -> None:
        """
        Aumenta a confiança do padrão aprendido.
        """

        self.confidence = min(1.0, self.confidence + value)

    def is_reliable(self) -> bool:
        """
        Verifica se o padrão atingiu nível confiável.
        """

        return self.confidence >= 0.7
