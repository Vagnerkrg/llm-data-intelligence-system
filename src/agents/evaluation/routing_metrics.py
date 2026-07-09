from typing import Dict

from src.agents.evaluation.routing_history import RoutingHistory



class RoutingMetrics:
    """
    Calculates metrics from routing history.
    """


    def __init__(
        self,
        history: RoutingHistory
    ):

        self.history = history



    def total_routes(
        self
    ) -> int:
        """
        Return total routing decisions.
        """

        return self.history.count()



    def average_confidence(
        self
    ) -> float:
        """
        Calculate average routing confidence.
        """


        records = self.history.all()


        if not records:

            return 0.0



        total = sum(
            record.confidence
            for record in records
        )


        return total / len(records)



    def success_rate(
        self
    ) -> float:
        """
        Calculate successful routing percentage.
        """


        records = self.history.all()


        if not records:

            return 0.0



        successful = sum(

            1
            for record in records
            if record.success

        )


        return successful / len(records)



    def tool_usage(
        self
    ) -> Dict[str, int]:
        """
        Count tool usage frequency.
        """


        usage = {}


        for record in self.history.all():

            if record.selected_tool:

                usage[record.selected_tool] = (
                    usage.get(
                        record.selected_tool,
                        0
                    )
                    + 1
                )


        return usage