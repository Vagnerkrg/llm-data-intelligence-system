from typing import Dict


class AdaptiveRoutingPolicy:
    """
    Adjusts routing decisions using
    historical performance signals.
    """


    def __init__(
        self,
        performance_weight: float = 0.30
    ):

        self.performance_weight = (
            performance_weight
        )



    def adjust_score(
        self,
        base_score: float,
        tool_name: str,
        performance: Dict[str, float]
    ) -> float:
        """
        Combine base routing score with
        historical tool performance.
        """


        historical_score = (
            performance.get(
                tool_name,
                0.0
            )
        )


        adjusted_score = (

            (
                base_score
                *
                (1 - self.performance_weight)
            )

            +

            (
                historical_score
                *
                self.performance_weight
            )

        )


        return adjusted_score



    def rank_tools(
        self,
        ranked_tools,
        performance: Dict[str, float]
    ):
        """
        Re-rank tools using historical performance.
        """


        adjusted_tools = []


        for tool, score, reason in ranked_tools:

            adjusted_score = self.adjust_score(

                score,

                tool.name,

                performance

            )


            adjusted_tools.append(

                (

                    tool,

                    adjusted_score,

                    reason

                )

            )



        return sorted(

            adjusted_tools,

            key=lambda item: item[1],

            reverse=True

        )