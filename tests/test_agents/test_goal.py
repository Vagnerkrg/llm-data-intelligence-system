from src.agents.planning.goal import Goal


def test_goal_creation():

    goal = Goal(
        objective="Analyze sales data",
        intent="analytics"
    )


    assert goal.objective == "Analyze sales data"

    assert goal.intent == "analytics"

    assert goal.required_capabilities == []

    assert goal.constraints == {}