from src.agents.cognitive_learning.services import (
    LearningSignalProcessor,
)
from src.agents.self_improvement.evaluation.domain.learning_signal import (
    LearningSignal,
)


def test_process_learning_signals():
    processor = LearningSignalProcessor()

    signals = [
        LearningSignal(
            signal_type="tool_usage",
            pattern="high tool usage",
            confidence=0.8,
            impact="medium",
            recommendation="Review execution strategy.",
        )
    ]

    result = processor.process(signals)

    assert len(result) == 1
    assert result[0].signal_type == "tool_usage"
    assert result[0].pattern == "high tool usage"
    assert result[0].confidence == 0.8
    assert result[0].source == "cognitive_learning"


def test_rejects_insufficient_signals():
    processor = LearningSignalProcessor()

    signals = [
        LearningSignal(
            signal_type="strategy",
            pattern="weak pattern",
            confidence=0.49,
            impact="low",
            recommendation="Monitor.",
        ),
        LearningSignal(
            signal_type="",
            pattern="missing type",
            confidence=0.9,
            impact="medium",
            recommendation="Monitor.",
        ),
        LearningSignal(
            signal_type="strategy",
            pattern="",
            confidence=0.9,
            impact="medium",
            recommendation="Monitor.",
        ),
    ]

    assert processor.process(signals) == []


def test_consolidates_related_signals():
    processor = LearningSignalProcessor()

    signals = [
        {
            "source": "experience_optimization",
            "signal_type": "optimization_signal",
            "pattern": "effective strategy",
            "confidence": 0.8,
            "impact": "medium",
        },
        {
            "source": "experience_optimization",
            "signal_type": "optimization_signal",
            "pattern": "effective strategy",
            "confidence": 1.0,
            "impact": "high",
        },
    ]

    result = processor.process(signals)

    assert len(result) == 1
    assert result[0].confidence == 0.9
    assert result[0].impact == "high"


def test_processes_known_signal_sources():
    processor = LearningSignalProcessor()

    signals = [
        {
            "signal_type": "cognitive_evaluation",
            "pattern": "evaluation pattern",
            "confidence": 0.8,
            "impact": "medium",
        },
        {
            "signal_type": "optimization_signal",
            "pattern": "optimization pattern",
            "confidence": 0.8,
            "impact": "medium",
        },
        {
            "signal_type": "execution_outcome",
            "pattern": "execution pattern",
            "confidence": 0.8,
            "impact": "medium",
        },
        {
            "signal_type": "reflection_insight",
            "pattern": "reflection pattern",
            "confidence": 0.8,
            "impact": "medium",
        },
        {
            "signal_type": "evolution_decision",
            "pattern": "evolution pattern",
            "confidence": 0.8,
            "impact": "medium",
        },
    ]

    result = processor.process(signals)

    assert sorted(item.source for item in result) == sorted(
        [
            "cognitive_evaluation",
            "autonomous_evolution",
            "agent_runtime",
            "cognitive_reflection",
            "experience_optimization",
        ]
    )


def test_processing_is_deterministic():
    processor = LearningSignalProcessor()

    signals = [
        {
            "source": "cognitive_evaluation",
            "signal_type": "strategy",
            "pattern": "stable strategy",
            "confidence": 0.9,
            "impact": "high",
        },
        {
            "source": "experience_optimization",
            "signal_type": "optimization",
            "pattern": "better routing",
            "confidence": 0.8,
            "impact": "medium",
        },
    ]

    first = processor.process(signals)
    second = processor.process(signals)

    assert first == second
    assert [item.experience_id for item in first] == [
        item.experience_id for item in second
    ]


def test_accepts_mapping_signals():
    processor = LearningSignalProcessor()

    result = processor.process(
        [
            {
                "signal_type": "reflection_insight",
                "pattern": "repeated reasoning error",
                "confidence": 0.85,
                "impact": "high",
                "recommendation": "Review reasoning.",
            }
        ]
    )

    assert len(result) == 1
    assert result[0].source == "cognitive_reflection"
    assert result[0].metadata["recommendation"] == ("Review reasoning.")
