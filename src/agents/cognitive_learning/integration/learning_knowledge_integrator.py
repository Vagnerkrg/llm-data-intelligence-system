from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.agents.cognitive_learning.domain.learning_outcome import (
    LearningOutcome,
)
from src.agents.self_improvement.knowledge.domain.knowledge_entry import (
    KnowledgeEntry,
)
from src.agents.self_improvement.knowledge.domain.knowledge_type import (
    KnowledgeType,
)
from src.agents.self_improvement.knowledge.services.knowledge_repository import (
    KnowledgeRepository,
)


@dataclass(frozen=True)
class LearningKnowledgeResult:
    """Result of integrating a learning outcome into knowledge."""

    outcome: LearningOutcome
    knowledge: KnowledgeEntry
    action: str

    @property
    def created(self) -> bool:
        return self.action == "created"

    @property
    def updated(self) -> bool:
        return self.action == "updated"

    @property
    def duplicated(self) -> bool:
        return self.action == "duplicate"


class LearningKnowledgeIntegrator:
    """Integrates Learning Outcomes into the Knowledge layer."""

    def __init__(
        self,
        repository: KnowledgeRepository | None = None,
    ) -> None:
        self.repository = (
            repository
            if repository is not None
            else KnowledgeRepository()
        )

    def integrate(
        self,
        outcome: LearningOutcome,
    ) -> LearningKnowledgeResult:
        """Integrate one learning outcome."""

        self._validate_outcome(outcome)

        existing = self._find_existing(outcome)

        if existing is None:
            knowledge = self._create_knowledge(outcome)
            self.repository.save(knowledge)

            return LearningKnowledgeResult(
                outcome=outcome,
                knowledge=knowledge,
                action="created",
            )

        if self._is_redundant(existing, outcome):
            return LearningKnowledgeResult(
                outcome=outcome,
                knowledge=existing,
                action="duplicate",
            )

        updated = self._update_knowledge(
            existing,
            outcome,
        )

        self.repository.replace(
            existing,
            updated,
        )

        return LearningKnowledgeResult(
            outcome=outcome,
            knowledge=updated,
            action="updated",
        )

    def integrate_many(
        self,
        outcomes: list[LearningOutcome],
    ) -> list[LearningKnowledgeResult]:
        """Integrate multiple learning outcomes deterministically."""

        return [
            self.integrate(outcome)
            for outcome in outcomes
        ]

    @staticmethod
    def _validate_outcome(
        outcome: LearningOutcome,
    ) -> None:
        if not isinstance(
            outcome,
            LearningOutcome,
        ):
            raise ValueError(
                "outcome must be a LearningOutcome."
            )

        if not outcome.knowledge_candidate.strip():
            raise ValueError(
                "knowledge_candidate must not be empty."
            )

        if not outcome.recommendation.strip():
            raise ValueError(
                "recommendation must not be empty."
            )

    def _find_existing(
        self,
        outcome: LearningOutcome,
    ) -> KnowledgeEntry | None:
        for entry in self.repository.get_all():
            if self._same_knowledge(
                entry,
                outcome,
            ):
                return entry

        return None

    @staticmethod
    def _same_knowledge(
        entry: KnowledgeEntry,
        outcome: LearningOutcome,
    ) -> bool:
        return (
            entry.title.strip().casefold()
            == outcome.knowledge_candidate.strip().casefold()
        )

    @staticmethod
    def _is_redundant(
        existing: KnowledgeEntry,
        outcome: LearningOutcome,
    ) -> bool:
        return (
            existing.description.strip().casefold()
            == outcome.recommendation.strip().casefold()
            and existing.confidence == outcome.confidence
        )

    def _create_knowledge(
        self,
        outcome: LearningOutcome,
    ) -> KnowledgeEntry:
        return KnowledgeEntry(
            knowledge_type=self._resolve_knowledge_type(
                outcome
            ),
            title=outcome.knowledge_candidate,
            description=outcome.recommendation,
            confidence=outcome.confidence,
            metadata=self._build_metadata(
                outcome
            ),
        )

    def _update_knowledge(
        self,
        existing: KnowledgeEntry,
        outcome: LearningOutcome,
    ) -> KnowledgeEntry:
        return KnowledgeEntry(
            knowledge_type=existing.knowledge_type,
            title=existing.title,
            description=outcome.recommendation,
            confidence=max(
                existing.confidence,
                outcome.confidence,
            ),
            metadata=self._merge_metadata(
                existing.metadata,
                outcome,
            ),
        )

    @staticmethod
    def _resolve_knowledge_type(
        outcome: LearningOutcome,
    ) -> KnowledgeType:
        signal_type = str(
            outcome.metadata.get(
                "signal_type",
                "",
            )
        ).strip().casefold()

        if signal_type == "strategy":
            return KnowledgeType.STRATEGY

        if signal_type == "insight":
            return KnowledgeType.INSIGHT

        return KnowledgeType.PATTERN

    @staticmethod
    def _build_metadata(
        outcome: LearningOutcome,
    ) -> dict[str, Any]:
        metadata = dict(outcome.metadata)

        metadata["source"] = "cognitive_learning"
        metadata["experience_id"] = outcome.experience_id

        return metadata

    @staticmethod
    def _merge_metadata(
        existing: dict[str, Any],
        outcome: LearningOutcome,
    ) -> dict[str, Any]:
        metadata = dict(existing)
        metadata.update(outcome.metadata)

        metadata["source"] = "cognitive_learning"
        metadata["experience_id"] = outcome.experience_id

        return metadata