import pytest

from src.agents.autonomous_evolution.domain import (
    EvolutionDecision,
    EvolutionEvidence,
    EvolutionStatus,
)
from src.agents.autonomous_evolution.services import (
    AdaptiveBehaviorPolicy,
)
from src.agents.self_improvement.adaptation.domain.adaptation_type import (
    AdaptationType,
)


def build_valid_decision(
    confidence: float = 0.85,
    status: EvolutionStatus = EvolutionStatus.PROPOSED,
) -> EvolutionDecision:
    return EvolutionDecision(
        should_evolve=True,
        confidence=confidence,
        status=status,
        reason="Improve future agent behavior.",
        evidence=[
            EvolutionEvidence(
                source="evaluation",
                signal="quality",
                value=0.85,
                confidence=confidence,
            ),
            EvolutionEvidence(
                source="learning",
                signal="improvement",
                value=0.80,
                confidence=confidence,
            ),
        ],
    )


def test_policy_creates_behavior_adaptation() -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(),
        target="agent",
    )

    assert action is not None
    assert action.adaptation_type is AdaptationType.BEHAVIOR
    assert action.target == "agent"
    assert action.description == "Improve future agent behavior."
    assert action.priority == "medium"


def test_policy_accepts_approved_decision() -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(
            status=EvolutionStatus.APPROVED,
        ),
        target="planning",
        adaptation_type=AdaptationType.STRATEGY,
    )

    assert action is not None
    assert action.adaptation_type is AdaptationType.STRATEGY
    assert action.target == "planning"


def test_policy_rejects_decision_that_does_not_require_evolution() -> None:
    policy = AdaptiveBehaviorPolicy()

    decision = build_valid_decision()
    decision.should_evolve = False

    action = policy.evaluate(
        decision=decision,
        target="agent",
    )

    assert action is None


def test_policy_rejects_non_evolutive_status() -> None:
    policy = AdaptiveBehaviorPolicy()

    decision = build_valid_decision(
        status=EvolutionStatus.PENDING,
    )

    action = policy.evaluate(
        decision=decision,
        target="agent",
    )

    assert action is None


def test_policy_rejects_low_confidence() -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(confidence=0.69),
        target="agent",
    )

    assert action is None


def test_policy_rejects_insufficient_evidence() -> None:
    policy = AdaptiveBehaviorPolicy()

    decision = build_valid_decision()
    decision.evidence = decision.evidence[:1]

    action = policy.evaluate(
        decision=decision,
        target="agent",
    )

    assert action is None


def test_policy_rejects_low_confidence_evidence() -> None:
    policy = AdaptiveBehaviorPolicy()

    decision = build_valid_decision()
    decision.evidence[1].confidence = 0.69

    action = policy.evaluate(
        decision=decision,
        target="agent",
    )

    assert action is None


@pytest.mark.parametrize(
    "target",
    [
        "",
        "unknown",
        "database",
    ],
)
def test_policy_rejects_invalid_target(target: str) -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(),
        target=target,
    )

    assert action is None


def test_policy_normalizes_target() -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(),
        target="  Planning ",
    )

    assert action is not None
    assert action.target == "planning"


def test_policy_rejects_high_risk_adaptation_below_high_confidence() -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(confidence=0.85),
        target="execution",
        adaptation_type=AdaptationType.EXECUTION_FLOW,
    )

    assert action is None


def test_policy_allows_high_risk_adaptation_with_high_confidence() -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(confidence=0.95),
        target="execution",
        adaptation_type=AdaptationType.EXECUTION_FLOW,
    )

    assert action is not None
    assert action.adaptation_type is AdaptationType.EXECUTION_FLOW
    assert action.priority == "high"


def test_policy_resolves_high_priority_for_high_confidence() -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(confidence=0.90),
        target="agent",
    )

    assert action is not None
    assert action.priority == "high"


def test_policy_resolves_low_priority_for_low_eligible_confidence() -> None:
    policy = AdaptiveBehaviorPolicy(
        min_confidence=0.60,
    )

    action = policy.evaluate(
        decision=build_valid_decision(confidence=0.70),
        target="agent",
    )

    assert action is not None
    assert action.priority == "low"


def test_policy_uses_explicit_description() -> None:
    policy = AdaptiveBehaviorPolicy()

    action = policy.evaluate(
        decision=build_valid_decision(),
        target="reasoning",
        description="Increase reasoning verification.",
    )

    assert action is not None
    assert action.description == "Increase reasoning verification."


def test_policy_rejects_empty_description_when_reason_is_empty() -> None:
    policy = AdaptiveBehaviorPolicy()

    decision = build_valid_decision()
    decision.reason = ""

    action = policy.evaluate(
        decision=decision,
        target="agent",
        description="   ",
    )

    assert action is None


def test_policy_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError):
        AdaptiveBehaviorPolicy(
            min_confidence=1.1,
        )


def test_policy_requires_evolution_decision() -> None:
    policy = AdaptiveBehaviorPolicy()

    with pytest.raises(TypeError):
        policy.evaluate(
            decision="invalid",  # type: ignore[arg-type]
            target="agent",
        )


def test_policy_requires_adaptation_type() -> None:
    policy = AdaptiveBehaviorPolicy()

    with pytest.raises(TypeError):
        policy.evaluate(
            decision=build_valid_decision(),
            target="agent",
            adaptation_type="behavior",  # type: ignore[arg-type]
        )
