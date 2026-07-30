from dataclasses import dataclass
from datetime import datetime


@dataclass
class ImprovementFeedback:
    """
    Registro de melhoria derivado de experiência anterior.
    """

    improvement_id: str
    feedback_id: str
    action: str
    expected_result: str
    created_at: datetime

    def matches_feedback(self, feedback_id: str) -> bool:
        return self.feedback_id == feedback_id