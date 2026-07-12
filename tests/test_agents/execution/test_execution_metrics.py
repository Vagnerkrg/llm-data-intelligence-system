from datetime import datetime, timedelta, timezone

from src.agents.execution.execution_metrics import (
    ExecutionMetrics,
)


def test_execution_metrics_default_values():
    """
    Validate default execution metrics state.
    """

    metrics = ExecutionMetrics()

    assert metrics.started_at is None

    assert metrics.completed_at is None

    assert metrics.total_steps == 0

    assert metrics.completed_steps == 0

    assert metrics.failed_steps == 0

    assert metrics.retry_count == 0

    assert metrics.tool_calls == 0

    assert metrics.metadata == {}


def test_execution_metrics_custom_values():
    """
    Validate custom metrics creation.
    """

    metrics = ExecutionMetrics(
        total_steps=5,
        completed_steps=3,
        failed_steps=1,
        retry_count=2,
        tool_calls=4,
        metadata={
            "agent": "analytics_agent",
        },
    )

    assert metrics.total_steps == 5

    assert metrics.completed_steps == 3

    assert metrics.failed_steps == 1

    assert metrics.retry_count == 2

    assert metrics.tool_calls == 4

    assert metrics.metadata["agent"] == "analytics_agent"


def test_execution_duration_calculation():
    """
    Validate execution duration calculation.
    """

    start = datetime.now(timezone.utc)

    end = start + timedelta(seconds=10)

    metrics = ExecutionMetrics(
        started_at=start,
        completed_at=end,
    )

    assert metrics.duration_seconds == 10


def test_execution_duration_without_completion():
    """
    Validate duration when execution is incomplete.
    """

    metrics = ExecutionMetrics(
        started_at=datetime.now(timezone.utc),
    )

    assert metrics.duration_seconds is None