"""Application service for the public Execution API."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from src.agents.runtime.agent_runtime import AgentRuntime
from src.api.schemas import (
    CreateExecutionRequest,
    ExecutionErrorResponse,
    ExecutionMetadata,
    ExecutionResponse,
    ExecutionResult,
    ExecutionStatus,
)


class ExecutionApplicationService:
    """Application boundary between API transport and Agent Runtime."""

    def __init__(
        self,
        runtime: Optional[AgentRuntime] = None,
    ) -> None:
        self.runtime = runtime or AgentRuntime()

    def execute(
        self,
        request: CreateExecutionRequest,
    ) -> ExecutionResponse:
        """
        Execute a request through Agent Runtime and map the result
        into the public API contract.
        """

        started_at = datetime.now(timezone.utc)

        try:
            context = self.runtime.execute(
                request.query,
            )

        except Exception as error:
            execution_id = self._extract_execution_id()

            return self._build_failure_response(
                execution_id=execution_id,
                error=error,
                started_at=started_at,
            )

        finished_at = datetime.now(timezone.utc)

        execution_id = getattr(
            context,
            "execution_id",
            None,
        )

        if not execution_id:
            raise RuntimeError("Agent Runtime did not return an execution_id.")

        status = self._map_status(
            getattr(
                context,
                "status",
                "completed",
            )
        )

        trace = self._get_trace(
            execution_id,
        )

        trace_started_at = (
            getattr(
                trace,
                "started_at",
                None,
            )
            if trace is not None
            else None
        )

        trace_finished_at = (
            getattr(
                trace,
                "finished_at",
                None,
            )
            if trace is not None
            else None
        )

        result = self._map_result(
            context,
        )

        error_response = self._map_context_error(
            context,
        )

        correlation_id = self._correlation_id(
            trace,
            request,
        )

        return ExecutionResponse(
            execution_id=execution_id,
            status=status,
            created_at=trace_started_at or started_at,
            started_at=trace_started_at or started_at,
            finished_at=trace_finished_at or finished_at,
            duration_ms=self._duration_ms(
                trace_started_at or started_at,
                trace_finished_at or finished_at,
            ),
            correlation_id=correlation_id,
            metadata=ExecutionMetadata(
                correlation_id=correlation_id,
                source="api",
                values=self._public_metadata(
                    context,
                    request,
                ),
            ),
            result=result,
            error=error_response,
        )

    def _extract_execution_id(self) -> Optional[str]:
        """Extract an execution ID from runtime observability."""
        observability = getattr(
            self.runtime,
            "observability",
            None,
        )

        if observability is None:
            return None

        traces = getattr(
            observability,
            "_traces",
            None,
        )

        if isinstance(traces, dict) and traces:
            return next(reversed(traces))

        return None

    def _get_trace(
        self,
        execution_id: str,
    ) -> Any:
        """Retrieve the runtime execution trace when available."""
        observability = getattr(
            self.runtime,
            "observability",
            None,
        )

        if observability is None:
            return None

        trace_method = getattr(
            observability,
            "trace",
            None,
        )

        if not callable(trace_method):
            return None

        try:
            return trace_method(
                execution_id,
            )
        except Exception:
            return None

    @staticmethod
    def _map_status(
        status: Any,
    ) -> ExecutionStatus:
        """Map internal runtime status to the public contract."""
        normalized = str(
            getattr(
                status,
                "value",
                status,
            )
        ).lower()

        mapping = {
            "initialized": ExecutionStatus.PENDING,
            "pending": ExecutionStatus.PENDING,
            "running": ExecutionStatus.RUNNING,
            "executing": ExecutionStatus.RUNNING,
            "completed": ExecutionStatus.COMPLETED,
            "failed": ExecutionStatus.FAILED,
            "cancelled": ExecutionStatus.CANCELLED,
            "canceled": ExecutionStatus.CANCELLED,
        }

        return mapping.get(
            normalized,
            ExecutionStatus.COMPLETED,
        )

    @staticmethod
    def _map_result(
        context: Any,
    ) -> Optional[ExecutionResult]:
        """Map internal runtime result into a public response."""
        results = getattr(
            context,
            "results",
            [],
        )

        if not results:
            return ExecutionResult()

        last_result = results[-1]

        if isinstance(
            last_result,
            dict,
        ):
            answer = last_result.get("answer")

            data = {key: value for key, value in last_result.items() if key != "answer"}

            return ExecutionResult(
                answer=(str(answer) if answer is not None else None),
                data=data,
                metadata={},
            )

        return ExecutionResult(
            answer=str(last_result),
            data={},
            metadata={},
        )

    @staticmethod
    def _map_context_error(
        context: Any,
    ) -> Optional[ExecutionErrorResponse]:
        """Map a failed runtime context to the public error contract."""
        status = str(
            getattr(
                context,
                "status",
                "",
            )
        ).lower()

        if status != "failed":
            return None

        metadata = getattr(
            context,
            "metadata",
            {},
        )

        message = str(
            metadata.get(
                "error",
                "Execution failed.",
            )
        )

        return ExecutionErrorResponse(
            code="EXECUTION_FAILED",
            message=message,
            details={},
        )

    @staticmethod
    def _public_metadata(
        context: Any,
        request: CreateExecutionRequest,
    ) -> dict[str, Any]:
        """Build safe public metadata."""
        context_metadata = getattr(
            context,
            "metadata",
            {},
        )

        return {
            "request_metadata": request.options.metadata,
            "runtime": {
                key: value
                for key, value in context_metadata.items()
                if key
                not in {
                    "error",
                    "execution_id",
                }
            },
        }

    @staticmethod
    def _correlation_id(
        trace: Any,
        request: CreateExecutionRequest,
    ) -> Optional[str]:
        """Resolve correlation ID without leaking internals."""
        if trace is not None:
            context = getattr(
                trace,
                "context",
                None,
            )

            if context is not None:
                correlation_id = getattr(
                    context,
                    "correlation_id",
                    None,
                )

                if correlation_id:
                    return correlation_id

        return request.options.metadata.get("correlation_id")

    @staticmethod
    def _duration_ms(
        started_at: datetime,
        finished_at: datetime,
    ) -> float:
        """Calculate duration in milliseconds."""
        return max(
            0.0,
            (finished_at - started_at).total_seconds() * 1000,
        )

    def _build_failure_response(
        self,
        *,
        execution_id: Optional[str],
        error: Exception,
        started_at: datetime,
    ) -> ExecutionResponse:
        """Build a safe public failure response."""
        finished_at = datetime.now(timezone.utc)

        return ExecutionResponse(
            execution_id=(execution_id or "unknown"),
            status=ExecutionStatus.FAILED,
            created_at=started_at,
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=self._duration_ms(
                started_at,
                finished_at,
            ),
            correlation_id=None,
            metadata=ExecutionMetadata(
                source="api",
            ),
            result=None,
            error=ExecutionErrorResponse(
                code="EXECUTION_FAILED",
                message=str(error),
                details={},
            ),
        )
