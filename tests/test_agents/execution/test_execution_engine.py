from src.agents.execution.execution_engine import ExecutionEngine
from src.agents.execution.step_executor import StepExecutor
from src.agents.runtime.execution_context import ExecutionContext
from src.agents.planning.execution_plan import ExecutionPlan
from src.agents.planning.plan_step import PlanStep



class FakeExecutor:

    def execute(
        self,
        step,
        question
    ):

        result = {

            "step": step.action

        }


        step.complete(
            result
        )


        return result



def create_context():

    context = ExecutionContext(

        question="test"

    )


    plan = ExecutionPlan(

        objective="test"

    )


    plan.add_step(

        PlanStep(

            step_id=1,

            action="step_one",

            description="First step"

        )

    )


    plan.add_step(

        PlanStep(

            step_id=2,

            action="step_two",

            description="Second step"

        )

    )


    context.set_plan(
        plan
    )


    context.update_current_step()


    return context



def test_execution_engine_executes_plan():

    engine = ExecutionEngine(

        step_executor=FakeExecutor()

    )


    context = create_context()


    result = engine.execute(
        context
    )


    assert result.status == "completed"

    assert len(
        result.results
    ) == 2



def test_execution_engine_handles_failure():

    class FailingExecutor:


        def execute(
            self,
            step,
            question
        ):

            raise Exception(
                "execution error"
            )


    engine = ExecutionEngine(

        step_executor=FailingExecutor()

    )


    context = create_context()


    result = engine.execute(
        context
    )


    assert result.status == "failed"

    assert "error" in result.metadata