import pytest

from src.agents.cognitive_learning.domain import (
    LearningExperience,
)
from src.agents.cognitive_learning.services import (
    LearningOutcomeEngine,
)


def _experience(
    *,
    experience_id: str = "exp-1",
    signal_type: str = "strategy",
    pattern: str = "stable strategy",
    confidence: float = 0.9,
    impact: str = "high",
    source: str = "cognitive_evaluation",
) -> LearningExperience:
    return LearningExperience(
        experience_id=experience_id,
        source=source,
        signal_type=signal_type,
        pattern=pattern,
        outcome="observed",
        confidence=confidence,
        impact=impact,
    )


def test_evaluate_produces_learning_outcome():
    engine = LearningOutcomeEngine()

    result = engine.evaluate([_experience()])

    assert len(result) == 1

    outcome = result[0]

    assert outcome.experience_id == "exp-1"
    assert outcome.learned_pattern == "effective: stable strategy"
    assert outcome.knowledge_candidate == ("strategy: effective: stable strategy")
    assert outcome.confidence == 0.9
    assert outcome.recommendation
    assert outcome.metadata["learning_type"] == "effective_behavior"


def test_identifies_ineffective_behavior():
    engine = LearningOutcomeEngine()

    result = engine.evaluate(
        [
            _experience(
                pattern="failed reasoning strategy",
                confidence=0.8,
                impact="medium",
            )
        ]
    )

    assert len(result) == 1

    outcome = result[0]

    assert outcome.learned_pattern == ("ineffective: failed reasoning strategy")
    assert outcome.metadata["learning_type"] == "ineffective_behavior"
    assert outcome.recommendation == (
        "Avoid repeating this behavior and evaluate alternative strategies."
    )


def test_identifies_improvement_opportunity():
    engine = LearningOutcomeEngine()

    result = engine.evaluate(
        [
            _experience(
                pattern="new routing opportunity",
                confidence=0.8,
                impact="low",
            )
        ]
    )

    assert len(result) == 1

    outcome = result[0]

    assert outcome.learned_pattern == ("improvement: new routing opportunity")
    assert outcome.metadata["learning_type"] == ("improvement_opportunity")


def test_calculates_confidence_by_impact():
    engine = LearningOutcomeEngine()

    result = engine.evaluate(
        [
            _experience(
                experience_id="high",
                confidence=0.8,
                impact="high",
            ),
            _experience(
                experience_id="medium",
                confidence=0.8,
                impact="medium",
            ),
            _experience(
                experience_id="low",
                confidence=0.8,
                impact="low",
            ),
        ]
    )

    assert result[0].confidence == 0.8
    assert result[1].confidence == 0.72
    assert result[2].confidence == 0.6


def test_rejects_incomplete_experiences():
    with pytest.raises(ValueError, match="source must not be empty"):
        LearningExperience(
            experience_id="missing-source",
            source="",
            signal_type="strategy",
            pattern="stable strategy",
            outcome="observed",
            confidence=0.9,
            impact="high",
        )


def test_rejects_invalid_confidence():
    with pytest.raises(
        ValueError,
        match="confidence must be between 0 and 1",
    ):
        LearningExperience(
            experience_id="negative",
            source="cognitive_evaluation",
            signal_type="strategy",
            pattern="stable strategy",
            outcome="observed",
            confidence=-0.1,
            impact="high",
        )

    with pytest.raises(
        ValueError,
        match="confidence must be between 0 and 1",
    ):
        LearningExperience(
            experience_id="above-range",
            source="cognitive_evaluation",
            signal_type="strategy",
            pattern="stable strategy",
            outcome="observed",
            confidence=1.1,
            impact="high",
        )


def test_rejects_non_learning_experiences():
    engine = LearningOutcomeEngine()

    result = engine.evaluate(
        [
            {
                "experience_id": "invalid",
                "pattern": "some pattern",
            },
            None,
            "invalid",
        ]
    )

    assert result == []


def test_processing_is_deterministic():
    engine = LearningOutcomeEngine()

    experiences = [
        _experience(
            experience_id="exp-1",
            pattern="stable strategy",
            confidence=0.9,
            impact="high",
        ),
        _experience(
            experience_id="exp-2",
            pattern="failed strategy",
            confidence=0.8,
            impact="medium",
        ),
    ]

    first = engine.evaluate(experiences)
    second = engine.evaluate(experiences)

    assert first == second


def test_preserves_experience_identity():
    engine = LearningOutcomeEngine()

    result = engine.evaluate(
        [
            _experience(
                experience_id="unique-experience-42",
            )
        ]
    )

    assert result[0].experience_id == "unique-experience-42"


def test_preserves_source_and_impact_metadata():
    engine = LearningOutcomeEngine()

    result = engine.evaluate(
        [
            _experience(
                source="experience_optimization",
                impact="medium",
            )
        ]
    )

    assert result[0].metadata == {
        "learning_type": "effective_behavior",
        "impact": "medium",
        "source": "experience_optimization",
    }
