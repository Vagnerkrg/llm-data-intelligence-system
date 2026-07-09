from src.agents.router.routing_result import RoutingResult
from src.agents.router.tool_scorer import ToolScorer


class AgentRouter:
    """
    Responsible for deciding which tool
    should handle a user request.
    """


    def __init__(
        self,
        registry=None,
        scorer=None
    ):

        self.registry = registry

        self.scorer = (
            scorer
            if scorer
            else ToolScorer()
        )



    def route(
        self,
        question: str
    ) -> RoutingResult:
        """
        Route a question using available
        tools and scoring strategy.
        """


        if self.registry:

            result = self._route_using_scorer(
                question
            )


            if result.tool:

                return result



        return self._route_using_keywords(
            question
        )



    def _route_using_scorer(
        self,
        question: str
    ) -> RoutingResult:
        """
        Route using tool scoring.
        """


        tools = (
            self.registry.list_tool_metadata()
        )


        ranked_tools = self.scorer.score(
            question,
            tools
        )


        if ranked_tools:

            tool, score, reason = ranked_tools[0]


            return RoutingResult(

                tool=tool.name,

                confidence=score,

                reason=reason

            )



        return RoutingResult(

            tool=None,

            confidence=0.0,

            reason=(

                "No scored tool match found."

            )

        )



    def _route_using_keywords(
        self,
        question: str
    ) -> RoutingResult:
        """
        Legacy keyword based fallback.
        """


        text = question.lower()


        analytical_keywords = [

            "quantos",

            "categoria",

            "colunas",

            "dados",

            "produtos",

            "clientes"

        ]


        if any(
            keyword in text
            for keyword in analytical_keywords
        ):

            return RoutingResult(

                tool="analytics",

                confidence=0.90,

                reason=(

                    "Analytical keywords detected."

                )

            )



        return RoutingResult(

            tool=None,

            confidence=0.0,

            reason=(

                "No matching tool found."

            )

        )