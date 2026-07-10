from typing import Optional

from src.agents.runtime.execution_context import ExecutionContext
from src.agents.execution.step_executor import StepExecutor
from src.agents.controller.agent_controller import AgentController


class ExecutionEngine:
    """
    Execution engine responsible for
    running agent execution plans.

    Coordinates:

    - execution context;
    - plan steps;
    - step executor;
    - execution lifecycle.
    """


    def __init__(
        self,
        step_executor: Optional[StepExecutor] = None,
        controller: Optional[AgentController] = None
    ):

        self.step_executor = (
            step_executor
            if step_executor
            else StepExecutor(
                controller=controller
            )
        )



    def execute(
        self,
        context: ExecutionContext
    ) -> ExecutionContext:
        """
        Execute all pending steps
        from the execution plan.
        """


        try:

            if not context.plan:

                context.fail(
                    "No execution plan available."
                )

                return context



            context.status = "executing"


            last_step = None



            while True:

                context.update_current_step()


                step = context.current_step


                if not step:

                    break



                last_step = step



                result = self.step_executor.execute(
                    step,
                    context.question
                )



                context.add_result(
                    result
                )



            # Preserve execution state
            # after finishing workflow

            context.current_step = last_step



            context.complete()



        except Exception as error:


            context.fail(
                str(error)
            )


        return context