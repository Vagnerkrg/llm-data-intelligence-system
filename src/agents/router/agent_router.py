from src.agents.router.routing_result import RoutingResult
from src.agents.router.tool_scorer import ToolScorer


class AgentRouter:
    """
    Responsible for deciding which tools
    should handle a user request.

    Supports single and multi-tool routing.
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

            if result.tools:

                return result


        performance_result = (
            self._route_using_performance()
        )

        if performance_result.tools:

            return performance_result


        return self._route_using_keywords(
            question
        )



    def _route_using_scorer(
        self,
        question: str
    ) -> RoutingResult:

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

                tools=[
                    tool.name
                ],

                confidence=score,

                reason=reason

            )


        return RoutingResult(

            tools=[],

            confidence=0.0,

            reason="No scored tool match found."

        )



    def _route_using_performance(
        self
    ) -> RoutingResult:

        if not self.performance_analyzer:

            return RoutingResult(

                tools=[],

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

                tools=[
                    best_tool
                ],

                confidence=0.70,

                reason=(
                    "Selected using routing "
                    "performance history."
                )

            )


        return RoutingResult(

            tools=[],

            confidence=0.0,

            reason="No performance signal found."

        )



    def _route_using_keywords(
        self,
        question: str
    ) -> RoutingResult:
        """
        Keyword routing with multi-tool detection.
        """

        text = question.lower()


        tools = []


        analytics_keywords = [

            "quantos",

            "categoria",

            "categorias",

            "colunas",

            "dados",

            "produtos",

            "clientes",

            "analise",

            "análise"

        ]


        rag_keywords = [

            "documentação",

            "documentacao",

            "explica",

            "manual",

            "informação",

            "informacao"

        ]



        if any(
            keyword in text
            for keyword in analytics_keywords
        ):

            tools.append(
                "analytics"
            )



        if any(
            keyword in text
            for keyword in rag_keywords
        ):

            tools.append(
                "rag"
            )



        if tools:

            return RoutingResult(

                tools=tools,

                confidence=0.90,

                reason=(
                    "Analytical keyword based "
                    "multi-tool routing."
                )

            )



        return RoutingResult(

            tools=[],

            confidence=0.0,

            reason=(
                "No matching tool found."
            )

        )