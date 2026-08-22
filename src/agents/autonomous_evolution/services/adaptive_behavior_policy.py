from src.agents.autonomous_evolution.domain.evolution_decision import (
    EvolutionDecision,
)
from src.agents.autonomous_evolution.domain.evolution_status import (
    EvolutionStatus,
)
from src.agents.self_improvement.adaptation.domain.adaptation_action import (
    AdaptationAction,
)
from src.agents.self_improvement.adaptation.domain.adaptation_type import (
    AdaptationType,
)


class AdaptiveBehaviorPolicy:
    """
    Controls whether an evolution decision can produce a behavioral
    adaptation action.

    The policy validates eligibility and safety constraints but does not
    execute the resulting adaptation.
    """

    DEFAULT_MIN_CONFIDENCE = 0.70
    HIGH_RISK_CONFIDENCE = 0.90
    MIN_EVIDENCE = 2

    HIGH_RISK_TYPES = {
        AdaptationType.TOOL_SELECTION,
        AdaptationType.EXECUTION_FLOW,
    }

    VALID_TARGETS = {
        "agent",
        "reasoning",
        "planning",
        "decision",
        "execution",
        "memory",
        "routing",
    }

    def __init__(
        self,
        min_confidence: float = DEFAULT_MIN_CONFIDENCE,
    ) -> None:
        if not 0.0 <= min_confidence <= 1.0:
            raise ValueError("min_confidence must be between 0.0 and 1.0.")

        self.min_confidence = min_confidence

    def evaluate(
        self,
        decision: EvolutionDecision,
        target: str,
        adaptation_type: AdaptationType = AdaptationType.BEHAVIOR,
        description: str | None = None,
    ) -> AdaptationAction | None:
        """
        Evaluate an evolution decision and produce a controlled
        AdaptationAction when eligible.

        Returns None when the proposed adaptation must be rejected.
        """
        if not isinstance(decision, EvolutionDecision):
            raise TypeError("decision must be an EvolutionDecision instance.")

        if not isinstance(adaptation_type, AdaptationType):
            raise TypeError("adaptation_type must be an AdaptationType instance.")

        normalized_target = target.strip().lower()

        if normalized_target not in self.VALID_TARGETS:
            return None

        if not decision.should_evolve:
            return None

        if decision.status not in {
            EvolutionStatus.PROPOSED,
            EvolutionStatus.APPROVED,
        }:
            return None

        if decision.confidence < self.min_confidence:
            return None

        if len(decision.evidence) < self.MIN_EVIDENCE:
            return None

        if any(
            evidence.confidence < self.min_confidence for evidence in decision.evidence
        ):
            return None

        if (
            adaptation_type in self.HIGH_RISK_TYPES
            and decision.confidence < self.HIGH_RISK_CONFIDENCE
        ):
            return None

        action_description = (
            description.strip()
            if description is not None and description.strip()
            else decision.reason.strip()
        )

        if not action_description:
            return None

        return AdaptationAction(
            adaptation_type=adaptation_type,
            target=normalized_target,
            description=action_description,
            priority=self._resolve_priority(
                decision.confidence,
                adaptation_type,
            ),
        )

    def _resolve_priority(
        self,
        confidence: float,
        adaptation_type: AdaptationType,
    ) -> str:
        """
        Determine adaptation priority deterministically.
        """
        if (
            adaptation_type in self.HIGH_RISK_TYPES
            or confidence >= self.HIGH_RISK_CONFIDENCE
        ):
            return "high"

        if confidence >= 0.80:
            return "medium"

        return "low"
