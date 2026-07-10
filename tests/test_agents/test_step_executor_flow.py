from src.agents.execution.step_executor import StepExecutor
from src.agents.planning.plan_step import PlanStep


def test_step_executor_route_request():

    executor = StepExecutor()

    step = PlanStep(
        step_id=1,
        action="route_request",
        description="Route request"
    )

    result = executor.execute(
        step,
        "Quantos produtos existem?"
    )


    assert result["status"] == "routing_ready"

    assert step.status == "completed"



def test_step_executor_execute_tool():

    executor = StepExecutor()

    step = PlanStep(
        step_id=2,
        action="execute_tool",
        description="Execute tool"
    )


    result = executor.execute(
        step,
        "Quantos produtos existem?"
    )


    assert "status" in result

    assert step.status == "completed"



def test_step_executor_generate_response():

    executor = StepExecutor()

    step = PlanStep(
        step_id=3,
        action="generate_response",
        description="Generate response"
    )


    result = executor.execute(
        step,
        "Teste"
    )


    assert result["status"] == "response_ready"

    assert step.status == "completed"