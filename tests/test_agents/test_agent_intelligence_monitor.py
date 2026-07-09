from datetime import datetime

from src.agents.observability.agent_intelligence_monitor import (
    AgentIntelligenceMonitor
)

from src.agents.observability.decision_analytics import (
    DecisionAnalytics
)

from src.agents.observability.decision_trace_store import (
    DecisionTraceStore
)

from src.agents.observability.agent_decision_trace import (
    AgentDecisionTrace
)

from src.agents.evaluation.routing_history import (
    RoutingHistory
)

from src.agents.evaluation.routing_metrics import (
    RoutingMetrics
)

from src.agents.evaluation.router_performance_analyzer import (
    RouterPerformanceAnalyzer
)

from src.agents.evaluation.routing_evaluator import (
    RoutingEvaluation
)



def create_trace():

    return AgentDecisionTrace(

        question="quantos produtos",

        selected_tool="analytics",

        confidence=0.9,

        success=True,

        reason="test",

        execution_time=0.1,

        result={
            "ok": True
        },

        timestamp=datetime.now()

    )



def create_routing():

    return RoutingEvaluation(

        question="quantos produtos",

        selected_tool="analytics",

        confidence=0.9,

        success=True,

        timestamp=datetime.now()

    )



def test_monitor_generates_report():

    decision_store = DecisionTraceStore()


    decision_store.add(
        create_trace()
    )


    decision_analytics = DecisionAnalytics(
        decision_store
    )


    routing_history = RoutingHistory()


    routing_history.add(
        create_routing()
    )


    routing_metrics = RoutingMetrics(
        routing_history
    )


    performance = RouterPerformanceAnalyzer(
        routing_history
    )


    monitor = AgentIntelligenceMonitor(

        decision_analytics,

        routing_metrics,

        performance

    )


    report = monitor.generate_report()


    assert report["total_decisions"] == 1

    assert report["success_rate"] == 1.0

    assert report["best_tool"] == "analytics"



def test_monitor_contains_routing_metrics():

    decision_store = DecisionTraceStore()


    decision_store.add(
        create_trace()
    )


    monitor = AgentIntelligenceMonitor(

        DecisionAnalytics(
            decision_store
        ),

        RoutingMetrics(
            RoutingHistory()
        ),

        RouterPerformanceAnalyzer(
            RoutingHistory()
        )

    )


    report = monitor.generate_report()


    assert "routing_total" in report

    assert "performance" in report