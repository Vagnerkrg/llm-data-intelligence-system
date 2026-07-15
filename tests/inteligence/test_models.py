from src.intelligence.execution.models import (
    ExecutionRecord,
    ExecutionStep,
)


def test_execution_step_creation():

    step = ExecutionStep(
        component="planner",
        action="create_plan",
    )

    assert step.component == "planner"
    assert step.action == "create_plan"
    assert step.status == "pending"


def test_execution_record_creation():

    record = ExecutionRecord(
        execution_id="exec-001",
        request="Analyze sales data",
    )

    assert record.execution_id == "exec-001"
    assert record.request == "Analyze sales data"
    assert record.status == "running"
    assert len(record.steps) == 0