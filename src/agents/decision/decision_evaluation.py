from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass(slots=True)
class DecisionEvaluation:
    """
    Represents the evaluation of a completed decision.

    Stores the quality assessment, outcome comparison,
    and feedback generated after execution.
    """

    decision_id: str
    success: bool
    score: float
    expected_outcome: str
    observed_outcome: str

    feedback: list[str] = field(default_factory=list)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict[str, str] = field(
        default_factory=dict
    )

    def add_feedback(
        self,
        message: str
    ) -> None:
        """
        Add evaluation feedback.
        """
        self.feedback.append(message)

    def is_successful(
        self
    ) -> bool:
        """
        Return whether the decision achieved success.
        """
        return self.success

    def has_feedback(
        self
    ) -> bool:
        """
        Check whether feedback exists.
        """
        return len(self.feedback) > 0