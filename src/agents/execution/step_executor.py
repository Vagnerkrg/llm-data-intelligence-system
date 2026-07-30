from src.agents.controller.agent_controller import AgentController


class StepExecutor:
    """
    Executes individual plan steps.

    Supports:
    - ExecutionStep (new planning model)
    - PlanStep (legacy compatibility)
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


    def _mark_running(
        self,
        step
    ):

        if hasattr(
            step,
            "mark_running"
        ):

            step.mark_running()


    def _complete(
        self,
        step,
        result
    ):

        if hasattr(
            step,
            "mark_completed"
        ):

            step.mark_completed(
                result
            )

            return


        if hasattr(
            step,
            "complete"
        ):

            step.complete(
                result
            )

            return



    def _fail(
        self,
        step,
        error
    ):

        if hasattr(
            step,
            "mark_failed"
        ):

            step.mark_failed(
                error
            )

            return


        if hasattr(
            step,
            "fail"
        ):

            step.fail(
                error
            )

            return



    def execute(
        self,
        step,
        question: str
    ):
        """
        Execute one plan step.
        """

        try:

            self._mark_running(
                step
            )


            action = step.action



            if action == "route_request":

                result = {
                    "status": "routing_ready"
                }


                self._complete(
                    step,
                    result
                )


                return result



            if action == "execute_tool":

                result = self.controller.run(
                    question
                )


                self._complete(
                    step,
                    result
                )


                return result



            if action == "generate_response":

                result = {
                    "status": "response_ready"
                }


                self._complete(
                    step,
                    result
                )


                return result



            error = (
                f"Unknown action: {action}"
            )


            self._fail(
                step,
                error
            )


            return {
                "error": error
            }



        except Exception as exc:


            self._fail(
                step,
                str(exc)
            )


            return {
                "error": str(exc)
            }