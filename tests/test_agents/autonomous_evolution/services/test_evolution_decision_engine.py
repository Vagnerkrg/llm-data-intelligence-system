import pytest

from src.agents.autonomous_evolution.domain import (
    EvolutionContext,
    EvolutionStatus,
)
from src.agents.autonomous_evolution.services import (
    EvolutionDecisionEngine,
)


def test_engine_requires_evolution_context() -> None:
    engine = EvolutionDecisionEngine()

    with pytest.raises(TypeError):
        engine.decide({"score": 0.8})


def test_engine_returns_pending_when_evidence_is_missing() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(EvolutionContext())

    assert decision.should_evolve is False
    assert decision.status is EvolutionStatus.PENDING
    assert decision.confidence == 0.0
    assert decision.evidence == []


def test_engine_returns_pending_with_insufficient_evidence() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            evaluation_information={
                "overall_score": 0.9,
                "confidence": 0.9,
            }
        )
    )

    assert decision.should_evolve is False
    assert decision.status is EvolutionStatus.PENDING
    assert len(decision.evidence) == 1


def test_engine_returns_pending_when_confidence_is_too_low() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            evaluation_information={
                "overall_score": 0.9,
                "confidence": 0.4,
            },
            learning_information={
                "score": 0.9,
                "confidence": 0.5,
            },
        )
    )

    assert decision.should_evolve is False
    assert decision.status is EvolutionStatus.PENDING
    assert decision.confidence == pytest.approx(0.45)


def test_engine_proposes_evolution_when_criteria_are_met() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            evaluation_information={
                "overall_score": 0.9,
                "confidence": 0.9,
            },
            learning_information={
                "score": 0.8,
                "confidence": 0.8,
            },
        )
    )

    assert decision.should_evolve is True
    assert decision.status is EvolutionStatus.PROPOSED
    assert decision.confidence == pytest.approx(0.85)
    assert len(decision.evidence) == 2


def test_engine_rejects_low_average_evidence_strength() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            evaluation_information={
                "overall_score": 0.6,
                "confidence": 0.9,
            },
            learning_information={
                "score": 0.7,
                "confidence": 0.9,
            },
        )
    )

    assert decision.should_evolve is False
    assert decision.status is EvolutionStatus.PENDING
    assert decision.confidence == pytest.approx(0.9)


def test_engine_processes_multiple_evidence_items() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            learning_information=[
                {
                    "score": 0.9,
                    "confidence": 0.9,
                },
                {
                    "score": 0.8,
                    "confidence": 0.8,
                },
            ]
        )
    )

    assert decision.should_evolve is True
    assert decision.status is EvolutionStatus.PROPOSED
    assert len(decision.evidence) == 2


def test_engine_processes_memory_and_knowledge_signals() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            memory_information={
                "relevance_score": 0.85,
                "confidence": 0.9,
            },
            knowledge_information={
                "quality_score": 0.8,
                "confidence": 0.9,
            },
        )
    )

    assert decision.should_evolve is True
    assert len(decision.evidence) == 2


def test_engine_processes_improvement_information() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            improvement_information={
                "effectiveness_score": 0.9,
                "confidence": 0.9,
            },
            evaluation_information={
                "overall_score": 0.85,
                "confidence": 0.85,
            },
        )
    )

    assert decision.should_evolve is True
    assert decision.status is EvolutionStatus.PROPOSED


def test_engine_ignores_invalid_scores() -> None:
    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            evaluation_information={
                "overall_score": 1.5,
                "confidence": 0.9,
            },
            learning_information={
                "score": "invalid",
                "confidence": 0.9,
            },
        )
    )

    assert decision.should_evolve is False
    assert decision.evidence == []


def test_engine_accepts_object_with_score_and_confidence() -> None:
    class Signal:
        score = 0.85
        confidence = 0.9

    engine = EvolutionDecisionEngine()

    decision = engine.decide(
        EvolutionContext(
            evaluation_information=Signal(),
            learning_information=Signal(),
        )
    )

    assert decision.should_evolve is True
    assert len(decision.evidence) == 2


@pytest.mark.parametrize(
    "kwargs",
    [
        {"min_evidence": 0},
        {"min_confidence": -0.1},
        {"min_confidence": 1.1},
        {"evolution_threshold": -0.1},
        {"evolution_threshold": 1.1},
    ],
)
def test_engine_rejects_invalid_configuration(
    kwargs: dict[str, float | int],
) -> None:
    with pytest.raises(ValueError):
        EvolutionDecisionEngine(**kwargs)
