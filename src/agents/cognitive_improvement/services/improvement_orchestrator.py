from ..domain.improvement_context import ImprovementContext
from ..domain.improvement_result import ImprovementResult

from .cycle_executor import CycleExecutor


class ImprovementOrchestrator:
    """
    Coordinates the Cognitive Improvement workflow.

    Responsibilities:
    - receive the improvement context;
    - delegate execution to the CycleExecutor;
    - return the improvement result.
    """

    def __init__(
        self,
        cycle_executor: CycleExecutor | None = None,
    ) -> None:

        self.cycle_executor = (
            cycle_executor
            if cycle_executor is not None
            else CycleExecutor()
        )

    def execute(
        self,
        context: ImprovementContext,
    ) -> ImprovementResult:
        """
        Execute the cognitive improvement workflow.
        """

        return self.cycle_executor.execute(
            context
        )