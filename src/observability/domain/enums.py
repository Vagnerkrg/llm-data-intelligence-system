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
    """Types of structured observable events."""

    # Execution lifecycle
    EXECUTION_STARTED = "execution.started"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"
    EXECUTION_CANCELLED = "execution.cancelled"
    EXECUTION_STATE_CHANGED = "execution.state_changed"

    # Execution stages
    EXECUTION_STAGE_STARTED = "execution.stage_started"
    EXECUTION_STAGE_COMPLETED = "execution.stage_completed"
    EXECUTION_STAGE_FAILED = "execution.stage_failed"

    # Generic execution steps
    STEP_STARTED = "execution.step_started"
    STEP_COMPLETED = "execution.step_completed"
    STEP_FAILED = "execution.step_failed"
    RETRY_REQUESTED = "execution.retry_requested"

    # Reasoning
    REASONING_STARTED = "reasoning.started"
    REASONING_COMPLETED = "reasoning.completed"
    REASONING_FAILED = "reasoning.failed"

    # Planning
    PLANNING_STARTED = "planning.started"
    PLANNING_COMPLETED = "planning.completed"
    PLANNING_FAILED = "planning.failed"
    PLAN_CREATED = "planning.plan_created"
    PLAN_UPDATED = "planning.plan_updated"
    REPLANNING_REQUESTED = "planning.replanning_requested"

    # Tool calls
    TOOL_CALL_STARTED = "tool_call.started"
    TOOL_CALL_COMPLETED = "tool_call.completed"
    TOOL_CALL_FAILED = "tool_call.failed"

    # Memory
    MEMORY_READ = "memory.read"
    MEMORY_WRITE = "memory.write"
    MEMORY_RETRIEVAL_STARTED = "memory.retrieval_started"
    MEMORY_RETRIEVAL_COMPLETED = "memory.retrieval_completed"
    MEMORY_RETRIEVAL_FAILED = "memory.retrieval_failed"

    # Knowledge
    KNOWLEDGE_ACCESSED = "knowledge.accessed"
    KNOWLEDGE_UPDATED = "knowledge.updated"
    KNOWLEDGE_QUERY_STARTED = "knowledge.query_started"
    KNOWLEDGE_QUERY_COMPLETED = "knowledge.query_completed"
    KNOWLEDGE_RETRIEVAL_FAILED = "knowledge.retrieval_failed"
    KNOWLEDGE_SOURCE_SELECTED = "knowledge.source_selected"

    # Cognitive evaluation
    COGNITIVE_EVALUATION_STARTED = "cognitive.evaluation_started"
    COGNITIVE_EVALUATION_COMPLETED = "cognitive.evaluation_completed"
    COGNITIVE_EVALUATION_FAILED = "cognitive.evaluation_failed"
    COGNITIVE_EVALUATION_SCORE_GENERATED = "cognitive.evaluation_score_generated"
    COGNITIVE_FEEDBACK_GENERATED = "cognitive.feedback_generated"

    # Backward-compatible evaluation names
    EVALUATION_STARTED = COGNITIVE_EVALUATION_STARTED
    EVALUATION_COMPLETED = COGNITIVE_EVALUATION_COMPLETED
    EVALUATION_FAILED = COGNITIVE_EVALUATION_FAILED
    EVALUATION_SCORE_GENERATED = COGNITIVE_EVALUATION_SCORE_GENERATED
    FEEDBACK_GENERATED = COGNITIVE_FEEDBACK_GENERATED

    # Learning
    LEARNING_SIGNAL_GENERATED = "learning.signal_generated"
    LEARNING_OUTCOME_CREATED = "learning.outcome_created"
    LEARNING_STARTED = "learning.started"
    LEARNING_COMPLETED = "learning.completed"
    LEARNING_SIGNAL_DETECTED = "learning.signal_detected"

    # Evolution
    EVOLUTION_DECISION_CREATED = "evolution.decision_created"
    ADAPTATION_APPLIED = "evolution.adaptation_applied"
    EVOLUTION_STARTED = "evolution.started"
    EVOLUTION_PROPOSAL_GENERATED = "evolution.proposal_generated"
    EVOLUTION_CHANGE_EVALUATED = "evolution.change_evaluated"
    EVOLUTION_APPROVED = "evolution.approved"
    EVOLUTION_REJECTED = "evolution.rejected"
    EVOLUTION_COMPLETED = "evolution.completed"

    # Errors and completion
    ERROR_OCCURRED = "error.occurred"

    # Generic extension point
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
