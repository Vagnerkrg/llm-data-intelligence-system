from src.intelligence.execution.collector import (
    ExecutionCollector,
)

from src.intelligence.execution.store import (
    ExecutionStore,
)

from src.intelligence.execution.events import (
    ExecutionEvent,
    ExecutionEventType,
)


def test_collector_execution_flow():

    store = ExecutionStore()

    collector = ExecutionCollector(
        store
    )

    execution_id = collector.start_execution(
        "Analyze customer data"
    )

    event = ExecutionEvent(
        execution_id=execution_id,
        event_type=ExecutionEventType.STEP_COMPLETED,
        component="analytics_tool",
        payload={
            "rows": 100
        },
    )

    collector.record_event(
        event
    )

    collector.finish_execution(
        execution_id
    )

    execution = store.get(
        execution_id
    )

    assert execution is not None
    assert execution.status == "completed"
    assert len(execution.steps) == 1
    assert execution.steps[0].component == "analytics_tool"