import pytest

from src.agents.autonomous_evolution.domain import EvolutionEvidence


def test_evolution_evidence_creation() -> None:
    evidence = EvolutionEvidence(
        source="cognitive_evaluation",
        signal="reasoning_score",
        value=0.72,
        confidence=0.91,
    )

    assert evidence.source == "cognitive_evaluation"
    assert evidence.signal == "reasoning_score"
    assert evidence.value == 0.72
    assert evidence.confidence == 0.91


@pytest.mark.parametrize("confidence", [-0.1, 1.1])
def test_evolution_evidence_rejects_invalid_confidence(
    confidence: float,
) -> None:
    with pytest.raises(ValueError):
        EvolutionEvidence(
            source="evaluation",
            signal="score",
            confidence=confidence,
        )


def test_evolution_evidence_rejects_empty_source() -> None:
    with pytest.raises(ValueError):
        EvolutionEvidence(
            source="",
            signal="score",
        )


def test_evolution_evidence_rejects_empty_signal() -> None:
    with pytest.raises(ValueError):
        EvolutionEvidence(
            source="evaluation",
            signal="",
        )


def test_evolution_evidence_serialization() -> None:
    evidence = EvolutionEvidence(
        source="evaluation",
        signal="score",
        value=0.85,
        confidence=0.9,
        metadata={"metric": "reasoning"},
    )

    result = evidence.to_dict()

    assert result["source"] == "evaluation"
    assert result["signal"] == "score"
    assert result["value"] == 0.85
    assert result["confidence"] == 0.9
    assert result["metadata"]["metric"] == "reasoning"
