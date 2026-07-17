from ..domain.improvement_context import ImprovementContext
from ..domain.improvement_result import ImprovementResult
from ..domain.improvement_status import ImprovementStatus

from .cycle_executor import CycleExecutor


class ImprovementOrchestrator:
    """
    Coordinates cognitive improvement execution flow.

    Responsibilities:

    - receive improvement context;
    - execute cognitive cycle;
    - return improvement result.
    """


    def __init__(
        self,
        cycle_executor: CycleExecutor | None = None
    ):
        self.cycle_executor = (
            cycle_executor
            if cycle_executor
            else CycleExecutor()
        )


    def execute(
        self,
        context: ImprovementContext
    ) -> ImprovementResult:
        """
        Execute improvement orchestration.
        """

        return self.cycle_executor.execute(
            context
        )