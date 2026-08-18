import pytest

from src.agents.cognitive_learning.domain.learning_outcome import (
    LearningOutcome,
)
from src.agents.cognitive_learning.integration.learning_knowledge_integrator import (
    LearningKnowledgeIntegrator,
)
from src.agents.self_improvement.knowledge.domain.knowledge_type import (
    KnowledgeType,
)
from src.agents.self_improvement.knowledge.services.knowledge_repository import (
    KnowledgeRepository,
)


def _outcome(
    *,
    experience_id: str = "exp-1",
    knowledge_candidate: str = "stable strategy",
    confidence: float = 0.9,
    recommendation: str = "reuse stable strategy",
    metadata: dict | None = None,
) -> LearningOutcome:
    return LearningOutcome(
        experience_id=experience_id,
        learned_pattern=knowledge_candidate,
        knowledge_candidate=knowledge_candidate,
        confidence=confidence,
        recommendation=recommendation,
        metadata=metadata or {},
    )


def test_creates_new_knowledge_from_learning_outcome():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    result = integrator.integrate(_outcome())

    assert result.created
    assert repository.count() == 1
    assert result.knowledge.title == "stable strategy"
    assert result.knowledge.description == "reuse stable strategy"
    assert result.knowledge.confidence == 0.9


def test_preserves_learning_provenance():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    result = integrator.integrate(
        _outcome(experience_id="experience-42")
    )

    assert result.knowledge.metadata["experience_id"] == (
        "experience-42"
    )
    assert result.knowledge.metadata["source"] == (
        "cognitive_learning"
    )


def test_preserves_confidence():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    result = integrator.integrate(
        _outcome(confidence=0.73)
    )

    assert result.knowledge.confidence == 0.73


def test_detects_redundant_knowledge():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    first = integrator.integrate(_outcome())

    second = integrator.integrate(
        _outcome(experience_id="exp-2")
    )

    assert first.created
    assert second.duplicated
    assert repository.count() == 1


def test_updates_existing_knowledge():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    integrator.integrate(
        _outcome(
            confidence=0.7,
            recommendation="initial strategy",
        )
    )

    result = integrator.integrate(
        _outcome(
            experience_id="exp-2",
            confidence=0.95,
            recommendation="improved strategy",
        )
    )

    assert result.updated
    assert repository.count() == 1
    assert result.knowledge.description == "improved strategy"
    assert result.knowledge.confidence == 0.95


def test_does_not_reduce_existing_confidence():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    integrator.integrate(
        _outcome(confidence=0.95)
    )

    result = integrator.integrate(
        _outcome(
            experience_id="exp-2",
            confidence=0.7,
            recommendation="different recommendation",
        )
    )

    assert result.updated
    assert result.knowledge.confidence == 0.95


def test_resolves_strategy_knowledge_type():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    result = integrator.integrate(
        _outcome(
            metadata={"signal_type": "strategy"}
        )
    )

    assert result.knowledge.knowledge_type == (
        KnowledgeType.STRATEGY
    )


def test_resolves_insight_knowledge_type():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    result = integrator.integrate(
        _outcome(
            metadata={"signal_type": "insight"}
        )
    )

    assert result.knowledge.knowledge_type == (
        KnowledgeType.INSIGHT
    )


def test_defaults_unknown_signal_to_pattern():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    result = integrator.integrate(
        _outcome(
            metadata={"signal_type": "unknown"}
        )
    )

    assert result.knowledge.knowledge_type == (
        KnowledgeType.PATTERN
    )


def test_rejects_invalid_outcome():
    integrator = LearningKnowledgeIntegrator()

    with pytest.raises(
        ValueError,
        match="outcome must be a LearningOutcome",
    ):
        integrator.integrate("invalid")


def test_rejects_missing_knowledge_candidate():
    integrator = LearningKnowledgeIntegrator()

    outcome = LearningOutcome(
        experience_id="exp-1",
        learned_pattern="pattern",
        knowledge_candidate="",
        confidence=0.8,
        recommendation="recommendation",
    )

    with pytest.raises(
        ValueError,
        match="knowledge_candidate must not be empty",
    ):
        integrator.integrate(outcome)


def test_integrates_multiple_outcomes_deterministically():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    outcomes = [
        _outcome(
            experience_id="exp-1",
            knowledge_candidate="pattern A",
        ),
        _outcome(
            experience_id="exp-2",
            knowledge_candidate="pattern B",
        ),
        _outcome(
            experience_id="exp-3",
            knowledge_candidate="pattern A",
        ),
    ]

    results = integrator.integrate_many(outcomes)

    assert [result.action for result in results] == [
        "created",
        "created",
        "duplicate",
    ]
    assert repository.count() == 2


def test_preserves_metadata_from_learning_outcome():
    repository = KnowledgeRepository()
    integrator = LearningKnowledgeIntegrator(repository)

    result = integrator.integrate(
        _outcome(
            metadata={
                "signal_type": "strategy",
                "impact": "high",
                "custom": "value",
            }
        )
    )

    assert result.knowledge.metadata["signal_type"] == "strategy"
    assert result.knowledge.metadata["impact"] == "high"
    assert result.knowledge.metadata["custom"] == "value"
    assert result.knowledge.metadata["source"] == (
        "cognitive_learning"
    )