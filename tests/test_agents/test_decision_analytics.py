from datetime import datetime

from src.agents.observability.agent_decision_trace import AgentDecisionTrace
from src.agents.observability.decision_trace_store import DecisionTraceStore
from src.agents.observability.decision_analytics import DecisionAnalytics



def create_trace(
    tool,
    confidence,
    success
):

    return AgentDecisionTrace(

        question="test question",

        selected_tool=tool,

        confidence=confidence,

        success=success,

        reason="test decision",

        execution_time=0.15,

        result={
            "status": "ok"
        },

        timestamp=datetime.now()

    )



def test_total_decisions():

    store = DecisionTraceStore()


    store.add(
        create_trace(
            "analytics",
            0.9,
            True
        )
    )


    analytics = DecisionAnalytics(
        store
    )


    assert analytics.total_decisions() == 1



def test_success_rate():

    store = DecisionTraceStore()


    store.add(
        create_trace(
            "analytics",
            0.9,
            True
        )
    )


    store.add(
        create_trace(
            "analytics",
            0.5,
            False
        )
    )


    analytics = DecisionAnalytics(
        store
    )


    assert analytics.success_rate() == 0.5



def test_average_confidence():

    store = DecisionTraceStore()


    store.add(
        create_trace(
            "analytics",
            0.8,
            True
        )
    )


    store.add(
        create_trace(
            "analytics",
            0.6,
            True
        )
    )


    analytics = DecisionAnalytics(
        store
    )


    assert analytics.average_confidence() == 0.7



def test_tool_usage_and_best_tool():

    store = DecisionTraceStore()


    store.add(
        create_trace(
            "analytics",
            0.9,
            True
        )
    )


    store.add(
        create_trace(
            "analytics",
            0.8,
            True
        )
    )


    store.add(
        create_trace(
            "search",
            0.7,
            True
        )
    )


    analytics = DecisionAnalytics(
        store
    )


    usage = analytics.tool_usage()


    assert usage["analytics"] == 2

    assert usage["search"] == 1

    assert analytics.best_tool() == "analytics"