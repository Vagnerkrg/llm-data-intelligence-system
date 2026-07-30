from dataclasses import dataclass


@dataclass
class ExecutionMetrics:
    """
    Métricas de execução de agentes.
    """

    execution_id: str

    success: bool

    duration: float


    @property
    def status(self) -> str:

        if self.success:
            return "completed"

        return "failed"