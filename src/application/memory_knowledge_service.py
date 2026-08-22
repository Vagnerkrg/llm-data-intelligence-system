"""Application service for public Memory and Knowledge queries."""

from __future__ import annotations

from typing import Any, Optional

from src.agents.runtime.agent_runtime import AgentRuntime
from src.api.schemas import (
    KnowledgeItemResponse,
    KnowledgeResponse,
    MemoryItemResponse,
    MemoryResponse,
)


class MemoryKnowledgeApplicationService:
    """Expose controlled Memory and Knowledge information."""

    def __init__(
        self,
        runtime: Optional[AgentRuntime] = None,
    ) -> None:
        self.runtime = runtime or AgentRuntime()

    def get_memory(
        self,
        execution_id: str,
    ) -> MemoryResponse:
        """Return memory observations associated with an execution."""
        trace = self._get_trace(
            execution_id,
        )

        events = [
            event
            for event in trace.events
            if self._event_value(
                event,
            ).startswith("memory.")
        ]

        events.sort(
            key=lambda item: item.timestamp,
        )

        items: list[MemoryItemResponse] = []

        for index, event in enumerate(events):
            metadata = dict(
                event.metadata,
            )

            memory_id = str(
                metadata.get(
                    "memory_id",
                    f"{execution_id}-memory-{index + 1}",
                )
            )

            content = metadata.get(
                "content",
            )

            relevance = self._optional_float(
                metadata.get(
                    "relevance",
                    metadata.get(
                        "relevance_score",
                    ),
                )
            )

            source = self._safe_dict(
                metadata.get(
                    "source",
                )
            )

            public_metadata = self._filter_public_metadata(
                metadata,
            )

            items.append(
                MemoryItemResponse(
                    id=memory_id,
                    content=(str(content) if content is not None else None),
                    relevance=relevance,
                    source=source,
                    metadata=public_metadata,
                )
            )

        return MemoryResponse(
            execution_id=execution_id,
            items=items,
            total=len(items),
            metadata={
                "observed_events": len(events),
                "source": "observability",
                "partial": not bool(items),
            },
        )

    def get_knowledge(
        self,
        execution_id: str,
    ) -> KnowledgeResponse:
        """Return knowledge observations associated with an execution."""
        trace = self._get_trace(
            execution_id,
        )

        events = [
            event
            for event in trace.events
            if self._event_value(
                event,
            ).startswith("knowledge.")
        ]

        events.sort(
            key=lambda item: item.timestamp,
        )

        items: list[KnowledgeItemResponse] = []

        for index, event in enumerate(events):
            metadata = dict(
                event.metadata,
            )

            item_id = str(
                metadata.get(
                    "knowledge_id",
                    metadata.get(
                        "source_id",
                        f"{execution_id}-knowledge-{index + 1}",
                    ),
                )
            )

            source_value = metadata.get(
                "source",
                metadata.get(
                    "source_name",
                ),
            )

            relevance = self._optional_float(
                metadata.get(
                    "relevance",
                    metadata.get(
                        "relevance_score",
                    ),
                )
            )

            items.append(
                KnowledgeItemResponse(
                    id=item_id,
                    source=(str(source_value) if source_value is not None else None),
                    relevance=relevance,
                    metadata=self._filter_public_metadata(
                        metadata,
                    ),
                )
            )

        return KnowledgeResponse(
            execution_id=execution_id,
            items=items,
            total=len(items),
            metadata={
                "observed_events": len(events),
                "source": "observability",
                "partial": not bool(items),
            },
        )

    def _get_trace(
        self,
        execution_id: str,
    ):
        """Retrieve the execution trace through the observability boundary."""
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
            raise RuntimeError("Unable to retrieve Memory or Knowledge data.") from exc

        if trace is None:
            raise LookupError(f"Execution '{execution_id}' not found.")

        return trace

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
    def _optional_float(
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
    def _filter_public_metadata(
        metadata: dict[str, Any],
    ) -> dict[str, Any]:
        """Remove values that should never cross the public API boundary."""
        blocked = {
            "token",
            "access_token",
            "password",
            "secret",
            "api_key",
            "embedding",
            "connection",
            "database_url",
            "query",
        }

        return {
            key: value for key, value in metadata.items() if key.lower() not in blocked
        }
