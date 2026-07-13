from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import List, Optional

from .decision_reason import DecisionReason
from .decision_alternative import DecisionAlternative


@dataclass
class DecisionTrace:
    """
    Represents the cognitive path used to reach a decision.

    A DecisionTrace records:
    - when the decision process started;
    - reasoning factors;
    - alternatives considered;
    - selected alternative;
    - decision metadata.
    """

    decision_id: str
    reasons: List[DecisionReason] = field(default_factory=list)
    alternatives: List[DecisionAlternative] = field(default_factory=list)

    selected_alternative_id: Optional[str] = None

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

    metadata: dict = field(default_factory=dict)

    def add_reason(
        self,
        reason: DecisionReason
    ) -> None:
        """
        Add a reasoning factor to the decision trace.
        """
        self.reasons.append(reason)

    def add_alternative(
        self,
        alternative: DecisionAlternative
    ) -> None:
        """
        Add a considered alternative.
        """
        self.alternatives.append(alternative)

    def select_alternative(
        self,
        alternative_id: str
    ) -> None:
        """
        Register the selected alternative.
        """
        self.selected_alternative_id = alternative_id

    def has_selected_alternative(self) -> bool:
        """
        Check whether a decision path has a selected option.
        """
        return self.selected_alternative_id is not None

    def get_selected_alternative(
        self
    ) -> Optional[DecisionAlternative]:
        """
        Retrieve selected alternative from trace.
        """
        for alternative in self.alternatives:
            if alternative.name == self.selected_alternative_id:
                return alternative

        return None