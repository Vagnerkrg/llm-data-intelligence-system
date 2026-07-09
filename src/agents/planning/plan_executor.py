from typing import Any

from src.agents.runtime.execution_context import ExecutionContext
from src.agents.controller.agent_controller import AgentController



class PlanExecutor:
    """
    Executes agent execution plans.

    Responsible for processing plan steps,
    coordinating execution and updating
    runtime context.
    """



    def __init__(
        self,
        controller: AgentController = None
    ):

        self.controller = (
            controller
            if controller
            else AgentController()
        )



    def execute(
        self,
        context: ExecutionContext
    ) -> ExecutionContext:
        """
        Execute all steps from
        the current execution plan.
        """


        if not context.plan:

            context.fail(
                "No execution plan available."
            )

            return context



        context.status = "executing"



        while True:

            context.update_current_step()


            step = context.current_step


            if not step:

                break



            try:

                result = self._execute_step(
                    step.action,
                    context
                )


                step.complete(
                    result
                )


                context.add_result(
                    result
                )


            except Exception as error:

                step.fail(
                    str(error)
                )


                context.fail(
                    str(error)
                )


                return context



        context.complete()


        return context



    def _execute_step(
        self,
        action: str,
        context: ExecutionContext
    ) -> Any:
        """
        Execute a single plan step.

        Initial implementation keeps
        execution deterministic.

        Future versions may introduce:
        - dynamic planners
        - tool selection
        - reasoning strategies
        """


        if action == "route_request":

            return {

                "status": "ready",

                "action": action,

                "message":
                    "Request prepared for routing."

            }



        if action == "execute_tool":

            return self.controller.run(
                context.question
            )



        if action == "generate_response":

            return {

                "status": "ready",

                "action": action,

                "message":
                    "Response generation step prepared."

            }



        return {

            "status": "unknown",

            "action": action

        }