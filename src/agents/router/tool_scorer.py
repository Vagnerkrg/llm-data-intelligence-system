from typing import List

from src.agents.tools.tool_metadata import ToolMetadata


class ToolScorer:
    """
    Calculates compatibility scores between
    user requests and available tools.
    """

    def score(
        self,
        question: str,
        tools: List[ToolMetadata]
    ) -> list[tuple[ToolMetadata, float, str]]:
        """
        Return ranked tool candidates.
        """

        text = question.lower()

        results = []


        for tool in tools:

            score = 0.0
            reason = "No capability match."


            for capability in tool.capabilities:

                capability_text = capability.lower()


                if capability_text in text:

                    score += 0.5

                    reason = (
                        "Matched capability: "
                        + capability
                    )


            if score > 0:

                results.append(
                    (
                        tool,
                        min(score, 1.0),
                        reason
                    )
                )


        return sorted(
            results,
            key=lambda item: item[1],
            reverse=True
        )