from typing import Dict

from src.agents.evaluation.routing_history import RoutingHistory


class RouterPerformanceAnalyzer:
    """
    Analyzes router performance based on
    historical routing decisions.
    """


    def __init__(
        self,
        history: RoutingHistory
    ):

        self.history = history



    def total_decisions(
        self
    ) -> int:
        """
        Return total analyzed routing decisions.
        """

        return self.history.count()



    def success_rate_by_tool(
        self
    ) -> Dict[str, float]:
        """
        Calculate success rate grouped by tool.
        """


        stats = {}


        for record in self.history.all():

            tool = record.selected_tool


            if not tool:

                continue


            if tool not in stats:

                stats[tool] = {

                    "total": 0,

                    "success": 0

                }


            stats[tool]["total"] += 1


            if record.success:

                stats[tool]["success"] += 1



        return {

            tool: (
                data["success"]
                /
                data["total"]
            )

            for tool, data in stats.items()

        }



    def average_confidence_by_tool(
        self
    ) -> Dict[str, float]:
        """
        Calculate average confidence grouped by tool.
        """


        confidence = {}


        for record in self.history.all():

            tool = record.selected_tool


            if not tool:

                continue


            if tool not in confidence:

                confidence[tool] = []



            confidence[tool].append(
                record.confidence
            )



        return {

            tool: (
                sum(values)
                /
                len(values)
            )

            for tool, values in confidence.items()

        }



    def best_tool(
        self
    ) -> str | None:
        """
        Return the best performing tool
        based on success rate.
        """


        rates = self.success_rate_by_tool()


        if not rates:

            return None



        return max(
            rates,
            key=rates.get
        )