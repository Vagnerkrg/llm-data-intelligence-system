from dataclasses import asdict, dataclass, field
from typing import Any

from .evolution_action import EvolutionAction
from .evolution_evidence import EvolutionEvidence
from .evolution_status import EvolutionStatus


@dataclass(slots=True)
class EvolutionDecision:
    """
    Represents the decision produced by the autonomous evolution process.

    The decision stores the outcome and supporting evidence but does not
    contain the logic required to calculate that outcome.
    """

    should_evolve: bool = False
    confidence: float = 0.0
    status: EvolutionStatus = EvolutionStatus.PENDING
    reason: str = ""
    evidence: list[EvolutionEvidence] = field(default_factory=list)
    action: EvolutionAction | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Evolution decision confidence must be between 0.0 and 1.0."
            )

        if not isinstance(self.status, EvolutionStatus):
            raise TypeError("status must be an EvolutionStatus instance.")

        if self.action is not None and not isinstance(
            self.action,
            EvolutionAction,
        ):
            raise TypeError("action must be an EvolutionAction instance or None.")

        for item in self.evidence:
            if not isinstance(item, EvolutionEvidence):
                raise TypeError(
                    "evidence must contain only EvolutionEvidence instances."
                )

    def add_evidence(self, evidence: EvolutionEvidence) -> None:
        """
        Add supporting evidence to the evolution decision.
        """
        if not isinstance(evidence, EvolutionEvidence):
            raise TypeError("evidence must be an EvolutionEvidence instance.")

        self.evidence.append(evidence)

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the evolution decision into a dictionary.
        """
        data = asdict(self)
        data["status"] = self.status.value

        return data
