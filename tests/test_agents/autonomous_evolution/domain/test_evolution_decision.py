import pytest

from src.agents.autonomous_evolution.domain import (
    EvolutionAction,
    EvolutionDecision,
    EvolutionEvidence,
    EvolutionStatus,
)


def test_evolution_decision_creation() -> None:
    decision = EvolutionDecision(
        should_evolve=True,
        confidence=0.87,
        status=EvolutionStatus.PROPOSED,
        reason="Sufficient evidence for adaptation.",
    )

    assert decision.should_evolve is True
    assert decision.confidence == 0.87
    assert decision.status is EvolutionStatus.PROPOSED


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_evolution_decision_rejects_invalid_confidence(
    confidence: float,
) -> None:
    with pytest.raises(ValueError):
        EvolutionDecision(confidence=confidence)


def test_evolution_decision_adds_evidence() -> None:
    decision = EvolutionDecision()

    evidence = EvolutionEvidence(
        source="evaluation",
        signal="performance",
        value=0.7,
        confidence=0.9,
    )

    decision.add_evidence(evidence)

    assert len(decision.evidence) == 1
    assert decision.evidence[0] is evidence


def test_evolution_decision_accepts_action() -> None:
    action = EvolutionAction(
        action_type="adapt_behavior",
        target="agent",
    )

    decision = EvolutionDecision(
        should_evolve=True,
        action=action,
    )

    assert decision.action is action


def test_evolution_decision_serialization() -> None:
    decision = EvolutionDecision(
        should_evolve=True,
        confidence=0.8,
        status=EvolutionStatus.APPROVED,
        reason="Approved evolution.",
        evidence=[
            EvolutionEvidence(
                source="evaluation",
                signal="score",
                value=0.9,
                confidence=0.95,
            )
        ],
    )

    result = decision.to_dict()

    assert result["should_evolve"] is True
    assert result["confidence"] == 0.8
    assert result["status"] == "approved"
    assert len(result["evidence"]) == 1