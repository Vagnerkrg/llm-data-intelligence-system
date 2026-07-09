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
        scorer=None,
        performance_analyzer=None
    ):

        self.registry = registry


        self.scorer = (
            scorer
            if scorer
            else ToolScorer()
        )


        self.performance_analyzer = (
            performance_analyzer
        )



    def route(
        self,
        question: str
    ) -> RoutingResult:
        """
        Route a question using available
        tools, scoring and historical performance.
        """


        if self.registry:

            result = self._route_using_scorer(
                question
            )


            if result.tool:

                return result



        performance_result = (
            self._route_using_performance()
        )


        if performance_result.tool:

            return performance_result



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



    def _route_using_performance(
        self
    ) -> RoutingResult:
        """
        Route using historical routing performance.
        """


        if not self.performance_analyzer:

            return RoutingResult(

                tool=None,

                confidence=0.0,

                reason=(

                    "Performance analyzer unavailable."

                )

            )



        best_tool = (
            self.performance_analyzer.best_tool()
        )



        if best_tool:

            return RoutingResult(

                tool=best_tool,

                confidence=0.70,

                reason=(

                    "Selected using routing "
                    "performance history."

                )

            )



        return RoutingResult(

            tool=None,

            confidence=0.0,

            reason=(

                "No performance signal found."

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