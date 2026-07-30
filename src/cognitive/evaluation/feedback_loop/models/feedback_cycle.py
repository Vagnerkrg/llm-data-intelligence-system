from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class FeedbackCycleStatus(str, Enum):
    CREATED = "created"
    PROCESSED = "processed"
    LEARNED = "learned"
    APPLIED = "applied"


@dataclass
class FeedbackCycle:
    """
    Representa o ciclo completo de evolução gerado
    a partir de um feedback cognitivo.
    """

    cycle_id: str
    evaluation_id: str
    status: FeedbackCycleStatus
    created_at: datetime

    def mark_processed(self) -> None:
        self.status = FeedbackCycleStatus.PROCESSED

    def mark_learned(self) -> None:
        self.status = FeedbackCycleStatus.LEARNED

    def mark_applied(self) -> None:
        self.status = FeedbackCycleStatus.APPLIED