"""Application service for public cognitive state queries."""

from __future__ import annotations

from typing import Any, Optional

from src.agents.runtime.agent_runtime import AgentRuntime
from src.api.schemas import (
    CognitiveStageState,
    CognitiveStateResponse,
    ExecutionStatus,
)


class CognitiveStateApplicationService:
    """Build a public cognitive view from the execution trace."""

    def __init__(
        self,
        runtime: Optional[AgentRuntime] = None,
    ) -> None:
        self.runtime = runtime or AgentRuntime()

    def get_state(
        self,
        execution_id: str,
    ) -> CognitiveStateResponse:
        """Return the consolidated cognitive state."""
        trace = self._get_trace(
            execution_id,
        )

        return CognitiveStateResponse(
            execution_id=trace.execution_id,
            execution_status=self._map_status(
                trace.status,
            ),
            reasoning=self._build_stage(
                trace,
                prefix="reasoning",
            ),
            planning=self._build_stage(
                trace,
                prefix="planning",
            ),
            execution=self._build_stage(
                trace,
                prefix="execution",
            ),
            memory=self._build_stage(
                trace,
                prefix="memory",
            ),
            knowledge=self._build_stage(
                trace,
                prefix="knowledge",
            ),
            evaluation=self._build_stage(
                trace,
                prefix="cognitive.evaluation",
            ),
            learning=self._build_stage(
                trace,
                prefix="learning",
            ),
            evolution=self._build_stage(
                trace,
                prefix="evolution",
            ),
            adaptation=self._build_stage(
                trace,
                prefix="evolution.adaptation",
            ),
        )

    def _get_trace(
        self,
        execution_id: str,
    ):
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
            raise RuntimeError("Unable to retrieve cognitive state.") from exc

        if trace is None:
            raise LookupError(f"Execution '{execution_id}' not found.")

        return trace

    def _build_stage(
        self,
        trace: Any,
        *,
        prefix: str,
    ) -> CognitiveStageState:
        """Build a stage state from structured events."""
        events = [
            event
            for event in trace.events
            if self._event_belongs_to_stage(
                event,
                prefix,
            )
        ]

        if not events:
            return CognitiveStageState()

        events = sorted(
            events,
            key=lambda item: item.timestamp,
        )

        started = None
        completed = None
        failed = None

        for event in events:
            event_type = str(
                getattr(
                    event.event_type,
                    "value",
                    event.event_type,
                )
            )

            if event_type.endswith(".started") or event_type.endswith("_started"):
                started = event

            elif event_type.endswith(".completed") or event_type.endswith("_completed"):
                completed = event

            elif event_type.endswith(".failed") or event_type.endswith("_failed"):
                failed = event

        latest = events[-1]

        if failed is not None and (
            completed is None or failed.timestamp > completed.timestamp
        ):
            status = "failed"
        elif completed is not None:
            status = "completed"
        elif started is not None:
            status = "running"
        else:
            status = "observed"

        metadata = dict(
            latest.metadata,
        )

        result = {}

        if "score" in metadata:
            result["score"] = metadata["score"]

        if "signals" in metadata:
            result["signals"] = metadata["signals"]

        if "outcomes" in metadata:
            result["outcomes"] = metadata["outcomes"]

        if "decision_created" in metadata:
            result["decision_created"] = metadata["decision_created"]

        if "adaptation_applied" in metadata:
            result["adaptation_applied"] = metadata["adaptation_applied"]

        started_at = started.timestamp if started is not None else None

        completed_at = (
            completed.timestamp
            if completed is not None
            else (failed.timestamp if failed is not None else None)
        )

        duration_ms = None

        if started_at is not None and completed_at is not None:
            duration_ms = max(
                0.0,
                (completed_at - started_at).total_seconds() * 1000,
            )

        return CognitiveStageState(
            status=status,
            component=latest.component,
            stage=latest.stage,
            started_at=started_at,
            completed_at=completed_at,
            duration_ms=duration_ms,
            result=result,
            metadata=metadata,
        )

    @staticmethod
    def _event_belongs_to_stage(
        event: Any,
        prefix: str,
    ) -> bool:
        event_type = str(
            getattr(
                event.event_type,
                "value",
                event.event_type,
            )
        )

        return event_type.startswith(prefix) or event_type.startswith(
            prefix.replace(
                ".",
                "_",
            )
        )

    @staticmethod
    def _map_status(
        status: Any,
    ) -> ExecutionStatus:
        value = str(
            getattr(
                status,
                "value",
                status,
            )
        ).lower()

        mapping = {
            "pending": ExecutionStatus.PENDING,
            "running": ExecutionStatus.RUNNING,
            "completed": ExecutionStatus.COMPLETED,
            "failed": ExecutionStatus.FAILED,
            "cancelled": ExecutionStatus.CANCELLED,
        }

        return mapping.get(
            value,
            ExecutionStatus.PENDING,
        )
