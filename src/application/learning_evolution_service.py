"""Application service for public Learning and Evolution queries."""

from __future__ import annotations

from typing import Any, Optional

from src.agents.runtime.agent_runtime import AgentRuntime
from src.api.schemas import (
    AdaptationResultResponse,
    EvolutionDecisionResponse,
    EvolutionResponse,
    LearningOutcomeResponse,
    LearningResponse,
    LearningSignalResponse,
)


class LearningEvolutionApplicationService:
    """Expose controlled Learning and Evolution observations."""

    def __init__(
        self,
        runtime: Optional[AgentRuntime] = None,
    ) -> None:
        self.runtime = runtime or AgentRuntime()

    def get_learning(
        self,
        execution_id: str,
    ) -> LearningResponse:
        """Return learning observations for an execution."""
        trace = self._get_trace(
            execution_id,
        )

        signals = []
        outcomes = []

        for index, event in enumerate(
            self._learning_events(
                trace,
            )
        ):
            event_type = self._event_value(
                event,
            )
            metadata = dict(
                event.metadata,
            )

            if event_type == "learning.signal_generated":
                signals.append(
                    self._map_signal(
                        event,
                        metadata,
                        index,
                    )
                )

            elif event_type == "learning.outcome_created":
                outcomes.append(
                    self._map_outcome(
                        event,
                        metadata,
                        index,
                    )
                )

        return LearningResponse(
            execution_id=execution_id,
            signals=signals,
            outcomes=outcomes,
            metadata={
                "source": "observability",
                "signal_count": len(signals),
                "outcome_count": len(outcomes),
                "partial": not bool(signals or outcomes),
            },
        )

    def get_evolution(
        self,
        execution_id: str,
    ) -> EvolutionResponse:
        """Return evolution observations for an execution."""
        trace = self._get_trace(
            execution_id,
        )

        decisions = []
        adaptations = []

        for index, event in enumerate(
            self._evolution_events(
                trace,
            )
        ):
            event_type = self._event_value(
                event,
            )
            metadata = dict(
                event.metadata,
            )

            if event_type == "evolution.decision_created":
                decisions.append(
                    self._map_decision(
                        event,
                        metadata,
                        index,
                    )
                )

            elif event_type == "evolution.adaptation_applied":
                adaptations.append(
                    self._map_adaptation(
                        event,
                        metadata,
                        index,
                    )
                )

        return EvolutionResponse(
            execution_id=execution_id,
            decisions=decisions,
            adaptations=adaptations,
            metadata={
                "source": "observability",
                "decision_count": len(decisions),
                "adaptation_count": len(adaptations),
                "partial": not bool(decisions or adaptations),
            },
        )

    def _get_trace(
        self,
        execution_id: str,
    ):
        """Retrieve the execution trace through Observability."""
        observability = getattr(
            self.runtime,
            "observability",
            None,
        )

        if observability is None:
            raise LookupError(f"Execution '{execution_id}' not found.")

        trace_method = getattr(
            observability,
            "trace",
            None,
        )

        if not callable(trace_method):
            raise LookupError(f"Execution '{execution_id}' not found.")

        try:
            trace = trace_method(
                execution_id,
            )
        except KeyError as exc:
            raise LookupError(f"Execution '{execution_id}' not found.") from exc
        except Exception as exc:
            raise RuntimeError(
                "Unable to retrieve Learning or Evolution data."
            ) from exc

        if trace is None:
            raise LookupError(f"Execution '{execution_id}' not found.")

        return trace

    @staticmethod
    def _learning_events(
        trace: Any,
    ) -> list[Any]:
        events = [
            event
            for event in trace.events
            if LearningEvolutionApplicationService._event_value(
                event,
            )
            in {
                "learning.signal_generated",
                "learning.outcome_created",
            }
        ]

        return sorted(
            events,
            key=lambda item: item.timestamp,
        )

    @staticmethod
    def _evolution_events(
        trace: Any,
    ) -> list[Any]:
        events = [
            event
            for event in trace.events
            if LearningEvolutionApplicationService._event_value(
                event,
            )
            in {
                "evolution.decision_created",
                "evolution.adaptation_applied",
            }
        ]

        return sorted(
            events,
            key=lambda item: item.timestamp,
        )

    @staticmethod
    def _map_signal(
        event: Any,
        metadata: dict[str, Any],
        index: int,
    ) -> LearningSignalResponse:
        return LearningSignalResponse(
            id=str(
                metadata.get(
                    "signal_id",
                    f"{event.execution_id}-signal-{index + 1}",
                )
            ),
            signal_type=LearningEvolutionApplicationService._optional_string(
                metadata.get(
                    "signal_type",
                )
            ),
            confidence=LearningEvolutionApplicationService._confidence(
                metadata.get(
                    "confidence",
                )
            ),
            provenance=LearningEvolutionApplicationService._safe_dict(
                metadata.get(
                    "provenance",
                )
            ),
            timestamp=event.timestamp,
            metadata=LearningEvolutionApplicationService._public_metadata(
                metadata,
            ),
        )

    @staticmethod
    def _map_outcome(
        event: Any,
        metadata: dict[str, Any],
        index: int,
    ) -> LearningOutcomeResponse:
        return LearningOutcomeResponse(
            id=str(
                metadata.get(
                    "outcome_id",
                    f"{event.execution_id}-outcome-{index + 1}",
                )
            ),
            outcome_type=LearningEvolutionApplicationService._optional_string(
                metadata.get(
                    "outcome_type",
                )
            ),
            success=(bool(metadata["success"]) if "success" in metadata else None),
            confidence=LearningEvolutionApplicationService._confidence(
                metadata.get(
                    "confidence",
                )
            ),
            provenance=LearningEvolutionApplicationService._safe_dict(
                metadata.get(
                    "provenance",
                )
            ),
            timestamp=event.timestamp,
            metadata=LearningEvolutionApplicationService._public_metadata(
                metadata,
            ),
        )

    @staticmethod
    def _map_decision(
        event: Any,
        metadata: dict[str, Any],
        index: int,
    ) -> EvolutionDecisionResponse:
        return EvolutionDecisionResponse(
            id=str(
                metadata.get(
                    "decision_id",
                    f"{event.execution_id}-decision-{index + 1}",
                )
            ),
            decision_type=LearningEvolutionApplicationService._optional_string(
                metadata.get(
                    "decision_type",
                )
            ),
            trigger=LearningEvolutionApplicationService._optional_string(
                metadata.get(
                    "trigger",
                    metadata.get(
                        "evolution_trigger",
                    ),
                )
            ),
            confidence=LearningEvolutionApplicationService._confidence(
                metadata.get(
                    "confidence",
                )
            ),
            provenance=LearningEvolutionApplicationService._safe_dict(
                metadata.get(
                    "provenance",
                )
            ),
            timestamp=event.timestamp,
            metadata=LearningEvolutionApplicationService._public_metadata(
                metadata,
            ),
        )

    @staticmethod
    def _map_adaptation(
        event: Any,
        metadata: dict[str, Any],
        index: int,
    ) -> AdaptationResultResponse:
        return AdaptationResultResponse(
            id=str(
                metadata.get(
                    "adaptation_id",
                    f"{event.execution_id}-adaptation-{index + 1}",
                )
            ),
            applied=bool(
                metadata.get(
                    "adaptation_applied",
                    True,
                )
            ),
            adaptation_type=LearningEvolutionApplicationService._optional_string(
                metadata.get(
                    "adaptation_type",
                )
            ),
            result=LearningEvolutionApplicationService._safe_dict(
                metadata.get(
                    "result",
                )
            ),
            provenance=LearningEvolutionApplicationService._safe_dict(
                metadata.get(
                    "provenance",
                )
            ),
            timestamp=event.timestamp,
            metadata=LearningEvolutionApplicationService._public_metadata(
                metadata,
            ),
        )

    @staticmethod
    def _event_value(
        event: Any,
    ) -> str:
        return str(
            getattr(
                event.event_type,
                "value",
                event.event_type,
            )
        )

    @staticmethod
    def _confidence(
        value: Any,
    ) -> float | None:
        if value is None:
            return None

        try:
            return max(
                0.0,
                min(
                    1.0,
                    float(value),
                ),
            )
        except (
            TypeError,
            ValueError,
        ):
            return None

    @staticmethod
    def _optional_string(
        value: Any,
    ) -> str | None:
        if value is None:
            return None

        return str(value)

    @staticmethod
    def _safe_dict(
        value: Any,
    ) -> dict[str, Any]:
        if isinstance(
            value,
            dict,
        ):
            return dict(value)

        return {}

    @staticmethod
    def _public_metadata(
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """Remove internal and sensitive implementation details."""
        blocked = {
            "token",
            "access_token",
            "password",
            "secret",
            "api_key",
            "database_url",
            "connection",
            "stacktrace",
            "traceback",
        }

        return {
            key: value for key, value in metadata.items() if key.lower() not in blocked
        }
