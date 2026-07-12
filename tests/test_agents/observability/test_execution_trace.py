from src.agents.observability.execution_trace import (
    ExecutionTrace
)



def test_execution_trace_creation():

    trace = ExecutionTrace(
        execution_id="exec_001"
    )

    assert trace.execution_id == "exec_001"

    assert trace.count_events() == 0



def test_execution_trace_add_event():

    trace = ExecutionTrace(
        execution_id="exec_001"
    )


    trace.add_event(
        event_type="execution_started",
        payload={
            "status": "running"
        }
    )


    assert trace.count_events() == 1

    assert (
        trace.events[0]["type"]
        ==
        "execution_started"
    )



def test_execution_trace_summary():

    trace = ExecutionTrace(
        execution_id="exec_001",
        metadata={
            "agent": "planner"
        }
    )


    result = trace.summary()


    assert result["execution_id"] == "exec_001"

    assert (
        result["metadata"]["agent"]
        ==
        "planner"
    )



def test_execution_trace_multiple_events():

    trace = ExecutionTrace(
        execution_id="exec_001"
    )


    trace.add_event(
        "started",
        {}
    )

    trace.add_event(
        "completed",
        {}
    )


    assert trace.count_events() == 2