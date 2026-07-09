from src.agents.controller.agent_controller import AgentController
from src.agents.planning.plan_step import PlanStep



class StepExecutor:
    """
    Executes individual steps from
    an agent execution plan.

    Responsible for translating
    plan actions into operations.
    """



    def __init__(
        self,
        controller=None
    ):

        self.controller = (
            controller
            if controller
            else AgentController()
        )



    def execute(
        self,
        step: PlanStep,
        question: str
    ):
        """
        Execute a single plan step.
        """

        if step.action == "route_request":

            result = {

                "status": "routing_ready"

            }


            step.complete(
                result
            )


            return result



        if step.action == "execute_tool":

            result = self.controller.run(
                question
            )


            step.complete(
                result
            )


            return result



        if step.action == "generate_response":

            result = {

                "status": "response_ready"

            }


            step.complete(
                result
            )


            return result



        error = {

            "error": (
                f"Unknown action: {step.action}"
            )

        }


        step.fail(
            error["error"]
        )


        return error