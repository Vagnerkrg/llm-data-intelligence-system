from datetime import datetime

from src.agents.router.agent_router import AgentRouter
from src.agents.agent_registry import AgentRegistry

from src.agents.evaluation.routing_history import RoutingHistory
from src.agents.evaluation.routing_evaluator import RoutingEvaluation
from src.agents.evaluation.router_performance_analyzer import (
    RouterPerformanceAnalyzer
)

from src.agents.tools.analytics_tool import AnalyticsTool



def test_router_uses_performance_signal():

    registry = AgentRegistry()


    analytics_tool = AnalyticsTool()


    registry.register_tool(
        analytics_tool
    )


    history = RoutingHistory()


    history.add(

        RoutingEvaluation(

            question="quantos produtos",

            selected_tool="analytics",

            confidence=0.95,

            success=True,

            timestamp=datetime.now()

        )

    )


    analyzer = RouterPerformanceAnalyzer(
        history
    )


    router = AgentRouter(

        registry=registry,

        performance_analyzer=analyzer

    )


    result = router.route(
        "qual ferramenta devo usar para análise?"
    )


    assert result.tool == "analytics"