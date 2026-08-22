from collections.abc import Mapping, Sequence
from numbers import Real
from typing import Any

from src.agents.autonomous_evolution.domain.evolution_context import (
    EvolutionContext,
)
from src.agents.autonomous_evolution.domain.evolution_decision import (
    EvolutionDecision,
)
from src.agents.autonomous_evolution.domain.evolution_evidence import (
    EvolutionEvidence,
)
from src.agents.autonomous_evolution.domain.evolution_status import (
    EvolutionStatus,
)


class EvolutionDecisionEngine:
    """
    Deterministic engine responsible for deciding whether an experience
    provides sufficient evidence to justify autonomous evolution.

    The engine remains independent from Agent Runtime, Cognitive Evaluation,
    Memory implementations, LLM providers, and external tools.
    """

    DEFAULT_MIN_EVIDENCE = 2
    DEFAULT_MIN_CONFIDENCE = 0.60
    DEFAULT_EVOLUTION_THRESHOLD = 0.70

    _SIGNAL_SOURCES = (
        ("execution_information", "execution"),
        ("evaluation_information", "cognitive_evaluation"),
        ("learning_information", "learning"),
        ("knowledge_information", "knowledge"),
        ("memory_information", "memory"),
        ("improvement_information", "improvement"),
    )

    def __init__(
        self,
        min_evidence: int = DEFAULT_MIN_EVIDENCE,
        min_confidence: float = DEFAULT_MIN_CONFIDENCE,
        evolution_threshold: float = DEFAULT_EVOLUTION_THRESHOLD,
    ) -> None:
        self._validate_configuration(
            min_evidence=min_evidence,
            min_confidence=min_confidence,
            evolution_threshold=evolution_threshold,
        )

        self.min_evidence = min_evidence
        self.min_confidence = min_confidence
        self.evolution_threshold = evolution_threshold

    def decide(
        self,
        context: EvolutionContext,
    ) -> EvolutionDecision:
        """
        Produce a deterministic evolution decision from an evolution context.
        """
        if not isinstance(context, EvolutionContext):
            raise TypeError("context must be an EvolutionContext instance.")

        evidence = self._collect_evidence(context)

        if len(evidence) < self.min_evidence:
            return EvolutionDecision(
                should_evolve=False,
                confidence=self._calculate_confidence(evidence),
                status=EvolutionStatus.PENDING,
                reason=("Insufficient evidence to justify autonomous evolution."),
                evidence=evidence,
            )

        eligible_evidence = [
            item for item in evidence if item.confidence >= self.min_confidence
        ]

        if len(eligible_evidence) < self.min_evidence:
            return EvolutionDecision(
                should_evolve=False,
                confidence=self._calculate_confidence(evidence),
                status=EvolutionStatus.PENDING,
                reason=(
                    "Evidence exists, but insufficient evidence meets "
                    "the minimum confidence threshold."
                ),
                evidence=evidence,
            )

        average_strength = self._calculate_average_strength(eligible_evidence)

        should_evolve = average_strength >= self.evolution_threshold

        if should_evolve:
            status = EvolutionStatus.PROPOSED
            reason = (
                "Evidence satisfies the minimum confidence and "
                "evolution score thresholds."
            )
        else:
            status = EvolutionStatus.PENDING
            reason = "Evidence does not satisfy the evolution score threshold."

        return EvolutionDecision(
            should_evolve=should_evolve,
            confidence=self._calculate_confidence(eligible_evidence),
            status=status,
            reason=reason,
            evidence=evidence,
        )

    def _collect_evidence(
        self,
        context: EvolutionContext,
    ) -> list[EvolutionEvidence]:
        evidence: list[EvolutionEvidence] = []

        for attribute_name, source_name in self._SIGNAL_SOURCES:
            value = getattr(context, attribute_name)
            evidence.extend(
                self._normalize_source(
                    source=source_name,
                    value=value,
                )
            )

        return evidence

    def _normalize_source(
        self,
        source: str,
        value: Any,
    ) -> list[EvolutionEvidence]:
        if value is None:
            return []

        if isinstance(value, Mapping):
            return self._normalize_mapping(
                source=source,
                value=value,
            )

        if isinstance(value, Sequence) and not isinstance(
            value,
            str | bytes,
        ):
            evidence: list[EvolutionEvidence] = []

            for item in value:
                evidence.extend(
                    self._normalize_source(
                        source=source,
                        value=item,
                    )
                )

            return evidence

        score = self._extract_numeric_score(value)

        if score is None:
            return []

        confidence = self._extract_confidence(value)

        return [
            EvolutionEvidence(
                source=source,
                signal="score",
                value=score,
                confidence=confidence,
            )
        ]

    def _normalize_mapping(
        self,
        source: str,
        value: Mapping[str, Any],
    ) -> list[EvolutionEvidence]:
        evidence: list[EvolutionEvidence] = []

        if "evidence" in value:
            evidence.extend(
                self._normalize_source(
                    source=source,
                    value=value["evidence"],
                )
            )

        score_keys = (
            "score",
            "overall_score",
            "quality_score",
            "relevance_score",
            "effectiveness_score",
        )

        for key in score_keys:
            if key not in value:
                continue

            score = self._extract_numeric_score(value[key])

            if score is None:
                continue

            confidence = self._extract_confidence(value)

            evidence.append(
                EvolutionEvidence(
                    source=source,
                    signal=key,
                    value=score,
                    confidence=confidence,
                )
            )

        return evidence

    def _extract_numeric_score(
        self,
        value: Any,
    ) -> float | None:
        if isinstance(value, bool):
            return None

        if isinstance(value, Real):
            score = float(value)

            if 0.0 <= score <= 1.0:
                return score

            return None

        for attribute_name in (
            "overall_score",
            "score",
            "quality_score",
            "relevance_score",
            "effectiveness_score",
        ):
            attribute = getattr(
                value,
                attribute_name,
                None,
            )

            if isinstance(attribute, bool):
                continue

            if isinstance(attribute, Real):
                score = float(attribute)

                if 0.0 <= score <= 1.0:
                    return score

        return None

    def _extract_confidence(
        self,
        value: Any,
    ) -> float:
        if isinstance(value, Mapping):
            confidence = value.get(
                "confidence",
                value.get("certainty", 1.0),
            )
        else:
            confidence = getattr(
                value,
                "confidence",
                1.0,
            )

        if isinstance(confidence, bool):
            return 1.0

        if isinstance(confidence, Real):
            confidence_value = float(confidence)

            if 0.0 <= confidence_value <= 1.0:
                return confidence_value

        return 0.0

    def _calculate_average_strength(
        self,
        evidence: list[EvolutionEvidence],
    ) -> float:
        if not evidence:
            return 0.0

        return sum(float(item.value) for item in evidence) / len(evidence)

    def _calculate_confidence(
        self,
        evidence: list[EvolutionEvidence],
    ) -> float:
        if not evidence:
            return 0.0

        return sum(item.confidence for item in evidence) / len(evidence)

    @staticmethod
    def _validate_configuration(
        min_evidence: int,
        min_confidence: float,
        evolution_threshold: float,
    ) -> None:
        if min_evidence < 1:
            raise ValueError("min_evidence must be greater than or equal to 1.")

        if not 0.0 <= min_confidence <= 1.0:
            raise ValueError("min_confidence must be between 0.0 and 1.0.")

        if not 0.0 <= evolution_threshold <= 1.0:
            raise ValueError("evolution_threshold must be between 0.0 and 1.0.")
