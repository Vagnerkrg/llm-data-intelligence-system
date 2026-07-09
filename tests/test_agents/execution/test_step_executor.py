from src.agents.execution.step_executor import StepExecutor
from src.agents.planning.plan_step import PlanStep



class FakeController:

    def run(
        self,
        question
    ):

        return {

            "status": "success",

            "question": question

        }



def test_step_executor_route_request():

    executor = StepExecutor(
        controller=FakeController()
    )


    step = PlanStep(

        step_id=1,

        action="route_request",

        description="Route request"

    )


    result = executor.execute(
        step,
        "test question"
    )


    assert result["status"] == "routing_ready"

    assert step.status == "completed"



def test_step_executor_execute_tool():

    executor = StepExecutor(
        controller=FakeController()
    )


    step = PlanStep(

        step_id=2,

        action="execute_tool",

        description="Execute tool"

    )


    result = executor.execute(

        step,

        "customer analysis"

    )


    assert result["status"] == "success"

    assert step.status == "completed"



def test_step_executor_generate_response():

    executor = StepExecutor(
        controller=FakeController()
    )


    step = PlanStep(

        step_id=3,

        action="generate_response",

        description="Generate response"

    )


    result = executor.execute(

        step,

        "question"

    )


    assert result["status"] == "response_ready"

    assert step.status == "completed"



def test_step_executor_unknown_action():

    executor = StepExecutor(
        controller=FakeController()
    )


    step = PlanStep(

        step_id=99,

        action="unknown",

        description="Unknown action"

    )


    result = executor.execute(

        step,

        "question"

    )


    assert "error" in result

    assert step.status == "failed"