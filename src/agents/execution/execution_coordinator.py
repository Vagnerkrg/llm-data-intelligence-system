from src.agents.execution.execution_event import (
    ExecutionEvent,
    ExecutionEventType,
)

from src.agents.execution.execution_state import (
    ExecutionState,
)

from src.agents.execution.execution_status import (
    ExecutionStatus,
)


class ExecutionCoordinator:
    """
    Coordinates execution lifecycle transitions.
    """

    def start_execution(
        self,
        state: ExecutionState,
    ) -> ExecutionState:
        """
        Start execution lifecycle.
        """

        state.status = ExecutionStatus.RUNNING

        state.events.append(
            ExecutionEvent(
                event_type=(
                    ExecutionEventType.EXECUTION_STARTED
                ),
                message="Execution started",
            )
        )

        return state


    def complete_execution(
        self,
        state: ExecutionState,
    ) -> ExecutionState:
        """
        Complete execution lifecycle.
        """

        state.status = ExecutionStatus.COMPLETED

        state.events.append(
            ExecutionEvent(
                event_type=(
                    ExecutionEventType.EXECUTION_COMPLETED
                ),
                message="Execution completed",
            )
        )

        return state


    def fail_execution(
        self,
        state: ExecutionState,
        error: str,
    ) -> ExecutionState:
        """
        Mark execution as failed.
        """

        state.status = ExecutionStatus.FAILED

        state.events.append(
            ExecutionEvent(
                event_type=(
                    ExecutionEventType.EXECUTION_FAILED
                ),
                message=error,
            )
        )

        return state