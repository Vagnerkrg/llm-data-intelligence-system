from datetime import datetime

from src.agents.observability.agent_decision_trace import AgentDecisionTrace
from src.agents.observability.decision_trace_store import DecisionTraceStore



def create_trace(
    tool="analytics",
    success=True
):

    return AgentDecisionTrace(

        question="analisar dados",

        selected_tool=tool,

        confidence=0.90,

        reason="Analytics tool selected.",

        execution_time=0.20,

        success=success,

        result={
            "rows": 50
        },

        timestamp=datetime.now()

    )



def test_store_add_trace():

    store = DecisionTraceStore()


    trace = create_trace()


    store.add(
        trace
    )


    assert store.count() == 1


    assert store.all()[0] == trace



def test_store_returns_all_traces():

    store = DecisionTraceStore()


    first = create_trace()

    second = create_trace(
        tool="analytics",
        success=False
    )


    store.add(first)

    store.add(second)


    traces = store.all()


    assert len(traces) == 2


    assert traces[0] == first

    assert traces[1] == second



def test_store_latest_trace():

    store = DecisionTraceStore()


    first = create_trace()


    second = create_trace(
        success=False
    )


    store.add(first)

    store.add(second)


    latest = store.latest()


    assert latest == second



def test_latest_returns_none_when_empty():

    store = DecisionTraceStore()


    assert store.latest() is None