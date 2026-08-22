from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from src.agents.cognitive_learning.domain import LearningExperience


class LearningSignalProcessor:
    """Transforms cognitive signals into structured learning experiences."""

    MIN_CONFIDENCE = 0.50

    SOURCE_BY_SIGNAL_TYPE = {
        "cognitive_evaluation": "cognitive_evaluation",
        "optimization_signal": "experience_optimization",
        "execution_outcome": "agent_runtime",
        "reflection_insight": "cognitive_reflection",
        "evolution_decision": "autonomous_evolution",
    }

    def process(
        self,
        signals: Sequence[Any],
    ) -> list[LearningExperience]:
        if not isinstance(signals, Sequence) or isinstance(
            signals,
            (str, bytes),
        ):
            raise TypeError("signals must be a sequence.")

        normalized: list[dict[str, Any]] = []

        for signal in signals:
            item = self._normalize_signal(signal)

            if item is None:
                continue

            normalized.append(item)

        consolidated = self._consolidate(normalized)

        return [
            self._build_experience(
                item,
                index=index,
            )
            for index, item in enumerate(consolidated)
        ]

    def _normalize_signal(
        self,
        signal: Any,
    ) -> dict[str, Any] | None:
        signal_type = self._get_value(
            signal,
            "signal_type",
            "type",
        )

        pattern = self._get_value(
            signal,
            "pattern",
            "learned_pattern",
            "insight",
            "description",
            "reason",
        )

        confidence = self._get_value(
            signal,
            "confidence",
            "certainty",
        )

        if not signal_type or not pattern:
            return None

        confidence_value = self._normalize_confidence(confidence)

        if confidence_value < self.MIN_CONFIDENCE:
            return None

        source = self._resolve_source(
            signal,
            signal_type,
        )

        impact = self._get_value(
            signal,
            "impact",
            "priority",
        )

        recommendation = self._get_value(
            signal,
            "recommendation",
        )

        return {
            "source": source,
            "signal_type": str(signal_type).strip(),
            "pattern": str(pattern).strip(),
            "confidence": confidence_value,
            "impact": self._normalize_impact(impact),
            "recommendation": (str(recommendation).strip() if recommendation else ""),
        }

    def _consolidate(
        self,
        signals: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        groups: dict[
            tuple[str, str, str],
            list[dict[str, Any]],
        ] = defaultdict(list)

        for signal in signals:
            key = (
                signal["source"],
                signal["signal_type"],
                signal["pattern"].lower(),
            )
            groups[key].append(signal)

        consolidated: list[dict[str, Any]] = []

        for key in sorted(groups):
            items = groups[key]

            confidence = sum(item["confidence"] for item in items) / len(items)

            impact = self._resolve_impact(items)

            recommendation = next(
                (item["recommendation"] for item in items if item["recommendation"]),
                "",
            )

            consolidated.append(
                {
                    "source": key[0],
                    "signal_type": key[1],
                    "pattern": items[0]["pattern"],
                    "confidence": confidence,
                    "impact": impact,
                    "recommendation": recommendation,
                }
            )

        return consolidated

    @staticmethod
    def _build_experience(
        signal: dict[str, Any],
        index: int,
    ) -> LearningExperience:
        identity = (
            f"{index}|"
            f"{signal['source']}|"
            f"{signal['signal_type']}|"
            f"{signal['pattern'].lower()}"
        )

        experience_id = str(
            uuid5(
                NAMESPACE_URL,
                identity,
            )
        )

        return LearningExperience(
            experience_id=experience_id,
            source=signal["source"],
            signal_type=signal["signal_type"],
            pattern=signal["pattern"],
            outcome="observed",
            confidence=signal["confidence"],
            impact=signal["impact"],
            metadata={
                "recommendation": signal["recommendation"],
            },
        )

    def _resolve_source(
        self,
        signal: Any,
        signal_type: Any,
    ) -> str:
        explicit_source = self._get_value(
            signal,
            "source",
        )

        if explicit_source:
            return str(explicit_source).strip()

        normalized_type = str(signal_type).strip().lower()

        return self.SOURCE_BY_SIGNAL_TYPE.get(
            normalized_type,
            "cognitive_learning",
        )

    @staticmethod
    def _get_value(
        value: Any,
        *names: str,
    ) -> Any:
        for name in names:
            if isinstance(value, Mapping):
                candidate = value.get(name)
            else:
                candidate = getattr(
                    value,
                    name,
                    None,
                )

            if candidate is not None:
                return candidate

        return None

    @staticmethod
    def _normalize_confidence(
        value: Any,
    ) -> float:
        if isinstance(value, bool):
            return 0.0

        try:
            confidence = float(value)
        except (TypeError, ValueError):
            return 0.0

        if not 0.0 <= confidence <= 1.0:
            return 0.0

        return confidence

    @staticmethod
    def _normalize_impact(
        value: Any,
    ) -> str:
        if value is None:
            return "unknown"

        normalized = str(value).strip().lower()

        if normalized in {
            "high",
            "medium",
            "low",
        }:
            return normalized

        return "unknown"

    @staticmethod
    def _resolve_impact(
        signals: list[dict[str, Any]],
    ) -> str:
        ranking = {
            "high": 3,
            "medium": 2,
            "low": 1,
            "unknown": 0,
        }

        return max(
            (item["impact"] for item in signals),
            key=lambda impact: ranking[impact],
        )
