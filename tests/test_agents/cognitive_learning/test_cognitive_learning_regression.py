from src.agents.cognitive_learning.domain.learning_outcome import (
    LearningOutcome,
)
from src.agents.cognitive_learning.domain.learning_experience import (
    LearningExperience,
)
from src.agents.cognitive_learning.services.cognitive_learning_loop import (
    CognitiveLearningLoop,
)
from src.agents.cognitive_learning.services.learning_outcome_engine import (
    LearningOutcomeEngine,
)
from src.agents.cognitive_learning.services.learning_signal_processor import (
    LearningSignalProcessor,
)


def test_learning_signal_processor_is_deterministic():
    processor = LearningSignalProcessor()

    signals = [
        {
            "signal_type": "strategy",
            "pattern": "stable strategy",
            "confidence": 0.9,
            "impact": "high",
        },
        {
            "signal_type": "strategy",
            "pattern": "stable strategy",
            "confidence": 0.8,
            "impact": "medium",
        },
    ]

    first = processor.process(signals)
    second = processor.process(signals)

    assert first == second


def test_learning_outcome_engine_is_deterministic():
    engine = LearningOutcomeEngine()

    experience = LearningExperience(
        experience_id="exp-1",
        source="cognitive_evaluation",
        signal_type="strategy",
        pattern="stable strategy",
        outcome="observed",
        confidence=0.9,
        impact="high",
    )

    first = engine.evaluate([experience])
    second = engine.evaluate([experience])

    assert first == second


def test_learning_outcome_rejects_incomplete_data():
    engine = LearningOutcomeEngine()

    result = engine.evaluate(
        [
            None,
            "invalid",
            {
                "experience_id": "invalid",
            },
        ]
    )

    assert result == []


def test_learning_loop_preserves_isolation():
    loop = CognitiveLearningLoop()

    assert loop.cognitive_evaluator is not None
    assert loop.learning_signal_processor is not None
    assert loop.learning_outcome_engine is not None
    assert loop.knowledge_integrator is not None
    assert loop.experience_optimizer is not None
    assert loop.evolution_bridge is not None


def test_learning_outcome_serialization_is_stable():
    outcome = LearningOutcome(
        experience_id="exp-1",
        learned_pattern="effective: stable strategy",
        knowledge_candidate="strategy: effective: stable strategy",
        confidence=0.9,
        recommendation="Reuse this strategy.",
        metadata={
            "learning_type": "effective_behavior",
        },
    )

    expected = {
        "experience_id": "exp-1",
        "learned_pattern": "effective: stable strategy",
        "knowledge_candidate": ("strategy: effective: stable strategy"),
        "confidence": 0.9,
        "recommendation": "Reuse this strategy.",
        "metadata": {
            "learning_type": "effective_behavior",
        },
    }

    assert outcome.to_dict() == expected
