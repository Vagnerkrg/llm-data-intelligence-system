from dataclasses import dataclass
from datetime import datetime


@dataclass
class LearningFeedback:
    """
    Representa um sinal de aprendizado extraído
    do processo de avaliação.
    """

    feedback_id: str
    source: str
    signal: str
    impact: str
    created_at: datetime

    def is_high_impact(self) -> bool:
        return self.impact.lower() == "high"