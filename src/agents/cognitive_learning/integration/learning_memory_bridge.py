from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.agents.cognitive_learning.domain.learning_outcome import (
    LearningOutcome,
)
from src.agents.memory.domain.memory_entry import (
    MemoryEntry,
)
from src.agents.memory.domain.memory_type import (
    MemoryType,
)
from src.agents.memory.integration.cognitive_memory_adapter import (
    CognitiveMemoryAdapter,
)


@dataclass(frozen=True)
class LearningMemoryResult:
    """Result produced when learning is converted into memory."""

    outcome: LearningOutcome
    memory: MemoryEntry | None
    stored: bool
    relevance: float
    reason: str


class LearningMemoryBridge:
    """
    Connects Cognitive Learning with Runtime Memory.

    Only relevant learning outcomes are transformed into reusable
    memories. Confidence and learning provenance are preserved.
    """

    DEFAULT_MIN_RELEVANCE = 0.70

    def __init__(
        self,
        memory_adapter: CognitiveMemoryAdapter,
        min_relevance: float = DEFAULT_MIN_RELEVANCE,
    ) -> None:
        if not isinstance(
            memory_adapter,
            CognitiveMemoryAdapter,
        ):
            raise ValueError(
                "memory_adapter must be a CognitiveMemoryAdapter."
            )

        if not 0.0 <= min_relevance <= 1.0:
            raise ValueError(
                "min_relevance must be between 0 and 1"
            )

        self.memory_adapter = memory_adapter
        self.min_relevance = min_relevance

    def store(
        self,
        outcome: LearningOutcome,
    ) -> LearningMemoryResult:
        """Convert a learning outcome into reusable memory."""

        if not isinstance(
            outcome,
            LearningOutcome,
        ):
            raise ValueError(
                "outcome must be a LearningOutcome."
            )

        relevance = self._calculate_relevance(
            outcome
        )

        if relevance < self.min_relevance:
            return LearningMemoryResult(
                outcome=outcome,
                memory=None,
                stored=False,
                relevance=relevance,
                reason="Learning outcome is not sufficiently relevant.",
            )

        memory = self._build_memory(
            outcome,
            relevance,
        )

        self.memory_adapter.store_learning(
            memory
        )

        return LearningMemoryResult(
            outcome=outcome,
            memory=memory,
            stored=True,
            relevance=relevance,
            reason="Learning outcome stored as reusable memory.",
        )

    def store_many(
        self,
        outcomes: list[LearningOutcome],
    ) -> list[LearningMemoryResult]:
        """Store multiple learning outcomes deterministically."""

        return [
            self.store(outcome)
            for outcome in outcomes
        ]

    def _calculate_relevance(
        self,
        outcome: LearningOutcome,
    ) -> float:
        confidence = outcome.confidence

        impact = str(
            outcome.metadata.get(
                "impact",
                "medium",
            )
        ).strip().casefold()

        impact_weight = {
            "high": 1.0,
            "medium": 0.85,
            "low": 0.70,
        }.get(
            impact,
            0.70,
        )

        return round(
            confidence * impact_weight,
            4,
        )

    def _build_memory(
        self,
        outcome: LearningOutcome,
        relevance: float,
    ) -> MemoryEntry:
        metadata: dict[str, Any] = dict(
            outcome.metadata
        )

        metadata.update(
            {
                "source": "cognitive_learning",
                "experience_id": outcome.experience_id,
                "confidence": outcome.confidence,
                "relevance": relevance,
                "learned_pattern": outcome.learned_pattern,
                "knowledge_candidate": outcome.knowledge_candidate,
                "recommendation": outcome.recommendation,
            }
        )

        return MemoryEntry(
            memory_id=f"learning-{outcome.experience_id}",
            content=(
                f"{outcome.knowledge_candidate}. "
                f"{outcome.recommendation}"
            ),
            memory_type=MemoryType.PROCEDURAL,
            source="cognitive_learning",
            metadata=metadata,
        )