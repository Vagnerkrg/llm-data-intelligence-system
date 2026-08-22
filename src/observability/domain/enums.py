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

    EXECUTION_STARTED = "execution.started"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"
    EXECUTION_CANCELLED = "execution.cancelled"
    EXECUTION_STATE_CHANGED = "execution.state_changed"

    EXECUTION_STAGE_STARTED = "execution.stage_started"
    EXECUTION_STAGE_COMPLETED = "execution.stage_completed"
    EXECUTION_STAGE_FAILED = "execution.stage_failed"

    STEP_STARTED = "execution.step_started"
    STEP_COMPLETED = "execution.step_completed"
    STEP_FAILED = "execution.step_failed"
    RETRY_REQUESTED = "execution.retry_requested"

    REASONING_STARTED = "reasoning.started"
    REASONING_COMPLETED = "reasoning.completed"
    REASONING_FAILED = "reasoning.failed"

    PLANNING_STARTED = "planning.started"
    PLANNING_COMPLETED = "planning.completed"
    PLANNING_FAILED = "planning.failed"
    PLAN_CREATED = "planning.plan_created"
    PLAN_UPDATED = "planning.plan_updated"
    REPLANNING_REQUESTED = "planning.replanning_requested"

    TOOL_CALL_STARTED = "tool_call.started"
    TOOL_CALL_COMPLETED = "tool_call.completed"
    TOOL_CALL_FAILED = "tool_call.failed"

    MEMORY_READ = "memory.read"
    MEMORY_WRITE = "memory.write"
    MEMORY_RETRIEVAL_STARTED = "memory.retrieval_started"
    MEMORY_RETRIEVAL_COMPLETED = "memory.retrieval_completed"
    MEMORY_RETRIEVAL_FAILED = "memory.retrieval_failed"

    KNOWLEDGE_ACCESSED = "knowledge.accessed"
    KNOWLEDGE_UPDATED = "knowledge.updated"
    KNOWLEDGE_QUERY_STARTED = "knowledge.query_started"
    KNOWLEDGE_QUERY_COMPLETED = "knowledge.query_completed"
    KNOWLEDGE_RETRIEVAL_FAILED = "knowledge.retrieval_failed"
    KNOWLEDGE_SOURCE_SELECTED = "knowledge.source_selected"

    COGNITIVE_EVALUATION_STARTED = "cognitive.evaluation_started"
    COGNITIVE_EVALUATION_COMPLETED = "cognitive.evaluation_completed"
    COGNITIVE_EVALUATION_FAILED = "cognitive.evaluation_failed"
    COGNITIVE_EVALUATION_SCORE_GENERATED = "cognitive.evaluation_score_generated"
    COGNITIVE_FEEDBACK_GENERATED = "cognitive.feedback_generated"

    EVALUATION_STARTED = COGNITIVE_EVALUATION_STARTED
    EVALUATION_COMPLETED = COGNITIVE_EVALUATION_COMPLETED
    EVALUATION_FAILED = COGNITIVE_EVALUATION_FAILED
    EVALUATION_SCORE_GENERATED = COGNITIVE_EVALUATION_SCORE_GENERATED
    FEEDBACK_GENERATED = COGNITIVE_FEEDBACK_GENERATED

    LEARNING_SIGNAL_GENERATED = "learning.signal_generated"
    LEARNING_OUTCOME_CREATED = "learning.outcome_created"
    LEARNING_STARTED = "learning.started"
    LEARNING_COMPLETED = "learning.completed"
    LEARNING_SIGNAL_DETECTED = "learning.signal_detected"

    EVOLUTION_DECISION_CREATED = "evolution.decision_created"
    ADAPTATION_APPLIED = "evolution.adaptation_applied"
    EVOLUTION_STARTED = "evolution.started"
    EVOLUTION_PROPOSAL_GENERATED = "evolution.proposal_generated"
    EVOLUTION_CHANGE_EVALUATED = "evolution.change_evaluated"
    EVOLUTION_APPROVED = "evolution.approved"
    EVOLUTION_REJECTED = "evolution.rejected"
    EVOLUTION_COMPLETED = "evolution.completed"

    ERROR_OCCURRED = "error.occurred"

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


class MetricName(str, Enum):
    """Canonical observability metric catalog."""

    # Execution
    EXECUTIONS_TOTAL = "executions_total"
    EXECUTIONS_SUCCESSFUL = "executions_successful"
    EXECUTIONS_FAILED = "executions_failed"
    EXECUTION_DURATION_MS = "execution_duration_ms"

    # Reasoning
    REASONING_DURATION_MS = "reasoning_duration_ms"

    # Planning
    PLANNING_DURATION_MS = "planning_duration_ms"

    # Tools
    TOOL_CALLS_TOTAL = "tool_calls_total"
    TOOL_CALLS_SUCCESSFUL = "tool_calls_successful"
    TOOL_CALLS_FAILED = "tool_calls_failed"
    TOOL_EXECUTION_DURATION_MS = "tool_execution_duration_ms"

    # Memory
    MEMORY_RETRIEVALS_TOTAL = "memory_retrievals_total"
    MEMORY_RETRIEVAL_DURATION_MS = "memory_retrieval_duration_ms"
    MEMORIES_RETRIEVED = "memories_retrieved"

    # Knowledge
    KNOWLEDGE_ACCESSES_TOTAL = "knowledge_accesses_total"
    KNOWLEDGE_UPDATES_TOTAL = "knowledge_updates_total"

    # Cognitive evaluation
    EVALUATIONS_TOTAL = "evaluations_total"
    EVALUATION_SCORE = "evaluation_score"
    EVALUATION_DURATION_MS = "evaluation_duration_ms"

    # Learning
    LEARNING_SIGNALS_TOTAL = "learning_signals_total"
    LEARNING_OUTCOMES_TOTAL = "learning_outcomes_total"
    LEARNING_DURATION_MS = "learning_duration_ms"

    # Evolution
    EVOLUTION_DECISIONS_TOTAL = "evolution_decisions_total"
    ADAPTATIONS_APPLIED_TOTAL = "adaptations_applied_total"
    EVOLUTION_DURATION_MS = "evolution_duration_ms"

    # System
    ERRORS_TOTAL = "errors_total"
    SUCCESS_RATE = "success_rate"
    FAILURE_RATE = "failure_rate"


class ErrorSeverity(str, Enum):
    """Severity of an execution error."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
