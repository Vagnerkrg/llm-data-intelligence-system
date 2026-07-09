from typing import Dict, List

from src.agents.observability.agent_decision_trace import AgentDecisionTrace
from src.agents.observability.decision_trace_store import DecisionTraceStore


class DecisionAnalytics:
    """
    Provides analytical insights from agent decision traces.

    Converts raw decision history into
    intelligence metrics for monitoring.
    """


    def __init__(
        self,
        store: DecisionTraceStore
    ):

        self.store = store



    def total_decisions(
        self
    ) -> int:
        """
        Return total number of decisions recorded.
        """

        return len(
            self.store.all()
        )



    def success_rate(
        self
    ) -> float:
        """
        Calculate successful decision percentage.
        """

        traces = self.store.all()


        if not traces:

            return 0.0



        successful = sum(
            1
            for trace in traces
            if trace.success
        )


        return successful / len(traces)



    def average_confidence(
        self
    ) -> float:
        """
        Calculate average confidence
        from recorded decisions.
        """

        traces = self.store.all()


        if not traces:

            return 0.0



        total = sum(
            trace.confidence
            for trace in traces
        )


        return total / len(traces)



    def tool_usage(
        self
    ) -> Dict[str, int]:
        """
        Return frequency of selected tools.
        """

        usage = {}


        for trace in self.store.all():

            if trace.selected_tool:

                usage[trace.selected_tool] = (
                    usage.get(
                        trace.selected_tool,
                        0
                    )
                    + 1
                )


        return usage



    def best_tool(
        self
    ) -> str | None:
        """
        Return the most frequently selected tool.
        """

        usage = self.tool_usage()


        if not usage:

            return None



        return max(
            usage,
            key=usage.get
        )