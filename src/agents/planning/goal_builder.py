from src.agents.planning.goal import Goal
from src.agents.reasoning.reasoning_result import ReasoningResult


class GoalBuilder:
    """
    Builds execution goals from reasoning results.

    This layer converts reasoning information
    into a structured objective consumed by
    planning components.
    """

    def build(
        self,
        reasoning_result: ReasoningResult
    ) -> Goal:
        """
        Create a goal from reasoning output.
        """


        metadata = (
            reasoning_result.metadata
            if hasattr(
                reasoning_result,
                "metadata"
            )
            and reasoning_result.metadata
            else {}
        )


        #
        # Preserve original user request
        #
        objective = (

            metadata.get(
                "question"
            )

            or metadata.get(
                "query"
            )

            or metadata.get(
                "user_request"
            )

            or getattr(
                reasoning_result,
                "goal",
                None
            )

            or getattr(
                reasoning_result,
                "conclusion",
                None
            )

            or "Solve user request"

        )


        intent = getattr(
            reasoning_result,
            "intent",
            "general"
        )


        required_capabilities = getattr(
            reasoning_result,
            "required_capabilities",
            []
        )


        strategy = getattr(
            reasoning_result,
            "strategy",
            "default"
        )


        return Goal(

            objective=objective,

            intent=intent,

            required_capabilities=(
                required_capabilities
            ),

            strategy=strategy,

            metadata={

                "reasoning": (

                    reasoning_result.reasoning

                ),

                "confidence": (

                    reasoning_result.confidence

                ),

                "source": (

                    metadata.get(
                        "source",
                        "goal_builder"
                    )

                )

            }

        )