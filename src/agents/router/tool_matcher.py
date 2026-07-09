from typing import List

from src.agents.tools.tool_metadata import ToolMetadata
from src.agents.router.routing_result import RoutingResult


class ToolMatcher:
    """
    Responsible for matching user requests
    against available tool metadata.

    This component isolates the decision logic
    from the AgentRouter.
    """



    def match(
        self,
        question: str,
        tools: List[ToolMetadata]
    ) -> RoutingResult:
        """
        Find the most suitable tool based
        on metadata capabilities.
        """


        text = question.lower()


        best_match = None

        best_capability = None


        for tool in tools:

            for capability in tool.capabilities:

                capability_text = capability.lower()


                if capability_text in text:

                    best_match = tool

                    best_capability = capability

                    break


            if best_match:

                break



        if best_match:

            return RoutingResult(

                tool=best_match.name,

                confidence=0.85,

                reason=(

                    "Matched tool capability: "

                    + best_capability

                )

            )



        return RoutingResult(

            tool=None,

            confidence=0.0,

            reason=(

                "No tool capability match found."

            )

        )