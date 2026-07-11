from typing import Optional

from src.agents.reasoning.reasoning_result import ReasoningResult


class PlannerStrategy:
    """
    Strategy layer responsible for
    identifying the intent of a user request.

    V1.12 evolution:
    The strategy layer can now consume
    structured reasoning information produced
    by the ReasoningEngine.

    The reasoning result becomes the primary
    source of planning intelligence.

    A legacy keyword-based fallback is kept
    to preserve compatibility.
    """

    def analyze(
        self,
        question: str,
        reasoning_result: Optional[ReasoningResult] = None
    ) -> dict:
        """
        Analyze user request and classify
        the planning strategy.

        Priority:

        1. ReasoningResult information
        2. Legacy keyword classification
        """

        if reasoning_result:

            return {

                "type": (
                    reasoning_result.intent
                    if reasoning_result.intent
                    else "unknown"
                ),

                "goal": (
                    reasoning_result.goal
                    if hasattr(
                        reasoning_result,
                        "goal"
                    )
                    else None
                ),

                "strategy": (
                    reasoning_result.strategy
                    if hasattr(
                        reasoning_result,
                        "strategy"
                    )
                    else "default"
                ),

                "required_capabilities": (
                    reasoning_result.required_capabilities
                    if hasattr(
                        reasoning_result,
                        "required_capabilities"
                    )
                    else []
                )

            }


        text = question.lower()


        if any(
            keyword in text
            for keyword in [
                "produto",
                "dataset",
                "dados",
                "quantos",
                "quantidade",
                "análise",
                "analise"
            ]
        ):

            return {

                "type": "analytics",
                "goal": None,
                "strategy": "keyword_analysis",
                "required_capabilities": [
                    "analytics"
                ]

            }



        if any(
            keyword in text
            for keyword in [
                "documento",
                "pdf",
                "arquivo",
                "texto",
                "explique",
                "resuma"
            ]
        ):

            return {

                "type": "document",
                "goal": None,
                "strategy": "keyword_document",
                "required_capabilities": [
                    "document_processing"
                ]

            }



        return {

            "type": "unknown",
            "goal": None,
            "strategy": "default",
            "required_capabilities": []

        }