from src.agents.router.routing_result import RoutingResult


class AgentRouter:
    """
    Responsible for deciding which tool
    should handle a user request.
    """


    def __init__(
        self,
        registry=None
    ):

        self.registry = registry



    def route(
        self,
        question: str
    ) -> RoutingResult:
        """
        Route a question and return
        a structured decision result.
        """


        if self.registry:

            result = self._route_using_metadata(
                question
            )

            if result.tool:

                return result



        return self._route_using_keywords(
            question
        )



    def _route_using_metadata(
        self,
        question: str
    ) -> RoutingResult:
        """
        Try routing using registered tool metadata.
        """


        text = question.lower()


        metadata_list = (
            self.registry.list_tool_metadata()
        )


        for metadata in metadata_list:

            for capability in metadata.capabilities:

                if capability.lower() in text:

                    return RoutingResult(

                        tool=metadata.name,

                        confidence=0.85,

                        reason=(

                            "Matched tool capability: "

                            + capability

                        )

                    )



        return RoutingResult(

            tool=None,

            confidence=0.0,

            reason=(

                "No metadata match found."

            )

        )



    def _route_using_keywords(
        self,
        question: str
    ) -> RoutingResult:
        """
        Legacy keyword based routing fallback.
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