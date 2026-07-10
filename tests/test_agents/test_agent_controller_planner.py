from src.agents.controller.agent_controller import AgentController
from src.agents.planning.execution_plan import ExecutionPlan


def test_agent_controller_creates_execution_plan():

    controller = AgentController()


    plan = controller.create_plan(
        "Analyze sales dataset"
    )


    assert plan is not None


    assert isinstance(
        plan,
        ExecutionPlan
    )



def test_agent_controller_plan_contains_expected_steps():

    controller = AgentController()


    plan = controller.create_plan(
        "Analyze customer information"
    )


    actions = [
        step.action
        for step in plan.steps
    ]


    assert actions == [
        "route_request",
        "execute_tool",
        "generate_response"
    ]



def test_agent_controller_plan_steps_start_pending():

    controller = AgentController()


    plan = controller.create_plan(
        "Test planning workflow"
    )


    statuses = [
        step.status
        for step in plan.steps
    ]


    assert statuses == [
        "pending",
        "pending",
        "pending"
    ]