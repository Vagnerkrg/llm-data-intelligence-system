import pytest

from src.agents.cognitive_learning.domain.learning_outcome import (
    LearningOutcome,
)
from src.agents.cognitive_learning.integration.learning_memory_bridge import (
    LearningMemoryBridge,
)
from src.agents.memory.domain.memory_type import (
    MemoryType,
)
from src.agents.memory.integration.cognitive_memory_adapter import (
    CognitiveMemoryAdapter,
)


class FakeStorage:
    def __init__(self) -> None:
        self.saved = []

    def save(self, memory):
        self.saved.append(memory)
        return memory

    def get(self, memory_id):
        return next(
            (memory for memory in self.saved if memory.memory_id == memory_id),
            None,
        )


def _outcome(
    *,
    experience_id: str = "exp-1",
    confidence: float = 0.9,
    impact: str = "high",
    metadata: dict | None = None,
) -> LearningOutcome:
    return LearningOutcome(
        experience_id=experience_id,
        learned_pattern="stable strategy",
        knowledge_candidate="Use stable strategy",
        confidence=confidence,
        recommendation="Reuse this strategy in future executions.",
        metadata={
            "impact": impact,
            **(metadata or {}),
        },
    )


def test_stores_relevant_learning_as_memory():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    result = bridge.store(_outcome())

    assert result.stored
    assert result.memory is not None
    assert len(storage.saved) == 1
    assert result.memory.memory_type == MemoryType.PROCEDURAL


def test_preserves_experience_context():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    result = bridge.store(
        _outcome(
            experience_id="experience-42",
        )
    )

    assert result.memory is not None
    assert result.memory.memory_id == "learning-experience-42"
    assert result.memory.metadata["experience_id"] == "experience-42"
    assert result.memory.metadata["source"] == "cognitive_learning"


def test_preserves_confidence():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    result = bridge.store(
        _outcome(
            confidence=0.83,
        )
    )

    assert result.memory is not None
    assert result.memory.metadata["confidence"] == 0.83


def test_calculates_high_impact_relevance():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    result = bridge.store(
        _outcome(
            confidence=0.8,
            impact="high",
        )
    )

    assert result.relevance == 0.8


def test_calculates_medium_impact_relevance():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    result = bridge.store(
        _outcome(
            confidence=0.8,
            impact="medium",
        )
    )

    assert result.relevance == 0.68
    assert not result.stored
    assert result.memory is None


def test_rejects_insufficient_learning():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    result = bridge.store(
        _outcome(
            confidence=0.5,
            impact="low",
        )
    )

    assert not result.stored
    assert result.memory is None
    assert storage.saved == []


def test_custom_relevance_threshold():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(
        adapter,
        min_relevance=0.60,
    )

    result = bridge.store(
        _outcome(
            confidence=0.8,
            impact="medium",
        )
    )

    assert result.stored
    assert result.relevance == 0.68


def test_rejects_invalid_outcome():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    with pytest.raises(
        ValueError,
        match="outcome must be a LearningOutcome",
    ):
        bridge.store("invalid")


def test_rejects_invalid_adapter():
    with pytest.raises(
        ValueError,
        match="memory_adapter must be a CognitiveMemoryAdapter",
    ):
        LearningMemoryBridge("invalid")


def test_rejects_invalid_relevance_threshold():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)

    with pytest.raises(
        ValueError,
        match="min_relevance must be between 0 and 1",
    ):
        LearningMemoryBridge(
            adapter,
            min_relevance=1.5,
        )


def test_stores_multiple_outcomes_deterministically():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    results = bridge.store_many(
        [
            _outcome(
                experience_id="exp-1",
                confidence=0.9,
                impact="high",
            ),
            _outcome(
                experience_id="exp-2",
                confidence=0.8,
                impact="low",
            ),
        ]
    )

    assert [result.stored for result in results] == [
        True,
        False,
    ]

    assert len(storage.saved) == 1
    assert storage.saved[0].memory_id == "learning-exp-1"


def test_preserves_learning_metadata():
    storage = FakeStorage()
    adapter = CognitiveMemoryAdapter(storage)
    bridge = LearningMemoryBridge(adapter)

    result = bridge.store(
        _outcome(
            metadata={
                "signal_type": "strategy",
                "custom": "value",
            }
        )
    )

    assert result.memory is not None
    assert result.memory.metadata["signal_type"] == "strategy"
    assert result.memory.metadata["custom"] == "value"
