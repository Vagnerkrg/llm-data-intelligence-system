"""Public API contracts for execution requests and responses."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Public execution lifecycle states."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ExecutionErrorResponse(BaseModel):
    """Public representation of an execution error."""

    code: str = Field(
        ...,
        description="Stable machine-readable error code.",
    )

    message: str = Field(
        ...,
        description="Safe human-readable error message.",
    )

    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional structured error details.",
    )


class ExecutionMetadata(BaseModel):
    """Public metadata associated with an execution."""

    correlation_id: str | None = Field(
        default=None,
        description="Optional external correlation identifier.",
    )

    source: str | None = Field(
        default=None,
        description="Origin of the execution request.",
    )

    values: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional public metadata.",
    )


class ExecutionOptions(BaseModel):
    """Public options accepted when creating an execution."""

    timeout_ms: int | None = Field(
        default=None,
        ge=1,
        description="Optional execution timeout in milliseconds.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional execution metadata.",
    )


class CreateExecutionRequest(BaseModel):
    """Request contract for starting an execution."""

    query: str = Field(
        ...,
        min_length=1,
        description="User query submitted for execution.",
    )

    context: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional public request context.",
    )

    options: ExecutionOptions = Field(
        default_factory=ExecutionOptions,
        description="Optional execution configuration.",
    )


class CreateExecutionResponse(BaseModel):
    """Response returned after accepting an execution."""

    execution_id: str = Field(
        ...,
        description="Unique identifier of the created execution.",
    )

    status: ExecutionStatus = Field(
        ...,
        description="Current execution lifecycle status.",
    )

    created_at: datetime = Field(
        ...,
        description="Timestamp when the execution was created.",
    )

    correlation_id: str | None = Field(
        default=None,
        description="Optional correlation identifier.",
    )

    message: str = Field(
        ...,
        description="Safe execution acknowledgement message.",
    )


class ExecutionResult(BaseModel):
    """Public execution result."""

    answer: str | None = Field(
        default=None,
        description="Final execution answer when available.",
    )

    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured public result data.",
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Public result metadata.",
    )


class ExecutionResponse(BaseModel):
    """Public representation of an execution."""

    execution_id: str = Field(
        ...,
        description="Unique execution identifier.",
    )

    status: ExecutionStatus = Field(
        ...,
        description="Current execution lifecycle status.",
    )

    created_at: datetime | None = Field(
        default=None,
        description="Execution creation timestamp.",
    )

    started_at: datetime | None = Field(
        default=None,
        description="Execution start timestamp.",
    )

    finished_at: datetime | None = Field(
        default=None,
        description="Execution completion timestamp.",
    )

    duration_ms: float | None = Field(
        default=None,
        ge=0,
        description="Execution duration in milliseconds.",
    )

    correlation_id: str | None = Field(
        default=None,
        description="Optional correlation identifier.",
    )

    metadata: ExecutionMetadata = Field(
        default_factory=ExecutionMetadata,
        description="Public execution metadata.",
    )

    result: ExecutionResult | None = Field(
        default=None,
        description="Public execution result.",
    )

    error: ExecutionErrorResponse | None = Field(
        default=None,
        description="Public execution error when execution failed.",
    )


class APIErrorResponse(BaseModel):
    """Standard API error envelope."""

    error: str = Field(
        ...,
        description="Stable API error code.",
    )

    message: str = Field(
        ...,
        description="Safe human-readable error message.",
    )

    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Optional structured error information.",
    )

    execution_id: str | None = Field(
        default=None,
        description="Execution identifier when applicable.",
    )


# ---------------------------------------------------------------------------
# Legacy compatibility contracts
# ---------------------------------------------------------------------------


class QuestionRequest(BaseModel):
    """
    Legacy request contract kept for backward compatibility.

    The new V1.29 execution contract is represented by
    CreateExecutionRequest.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="Legacy question field.",
    )


class AnswerResponse(BaseModel):
    """
    Legacy response contract kept for backward compatibility.

    The new V1.29 execution contract is represented by
    ExecutionResponse.
    """

    answer: str

    source: str | None = None

    confidence: float | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )
