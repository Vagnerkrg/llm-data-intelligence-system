"""Enumerations used by the observability domain."""

from enum import Enum


class ExecutionStatus(str, Enum):
    """Lifecycle state of an execution."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EventType(str, Enum):
    """Types of observable execution events."""

    EXECUTION_STARTED = "execution.started"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"
    EXECUTION_CANCELLED = "execution.cancelled"

    STEP_STARTED = "execution.step_started"
    STEP_COMPLETED = "execution.step_completed"
    STEP_FAILED = "execution.step_failed"
    RETRY_REQUESTED = "execution.retry_requested"

    REASONING_STARTED = "reasoning.started"
    REASONING_COMPLETED = "reasoning.completed"
    REASONING_FAILED = "reasoning.failed"

    PLANNING_STARTED = "planning.started"
    PLANNING_COMPLETED = "planning.completed"
    PLAN_CREATED = "planning.plan_created"
    PLAN_UPDATED = "planning.plan_updated"
    REPLANNING_REQUESTED = "planning.replanning_requested"

    EXECUTION_COMPONENT_STARTED = "execution.component_started"
    EXECUTION_COMPONENT_COMPLETED = "execution.component_completed"

    MEMORY_READ = "memory.read"
    MEMORY_WRITE = "memory.write"
    MEMORY_RETRIEVAL_STARTED = "memory.retrieval_started"
    MEMORY_RETRIEVAL_COMPLETED = "memory.retrieval_completed"
    MEMORY_RETRIEVAL_FAILED = "memory.retrieval_failed"

    KNOWLEDGE_QUERY_STARTED = "knowledge.query_started"
    KNOWLEDGE_QUERY_COMPLETED = "knowledge.query_completed"
    KNOWLEDGE_RETRIEVAL_FAILED = "knowledge.retrieval_failed"
    KNOWLEDGE_SOURCE_SELECTED = "knowledge.source_selected"

    EVALUATION_STARTED = "evaluation.started"
    EVALUATION_COMPLETED = "evaluation.completed"
    EVALUATION_FAILED = "evaluation.failed"
    EVALUATION_SCORE_GENERATED = "evaluation.score_generated"
    FEEDBACK_GENERATED = "evaluation.feedback_generated"

    LEARNING_STARTED = "learning.started"
    LEARNING_COMPLETED = "learning.completed"
    LEARNING_SIGNAL_DETECTED = "learning.signal_detected"

    EVOLUTION_STARTED = "evolution.started"
    EVOLUTION_PROPOSAL_GENERATED = "evolution.proposal_generated"
    EVOLUTION_CHANGE_EVALUATED = "evolution.change_evaluated"
    EVOLUTION_APPROVED = "evolution.approved"
    EVOLUTION_REJECTED = "evolution.rejected"
    EVOLUTION_COMPLETED = "evolution.completed"

    CUSTOM = "custom"


class MetricType(str, Enum):
    """Semantic type of an execution metric."""

    DURATION = "duration"
    COUNT = "count"
    RATE = "rate"
    SCORE = "score"
    LATENCY = "latency"
    SIZE = "size"
    VALUE = "value"


class ErrorSeverity(str, Enum):
    """Severity of an execution error."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
