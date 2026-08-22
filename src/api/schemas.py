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


class APIErrorDetail(BaseModel):
    """Public standardized API error."""

    code: str = Field(
        ...,
        description="Stable machine-readable error code.",
    )

    category: str = Field(
        ...,
        description="Public error category.",
    )

    message: str = Field(
        ...,
        description="Safe human-readable error message.",
    )

    severity: str = Field(
        default="error",
        description="Public error severity.",
    )

    execution_id: str | None = Field(
        default=None,
        description="Execution identifier when applicable.",
    )

    correlation_id: str | None = Field(
        default=None,
        description="External correlation identifier when applicable.",
    )

    details: dict[str, Any] = Field(
        default_factory=dict,
        description="Safe structured diagnostic information.",
    )


class APIErrorResponse(BaseModel):
    """Standard API error envelope."""

    error: APIErrorDetail


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


class ExecutionStateResponse(BaseModel):
    """Public execution state representation."""

    execution_id: str
    status: ExecutionStatus
    current_component: str | None = None
    current_stage: str | None = None
    current_step: str | None = None
    started_at: datetime | None = None
    updated_at: datetime
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ExecutionEventResponse(BaseModel):
    """Public structured execution event."""

    event_id: str
    execution_id: str
    event_type: str
    timestamp: datetime
    component: str
    stage: str | None = None
    status: ExecutionStatus | None = None
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ExecutionMetricResponse(BaseModel):
    """Public execution metric."""

    metric_name: str
    value: float
    unit: str
    timestamp: datetime
    execution_id: str
    component: str
    metric_type: str
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ExecutionErrorTraceResponse(BaseModel):
    """Public execution error."""

    error_id: str
    execution_id: str
    timestamp: datetime
    component: str
    stage: str | None = None
    severity: str
    error_type: str
    message: str
    recoverable: bool
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class ExecutionTraceResponse(BaseModel):
    """Public execution trace contract."""

    execution_id: str
    status: ExecutionStatus
    started_at: datetime | None = None
    finished_at: datetime | None = None
    duration_ms: float | None = Field(
        default=None,
        ge=0,
    )
    state: ExecutionStateResponse | None = None
    events: list[ExecutionEventResponse] = Field(
        default_factory=list,
    )
    metrics: list[ExecutionMetricResponse] = Field(
        default_factory=list,
    )
    errors: list[ExecutionErrorTraceResponse] = Field(
        default_factory=list,
    )


class CognitiveStageState(BaseModel):
    """Public state of one cognitive stage."""

    status: str = "not_started"
    component: str | None = None
    stage: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    duration_ms: float | None = None
    result: dict[str, Any] = Field(
        default_factory=dict,
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class CognitiveStateResponse(BaseModel):
    """Public consolidated cognitive execution state."""

    execution_id: str
    execution_status: ExecutionStatus
    reasoning: CognitiveStageState
    planning: CognitiveStageState
    execution: CognitiveStageState
    memory: CognitiveStageState
    knowledge: CognitiveStageState
    evaluation: CognitiveStageState
    learning: CognitiveStageState
    evolution: CognitiveStageState
    adaptation: CognitiveStageState


class MemoryItemResponse(BaseModel):
    """Public memory item."""

    id: str
    content: str | None = None
    relevance: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    source: dict[str, Any] = Field(
        default_factory=dict,
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class MemoryResponse(BaseModel):
    """Public memory retrieval response."""

    execution_id: str
    items: list[MemoryItemResponse] = Field(
        default_factory=list,
    )
    total: int = Field(
        default=0,
        ge=0,
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class KnowledgeItemResponse(BaseModel):
    """Public knowledge item."""

    id: str
    source: str | None = None
    relevance: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class KnowledgeResponse(BaseModel):
    """Public knowledge access response."""

    execution_id: str
    items: list[KnowledgeItemResponse] = Field(
        default_factory=list,
    )
    total: int = Field(
        default=0,
        ge=0,
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class LearningSignalResponse(BaseModel):
    """Public learning signal."""

    id: str
    signal_type: str | None = None
    confidence: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    provenance: dict[str, Any] = Field(
        default_factory=dict,
    )
    timestamp: datetime
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class LearningOutcomeResponse(BaseModel):
    """Public learning outcome."""

    id: str
    outcome_type: str | None = None
    success: bool | None = None
    confidence: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    provenance: dict[str, Any] = Field(
        default_factory=dict,
    )
    timestamp: datetime
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class LearningResponse(BaseModel):
    """Public learning response."""

    execution_id: str
    signals: list[LearningSignalResponse] = Field(
        default_factory=list,
    )
    outcomes: list[LearningOutcomeResponse] = Field(
        default_factory=list,
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class EvolutionDecisionResponse(BaseModel):
    """Public evolution decision."""

    id: str
    decision_type: str | None = None
    trigger: str | None = None
    confidence: float | None = Field(
        default=None,
        ge=0,
        le=1,
    )
    provenance: dict[str, Any] = Field(
        default_factory=dict,
    )
    timestamp: datetime
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class AdaptationResultResponse(BaseModel):
    """Public adaptation result."""

    id: str
    applied: bool
    adaptation_type: str | None = None
    result: dict[str, Any] = Field(
        default_factory=dict,
    )
    provenance: dict[str, Any] = Field(
        default_factory=dict,
    )
    timestamp: datetime
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )


class EvolutionResponse(BaseModel):
    """Public evolution response."""

    execution_id: str
    decisions: list[EvolutionDecisionResponse] = Field(
        default_factory=list,
    )
    adaptations: list[AdaptationResultResponse] = Field(
        default_factory=list,
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
    )
