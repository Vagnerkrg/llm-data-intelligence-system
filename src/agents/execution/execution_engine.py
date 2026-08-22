from typing import Optional

from src.agents.runtime.execution_context import ExecutionContext
from src.agents.execution.step_executor import StepExecutor
from src.agents.controller.agent_controller import AgentController


class ExecutionEngine:
    """
    Execution engine responsible for
    running agent execution plans.
    """

    def __init__(
        self,
        step_executor: Optional[StepExecutor] = None,
        controller: Optional[AgentController] = None,
        observability=None,
    ):
        self.step_executor = (
            step_executor
            if step_executor
            else StepExecutor(
                controller=controller,
            )
        )

        self.observability = observability

    def execute(
        self,
        context: ExecutionContext,
    ) -> ExecutionContext:
        """
        Execute all pending steps from the execution plan.
        """

        try:
            if not context.plan:
                context.fail(
                    "No execution plan available.",
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

                step_name = getattr(
                    step,
                    "action",
                    None,
                )

                if self.observability:
                    self.observability.step_started(
                        context.execution_id,
                        step=step_name,
                    )

                try:
                    result = self.step_executor.execute(
                        step,
                        context.question,
                    )

                    context.add_result(
                        result,
                    )

                    if self.observability:
                        if isinstance(result, dict) and "error" in result:
                            self.observability.step_failed(
                                context.execution_id,
                                RuntimeError(
                                    str(
                                        result["error"],
                                    )
                                ),
                                step=step_name,
                            )
                        else:
                            self.observability.step_completed(
                                context.execution_id,
                                step=step_name,
                            )

                except Exception as error:
                    if self.observability:
                        self.observability.step_failed(
                            context.execution_id,
                            error,
                            step=step_name,
                        )

                    raise

            context.current_step = last_step
            context.complete()

        except Exception as error:
            context.fail(str(error))

        return context
