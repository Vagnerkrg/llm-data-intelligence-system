from src.agents.planning.goal_builder import GoalBuilder
from src.agents.reasoning.reasoning_result import ReasoningResult



def test_goal_builder_creates_goal_from_reasoning():

    reasoning = ReasoningResult(

        reasoning="Analyze user request",

        conclusion="Analyze sales data",

        confidence=0.95,

        goal="Analyze sales patterns",

        intent="analytics",

        required_capabilities=[
            "analytics",
            "statistics"
        ],

        strategy="analytical"

    )


    builder = GoalBuilder()


    goal = builder.build(
        reasoning
    )


    assert goal is not None

    assert goal.objective == (
        "Analyze sales patterns"
    )

    assert goal.intent == (
        "analytics"
    )

    assert (
        "analytics"
        in goal.required_capabilities
    )



def test_goal_builder_uses_conclusion_as_fallback():

    reasoning = ReasoningResult(

        reasoning="Understand request",

        conclusion="Explain document",

        confidence=0.8,

        intent="document",

        required_capabilities=[
            "retrieval"
        ]

    )


    builder = GoalBuilder()


    goal = builder.build(
        reasoning
    )


    assert goal.objective == (
        "Explain document"
    )

    assert goal.intent == (
        "document"
    )