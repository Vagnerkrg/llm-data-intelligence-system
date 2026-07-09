from typing import Dict

from src.agents.evaluation.routing_metrics import RoutingMetrics
from src.agents.evaluation.router_performance_analyzer import (
    RouterPerformanceAnalyzer
)

from src.agents.observability.decision_analytics import (
    DecisionAnalytics
)



class AgentIntelligenceMonitor:
    """
    Consolidates intelligence signals from
    decision observability and routing performance.

    Provides a unified agent intelligence report.
    """


    def __init__(
        self,
        decision_analytics: DecisionAnalytics,
        routing_metrics: RoutingMetrics,
        performance_analyzer: RouterPerformanceAnalyzer
    ):

        self.decision_analytics = decision_analytics

        self.routing_metrics = routing_metrics

        self.performance_analyzer = performance_analyzer



    def generate_report(
        self
    ) -> Dict:
        """
        Generate consolidated intelligence report.
        """


        return {

            "total_decisions": (
                self.decision_analytics.total_decisions()
            ),


            "success_rate": (
                self.decision_analytics.success_rate()
            ),


            "average_confidence": (
                self.decision_analytics.average_confidence()
            ),


            "best_tool": (
                self.decision_analytics.best_tool()
            ),


            "tool_usage": (
                self.decision_analytics.tool_usage()
            ),


            "routing_total": (
                self.routing_metrics.total_routes()
            ),


            "routing_success_rate": (
                self.routing_metrics.success_rate()
            ),


            "routing_average_confidence": (
                self.routing_metrics.average_confidence()
            ),


            "performance": {

                "total_decisions": (
                    self.performance_analyzer.total_decisions()
                ),


                "success_rate_by_tool": (
                    self.performance_analyzer.success_rate_by_tool()
                ),


                "average_confidence_by_tool": (
                    self.performance_analyzer.average_confidence_by_tool()
                ),


                "best_tool": (
                    self.performance_analyzer.best_tool()
                )

            }

        }