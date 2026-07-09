from typing import List

from src.agents.observability.agent_decision_trace import AgentDecisionTrace



class DecisionTraceStore:
    """
    Stores agent decision traces.

    Provides a simple in-memory observability layer
    for tracking agent execution history.
    """


    def __init__(self):

        self._traces: List[AgentDecisionTrace] = []



    def add(
        self,
        trace: AgentDecisionTrace
    ):
        """
        Store an agent decision trace.
        """

        self._traces.append(
            trace
        )



    def all(
        self
    ) -> List[AgentDecisionTrace]:
        """
        Return all stored traces.
        """

        return self._traces



    def count(
        self
    ) -> int:
        """
        Return number of stored traces.
        """

        return len(
            self._traces
        )



    def latest(
        self
    ) -> AgentDecisionTrace | None:
        """
        Return latest stored trace.
        """

        if not self._traces:

            return None


        return self._traces[-1]